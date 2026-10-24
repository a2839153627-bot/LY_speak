#!/bin/bash
# 讲解任务节点 —— 遥控手动模式启动脚本
# 按键分工：B=开始任务（一键开启预设方案，原地不动）
#           A=下一个点位（到点播报完停下；全部完成后 A 返回充电点）
#           C=重播当前点位讲解词
#           D=急停（取消导航、结束任务）
# 用法：bash start_remote.sh [ros2 run 参数...]
# 注意：
#   - 不能加 -u（nounset）——/opt/ros/humble/setup.bash 引用了未定义变量，严格模式下直接报 unbound variable
#   - run_mode 参数必须带 --ros-args，裸 -p run_mode:=remote 会被 ROS 当成 remap 规则不生效
set -eo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

export ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-6}"

source /opt/ros/humble/setup.bash
# /guide_voice/speak 服务类型（insp_interfaces）由 LY_speak_ws 自带的 voice
# 接口包提供，本工作区一条龙，不再依赖巡检的 LY_inspect_ws
source "${SCRIPT_DIR}/../install/setup.bash"

exec ros2 run ly_speak_mission guide_mission_node --ros-args -p run_mode:=remote "$@"
