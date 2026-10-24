#!/usr/bin/env bash
#
# LY_Guide 讲解任务一键启动（机器人端）
#
# 作用：按配置指定的地图拉起导航栈，待 /navigate_to_pose 就绪后启动讲解任务节点。
#
# 背景：讲解任务节点 ly_speak_mission 自己不加载地图，它只把后端下发的
#       (x, y, angle) 交给 Nav2 去走；这些坐标定义在「当前加载的那张地图」
#       的 map 坐标系下。所以要换地图跑讲解任务，必须同时做两件事：
#         1) 用 MAP_FILE / MAP3D_FILE 让导航栈加载新地图（本脚本负责）
#         2) 在 LY_Guide 平台上用同一张地图重新标定讲解点与充电点（平台侧负责）
#       只做第 1 步会导致机器人按旧坐标乱跑。
#
# 用法：
#   bash start_guide.sh --print-config        只打印解析出的地图与参数，不启动任何进程
#   bash start_guide.sh                       用 guide_map.conf 的地图起导航 + 讲解任务
#   bash start_guide.sh --map /path/to/mapdir 临时指定地图目录
#   bash start_guide.sh --no-nav              导航已在运行，只启动讲解任务节点
#   bash start_guide.sh --plan 3              指定讲解方案 ID（0 = 后端第一个启用方案）
#   bash start_guide.sh --dry-run             跳过导航、点位虚拟到达（仅联调播报流程）
#
# 可用环境变量覆盖：CONF_FILE / NAV_SCRIPT / MISSION_START / NAV_LOG / NAV_WAIT_SEC
#
set -Eeuo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

CONF_FILE=${CONF_FILE:-${SCRIPT_DIR}/guide_map.conf}
NAV_SCRIPT=${NAV_SCRIPT:-/home/smart/robot_scripts/navigation.sh}
MISSION_START=${MISSION_START:-/home/smart/LY_speak_ws/ros2/ly_speak_mission/start_mission.sh}
NAV_LOG=${NAV_LOG:-/home/smart/LY_speak_ws/nav.log}
NAV_WAIT_SEC=${NAV_WAIT_SEC:-150}

MAP_DIR=${MAP_DIR:-}
PLAN_ID=${PLAN_ID:-}
DRY_RUN=${DRY_RUN:-}
BACKEND_URL=${BACKEND_URL:-}
START_NAV=1
PRINT_ONLY=0

# ── 工具函数 ────────────────────────────────────────────

die() { echo "[ERROR] $*" >&2; exit 1; }

usage() {
  local end
  end=$(grep -n '^set -Eeuo pipefail' "${BASH_SOURCE[0]}" | head -n1 | cut -d: -f1)
  sed -n "2,$(( end - 1 ))p" "${BASH_SOURCE[0]}" \
    | sed -e 's/^#\{1,\}[[:space:]]\{0,1\}//' -e 's/^#$//'
  exit "${1:-0}"
}

# 取 ini 风格配置里某个键的值（忽略注释行与行内注释）
conf_get() {
  [[ -r "$CONF_FILE" ]] || return 0
  sed -n "s/^[[:space:]]*$1[[:space:]]*=[[:space:]]*\([^#]*\).*$/\1/p" "$CONF_FILE" \
    | head -n1 | sed -e 's/[[:space:]]*$//'
}

# 取 YAML 里某个标量键的值
yaml_val() {
  [[ -r "$1" ]] || return 0
  sed -n "s/^[[:space:]]*$2[[:space:]]*:[[:space:]]*\(.*\)$/\1/p" "$1" | head -n1
}

ros_env() {
  set +u
  # shellcheck disable=SC1091
  source /opt/ros/humble/setup.bash
  if [[ -r /home/smart/wheeltec_ws/install/local_setup.bash ]]; then
    source /home/smart/wheeltec_ws/install/local_setup.bash
  fi
  if [[ -r "${ROBOT_INSPECT_WS}/install/local_setup.bash" ]]; then
    source "${ROBOT_INSPECT_WS}/install/local_setup.bash"
  fi
  if [[ -r "${ROBOT_NAV_WS}/install/setup.bash" ]]; then
    source "${ROBOT_NAV_WS}/install/setup.bash"
  fi
  set -u
}

# 等待某个 ROS2 action 上线（nav2 起来要几十秒）
wait_for_action() {
  local name=$1 timeout=$2 elapsed=0 list
  echo "[WAIT] action ${name}（最长 ${timeout}s）"
  while (( elapsed < timeout )); do
    # 先完整取回列表再匹配：直接管道给 grep -q 会因 SIGPIPE 误报失败
    if list=$(timeout 4 ros2 action list 2>/dev/null) && grep -Fxq "$name" <<<"$list"; then
      echo "[READY] action ${name}"
      return 0
    fi
    sleep 2
    elapsed=$(( elapsed + 2 ))
  done
  return 1
}

