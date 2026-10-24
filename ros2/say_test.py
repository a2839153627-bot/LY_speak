#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""手动让讲解语音说一句话的测试工具。

用法: python3 say_test.py [要说的话]
示例: python3 say_test.py "你好呀，我是讲解机器人"
不带参数时默认说"讲解语音服务测试成功"。

前提:
  1. 讲解语音服务已在跑（bash .../ly_speak_mission/start_voice.sh）
  2. 本终端环境: source /opt/ros/humble/setup.bash
                source /home/smart/LY_speak_ws/ros2/install/setup.bash
    且 ROS_DOMAIN_ID=6（语音服务起在频道 6）
"""
import sys
import rclpy
from insp_interfaces.srv import Speak


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else "讲解语音服务测试成功"
    rclpy.init()
    node = rclpy.create_node("say_test")
    cli = node.create_client(Speak, "/guide_voice/speak")
    print("等 /guide_voice/speak 上线 ...")
    if not cli.wait_for_service(timeout_sec=5.0):
        print("连不上语音服务：先开 start_voice.sh，并确认本终端 ROS_DOMAIN_ID=6")
        sys.exit(1)
    req = Speak.Request()
    req.text = text
    req.interrupt_current = False
    fut = cli.call_async(req)
    rclpy.spin_until_future_complete(node, fut, timeout_sec=60.0)
    if fut.done() and fut.result() is not None:
        r = fut.result()
        print(f"语音服务回应: accepted={r.accepted}, message={r.message!r}")
    else:
        print("60 秒内没等到回应（合成+播放较慢时可能超时）")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
