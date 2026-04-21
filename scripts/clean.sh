#!/bin/bash
# clean.sh - 清理构建产物

set -e

echo "清理构建产物..."

# CMake
if [ -d "build" ]; then
    rm -rf build
    echo "  ✓ 删除 build/"
fi

# Node.js
if [ -d "node_modules" ]; then
    rm -rf node_modules
    echo "  ✓ 删除 node_modules/"
fi

# Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "  ✓ 清理 Python 缓存"

# Logs
find . -type f -name "*.log" -delete 2>/dev/null || true
echo "  ✓ 清理日志文件"

echo ""
echo "清理完成!"
