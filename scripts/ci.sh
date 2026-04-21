#!/bin/bash
# ci.sh - 本地 CI 检查

set -e

echo "=========================================="
echo "  本地 CI 检查"
echo "=========================================="
echo ""

FAILED=0

# Lint
echo "[1/4] 代码检查..."
if bash scripts/lint.sh; then
    echo "✓ Lint 通过"
else
    echo "✗ Lint 失败"
    FAILED=1
fi
echo ""

# Build
echo "[2/4] 编译项目..."
if bash scripts/build.sh; then
    echo "✓ Build 通过"
else
    echo "✗ Build 失败"
    FAILED=1
fi
echo ""

# Test
echo "[3/4] 运行测试..."
if bash scripts/test.sh; then
    echo "✓ Test 通过"
else
    echo "✗ Test 失败"
    FAILED=1
fi
echo ""

# Format
echo "[4/4] 格式检查..."
if [ -f "CMakeLists.txt" ] && command -v clang-format &> /dev/null; then
    if clang-format --dry-run src/ &>/dev/null; then
        echo "✓ Format 通过"
    else
        echo "✗ Format 失败 (运行 clang-format src/ 修复)"
        FAILED=1
    fi
elif [ -f "pyproject.toml" ] && command -v black &> /dev/null; then
    if black --check src/ &>/dev/null; then
        echo "✓ Format 通过"
    else
        echo "✗ Format 失败 (运行 black src/ 修复)"
        FAILED=1
    fi
fi
echo ""

echo "=========================================="
if [ $FAILED -eq 0 ]; then
    echo "  ✓ CI 检查全部通过"
else
    echo "  ✗ CI 检查有失败项"
fi
echo "=========================================="

exit $FAILED
