#!/bin/bash
# new-plan.sh - 创建计划文档

set -e

TOPIC=$1

if [ -z "$TOPIC" ]; then
    echo "Error: TOPIC is required"
    echo "Usage: make new-plan TOPIC=<topic>"
    exit 1
fi

PLAN_DIR="docs/plan"
mkdir -p "$PLAN_DIR"

FILE="$PLAN_DIR/${TOPIC}_plan.md"

if [ -f "$FILE" ]; then
    echo "Warning: $FILE already exists"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

cat > "$FILE" << EOF
# ${TOPIC} 实施计划

## 背景
{基于调研得出的结论}

## 阶段目标
{最终要达成的目标}

## 里程碑
- [ ] 里程碑1
- [ ] 里程碑2

---

## 子任务清单

### [ ] Task 1: {子任务名称}
**目标**: {明确要解决的问题}

**实施方案**:
1. 步骤1
2. 步骤2
3. 步骤3

**验收标准**:
- [ ] 验收项1
- [ ] 验收项2

**文件改动**:
- \`src/xxx.cpp\`
- \`tests/xxx.cpp\`
- \`examples/xxx.cpp\`

---

### [ ] Task 2: {子任务名称}
**目标**: {明确要解决的问题}

**实施方案**:
1. 步骤1
2. 步骤2

**验收标准**:
- [ ] 验收项1

**文件改动**:
- \`src/xxx.cpp\`

---

### [ ] Task 3: {子任务名称}
**目标**: {明确要解决的问题}

**实施方案**:
1. 步骤1

**验收标准**:
- [ ] 验收项1

**文件改动**:
- \`src/xxx.cpp\`

---

## 执行记录

| 日期 | 完成任务 | 状态 | 备注 |
|------|----------|------|------|
| | | | |

---

## 使用说明

### 查看计划进度
\`\`\`bash
make show-plan TOPIC=${TOPIC}
\`\`\`

### 标记任务完成
\`\`\`bash
make done TASK=1 TOPIC=${TOPIC}
\`\`\`

---

*创建时间: $(date +%Y-%m-%d)*
EOF

echo "Created: $FILE"
echo "Please edit this file to add your task details."
