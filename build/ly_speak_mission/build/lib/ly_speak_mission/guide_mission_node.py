"""LY_Guide 讲解任务执行节点。

流程：从 LY_speak_ws 后端（Flask，本机 5000 端口）拉取讲解方案点位，
按 sort 顺序导航到每个点位，**到达即触发播报**讲解词，播报完成后
立即前往下一点；全部点位完成后导航回充电点。

取数接口：
    GET /api/plan/list?status=1       选择方案（plan_id 参数 > 0 时指定）
    GET /api/guide/byPlan/<planId>    方案点位（已按 sort 排序）
    GET /api/map/<mapId>              充电点 chargeX / chargeY / chargeAngle

运行依赖：
    /navigate_to_pose  Nav2 action（必须在线）
    /voice/speak       LY_inspect_ws voice 服务（离线 TTS，缺失则静音执行）

触发方式：
    节点启动即执行（auto_start 参数，默认 true）；
    也可通过 /ly_speak_mission/start（std_srvs/Trigger）随时触发下一次任务。
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

from .navigation_client import NavigationClient
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

        self._navigation = NavigationClient(
            self, frame_id=self.get_parameter("frame_id").value
        )
        self._voice = VoiceClient(self)
        self._voice_enabled = False
        self._busy = False
        self._start_requested = bool(self.get_parameter("auto_start").value)

        self._start_service = self.create_service(
            Trigger, "/ly_speak_mission/start", self._on_start
        )
        self.get_logger().info(
            "讲解任务执行节点就绪（/ly_speak_mission/start 可触发，"
            f"auto_start={self._start_requested}, dry_run={self.get_parameter('dry_run').value}）"
        )

    # ── 触发 ──────────────────────────────────────────

    def _on_start(self, request, response):
        if self._busy:
            response.success = False
            response.message = "任务正在执行中"
        else:
            self._start_requested = True
            response.success = True
            response.message = "已受理，即将开始讲解任务"
        return response

    def run(self):
        """主循环：spin_once 驱动；空闲时受理 start 请求后同步执行任务。"""
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
            if self._start_requested and not self._busy:
                self._start_requested = False
                self._run_mission()

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
                self.get_logger().warn("/voice/speak 未就绪，本次任务静音执行")

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
                self._speak(f"正在前往{index}号点位{name}。")
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
            self._speak("所有讲解点位已完成，正在返回充电点。")
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
        return points, map_info

    def _resolve_charge(self, map_info):
        """确定充电点：后端地图 chargeX/chargeY 优先，否则用兜底参数。"""
        if map_info and map_info.get("chargeX") is not None and map_info.get("chargeY") is not None:
            return {
                "name": "充电点",
                "x": float(map_info["chargeX"]),
                "y": float(map_info["chargeY"]),
                "angle": float(map_info.get("chargeAngle") or 0),
            }
        return {
            "name": "充电点（兜底）",
            "x": float(self.get_parameter("fallback_charge_x").value),
            "y": float(self.get_parameter("fallback_charge_y").value),
            "angle": float(self.get_parameter("fallback_charge_angle").value),
        }

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