# ROS 侧预检：明确指出「缺哪一环」，避免启动后干等、或机器人根本不会动
ros_preflight() {
  local subs pubs tf_out
  echo " ROS 预检（ROS_DOMAIN_ID=${ROS_DOMAIN_ID}）："

  if ! command -v ros2 >/dev/null 2>&1; then
    echo "   [SKIP] 当前 shell 没有 ros2，跳过 ROS 预检"
    return 0
  fi

  # 1) 底盘：/cmd_vel 有订阅者才算底盘 bringup 在跑（没有它机器人不会动）
  subs=$(timeout 8 ros2 topic info /cmd_vel 2>/dev/null | sed -n 's/^Subscription count: *//p' | head -n1 || true)
  if [[ -n "$subs" && "$subs" != "0" ]]; then
    echo "   [OK]   底盘 : /cmd_vel 有 ${subs} 个订阅者"
  else
    echo "   [WARN] 底盘 : /cmd_vel 无订阅者 → 请先跑 /home/smart/robot_scripts/base.sh"
  fi

  # 2) 地图
  pubs=$(timeout 8 ros2 topic info /map 2>/dev/null | sed -n 's/^Publisher count: *//p' | head -n1 || true)
  if [[ -n "$pubs" && "$pubs" != "0" ]]; then
    echo "   [OK]   地图 : /map 有发布者"
  else
    echo "   [WARN] 地图 : /map 无发布者 → 导航栈未就绪或已挂掉"
  fi

  # 3) Nav2 导航 action
  if timeout 8 ros2 action list 2>/dev/null | grep -Fxq /navigate_to_pose; then
    echo "   [OK]   Nav2 : /navigate_to_pose 在线"
  else
    echo "   [WARN] Nav2 : /navigate_to_pose 不在线"
  fi

  # 4) 语音（缺失时节点静音继续、不报错，所以必须显式提示）
  if timeout 8 ros2 service list 2>/dev/null | grep -Fxq /guide_voice/speak; then
    echo "   [OK]   语音 : /guide_voice/speak 在线（讲解任务自己的语音服务）"
  else
    echo "   [WARN] 语音 : /guide_voice/speak 不在线 → 讲解时不出声（节点静音执行）"
  fi

  # 5) 当前位姿 map→base_footprint：定位收敛后，也可用它直接读出充电点坐标
  tf_out=$(timeout 10 ros2 run tf2_ros tf2_echo map base_footprint 2>/dev/null | grep -A3 -m1 'Translation' || true)
  if [[ -n "$tf_out" ]]; then
    echo "   [OK]   位姿 : $(echo "$tf_out" | tr '\n' ' ' | tr -s ' ')"
  else
    echo "   [INFO] 位姿 : map→base_footprint 暂不可用（定位未收敛或导航栈未启动）"
  fi
  return 0
}

# 读 map.pgm 头部的宽高（去掉注释行后取 P5 后面的两个数）
pgm_dims() {
  local py=${PYTHON:-python3}
  command -v "$py" >/dev/null 2>&1 || return 0
  [[ -r "${MAP_DIR}/map.pgm" ]] || return 0
  "$py" - "${MAP_DIR}/map.pgm" <<'PY' 2>/dev/null || true
import re
import sys

head = open(sys.argv[1], "rb").read(300)
tokens = re.sub(rb"#[^\n]*", b"", head).split()
if len(tokens) >= 3:
    print("%sx%s" % (tokens[1].decode(), tokens[2].decode()))
PY
}

# 把「导航栈实际加载的 /map」与「配置文件期望的地图」并排打出来，
# 一眼就能看出有没有加载错地图（换图后最关键的一次确认）
show_loaded_map() {
  local info res w h ox oy
  info=$(timeout 12 ros2 topic echo /map --once --field info 2>/dev/null || true)
  if [[ -z "$info" ]]; then
    echo "   [WARN] 读不到 /map（地图尚未发布）"
    return 0
  fi
  res=$(echo "$info" | sed -n 's/^resolution: *//p' | head -n1)
  w=$(echo "$info"   | sed -n 's/^width: *//p'      | head -n1)
  h=$(echo "$info"   | sed -n 's/^height: *//p'     | head -n1)
  ox=$(echo "$info" | sed -n '/^origin:/,/^[[:space:]]*orientation:/p' | sed -n 's/^[[:space:]]*x: *//p' | head -n1)
  oy=$(echo "$info" | sed -n '/^origin:/,/^[[:space:]]*orientation:/p' | sed -n 's/^[[:space:]]*y: *//p' | head -n1)
  echo "   实际加载 : resolution=${res}  ${w}x${h}  origin=(${ox}, ${oy})"
  echo "   配置期望 : resolution=$(yaml_val "$MAP_FILE" resolution)  $(pgm_dims)  origin=$(yaml_val "$MAP_FILE" origin)"
}

