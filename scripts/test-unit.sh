#!/bin/bash
# test-unit.sh - 运行单元测试

set -e

echo "=========================================="
echo "  运行单元测试"
echo "=========================================="

# 检测测试系统
if [ -f "pytest.ini" ] || [ -f "pyproject.toml" ]; then
    echo "运行 Python 单元测试..."
    python -m pytest tests/unit/ -v
    
elif [ -f "CMakeLists.txt" ]; then
    echo "运行 C++ 单元测试..."
    if [ -d "build" ]; then
        cd build
        ctest -R unit --output-on-failure
    else
        echo "请先运行 make build"
        exit 1
    fi
    
elif [ -f "package.json" ]; then
    echo "运行 Node.js 单元测试..."
    npm run test:unit
    
else
    echo "未检测到测试系统"
    exit 1
fi

echo "=========================================="
