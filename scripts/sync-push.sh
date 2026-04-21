#!/bin/bash
# sync-push.sh - 推送到云电脑

# 需要配置环境变量或编辑此脚本
CLOUD_USER=${CLOUD_USER:-"root"}
CLOUD_HOST=${CLOUD_HOST:-"your-cloud-pc-ip"}
CLOUD_PATH=${CLOUD_PATH:-"/home/user/volc_ai_realtime_agent"}

echo "=========================================="
echo "  推送到云电脑"
echo "=========================================="
echo ""
echo "配置:"
echo "  用户: $CLOUD_USER"
echo "  主机: $CLOUD_HOST"
echo "  路径: $CLOUD_PATH"
echo ""

# 检查是否配置
if [ "$CLOUD_HOST" = "your-cloud-pc-ip" ]; then
    echo "Error: 请配置 CLOUD_HOST 环境变量或编辑 sync-push.sh"
    echo ""
    echo "方式 1: 环境变量"
    echo "  export CLOUD_HOST=192.168.1.100"
    echo "  export CLOUD_USER=root"
    echo "  make sync-push"
    echo ""
    echo "方式 2: 编辑脚本"
    echo "  vim scripts/sync-push.sh"
    exit 1
fi

# 检查 git 状态
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "Warning: 有未提交的更改"
    echo ""
    read -p "是否继续? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# 检查远程
if ! git remote get-url cloud &>/dev/null; then
    echo "添加 cloud 远程..."
    git remote add cloud "ssh://${CLOUD_USER}@${CLOUD_HOST}/${CLOUD_PATH}"
fi

# 推送
echo "推送代码到云电脑..."
git push cloud HEAD:main

echo ""
echo "=========================================="
echo "  推送完成"
echo "=========================================="
echo ""
echo "下一步: 在云电脑上运行:"
echo "  cd $CLOUD_PATH"
echo "  make build"
