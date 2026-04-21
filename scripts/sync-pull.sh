#!/bin/bash
# sync-pull.sh - 从云电脑拉取

# 需要配置环境变量或编辑此脚本
CLOUD_USER=${CLOUD_USER:-"root"}
CLOUD_HOST=${CLOUD_HOST:-"your-cloud-pc-ip"}
CLOUD_PATH=${CLOUD_PATH:-"/home/user/volc_ai_realtime_agent"}

echo "=========================================="
echo "  从云电脑拉取"
echo "=========================================="
echo ""

# 检查是否配置
if [ "$CLOUD_HOST" = "your-cloud-pc-ip" ]; then
    echo "Error: 请配置 CLOUD_HOST 环境变量"
    echo "  export CLOUD_HOST=192.168.1.100"
    exit 1
fi

# 检查远程
if ! git remote get-url cloud &>/dev/null; then
    echo "添加 cloud 远程..."
    git remote add cloud "ssh://${CLOUD_USER}@${CLOUD_HOST}/${CLOUD_PATH}"
fi

# 拉取
echo "从云电脑拉取..."
git pull cloud main

echo ""
echo "=========================================="
echo "  拉取完成"
echo "=========================================="
