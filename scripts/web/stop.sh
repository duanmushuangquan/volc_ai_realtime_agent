#!/bin/bash
# stop.sh - 优雅停止 Web 开发服务器

echo "==> 停止 Web 开发服务器..."

# 查找并优雅停止 react-scripts/node 进程
if pgrep -f "react-scripts start" > /dev/null; then
    echo "找到 react-scripts 进程，正在停止..."
    pkill -f "react-scripts start"
    sleep 2
    
    if pgrep -f "react-scripts start" > /dev/null; then
        echo "进程仍在运行，尝试强制停止..."
        pkill -9 -f "react-scripts start"
        sleep 1
    fi
    echo "服务已停止"
else
    echo "没有找到运行中的 Web 服务"
fi

# 检查端口 5000
if ss -tuln 2>/dev/null | grep -q ":5000"; then
    PID=$(ss -lptn 'sport = :5000' 2>/dev/null | grep -oP 'pid=\K\d+' | head -1)
    if [ -n "$PID" ]; then
        echo "端口 5000 被 PID $PID 占用，正在停止..."
        kill -TERM "$PID" 2>/dev/null
        sleep 2
        
        if ss -tuln 2>/dev/null | grep -q ":5000"; then
            echo "强制停止进程..."
            kill -9 "$PID" 2>/dev/null
        fi
    fi
fi

echo "完成"
