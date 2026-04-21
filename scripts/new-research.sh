#!/bin/bash
# new-research.sh - 创建调研文档

set -e

TOPIC=$1

if [ -z "$TOPIC" ]; then
    echo "Error: TOPIC is required"
    echo "Usage: make new-research TOPIC=<topic>"
    exit 1
fi

RESEARCH_DIR="docs/research"
mkdir -p "$RESEARCH_DIR"

FILE="$RESEARCH_DIR/${TOPIC}.md"

if [ -f "$FILE" ]; then
    echo "Warning: $FILE already exists"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

cat > "$FILE" << EOF
# ${TOPIC} 调研

## 调研信息
- 调研时间：$(date +%Y-%m-%d)
- 调研人：
- 状态：进行中

## 信息来源
- [火山 RTC 文档](https://www.volcengine.com/docs/6348/)
- [GitHub](https://github.com)
- [其他来源]

## 核心发现

### 1. {发现1}
{详细描述}

### 2. {发现2}
{详细描述}

## 关键技术点

| 技术 | 说明 | 备注 |
|------|------|------|
| | | |

## 结论

{基于调研得出的结论}

## 待确认
- [ ] 问题1
- [ ] 问题2

## 相关链接
- [文档1]
- [文档2]

---

*最后更新: $(date +%Y-%m-%d)*
EOF

echo "Created: $FILE"
echo "Please edit this file to add your research findings."