# 向后端核对「将要执行哪个方案 / 哪张地图 / 充电点是否配好」
# 这一步是为了把两个静默陷阱显式暴露出来：
#   1. plan_id=0 取的是「id 最大的已启用方案」，不一定是你想跑的那个；
#   2. 地图未配 chargeX/chargeY 时，节点会静默退回到 LY_Nav 坐标系的兜底充电点。
backend_probe() {
  # 自检失败绝不能影响正常启动：解释器缺失直接返回，调用处再兜一层 || true
  local py=${PYTHON:-python3}
  command -v "$py" >/dev/null 2>&1 || return 0
  BACKEND_URL="$BACKEND_URL" PLAN_ID="$PLAN_ID" "$py" - <<'PY' || true
import json
import os
import urllib.request

base = os.environ["BACKEND_URL"].rstrip("/")
pid = int(os.environ.get("PLAN_ID") or 0)


def get(path):
    with urllib.request.urlopen(base + path, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


try:
    if pid > 0:
        plan = (get("/api/plan/%d" % pid) or {}).get("data")
    else:
        rows = (get("/api/plan/list?status=1") or {}).get("rows") or []
        plan = rows[0] if rows else None
except Exception as exc:  # noqa: BLE001
    print(" [WARN] 后端自检失败（%s）" % exc)
    print("        请自行确认「方案 ↔ 地图 ↔ 导航加载的地图」三者一致。")
    raise SystemExit(0)

if not plan:
    print(" [ERROR] 后端没有可用的启用方案，讲解任务会立刻终止！")
    raise SystemExit(0)

print(" 将执行方案 : id=%s  name=%s" % (plan.get("id"), plan.get("planName")))
print(" 方案绑定图 : id=%s  name=%s" % (plan.get("mapId"), plan.get("mapName")))

try:
    m = (get("/api/map/%s" % plan.get("mapId")) or {}).get("data") or {}
except Exception:  # noqa: BLE001
    m = {}

if m.get("chargeX") is None or m.get("chargeY") is None:
    print(" [WARN] 该地图未配置充电点 chargeX/chargeY！")
    print("        节点会退回兜底坐标 (18.52, 1.0, -94)，那是 LY_Nav 坐标系的点，")
    print("        机器人跑完最后一段会朝错误方向走。请先在平台上设置充电点。")
else:
    print(" 充电点     : x=%s  y=%s  angle=%s"
          % (m.get("chargeX"), m.get("chargeY"), m.get("chargeAngle")))

if pid == 0:
    print(" [注意] plan_id=0 取的是「id 最大的已启用方案」，本次为 id=%s；"
          % plan.get("id"))
    print("        若不是你要的方案，请用 --plan <ID> 明确指定。")
PY
}

# ── 解析命令行 ──────────────────────────────────────────

while (( $# )); do
  case "$1" in
    --map)          MAP_DIR=${2:-}; shift 2 ;;
    --map=*)        MAP_DIR=${1#*=}; shift ;;
    --plan)         PLAN_ID=${2:-}; shift 2 ;;
    --plan=*)       PLAN_ID=${1#*=}; shift ;;
    --dry-run)      DRY_RUN=true; shift ;;
    --no-nav)       START_NAV=0; shift ;;
    --print-config) PRINT_ONLY=1; shift ;;
    --conf)         CONF_FILE=${2:-}; shift 2 ;;
    -h|--help)      usage 0 ;;
    *)              die "未知参数: $1（用 --help 查看用法）" ;;
  esac
done

# ── 配置回退 ────────────────────────────────────────────

[[ -n "$MAP_DIR" ]]     || MAP_DIR=$(conf_get dir)
[[ -n "$PLAN_ID" ]]     || PLAN_ID=$(conf_get plan_id)
[[ -n "$DRY_RUN" ]]     || DRY_RUN=$(conf_get dry_run)
[[ -n "$BACKEND_URL" ]] || BACKEND_URL=$(conf_get backend_url)

