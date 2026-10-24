#!/bin/bash
# LY_Guide 远程启动脚本（部署到远程服务器后执行）
cd "$(dirname "$0")"

# 停掉旧进程
pkill -f "app.py" 2>/dev/null
sleep 1

# 启动后端（同时托管 web/ 下的前端构建产物）
cd backend
nohup python3 app.py > ../app.log 2>&1 &
echo "LY_Guide 服务已启动，PID: $!  端口: ${PORT:-5000}"
