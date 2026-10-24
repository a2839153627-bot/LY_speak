"""遥控器按键读取：雷柏 Knight22 无线遥控（USB HID，被内核识别为键盘）。

遥控上的 A/B/C/D 四个键发的是**数字键 1/2/3/4**（Linux 按键码
KEY_1=2 / KEY_2=3 / KEY_3=4 / KEY_4=5，2026-10-20 在真机上抓包确认）。

USB 复合设备在系统里会注册多个 input 接口（键盘 / System Control /
Consumer Control / Mouse），数字键只发在**键盘接口**上。本模块的
_find_device 用**能力位图**精确识别键盘接口：读每个接口的
/sys/.../capabilities/key（内核格式：空格分隔的 64 位十六进制组，从
最高组往下排，第 g 组的第 b 位 = 按键码 64*g + b），只接受"能发出
我们要监听的按键码"的接口。2026-10-24 真机实锤：四个接口里只有键盘
接口的位图含 KEY_1~KEY_4（组0 = fffffffffffffffe），其余接口组0=0。

**热插拔**：监听线程常驻——启动时找不到设备就周期性重试（运行中插入
也能用）；读取出错（拔掉）后关闭句柄重新搜索，插回后自动重连。设备
重新枚举时 event 编号会漂移（10-20 是 event14，10-24 是 event7），
所以永远按名字+能力找，绝不按固定编号。

后台线程以 O_RDONLY | O_NONBLOCK 打开 /dev/input/eventN 解析 input_event
结构（只读，不触发任何动作），把"按下"事件（EV_KEY 且 value==1，长按
自动重复 value==2 丢弃）放进线程安全队列，供任务节点主循环轮询。

急停键（D）在**读线程里直接置 abort_event**：任务节点导航/播报的等待
循环里都在轮询这个事件（abort_check 回调），这样即使主循环正阻塞在
导航等待里，急停也能立即打断，而不是等按键被主循环处理。

读 /dev/input 需要 root 或 input 组权限。机器人上的放权方式（udev 规则
+ 把运行用户加入 input 组，见 deploy/udev/99-ly-remote.rules）：

    KERNEL=="event*", ATTRS{idVendor}=="24ae", ATTRS{idProduct}=="2013",
    MODE="0664", GROUP="input"

没配权限时这里会报出明确错误日志（节点照常启动，只是收不到按键）。
"""

from __future__ import annotations

import glob
import os
import queue
import select
import struct
import threading
import time

EV_KEY = 1

# x86_64 的 struct input_event：秒(long) 微秒(long) type(ushort)
# code(ushort) value(int) = 24 字节
EVENT_FMT = "llHHi"
EVENT_SIZE = struct.calcsize(EVENT_FMT)

# 找不到设备 / 打开失败后的重试间隔（秒）
RETRY_INTERVAL = 2.0
OPEN_FAIL_INTERVAL = 5.0


