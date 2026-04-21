#!/bin/bash
# update_config.sh - 更新 Web SDK 配置

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 路径配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CONFIG_FILE="$PROJECT_ROOT/config/token.conf"
SDK_CONFIG_FILE="$PROJECT_ROOT/src/web/volc_web_sdk/src/config.ts"
TOKEN_GENERATOR="$PROJECT_ROOT/src/web/tools/token/token_generator.py"

# 检查配置文件
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}错误：配置文件 $CONFIG_FILE 不存在${NC}"
        echo "请先复制并编辑配置文件："
        echo "  cp config/token.conf.example config/token.conf"
        echo "  vim config/token.conf"
        exit 1
    fi
}

# 解析 INI 文件
parse_ini() {
    local file="$1"
    local section="$2"
    local key="$3"
    
    awk -F ' = ' -v section="[$section]" -v key="$key" '
        BEGIN { in_section = 0 }
        /^\[/ { in_section = ($0 == section) ? 1 : 0 }
        in_section && $1 == key { gsub(/^[ \t]+|[ \t]+$/, "", $2); gsub(/^"|"$/, "", $2); print $2; exit }
    ' "$file"
}

# 读取配置
read_config() {
    APP_ID=$(parse_ini "$CONFIG_FILE" "volc" "app_id")
    APP_KEY=$(parse_ini "$CONFIG_FILE" "volc" "app_key")
    ROOM_ID=$(parse_ini "$CONFIG_FILE" "volc" "room_id")
    EXPIRE=$(parse_ini "$CONFIG_FILE" "options" "expire")
    USER_IDS_RAW=$(parse_ini "$CONFIG_FILE" "users" "user_ids")
    
    if [ -z "$APP_ID" ] || [ -z "$APP_KEY" ]; then
        echo -e "${RED}错误：配置文件缺少必要的 app_id 或 app_key${NC}"
        exit 1
    fi
    
    # 默认值
    EXPIRE=${EXPIRE:-604800}
    ROOM_ID=${ROOM_ID:-test_room}
}

# 生成 Token
generate_token() {
    local user_id="$1"
    
    TOKEN=$(python3 "$TOKEN_GENERATOR" \
        --app-id "$APP_ID" \
        --app-key "$APP_KEY" \
        --room-id "$ROOM_ID" \
        --user-id "$user_id" \
        --expire "$EXPIRE" 2>/dev/null | grep "^Token:" | cut -d: -f2 | tr -d ' ')
    
    if [ -z "$TOKEN" ]; then
        echo -e "${RED}错误：Token 生成失败 for user: $user_id${NC}"
        exit 1
    fi
}

# 重写整个 config.ts
rewrite_config() {
    echo -e "${GREEN}正在重写 SDK 配置...${NC}"
    
    # 解析用户列表
    USER_LIST=$(echo "$USER_IDS_RAW" | sed 's/[][]//g' | tr ',' '\n' | tr -d ' "')
    USER_COUNT=$(echo "$USER_LIST" | wc -l)
    
    # 创建临时文件
    local tmp_file=$(mktemp)
    
    # 写入文件头
    cat > "$tmp_file" << 'HEADER'
/**
 * Copyright 2024 Beijing Volcano Engine Technology Co., Ltd. All Rights Reserved.
 * SPDX-license-identifier: BSD-3-Clause
 */

/*
 * On initiation. `engine` is not attached to any project or room for any specific user.
 */

const config = {
  appId: 'APP_ID_PLACEHOLDER',
  roomId: 'ROOM_ID_PLACEHOLDER',
  tokens: [
HEADER

    # 添加用户 tokens
    local count=0
    while IFS= read -r user_id; do
        [ -z "$user_id" ] && continue
        count=$((count + 1))
        
        echo -e "  ${GREEN}正在生成用户 $user_id 的 Token...${NC}"
        generate_token "$user_id"
        
        if [ $count -gt 1 ]; then
            echo "    }," >> "$tmp_file"
        fi
        
        echo "    {" >> "$tmp_file"
        echo "      userId: '$user_id'," >> "$tmp_file"
        echo "      token: '$TOKEN'," >> "$tmp_file"
    done <<< "$USER_LIST"
    
    # 关闭最后一个用户
    echo "    }" >> "$tmp_file"
    
    # 写入文件尾
    cat >> "$tmp_file" << 'FOOTER'
  ],
};

export default config;
FOOTER

    # 替换占位符
    sed -i "s/APP_ID_PLACEHOLDER/$APP_ID/" "$tmp_file"
    sed -i "s/ROOM_ID_PLACEHOLDER/$ROOM_ID/" "$tmp_file"
    
    # 复制到目标位置
    cp "$tmp_file" "$SDK_CONFIG_FILE"
    rm "$tmp_file"
    
    echo -e "${GREEN}SDK 配置已更新！${NC}"
    echo -e "${GREEN}共更新了 $USER_COUNT 个用户的配置${NC}"
}

# 主流程
main() {
    echo -e "${GREEN}==================================================${NC}"
    echo -e "${GREEN}火山 RTC Web SDK 配置更新工具${NC}"
    echo -e "${GREEN}==================================================${NC}"
    
    # 检查配置文件
    check_config
    
    # 读取配置
    echo -e "${GREEN}读取配置文件: $CONFIG_FILE${NC}"
    read_config
    
    echo -e "${GREEN}配置信息:${NC}"
    echo -e "  App ID: $APP_ID"
    echo -e "  Room ID: $ROOM_ID"
    echo -e "  Expire: $EXPIRE 秒"
    echo -e "  Users: $USER_IDS_RAW"
    echo ""
    
    # 重写配置
    rewrite_config
    
    echo ""
    echo -e "${GREEN}==================================================${NC}"
    echo -e "${GREEN}配置更新完成！${NC}"
    echo -e "${GREEN}==================================================${NC}"
    echo ""
    echo -e "现在可以运行以下命令启动开发服务器："
    echo -e "  ${YELLOW}bash scripts/web/start.sh${NC}"
}

main "$@"
