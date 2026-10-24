"""LY_Guide 讲解任务执行节点。

auto 模式（run_mode=auto，默认）：从 LY_speak_ws 后端（Flask，本机 5000 端口）
拉取讲解方案点位，按 sort 顺序导航到每个点位，**到达即触发播报**讲解词，
播报完成后立即前往下一点；全部点位完成后导航回充电点。

remote 模式（run_mode=remote）：讲解员用雷柏遥控手动步进，机器人
不再全自动走完全程——B 键开始任务（原地不动只播报提示），A 键去
下一个点位（到点播报完停下等下一按），C 键重播当前点位讲解词，
D 键急停（取消导航并结束任务）。只能往后走、不能往回，按未到点位
之前的键无效。全部点位完成后按 A 键返回充电点收尾。

取数接口：
    GET /api/plan/list?status=1       选择方案（plan_id 参数 > 0 时指定）
    GET /api/guide/byPlan/<planId>    方案点位（已按 sort 排序）
    GET /api/map/<mapId>              充电点 chargeX / chargeY / chargeAngle
                                      及禁区 keepoutZones（任务开始时发布给 Nav2 KeepoutFilter）

运行依赖：
    /navigate_to_pose  Nav2 action（必须在线）
    /guide_voice/speak LY_speak_ws 自带 voice 服务（离线 TTS，缺失则静音执行）
    /dev/input/event*  遥控器（remote 模式，雷柏 Knight22，见 remote_input.py）

触发方式：
    auto 模式：节点启动即执行（auto_start 参数，默认 true），或通过
    /ly_speak_mission/start（std_srvs/Trigger）随时触发下一次任务；
    remote 模式：遥控 B 键（或 /ly_speak_mission/start）开始任务。
"""

from __future__ import annotations

import json
import math
import re
import time
import urllib.error
import urllib.request

import rclpy
from nav2_msgs.msg import CostmapFilterInfo
from nav_msgs.msg import OccupancyGrid
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_srvs.srv import Trigger

from .navigation_client import NavigationClient
from .remote_input import RemoteKeyReader
from .voice_client import VoiceClient


