#!/bin/bash
# show-plan.sh - 显示计划进度

set -e

TOPIC=$1

if [ -z "$TOPIC" ]; then
    echo "Error: TOPIC is required"
    echo "Usage: make show-plan TOPIC=<topic>"
    exit 1
fi

FILE="docs/plan/${TOPIC}_plan.md"

if [ ! -f "$FILE" ]; then
    echo "Error: $FILE not found"
    echo "Run 'make new-plan TOPIC=$TOPIC' first"
    exit 1
fi

echo "=========================================="
echo "  计划: $TOPIC"
echo "=========================================="
echo ""

# 提取背景和目标
echo "## 背景"
grep -A 2 "^## 背景" "$FILE" | tail -n +2 | head -5
echo ""

echo "## 阶段目标"
grep -A 2 "^## 阶段目标" "$FILE" | tail -n +2 | head -5
echo ""

# 统计任务
TOTAL=$(grep -c "^### \[ \]" "$FILE" || true)
DONE=$(grep -c "^### \[x\]" "$FILE" || true)

if [ -z "$TOTAL" ]; then TOTAL=0; fi
if [ -z "$DONE" ]; then DONE=0; fi

echo "## 进度: $DONE / $TOTAL"
echo ""

# 显示任务列表
echo "## 子任务"
grep -E "^### \[|\*\*目标\*\*" "$FILE" | sed 's/^### \[.*\] /[ ] /g; s/### \[x\] /[x] /g'

echo ""
echo "=========================================="
echo "详细计划: $FILE"
echo "=========================================="
