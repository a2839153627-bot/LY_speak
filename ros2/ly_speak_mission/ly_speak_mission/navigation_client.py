"""Nav2 导航最小封装：发送单个目标位姿并等待最终结果。

复刻自 LY_inspect_ws 巡检流程中已验证的 NavigationClient（行为一致）。
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import rclpy
from action_msgs.msg import GoalStatus
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient


@dataclass(frozen=True)
class NavigationResult:
    success: bool
    status: str
    message: str = ""


class NavigationClient:
    """Send one pose goal and return the final Nav2 result."""

    def __init__(self, node, action_name: str = "navigate_to_pose", frame_id: str = "map") -> None:
        self._node = node
        self._frame_id = frame_id
        self._client = ActionClient(node, NavigateToPose, action_name)
        self._goal_handle = None

    def wait_until_ready(self, timeout_sec: float = 45.0) -> bool:
        return self._client.wait_for_server(timeout_sec=timeout_sec)

    def navigate(
        self,
        x: float,
        y: float,
        yaw_degrees: float,
        timeout_sec: float = 120.0,
        abort_check=None,
    ) -> NavigationResult:
        """发送导航目标并等最终结果。

        abort_check：可选回调，返回 True 表示外部急停（遥控 D 键），
        立即取消目标并返回 NavigationResult(False, "aborted", ...)。
        """
        if not self._client.server_is_ready():
            return NavigationResult(False, "unavailable", "navigate_to_pose unavailable")

        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = self._frame_id
        goal.pose.header.stamp = self._node.get_clock().now().to_msg()
        goal.pose.pose.position.x = float(x)
        goal.pose.pose.position.y = float(y)
        yaw = math.radians(float(yaw_degrees))
        goal.pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal.pose.pose.orientation.w = math.cos(yaw / 2.0)

        send_future = self._client.send_goal_async(goal)
        if not self._wait(send_future, 10.0, abort_check):
            if abort_check is not None and abort_check():
                # 急停发生在目标发送途中：等 send 完成立刻取消，
                # 避免目标落到 Nav2 后机器人自己走
                if self._wait(send_future, 10.0):
                    self._cancel_handle(send_future)
                else:
                    send_future.cancel()
                return NavigationResult(False, "aborted", "remote abort")
            send_future.cancel()
            return NavigationResult(False, "timeout", "send goal timeout")

        try:
            self._goal_handle = send_future.result()
        except Exception as exc:
            return NavigationResult(False, "failed", str(exc))
        if self._goal_handle is None or not self._goal_handle.accepted:
            self._goal_handle = None
            return NavigationResult(False, "rejected", "goal rejected")

        result_future = self._goal_handle.get_result_async()
        if not self._wait(result_future, timeout_sec, abort_check):
            self.cancel()
            if abort_check is not None and abort_check():
                return NavigationResult(False, "aborted", "remote abort")
            return NavigationResult(False, "timeout", "navigation timeout")

        try:
            status = int(result_future.result().status)
        except Exception as exc:
            self.cancel()
            return NavigationResult(False, "failed", str(exc))

        self._goal_handle = None
        if status == GoalStatus.STATUS_SUCCEEDED:
            return NavigationResult(True, "succeeded")
        if status == GoalStatus.STATUS_CANCELED:
            return NavigationResult(False, "canceled")
        return NavigationResult(False, "failed", f"Nav2 status={status}")

    def cancel(self, timeout_sec: float = 5.0) -> bool:
        if self._goal_handle is None:
            return True
        future = self._goal_handle.cancel_goal_async()
        canceled = self._wait(future, timeout_sec)
        self._goal_handle = None
        return canceled

    def close(self) -> None:
        self.cancel()
        self._client.destroy()

    def _cancel_handle(self, send_future) -> None:
        """目标刚被接受就立刻取消（用于急停发生在 send 阶段的情况）。"""
        try:
            handle = send_future.result()
        except Exception:
            return
        if handle is not None and handle.accepted:
            handle.cancel_goal_async()

    def _wait(self, future, timeout_sec: float, abort_check=None) -> bool:
        deadline = time.monotonic() + max(0.0, float(timeout_sec))
        while rclpy.ok() and not future.done() and time.monotonic() < deadline:
            if abort_check is not None and abort_check():
                return False
            rclpy.spin_once(self._node, timeout_sec=0.1)
        return future.done()
