#!/bin/bash
# LY_Guide 讲解任务自己的语音服务启动脚本（独立于巡检 LY_inspect_ws）
# 服务：/guide_voice/speak    状态话题：/guide_tts/status    节点名：guide_tts_node
# 用法：bash start_voice.sh（前台跑）；后台跑：setsid nohup bash start_voice.sh > voice.log 2>&1 &
# 注意：不能加 -u（nounset）——/opt/ros/humble/setup.bash 引用了未定义变量，严格模式下直接报 unbound variable
set -eo pipefail

export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-6}"

source /opt/ros/humble/setup.bash
source /home/smart/LY_speak_ws/ros2/install/setup.bash

exec ros2 launch guide_voice guide_voice.launch.py