class RemoteKeyReader:
    """读遥控按键的后台线程；get_press() 非阻塞取一次按键码。

    支持热插拔：未插入时等待，拔出后自动重搜，插回后自动重连。
    """

    def __init__(self, node, device_name: str, event_no: int, abort_code: int,
                 key_codes=None):
        self._node = node
        self._device_name = device_name
        self._event_no = event_no
        self._abort_code = abort_code
        # 需要监听的按键码列表：用于能力位图匹配（精确识别键盘接口）
        self._key_codes = list(key_codes) if key_codes else []
        self._queue: queue.Queue = queue.Queue()
        # 急停标志：读线程在 D 键按下的瞬间置位，主循环/等待循环随时可见
        self.abort_event = threading.Event()
        self._thread = None
        self.device_path = None

    def start(self) -> bool:
        """启动后台监听线程。找不到设备时线程会持续重试，运行中插拔自动重连。"""
        self._thread = threading.Thread(target=self._run, daemon=True, name="remote-key")
        self._thread.start()
        return True

    def get_press(self):
        """非阻塞取一个按键码，没有则返回 None。"""
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def _find_device(self):
        """按名字+按键能力找遥控的键盘接口；找不到返回 None。

        候选条件（两道筛选）：
        1. 接口名包含 device_name（排除机器人上插的其他键盘/触摸屏）；
        2. 能力位图里包含所有要监听的按键码（排除同一接收器的
           System Control / Consumer Control / Mouse 接口——它们名字也
           包含 "Knight22" 但发不出数字键）。
        多个候选时取名字最短的（裸键盘接口名字最短），保证结果稳定。
        """
        if self._event_no > 0:
            return f"/dev/input/event{self._event_no}"
        candidates = []
        for event_dir in sorted(glob.glob("/sys/class/input/event*")):
            name_file = f"{event_dir}/device/name"
            try:
                with open(name_file, encoding="utf-8", errors="replace") as f:
                    name = f.read().strip()
            except OSError:
                continue
            if self._device_name not in name:
                continue
            if self._key_codes and not self._has_key_cap(event_dir, self._key_codes):
                continue
            candidates.append((len(name), event_dir))
        if not candidates:
            return None
        _, event_dir = min(candidates)
        return "/dev/input/" + os.path.basename(event_dir)

    @staticmethod
    def _has_key_cap(event_dir: str, key_codes) -> bool:
        """读 capabilities/key 位图，判断接口能否发出这些按键码。

        位图格式（内核 input 子系统）：空格分隔的 64 位十六进制组，
        从最高非零组往下排到组 0；第 g 组的第 b 位 = 按键码 64*g + b。
        每个组按数值解析（int(x, 16)），十六进制位数不需要补齐。
        """
        try:
            with open(f"{event_dir}/device/capabilities/key") as f:
                raw = f.read().strip()
        except OSError:
            return False
        try:
            words = [int(w, 16) for w in raw.split()]
        except ValueError:
            return False
        for code in key_codes:
            g, b = divmod(code, 64)
            idx = len(words) - 1 - g  # 打印顺序从高组到低组
            if idx < 0 or not ((words[idx] >> b) & 1):
                return False
        return True

    def _run(self):
        fd = None
        warned_missing = False
        while True:  # daemon 线程，节点退出时随进程结束
            if fd is None:
                path = self._find_device()
                if path is None:
                    if not warned_missing:
                        self._node.get_logger().error(
                            f"未找到遥控设备（名字包含 {self._device_name!r} 且"
                            "能发出 A/B/C/D 按键的接口），将持续等待接入"
                        )
                        warned_missing = True
                    time.sleep(RETRY_INTERVAL)
                    continue
                try:
                    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
                except PermissionError:
                    self._node.get_logger().error(
                        f"无权限读 {path}：请确认运行用户已加入 input 组"
                        "且 udev 规则已生效（重新插拔遥控或重启）"
                    )
                    time.sleep(OPEN_FAIL_INTERVAL)
                    continue
                except OSError as exc:
                    self._node.get_logger().error(f"打开遥控设备失败 {path}: {exc}")
                    time.sleep(OPEN_FAIL_INTERVAL)
                    continue
                warned_missing = False
                self.device_path = path
                self._node.get_logger().info(f"遥控按键监听已启动：{path}")
            ready, _, _ = select.select([fd], [], [], 0.5)
            if not ready:
                continue
            try:
                data = os.read(fd, EVENT_SIZE * 16)
            except OSError:
                # 设备被拔掉：句柄失效，关掉重新按名字找（重新枚举后
                # event 编号可能变，不能沿用旧路径）
                self._node.get_logger().warn("遥控设备读取失败（可能被拔掉），重新搜索设备")
                try:
                    os.close(fd)
                except OSError:
                    pass
                fd = None
                self.device_path = None
                continue
            for i in range(0, len(data) - EVENT_SIZE + 1, EVENT_SIZE):
                _sec, _usec, etype, code, value = struct.unpack(
                    EVENT_FMT, data[i : i + EVENT_SIZE]
                )
                if etype != EV_KEY:
                    continue
                if value == 0:  # 松开
                    continue
                if value == 2:  # 长按自动重复，忽略（避免误触发多次）
                    continue
                self._queue.put(code)
                if code == self._abort_code:
                    self.abort_event.set()
