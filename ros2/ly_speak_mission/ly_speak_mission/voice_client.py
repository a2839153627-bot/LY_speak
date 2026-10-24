"""讲解任务语音客户端：调用讲解任务自己的语音服务 /guide_voice/speak。

LY_speak_ws 自带 voice 包与 insp_interfaces 接口包，rclpy 客户端直接可用；
若导入失败则退回 ros2 CLI 调用。两种模式都通过 /guide_tts/status
（std_msgs/String，JSON）判断当前播报是否结束。
"""

from __future__ import annotations

import json
import re
import subprocess
import threading
import time

import rclpy
from std_msgs.msg import String

try:
    from insp_interfaces.srv import Speak

    _HAS_INSP_INTERFACES = True
except ImportError:
    _HAS_INSP_INTERFACES = False

_PUNCT_RE = re.compile(
    r"[\s，。！？；、,.!?;:：；（）()【】\[\]{}《》<>\"'‘’“”`·~～@#￥$%^&*_+=|\\/—-]+"
)


class VoiceClient:
    """讲解任务唯一语音调用方，统一调用讲解任务语音服务 /guide_voice/speak。"""

    def __init__(self, node):
        self._node = node
        self._status_sub = node.create_subscription(
            String, "/guide_tts/status", self._on_status, 10
        )
        self._lock = threading.Lock()
        self._last_status = {}
        self._mode = "client" if _HAS_INSP_INTERFACES else "cli"
        if self._mode == "client":
            self._client = node.create_client(Speak, "/guide_voice/speak")

    def wait_ready(self, timeout_sec: float = 10.0) -> bool:
        """等待 /guide_voice/speak 服务就绪。"""
        if self._mode == "client":
            return self._client.wait_for_service(timeout_sec=timeout_sec)
        deadline = time.monotonic() + max(0.0, float(timeout_sec))
        while rclpy.ok() and time.monotonic() < deadline:
            try:
                out = subprocess.run(
                    ["ros2", "service", "list"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                ).stdout
                if "/guide_voice/speak" in out:
                    return True
            except Exception:
                pass
            time.sleep(1.0)
        return False

    def speak(self, text: str, *, wait: bool = True, abort_check=None) -> None:
        """请求播报；abort_check 返回 True 时不再等待播完（急停用），
        已发出的请求会排队自然播完。"""
        text = str(text or "").strip()
        if not text:
            return
        if self._mode == "client":
            self._speak_client(text, wait, abort_check)
        else:
            self._speak_cli(text, wait, abort_check)

    def _speak_client(self, text: str, wait: bool, abort_check) -> None:
        if not self._client.service_is_ready():
            return
        req = Speak.Request()
        req.text = text
        # 任务按顺序播报，永远等上一条播完才发下一条，无需抢占。
        # interrupt_current=True 会让 TTS 节点杀掉正在播放的音频（吞话根因），
        # 这里传 False，让本条排队等待上一条自然播完。
        req.interrupt_current = False
        started = time.monotonic()
        future = self._client.call_async(req)
        if not wait:
            return
        while rclpy.ok():
            if future.done() or time.monotonic() - started >= 2.0:
                break
            rclpy.spin_once(self._node, timeout_sec=0.05)
        self._wait_finished(text, started, abort_check)

    def _speak_cli(self, text: str, wait: bool, abort_check) -> None:
        payload = json.dumps(
            {"text": text, "interrupt_current": True}, ensure_ascii=False
        )
        try:
            subprocess.run(
                [
                    "ros2", "service", "call", "/guide_voice/speak",
                    "insp_interfaces/srv/Speak", payload,
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
        except Exception as exc:
            self._node.get_logger().warn(f"/guide_voice/speak CLI 调用失败: {exc}")
            return
        if not wait:
            return
        self._wait_finished(text, time.monotonic(), abort_check)

    def _wait_finished(self, text: str, started: float, abort_check=None) -> None:
        """等待 /guide_tts/status 上报本次播报结束（end / interrupted / error）。

        时长上限需覆盖整段的合成（约 0.35s/字）+ 播放（约 0.25s/字）：
        超长文本宁可等满，也不能提前超时，否则下一句会打断还在播放的音频。
        """
        deadline = time.monotonic() + min(120.0, max(10.0, len(text) * 0.7 + 6.0))
        key = _PUNCT_RE.sub("", text)
        while rclpy.ok() and time.monotonic() < deadline:
            if abort_check is not None and abort_check():
                self._node.get_logger().warn("语音等待被急停打断（已请求的句子会自然播完）")
                return
            with self._lock:
                status = dict(self._last_status)
            completed = status.get("state") in {"end", "interrupted", "error"}
            received_after_request = status.get("_recv_mono", 0) >= started
            matching_text = _PUNCT_RE.sub(
                "", str(status.get("text") or "")
            ) == key
            if completed and received_after_request and matching_text:
                self._node.get_logger().info(
                    f"语音播报结束(等待 {time.monotonic() - started:.1f}s, "
                    f"state={status.get('state')}, gen={status.get('generation')})"
                )
                return
            rclpy.spin_once(self._node, timeout_sec=0.05)
        self._node.get_logger().warn(
            f"语音播报等待超时({len(text)}字), 最后状态="
            f"{self._last_status.get('state')}/{self._last_status.get('text')}"
        )

    def _on_status(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data or "{}")
        except (TypeError, ValueError):
            return
        if isinstance(payload, dict):
            payload["_recv_mono"] = time.monotonic()
            with self._lock:
                self._last_status = payload
