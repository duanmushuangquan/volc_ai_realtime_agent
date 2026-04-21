#!/bin/bash
# done.sh - 标记任务完成

set -e

TASK=$1
TOPIC=$2

if [ -z "$TASK" ] || [ -z "$TOPIC" ]; then
    echo "Error: TASK and TOPIC are required"
    echo "Usage: make done TASK=N TOPIC=<topic>"
    exit 1
fi

FILE="docs/plan/${TOPIC}_plan.md"

if [ ! -f "$FILE" ]; then
    echo "Error: $FILE not found"
    exit 1
fi

# 查找并标记任务
TASK_LINE=$(grep -n "^### \[ \] Task $TASK:" "$FILE" | cut -d: -f1)

if [ -z "$TASK_LINE" ]; then
    TASK_LINE=$(grep -n "^### \[ \] Task $TASK " "$FILE" | cut -d: -f1)
fi

if [ -z "$TASK_LINE" ]; then
    echo "Error: Task $TASK not found or already completed"
    exit 1
fi

# 替换 [ ] 为 [x]
sed -i "${TASK_LINE}s/\[ \]/[x]/" "$FILE"

# 添加执行记录
DATE=$(date +%Y-%m-%d)
TASK_NAME=$(grep "^### \[x\] Task $TASK" "$FILE" | sed 's/^### \[x\] //')

# 更新执行记录表格
if grep -q "| 日期 | 完成任务 |" "$FILE"; then
    sed -i "/| 日期 | 完成任务 |/a | $DATE | Task $TASK | ✅ | |" "$FILE"
fi

echo "=========================================="
echo "  Task $TASK 已完成"
echo "=========================================="
echo ""
echo "任务: $TASK_NAME"
echo "日期: $DATE"
echo ""
echo "下一步: 请确认是否进入下一个任务"
echo "运行 'make show-plan TOPIC=$TOPIC' 查看进度"
