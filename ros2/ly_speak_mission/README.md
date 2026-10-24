# ly_speak_mission — LY_Guide 讲解任务执行节点（ROS2）

部署于机器人 `/home/smart/LY_speak_ws/ros2/ly_speak_mission/`，`ros2/` 为 colcon 工作空间根目录，与后端（Flask 5000）、前端（web/）同属 LY_speak_ws。

## 功能

1. 从后端拉取讲解方案点位（`/api/guide/byPlan/<planId>`，已按 sort 排序）；
2. 按顺序用 Nav2（`/navigate_to_pose`）导航到每个点位；
3. **到达即触发播报**讲解词（`/voice/speak`，等播报完成后继续）；
4. 播报完成后立即前往下一点；
5. 全部点位完成后导航回充电点（后端地图 `chargeX/chargeY/chargeAngle`，缺省用节点兜底参数）。

## 构建（在机器人上）

```bash
cd /home/smart/LY_speak_ws/ros2
source /opt/ros/humble/setup.bash
source /home/smart/LY_inspect_ws/install/local_setup.bash
colcon build --symlink-install --packages-select ly_speak_mission
```

## 运行

```bash
cd /home/smart/LY_speak_ws
bash ros2/ly_speak_mission/start_mission.sh        # 全自动模式
bash ros2/ly_speak_mission/start_remote.sh         # 遥控手动模式
```

前提：导航栈（mid360_nav_bridge）与 voice 服务在线：
`ros2 launch voice robot_voice.launch.py`（语音缺失时节点静音执行，不中断任务）。
遥控模式还需要雷柏遥控接入，且运行用户有 /dev/input 读权限（udev 规则，见 deploy/）。

### 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| backend_url | http://127.0.0.1:5000 | LY_Guide 后端地址 |
| plan_id | 0 | 讲解方案 ID；0 = 自动选第一个启用方案 |
| auto_start | true | 节点启动即执行 |
| dry_run | false | true = 跳过导航，点位虚拟到达（联调） |
| nav_timeout_sec | 120 | 单段导航超时（秒） |
| voice_timeout_sec | 10 | 等待 /voice/speak 就绪（秒） |
| fallback_charge_x/y/angle | 18.52 / 1.0 / -94 | 后端未配充电点时的兜底坐标 |
| run_mode | auto | auto = 全自动走完所有点位；remote = 遥控手动步进 |
| remote_device_name | Knight22 | 遥控设备名（/dev/input 设备名包含该串即选中） |
| remote_event_no | 0 | 0 = 按设备名自动找；>0 = 指定 /dev/input/eventN |
| key_a_code | 2 | 遥控 A 键的 Linux 按键码（KEY_1） |
| key_b_code | 3 | 遥控 B 键的 Linux 按键码（KEY_2） |
| key_c_code | 4 | 遥控 C 键的 Linux 按键码（KEY_3） |
| key_d_code | 5 | 遥控 D 键的 Linux 按键码（KEY_4，兼急停键） |

示例（联调）：`bash start_mission.sh --ros-args -p dry_run:=true`

## 遥控手动模式（run_mode=remote）

讲解员持雷柏遥控手动控制节奏，机器人不自动走完全程：

- **B 键**：一键开启预设讲解方案（自动选第一个启用方案，plan_id 可指定）；
  机器人**原地不动**，只播报"开始讲解任务…请按A键前往1号点位"
- **A 键**：前往**下一个**点位 → 到达即播报该点位讲解词 → 播完停下等下一按；
  只能往前走，走过/未到的点位无法回头或跳步；导航失败再按 A 重试同一点
- **C 键**：重播当前点位的讲解词（参观者没听清时用）
- **D 键**：急停——立即取消导航、结束任务（正在播放的语音等当前句播完）
- 全部点位讲解完后按 **A 键**返回充电点，播报"本次讲解结束"；
  之后 B 键可重新开始新一轮

### 手动触发

节点空闲时：`ros2 service call /ly_speak_mission/start std_srvs/srv/Trigger "{}"`（遥控模式下等同按 B 键）