class GuideMissionNode(Node):
    def __init__(self):
        super().__init__("guide_mission_node")

        self.declare_parameter("backend_url", "http://127.0.0.1:5000")
        self.declare_parameter("plan_id", 0)  # 0 = 自动选择第一个启用方案
        self.declare_parameter("auto_start", True)
        self.declare_parameter("dry_run", False)  # 跳过导航，点位虚拟到达（流程联调）
        self.declare_parameter("frame_id", "map")
        self.declare_parameter("nav_timeout_sec", 120.0)
        self.declare_parameter("voice_timeout_sec", 10.0)
        # 后端地图未配置充电点时使用的兜底坐标（机器人 profile 充电桩）
        self.declare_parameter("fallback_charge_x", 18.52)
        self.declare_parameter("fallback_charge_y", 1.0)
        self.declare_parameter("fallback_charge_angle", -94.0)
        # 遥控手动模式（remote）：B=开始任务 A=下一个点位 C=重播当前讲解 D=急停
        self.declare_parameter("run_mode", "auto")
        self.declare_parameter("remote_device_name", "Knight22 USB DEVICE")
        self.declare_parameter("remote_event_no", 0)  # 0 = 按设备名自动找
        # 雷柏 Knight22 遥控的 A/B/C/D 键发的是数字键 1/2/3/4
        # （Linux 按键码 KEY_1=2 / KEY_2=3 / KEY_3=4 / KEY_4=5，真机抓包确认）
        self.declare_parameter("key_a_code", 2)
        self.declare_parameter("key_b_code", 3)
        self.declare_parameter("key_c_code", 4)
        self.declare_parameter("key_d_code", 5)

        self._navigation = NavigationClient(
            self, frame_id=self.get_parameter("frame_id").value
        )
        # 禁区（keepout）发布：Nav2 costmap 的 KeepoutFilter 订阅
        # /costmap_filter_info；两个话题都用 transient_local，发布一次持续生效
        _latched = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self._keepout_info_pub = self.create_publisher(
            CostmapFilterInfo, "/costmap_filter_info", _latched
        )
        self._keepout_mask_pub = self.create_publisher(
            OccupancyGrid, "/keepout_filter_mask", _latched
        )
        self._voice = VoiceClient(self)
        self._voice_enabled = False
        self._busy = False
        self._start_requested = bool(self.get_parameter("auto_start").value)

        # 遥控模式状态：任务是否进行中 / 点位列表 / 充电点 / 下一个点位下标
        self._remote_reader = None
        self._rm_active = False
        self._rm_points = []
        self._rm_charge = None
        self._rm_idx = 0
        self._rm_start_requested = False
        if self.get_parameter("run_mode").value == "remote":
            self._remote_reader = RemoteKeyReader(
                self,
                device_name=self.get_parameter("remote_device_name").value,
                event_no=int(self.get_parameter("remote_event_no").value or 0),
                abort_code=int(self.get_parameter("key_d_code").value),
                key_codes=[
                    int(self.get_parameter("key_a_code").value),
                    int(self.get_parameter("key_b_code").value),
                    int(self.get_parameter("key_c_code").value),
                    int(self.get_parameter("key_d_code").value),
                ],
            )
            self._remote_reader.start()
            # 按键码 → 处理函数（B 开始 / A 下一个 / C 重播 / D 急停）
            self._key_handlers = {
                int(self.get_parameter("key_a_code").value): self._rm_next,
                int(self.get_parameter("key_b_code").value): self._rm_start,
                int(self.get_parameter("key_c_code").value): self._rm_replay,
                int(self.get_parameter("key_d_code").value): self._rm_stop,
            }

        self._start_service = self.create_service(
            Trigger, "/ly_speak_mission/start", self._on_start
        )
        self.get_logger().info(
            "讲解任务执行节点就绪（/ly_speak_mission/start 可触发，"
            f"run_mode={self.get_parameter('run_mode').value}, "
            f"auto_start={self._start_requested}, dry_run={self.get_parameter('dry_run').value}）"
        )

    # ── 触发 ──────────────────────────────────────────

    def _on_start(self, request, response):
        if self.get_parameter("run_mode").value == "remote":
            self._rm_start_requested = True
            response.success = True
            response.message = "已受理，遥控模式开始任务"
            return response
        if self._busy:
            response.success = False
            response.message = "任务正在执行中"
        else:
            self._start_requested = True
            response.success = True
            response.message = "已受理，即将开始讲解任务"
        return response

    def run(self):
        """主循环：spin_once 驱动；auto 模式空闲时受理 start 请求后同步
        执行任务，remote 模式由遥控按键驱动手动步进。"""
        if self.get_parameter("run_mode").value == "remote":
            self._run_remote()
            return
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
            if self._start_requested and not self._busy:
                self._start_requested = False
                self._run_mission()

    # ── 遥控手动模式 ────────────────────────────────

    def _run_remote(self):
        """遥控模式主循环：B 开始任务后，A 逐个去点位，C 重播讲解，D 急停。

        导航/播报是同步阻塞的（内部一直在 spin_once），所以主循环本身
        天然串行——按键在等待期间会排队，播完/到点后才处理下一个。
        唯一的例外是急停：读线程按下 D 的瞬间就置 abort_event，
        导航/播报的等待循环都在轮询它，可以立即打断。
        """
        self.get_logger().info(
            "遥控手动模式就绪：B=开始任务，A=下一个点位，C=重播当前讲解，D=急停"
        )
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
            if self._rm_start_requested:
                self._rm_start_requested = False
                self._rm_start()
            key = self._remote_reader.get_press()
            if key is None:
                continue
            handler = self._key_handlers.get(key)
            if handler is None:
                self.get_logger().info(f"遥控按键 code={key} 未绑定，忽略")
                continue
            handler()

    def _rm_start(self):
        """B 键：一键开启预设任务。只播报开始提示，机器人原地不动，等 A 键。"""
        if self._rm_active:
            self.get_logger().info("任务已在进行中，B 键忽略")
            return
        # 新任务开始时清掉历史急停标志：上次 D 急停（或空闲时误按 D）都会
        # 把 abort_event 置位，不清的话后续所有 B 都被"任务开始前已急停"
        # 拦死，节点必须重启才能再开任务（2026-10-24 实测踩中）。准备期间
        # 新按的 D 仍会被下面第 232 行的检查拦住，不会丢。
        self._remote_reader.abort_event.clear()
        plan = self._pick_plan()
        if plan is None:
            self.get_logger().error("未找到启用的讲解方案，任务终止")
            self._rm_speak("未找到可用的讲解方案，任务终止。")
            return
        points, map_info = self._fetch_points(plan["id"])
        if points is None:
            self.get_logger().error("讲解点数据获取失败，任务终止")
            self._rm_speak("讲解点数据获取失败，任务终止。")
            return
        if not points:
            self.get_logger().warn("该方案没有启用的讲解点，任务终止")
            self._rm_speak("该方案没有启用的讲解点。")
            return
        charge = self._resolve_charge(map_info)
        if charge is None:
            self.get_logger().error("无法确定充电点，任务终止")
            self._rm_speak("充电点未配置，任务终止。")
            return

        if self.get_parameter("dry_run").value:
            self.get_logger().info("dry_run 模式：跳过导航，点位虚拟到达")
        elif not self._navigation.wait_until_ready():
            self.get_logger().error("/navigate_to_pose 未就绪，任务终止")
            self._rm_speak("导航服务未就绪，任务终止。")
            return

        # 地图级禁区 → Nav2 KeepoutFilter
        self._publish_keepout(map_info.get("keepoutZones") if map_info else None)

        self._voice_enabled = self._voice.wait_ready(
            self.get_parameter("voice_timeout_sec").value
        )
        if not self._voice_enabled:
            self.get_logger().warn("/guide_voice/speak 未就绪，本次任务静音执行")

        # 禁区发布后的生效自检：读全局代价图数致命格，未生效会打日志+语音提示
        if not self.get_parameter("dry_run").value:
            self._check_keepout_effect(map_info.get("keepoutZones") if map_info else None)

        # 启动准备期间的 D 键急停也要生效，不能被下面的 clear() 吞掉
        if self._remote_reader.abort_event.is_set():
            self.get_logger().warn("任务开始前已急停，放弃启动")
            return

        self._remote_reader.abort_event.clear()
        self._rm_active = True
        self._rm_points = points
        self._rm_charge = charge
        self._rm_idx = 0

        plan_name = plan.get("planName") or ""
        self._rm_speak(f"开始讲解任务{plan_name}，共{len(points)}个点位。")
        self.get_logger().info(
            f"== 遥控模式开始 方案[{plan_name}] 点位 {len(points)} 个，充电点 {charge} =="
        )

    def _rm_next(self):
        """A 键：前往下一个点位并播报讲解词；全部点位完成后 A 键返回充电点收尾。

        只能往前走：已经走过的点位（_rm_idx 之前的）和更后面的点位都
        没有对应的按键处理路径——A 键永远指向 _rm_idx 指向的下一个点。
        导航失败时不推进 _rm_idx，再按 A 重试同一点。
        """
        if not self._rm_active:
            self.get_logger().info("任务未开始，A 键忽略（请先按 B 键开始任务）")
            return
        points = self._rm_points
        idx = self._rm_idx
        if idx < len(points):
            p = points[idx]
            name = p.get("pointName") or f"{idx + 1}号点位"
            self.get_logger().info(f"遥控前往 [{idx + 1}/{len(points)}] {name}")
            self._rm_speak(f"正在前往{idx + 1}号点位{name}。")
            if not self._rm_navigate(p):
                if self._rm_aborted():
                    return
                self._rm_speak(f"{name}导航失败，请按A键重试。")
                return
            self.get_logger().info(f"已到达 {name}")
            content = (p.get("content") or "").strip()
            if content:
                self._rm_speak_long(content)
            if self._rm_aborted():
                return
            self._rm_idx = idx + 1
            if self._rm_idx < len(points):
                self.get_logger().info("播报完成，等待 A 键前往下一个点位")
            else:
                self._rm_speak("所有点位讲解完成，按A键返回。")
            return
        # 所有点位已完成：A 键返回充电点，任务结束
        self._rm_speak("正在返回充电点。")
        if not self._rm_navigate(self._rm_charge):
            if self._rm_aborted():
                return
            self._rm_speak("返回充电点失败，请按A键重试。")
            return
        self._rm_speak("已返回充电点，本次讲解结束。")
        self._rm_active = False
        self._rm_points = []
        self._rm_charge = None
        self._rm_idx = 0
        self.get_logger().info("遥控模式任务结束，可按 B 键重新开始")

    def _rm_replay(self):
        """C 键：重播当前点位（刚到达的点位）的讲解词。"""
        if not self._rm_active:
            self.get_logger().info("任务未开始，C 键忽略")
            return
        if self._rm_idx <= 0 or self._rm_idx > len(self._rm_points):
            self.get_logger().info("还没有到达过点位，C 键忽略")
            return
        p = self._rm_points[self._rm_idx - 1]
        content = (p.get("content") or "").strip()
        if content:
            self.get_logger().info(f"重播当前点位 {self._rm_idx} 的讲解词")
            self._rm_speak_long(content)
            self._rm_aborted()

    def _rm_stop(self):
        """D 键：急停。取消导航并结束任务（正在播放的语音等当前句自然播完）。"""
        if not self._rm_active:
            self.get_logger().info("任务未在运行，D 键忽略")
            return
        # 读线程按下 D 的瞬间已置 abort_event，导航等待循环已开始取消；
        # 这里兜底再置一次并清理任务状态
        self._remote_reader.abort_event.set()
        self._rm_aborted()

    def _rm_aborted(self) -> bool:
        """急停清理：重置任务状态并播报提示。返回是否发生了急停。"""
        if not self._remote_reader.abort_event.is_set():
            return False
        self._rm_active = False
        self._rm_points = []
        self._rm_charge = None
        self._rm_idx = 0
        self.get_logger().warn("任务已紧急停止")
        self._rm_speak("已紧急停止任务。")
        return True

    def _rm_navigate(self, target) -> bool:
        """遥控模式导航（带急停打断）。dry_run 模式下虚拟到达。"""
        if self.get_parameter("dry_run").value:
            self.get_logger().info(f"[DRY-RUN] 虚拟到达 {target.get('name', '')}")
            self._sleep(1.0)
            return True
        result = self._navigation.navigate(
            target["x"],
            target["y"],
            target["angle"],
            timeout_sec=float(self.get_parameter("nav_timeout_sec").value),
            abort_check=lambda: self._remote_reader.abort_event.is_set(),
        )
        if not result.success:
            self.get_logger().warn(
                f"导航失败 {target.get('name', '')}: {result.status} {result.message}"
            )
        return result.success

    def _rm_speak(self, text: str) -> None:
        """遥控模式播报：急停事件会打断"等播完"的等待（已请求的句子会自然播完）。"""
        if not self._voice_enabled:
            return
        self._voice.speak(
            text, abort_check=lambda: self._remote_reader.abort_event.is_set()
        )

    def _rm_speak_long(self, text: str) -> None:
        """遥控模式整段播报讲解词（同 _speak_long，带急停打断）。"""
        text = re.sub(r"\s+", "", text)
        if text:
            self._rm_speak(text)

    # ── 任务主流程 ───────────────────────────────────

    def _run_mission(self):
        self._busy = True
        try:
            plan = self._pick_plan()
            if plan is None:
                self.get_logger().error("未找到启用的讲解方案，任务终止")
                self._speak("未找到可用的讲解方案，任务终止。")
                return

            points, map_info = self._fetch_points(plan["id"])
            if points is None:
                self.get_logger().error("讲解点数据获取失败，任务终止")
                self._speak("讲解点数据获取失败，任务终止。")
                return
            if not points:
                self.get_logger().warn("该方案没有启用的讲解点，任务终止")
                self._speak("该方案没有启用的讲解点。")
                return

            charge = self._resolve_charge(map_info)
            if charge is None:
                self.get_logger().error("无法确定充电点，任务终止")
                self._speak("充电点未配置，任务终止。")
                return

            # 地图级禁区（低矮障碍等避障识别不到的区域）→ Nav2 KeepoutFilter
            self._publish_keepout(map_info.get("keepoutZones") if map_info else None)

            if self.get_parameter("dry_run").value:
                self.get_logger().info("dry_run 模式：跳过导航，点位虚拟到达")
            elif not self._navigation.wait_until_ready():
                self.get_logger().error("/navigate_to_pose 未就绪，任务终止")
                self._speak("导航服务未就绪，任务终止。")
                return

            self._voice_enabled = self._voice.wait_ready(
                self.get_parameter("voice_timeout_sec").value
            )
            if not self._voice_enabled:
                self.get_logger().warn("/guide_voice/speak 未就绪，本次任务静音执行")

            # 禁区发布后的生效自检：读全局代价图数致命格，未生效会打日志+语音提示
            if not self.get_parameter("dry_run").value:
                self._check_keepout_effect(
                    map_info.get("keepoutZones") if map_info else None
                )

            plan_name = plan.get("planName") or ""
            self._speak(f"开始讲解任务{plan_name}，共{len(points)}个点位。")
            self.get_logger().info(
                f"== 开始讲解任务 方案[{plan_name}] 点位 {len(points)} 个，充电点 {charge} =="
            )

            for index, p in enumerate(points, start=1):
                name = p.get("pointName") or f"{index}号点位"
                self.get_logger().info(
                    f"[{index}/{len(points)}] 前往 {name} "
                    f"({p.get('x')}, {p.get('y')}, {p.get('angle')}°)"
                )
                self._speak(f"正在前往{name}。")
                nav_ok = self._navigate_to(p)
                if not nav_ok:
                    self.get_logger().warn(f"点位 {name} 导航失败，继续下一个点位")
                    self._speak(f"{name}导航失败，继续前往下一个点位。")
                    continue

                self.get_logger().info(f"已到达 {name}")
                # 到达即触发播报讲解词，播报完成后立即前往下一个点位
                content = (p.get("content") or "").strip()
                if content:
                    self._speak_long(content)

            self.get_logger().info("所有讲解点位执行完毕，返回充电点")
            self._speak("所有讲解点位已完成，正在返回。")
            if self._navigate_to(charge):
                self.get_logger().info("已到达充电点，任务完成")
                self._speak("已返回充电点，本次讲解结束。")
            else:
                self.get_logger().warn("返回充电点导航失败")
                self._speak("返回充电点失败。")
        finally:
            self._busy = False

    # ── 数据获取 ─────────────────────────────────────

    def _http_get(self, path: str):
        """GET 后端接口，返回解析后的 JSON（失败返回 None）。"""
        url = self.get_parameter("backend_url").value.rstrip("/") + path
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, ValueError) as exc:
            self.get_logger().error(f"接口请求失败 {url}: {exc}")
            return None

    def _pick_plan(self):
        """选择讲解方案：plan_id 参数 > 0 时指定，否则取第一个启用方案。"""
        plan_id = int(self.get_parameter("plan_id").value or 0)
        if plan_id > 0:
            res = self._http_get(f"/api/plan/{plan_id}")
            if res and res.get("code") == 200 and res.get("data"):
                return res["data"]
            self.get_logger().warn(f"指定方案 {plan_id} 不存在，回退自动选择")
        res = self._http_get("/api/plan/list?status=1")
        if not res or res.get("code") != 200:
            return None
        rows = res.get("rows") or []
        return rows[0] if rows else None

    def _fetch_points(self, plan_id: int):
        """拉取方案启用点位（按 sort 排序）与地图充电点信息。

        返回 (points, map_info)；接口失败时返回 (None, None)。
        """
        res = self._http_get(f"/api/guide/byPlan/{plan_id}")
        if not res or res.get("code") != 200 or not isinstance(res.get("data"), list):
            return None, None
        points = [
            p for p in res["data"]
            if int(p.get("status") or 0) == 1
            and p.get("x") is not None
            and p.get("y") is not None
        ]
        points.sort(key=lambda p: (int(p.get("sort") or 0), int(p.get("id") or 0)))

        map_id = (points[0].get("mapId") if points else None)
        map_info = None
        if map_id is not None:
            map_res = self._http_get(f"/api/map/{map_id}")
            if map_res and map_res.get("code") == 200:
                map_info = map_res.get("data") or {}
        if map_info is None:
            map_info = {}
        # 禁区汇总：方案可能挂在别的逻辑地图上（如方案[123]挂在"44"图，
        # 禁区却画在"一楼展厅图"），而机器人只有一张物理导航地图，
        # 因此汇总所有地图的 keepoutZones 一起发布，避免画了不生效
        zones = []
        maps_res = self._http_get("/api/map/list")
        if maps_res and maps_res.get("code") == 200:
            for row in maps_res.get("rows") or []:
                if isinstance(row.get("keepoutZones"), list):
                    zones.extend(row["keepoutZones"])
        map_info["keepoutZones"] = zones
        return points, map_info

    def _resolve_charge(self, map_info):
        """确定充电点：本图 chargeX/chargeY 优先；本图没配时取后台任一
        地图配置的充电点（同一台机器人一个物理充电桩）；都没有才用兜底参数。"""
        if map_info and map_info.get("chargeX") is not None and map_info.get("chargeY") is not None:
            return {
                "name": "充电点",
                "x": float(map_info["chargeX"]),
                "y": float(map_info["chargeY"]),
                "angle": float(map_info.get("chargeAngle") or 0),
            }
        maps_res = self._http_get("/api/map/list")
        if maps_res and maps_res.get("code") == 200:
            for row in maps_res.get("rows") or []:
                if row.get("chargeX") is not None and row.get("chargeY") is not None:
                    self.get_logger().info(
                        f"本图未配置充电点，采用地图[{row.get('mapName')}]的充电点"
                    )
                    return {
                        "name": "充电点",
                        "x": float(row["chargeX"]),
                        "y": float(row["chargeY"]),
                        "angle": float(row.get("chargeAngle") or 0),
                    }
        return {
            "name": "充电点（兜底）",
            "x": float(self.get_parameter("fallback_charge_x").value),
            "y": float(self.get_parameter("fallback_charge_y").value),
            "angle": float(self.get_parameter("fallback_charge_angle").value),
        }

    # ── 禁区发布 ─────────────────────────────────────

    @staticmethod
    def _parse_zones(zones):
        """zones（[[{x, y}, ...], ...]）→ 有效多边形顶点列表 [[(x, y), ...], ...]。

        前端画禁区是「点回起点闭合」，早期版本要求 ≥3 个顶点才能闭合：
        用户点 2 个端点后第 3 下点回起点，会被存成与首点近重合的第 3 个
        顶点，形成面积≈0 的退化细条（整张掩码只标几个散点格，规划器无视）。
        这里修复这类历史数据：末点与首点距离 ≤0.15m 视为闭合误点丢弃；
        剩下 2 点时按线状障碍展开成 0.3m 宽矩形（垂线各外扩 0.15m）。
        """
        polys = []
        for zone in zones or []:
            pts = [
                (float(p["x"]), float(p["y"]))
                for p in zone
                if p and p.get("x") is not None and p.get("y") is not None
            ]
            if len(pts) >= 3 and math.hypot(
                pts[-1][0] - pts[0][0], pts[-1][1] - pts[0][1]
            ) <= 0.15:
                pts = pts[:-1]  # 闭合误点，丢弃
            if len(pts) == 2:
                (ax, ay), (bx, by) = pts
                dx, dy = bx - ax, by - ay
                ln = math.hypot(dx, dy)
                if ln < 1e-6:
                    continue
                px, py = -dy / ln * 0.15, dx / ln * 0.15
                pts = [
                    (ax + px, ay + py),
                    (bx + px, by + py),
                    (bx - px, by - py),
                    (ax - px, ay - py),
                ]
            if len(pts) >= 3:
                polys.append(pts)
        return polys

    def _publish_keepout(self, zones):
        """发布禁区多边形给 Nav2 KeepoutFilter。

        zones: [[{x, y}, ...], ...]（世界坐标米，与讲解点同坐标系）。
        掩码与全局代价图同尺寸/同分辨率/同原点——Nav2 对掩码与代价图
        按格子一一对应，尺寸或原点不一致时禁区会标错位置甚至不生效
        （官方教程的掩码就是整张地图大小）。多边形内部标 100（障碍），
        外部为 0；zones 为空时发全 0 掩码清除。取不到代价图几何信息时
        退化为只覆盖禁区外接矩形的小掩码。
        """
        polys = self._parse_zones(zones)

        info = CostmapFilterInfo()
        info.header.frame_id = "map"
        info.header.stamp = self.get_clock().now().to_msg()
        info.type = 0  # KEEPOUT
        info.filter_mask_topic = "/keepout_filter_mask"
        info.base = 0.0
        info.multiplier = 1.0

        meta = self._fetch_costmap_meta()
        if meta is None:
            # 导航栈未就绪取不到代价图几何，退化为小掩码（外接矩形）
            res = 0.05
            if polys:
                xs = [p[0] for poly in polys for p in poly]
                ys = [p[1] for poly in polys for p in poly]
                ox = math.floor((min(xs) - 0.2) / res) * res
                oy = math.floor((min(ys) - 0.2) / res) * res
                w = int(math.ceil((max(xs) - ox) / res)) + 2
                h = int(math.ceil((max(ys) - oy) / res)) + 2
            else:
                ox, oy, w, h = 0.0, 0.0, 2, 2
            self.get_logger().warn("未取到全局代价图几何信息，禁区掩码退化为小掩码")
        else:
            w, h, res, ox, oy = meta

        grid = OccupancyGrid()
        grid.header.frame_id = "map"
        grid.header.stamp = self.get_clock().now().to_msg()
        grid.info.resolution = res
        grid.info.width = w
        grid.info.height = h
        grid.info.origin.position.x = ox
        grid.info.origin.position.y = oy
        grid.info.origin.orientation.w = 1.0
        data = bytearray(w * h)  # 默认 0（自由）
        for poly in polys:  # 只扫多边形外接矩形内的格点，其余保持 0
            i0 = max(0, int(math.floor((min(p[0] for p in poly) - 0.2 - ox) / res)))
            i1 = min(w - 1, int(math.ceil((max(p[0] for p in poly) + 0.2 - ox) / res)))
            j0 = max(0, int(math.floor((min(p[1] for p in poly) - 0.2 - oy) / res)))
            j1 = min(h - 1, int(math.ceil((max(p[1] for p in poly) + 0.2 - oy) / res)))
            for j in range(j0, j1 + 1):
                wy = oy + (j + 0.5) * res
                for i in range(i0, i1 + 1):
                    if self._in_polys(ox + (i + 0.5) * res, wy, polys):
                        data[j * w + i] = 100  # 障碍
        grid.data = list(data)

        # 先发 mask 再发 info：filter 收到 info 后才订阅 mask，
        # 两者都 transient_local，顺序不影响，但这样首帧必得
        self._keepout_mask_pub.publish(grid)
        self._keepout_info_pub.publish(info)
        self.get_logger().info(f"已发布禁区 {len(polys)} 个（mask {w}x{h} @{res}m）")

    def _fetch_costmap_meta(self, timeout_sec=3.0):
        """取一帧 /global_costmap/costmap 的几何信息 (w, h, res, ox, oy)；失败返回 None。"""
        meta = []

        def _cb(msg):
            meta.append((
                msg.info.width,
                msg.info.height,
                float(msg.info.resolution),
                float(msg.info.origin.position.x),
                float(msg.info.origin.position.y),
            ))

        sub = self.create_subscription(
            OccupancyGrid,
            "/global_costmap/costmap",
            _cb,
            QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE),
        )
        deadline = time.monotonic() + max(0.5, float(timeout_sec))
        while not meta and time.monotonic() < deadline and rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
        self.destroy_subscription(sub)
        return meta[0] if meta else None

    @staticmethod
    def _in_polys(px, py, polys):
        """射线法：点是否落在任一多边形内。"""
        for poly in polys:
            n = len(poly)
            j = n - 1
            inside = False
            for i in range(n):
                xi, yi = poly[i]
                xj, yj = poly[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                return True
        return False

    @staticmethod
    def _count_lethal_in_polys(msg, polys):
        """数一帧代价图里落在禁区多边形内的致命格数量。

        OccupancyGrid 的 data 是 int8。致命判定兼容两套成本约定：
        - 标准 Nav2：致命 254 在 Python 里是 -2（空闲 0、膨胀 1~99、
          未知 -1），所以 `<= -2` 即致命；
        - 本机厂商导航链用 0-100 成本体系（墙=100 即致命，SmacPlanner2D/
          MPPI 按 100 判致命）：掩码 100 经 KeepoutFilter 缩放成 254 后，
          会被厂商的 keepout_inflation_filter 重写回 100，代价图里禁区
          呈现为 100（已用 10-21 真机数据核实），所以 `>= 100` 也算致命。
        只扫多边形外接矩形（+0.2m 边距）内的格点，用射线法确认格心在
        多边形内。返回 (致命格数, 接近致命格数 90~99，仅供诊断)。
        """
        res = float(msg.info.resolution)
        ox = float(msg.info.origin.position.x)
        oy = float(msg.info.origin.position.y)
        min_x = min(p[0] for poly in polys for p in poly) - 0.2
        max_x = max(p[0] for poly in polys for p in poly) + 0.2
        min_y = min(p[1] for poly in polys for p in poly) - 0.2
        max_y = max(p[1] for poly in polys for p in poly) + 0.2
        lethal = 0
        near_lethal = 0
        for row in range(msg.info.height):
            wy = oy + (row + 0.5) * res
            if not min_y <= wy <= max_y:
                continue
            for col in range(msg.info.width):
                wx = ox + (col + 0.5) * res
                if not min_x <= wx <= max_x:
                    continue
                if not GuideMissionNode._in_polys(wx, wy, polys):
                    continue
                v = msg.data[row * msg.info.width + col]
                if v <= -2 or v >= 100:
                    lethal += 1
                elif v >= 90:
                    near_lethal += 1
        return lethal, near_lethal

    def _check_keepout_effect(self, zones, wait_sec=8.0):
        """禁区生效自检：读 /global_costmap/costmap，数禁区格点是否被标致命。

        Nav2 KeepoutFilter 的 updateBounds 入口就是 `if (!enabled_) return`，
        enabled_ 是导航栈启动时读定的内存值，运行时 ros2 param set 不生效。
        导航栈若是在 yaml 翻转 enabled 之前启动的，过滤器会照常收掩码但
        一个格都不标，全局规划就不会绕开。这里发布掩码后读几帧代价图核实：
        禁区格点出现致命值即生效（提前结束等待）；读满 wait_sec 仍是 0 则
        打错误日志并语音提示（任务照常继续，由操作者决定是否让机器人走）。
        """
        polys = self._parse_zones(zones)
        if not polys:
            return  # 没有禁区，无需检查
        self._keepout_costmaps = []
        sub = self.create_subscription(
            OccupancyGrid,
            "/global_costmap/costmap",
            lambda msg: self._keepout_costmaps.append(msg),
            QoSProfile(depth=5, reliability=ReliabilityPolicy.RELIABLE),
        )
        deadline = time.monotonic() + wait_sec
        got_msg = False
        aborted = False
        lethal_seen = 0
        near_seen = 0
        while time.monotonic() < deadline:
            # remote 模式急停（D 键）可打断自检等待
            if self._remote_reader is not None and self._remote_reader.abort_event.is_set():
                aborted = True
                break
            if self._keepout_costmaps:
                got_msg = True
                msg = self._keepout_costmaps.pop()  # 最新一帧
                cnt, near = self._count_lethal_in_polys(msg, polys)
                lethal_seen = max(lethal_seen, cnt)
                near_seen = max(near_seen, near)
                if lethal_seen >= 5:
                    break
            self._sleep(0.2)
        self.destroy_subscription(sub)
        self._keepout_costmaps = []
        if aborted:
            self.get_logger().warn("禁区自检被急停打断")
            return
        if not got_msg:
            self.get_logger().warn("禁区自检：读不到 /global_costmap/costmap，跳过")
            return
        if lethal_seen >= 5:
            self.get_logger().info(f"禁区已生效：代价图禁区格点致命 {lethal_seen} 格")
            return
        self.get_logger().error(
            f"禁区未生效：KeepoutFilter 收到掩码但代价图未出现致命格"
            f"（禁区格点内接近致命 90~99 值 {near_seen} 格），"
            "请保留本次任务日志用于排查（过滤器未启用/掩码几何不一致等）"
        )
        self._speak("注意，地图禁区保护未生效，本次任务可能进入禁区。")

    # ── 执行动作 ─────────────────────────────────────

    def _navigate_to(self, target) -> bool:
        """导航到目标点（dict: x / y / angle 度）。dry_run 模式下虚拟到达。"""
        if self.get_parameter("dry_run").value:
            self.get_logger().info(f"[DRY-RUN] 虚拟到达 {target.get('name', '')}")
            self._sleep(1.0)
            return True
        result = self._navigation.navigate(
            target["x"],
            target["y"],
            target["angle"],
            timeout_sec=float(self.get_parameter("nav_timeout_sec").value),
        )
        if not result.success:
            self.get_logger().warn(
                f"导航失败 {target.get('name', '')}: {result.status} {result.message}"
            )
        return result.success

    def _speak(self, text: str) -> None:
        if not self._voice_enabled:
            return
        self._voice.speak(text)

    def _speak_long(self, text: str) -> None:
        """讲解词整段一次播报。

        TTS 节点（tts_python_node）内部会按 80 字分块连续合成一个 wav，
        片段间只留 0.12s；若这里逐句发请求，每个句末标点都是一次
        "等播完 → 发新请求 → 重新合成"的往返，会造成明显停顿，且每段
        开头的字容易因重新打开播放设备而被吞掉。
        """
        text = re.sub(r"\s+", "", text)
        if text:
            self._speak(text)

    def _sleep(self, sec: float) -> None:
        deadline = time.monotonic() + max(0.0, float(sec))
        while rclpy.ok() and time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)


def main(args=None):
    rclpy.init(args=args)
    node = GuideMissionNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
