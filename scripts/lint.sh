#!/bin/bash
# lint.sh - 代码检查

set -e

echo "=========================================="
echo "  代码检查"
echo "=========================================="

# 检测 linter
if [ -f "pyproject.toml" ]; then
    echo "检测到 Python 项目..."
    if command -v black &> /dev/null; then
        black --check src/ tests/
    fi
    if command -v ruff &> /dev/null; then
        ruff check src/ tests/
    fi
    if command -v mypy &> /dev/null; then
        mypy src/
    fi
    
elif [ -f "CMakeLists.txt" ]; then
    echo "检测到 C++ 项目..."
    if command -v clang-format &> /dev/null; then
        echo "检查代码格式..."
        clang-format --dry-run -Werror src/
    fi
    if command -v cppcheck &> /dev/null; then
        cppcheck --enable=all src/
    fi
    
elif [ -f "package.json" ]; then
    echo "检测到 Node.js 项目..."
    if [ -f "pnpm-lock.yaml" ]; then
        pnpm lint --quiet
    else
        npm run lint
    fi
    
else
    echo "未检测到 linter"
fi

echo ""
echo "=========================================="
echo "  代码检查完成"
echo "=========================================="
