#!/bin/bash
# build.sh - 编译项目

set -e

echo "=========================================="
echo "  编译项目"
echo "=========================================="

# 检测构建系统
if [ -f "CMakeLists.txt" ]; then
    echo "检测到 CMake 项目..."
    
    # 创建 build 目录
    mkdir -p build
    cd build
    
    # 配置
    echo "配置 CMake..."
    cmake ..
    
    # 编译
    echo "编译..."
    make -j$(nproc)
    
    echo ""
    echo "编译完成!"
    echo "可执行文件: build/"
    
elif [ -f "Makefile" ] && grep -q "^build:" Makefile 2>/dev/null; then
    echo "检测到 Make 项目..."
    make build
    
else
    echo "未检测到构建系统 (CMake/Makefile)"
    echo "请手动配置构建"
    exit 1
fi

echo "=========================================="