PLAN_ID=${PLAN_ID:-0}
DRY_RUN=${DRY_RUN:-false}
BACKEND_URL=${BACKEND_URL:-http://127.0.0.1:5000}

[[ -n "$MAP_DIR" ]] || die "未指定地图目录：请用 --map <目录>，或在 ${CONF_FILE} 里设置 dir"

MAP_FILE="${MAP_DIR}/map.yaml"
MAP3D_FILE="${MAP_DIR}/map.pcd"
export MAP_FILE MAP3D_FILE
export ROBOT_NAV_WS=${ROBOT_NAV_WS:-/home/smart/LY_Nav/LY_Nav}
export ROBOT_INSPECT_WS=${ROBOT_INSPECT_WS:-/home/smart/LY_inspect_ws}
export ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-6}

print_config() {
  echo "────────────────────────────────────────────────────"
  echo " LY_Guide 讲解任务启动配置"
  echo "────────────────────────────────────────────────────"
  echo " 配置文件   : ${CONF_FILE}"
  echo " 地图目录   : ${MAP_DIR}"
  echo " 2D 地图    : ${MAP_FILE}$( [[ -r "$MAP_FILE" ]] || echo '   <<< 缺失' )"
  echo " 3D 点云    : ${MAP3D_FILE}$( [[ -r "$MAP3D_FILE" ]] || echo '   <<< 缺失' )"
  if [[ -r "$MAP_FILE" ]]; then
    echo " 分辨率     : $(yaml_val "$MAP_FILE" resolution) m/px"
    echo " 原点 origin: $(yaml_val "$MAP_FILE" origin)"
  fi
  echo " 讲解方案   : plan_id=${PLAN_ID}$( [[ "$PLAN_ID" == "0" ]] && echo '  （自动取后端第一个启用方案）' )"
  echo " dry_run    : ${DRY_RUN}"
  echo " 后端地址   : ${BACKEND_URL}"
  echo " 启动导航   : $( (( START_NAV )) && echo '是' || echo '否（--no-nav）' )"
  echo " ROS_DOMAIN : ${ROS_DOMAIN_ID}"
  echo "────────────────────────────────────────────────────"
  echo " 后端自检："
  backend_probe
  echo "────────────────────────────────────────────────────"
  ros_preflight
  echo "────────────────────────────────────────────────────"
  echo " ⚠ 讲解点/充电点坐标必须与本地图配套；换图后需在 LY_Guide 平台重新标定。"
  echo "────────────────────────────────────────────────────"
}

if (( PRINT_ONLY )); then
  print_config
  exit 0
fi

[[ -r "$MAP_FILE"   ]] || die "找不到 2D 地图: ${MAP_FILE}"
[[ -r "$MAP3D_FILE" ]] || die "找不到 3D 点云: ${MAP3D_FILE}"
[[ -r "$MISSION_START" ]] || die "找不到讲解任务启动脚本: ${MISSION_START}"

print_config

# ── 1. 用指定地图拉起导航栈 ────────────────────────────
if (( START_NAV )); then
  [[ -r "$NAV_SCRIPT" ]] || die "找不到导航启动脚本: ${NAV_SCRIPT}"
  echo "[START] 以该地图启动导航栈（后台运行，日志：${NAV_LOG}）"
  # setsid + nohup：脚本退出/终端关闭后导航栈继续存活
  setsid nohup bash "$NAV_SCRIPT" >"$NAV_LOG" 2>&1 </dev/null &
  echo "[INFO]  导航栈 pid=$!   跟踪日志： tail -f ${NAV_LOG}"
else
  echo "[SKIP] --no-nav：沿用正在运行的导航栈（下面会核对它加载的是哪张图）"
fi

# ── 2. 等 Nav2 就绪 ────────────────────────────────────
ros_env

if [[ "$DRY_RUN" == "true" ]]; then
  echo "[SKIP] dry_run=true：不等待 /navigate_to_pose"
elif ! wait_for_action /navigate_to_pose "$NAV_WAIT_SEC"; then
  die "等待 /navigate_to_pose 超时；请查看 ${NAV_LOG} 排查导航启动失败原因"
fi

# ── 3. 确认加载的是哪张地图（换图后最关键的一次核对）──
echo "[CHECK] 导航栈实际加载的地图："
show_loaded_map
ros_preflight

# ── 4. 启动讲解任务节点（前台，Ctrl+C 结束）────────────
echo "[START] 讲解任务节点（plan_id=${PLAN_ID}, dry_run=${DRY_RUN}）"
exec bash "$MISSION_START" --ros-args \
  -p "plan_id:=${PLAN_ID}" \
  -p "dry_run:=${DRY_RUN}" \
  -p "backend_url:=${BACKEND_URL}"
