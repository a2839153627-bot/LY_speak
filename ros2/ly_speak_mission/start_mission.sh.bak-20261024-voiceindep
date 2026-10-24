#!/bin/bash
# LY_Guide 讲解任务执行节点启动脚本
# 用法：bash start_mission.sh [ros2 run 参数...]
# 常用参数：--ros-args -p dry_run:=true -p plan_id:=1
# 注意：不能加 -u（nounset）——/opt/ros/humble/setup.bash 引用了未定义变量，严格模式下直接报 unbound variable
set -eo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-6}"

source /opt/ros/humble/setup.bash
# /guide_voice/speak 服务类型（insp_interfaces）由 LY_speak_ws 自带的 voice
# 接口包提供，本工作区一条龙，不再依赖巡检的 LY_inspect_ws
source "${SCRIPT_DIR}/../install/setup.bash"

exec ros2 run ly_speak_mission guide_mission_node "$@"
