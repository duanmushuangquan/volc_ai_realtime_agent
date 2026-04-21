#!/bin/bash
# test.sh - 运行所有测试

set -e

echo "=========================================="
echo "  运行测试"
echo "=========================================="

# 设置 PYTHONPATH 以支持 src 模块导入
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src/python"

# 检测测试系统
if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
    echo "检测到 Python 测试..."
    python -m pytest -v tests/
    
elif [ -f "CMakeLists.txt" ]; then
    echo "检测到 C++ 测试..."
    if [ -d "build" ]; then
        cd build
        ctest --output-on-failure
    else
        echo "请先运行 make build"
        exit 1
    fi
    
elif [ -f "package.json" ]; then
    echo "检测到 Node.js 项目..."
    npm test
    
else
    echo "未检测到测试系统"
    echo "请手动配置测试"
    exit 1
fi

echo ""
echo "=========================================="
echo "  测试完成"
echo "=========================================="
