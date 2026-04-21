#!/bin/bash
# kill.sh - 强制清理所有后台 node/pnpm 进程

echo "==> 强制清理后台进程..."
echo ""

# 检查是否有运行的进程
if ! pgrep -f "node|react-scripts|pnpm|npm" > /dev/null; then
    echo "没有找到相关的 node/pnpm 进程"
    echo "完成"
    exit 0
fi

# 显示将要清理的进程
echo "当前运行的进程："
ps aux | grep -E "node|react-scripts|pnpm|npm" | grep -v grep | head -10
echo ""

# 确认操作
read -p "确认清理所有 node/pnpm 进程? [y/N]: " confirm
confirm=${confirm:-n}

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "正在清理..."
    
    # 停止 react-scripts
    if pgrep -f "react-scripts" > /dev/null; then
        echo "停止 react-scripts..."
        pkill -9 -f "react-scripts"
    fi
    
    # 停止 node 服务
    if pgrep -f "node.*5000" > /dev/null; then
        echo "停止端口 5000 上的 node 进程..."
        PID=$(ss -lptn 'sport = :5000' 2>/dev/null | grep -oP 'pid=\K\d+' | head -1)
        if [ -n "$PID" ]; then
            kill -9 "$PID" 2>/dev/null
        fi
    fi
    
    # 清理其他 node 进程（在项目目录中的）
    if pgrep -f "node" > /dev/null; then
        echo "清理其他 node 进程..."
        pkill -9 -f "node"
    fi
    
    sleep 1
    
    # 验证清理结果
    echo ""
    echo "清理后的进程："
    if pgrep -f "node|react-scripts" > /dev/null; then
        ps aux | grep -E "node|react-scripts" | grep -v grep || echo "  无相关进程"
    else
        echo "  无相关进程"
    fi
    
    echo ""
    echo "清理完成"
else
    echo "已取消"
fi
