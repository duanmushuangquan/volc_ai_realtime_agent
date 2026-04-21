#!/bin/bash
# 更新 Web SDK 配置脚本
# 从 config/token.conf 读取配置，生成 Token 并更新 src/web/volc_web_sdk/src/config.ts

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置路径
CONFIG_FILE="config/token.conf"
CONFIG_TEMPLATE="config/token.conf.example"
SDK_CONFIG_FILE="src/web/volc_web_sdk/src/config.ts"
TOKEN_GENERATOR="src/web/tools/token/token_generator.py"

# 检查配置文件
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${YELLOW}配置文件 $CONFIG_FILE 不存在，正在从模板创建...${NC}"
        if [ -f "$CONFIG_TEMPLATE" ]; then
            cp "$CONFIG_TEMPLATE" "$CONFIG_FILE"
            echo -e "${YELLOW}请编辑 $CONFIG_FILE 填写正确的配置${NC}"
            exit 1
        else
            echo -e "${RED}错误：配置文件模板 $CONFIG_TEMPLATE 也不存在${NC}"
            exit 1
        fi
    fi
}

# 解析 INI 格式配置文件
parse_ini() {
    local section="$1"
    local key="$2"
    local file="$3"
    
    # 使用 awk 解析 INI 文件
    awk -F ' = ' -v section="$section" -v key="$key" '
        BEGIN { in_section = 0 }
        /^\[/ { in_section = ($0 == "[" section "]") ? 1 : 0 }
        in_section && $1 == key { gsub(/^[ \t]+|[ \t]+$/, "", $2); gsub(/^"|"$/, "", $2); print $2; exit }
    ' "$file"
}

# 读取配置
read_config() {
    APP_ID=$(parse_ini "volc" "app_id" "$CONFIG_FILE")
    APP_KEY=$(parse_ini "volc" "app_key" "$CONFIG_FILE")
    ROOM_ID=$(parse_ini "volc" "room_id" "$CONFIG_FILE")
    EXPIRE=$(parse_ini "options" "expire" "$CONFIG_FILE")
    USER_IDS=$(parse_ini "users" "user_ids" "$CONFIG_FILE")
    
    # 解析用户数组
    USER_IDS=$(echo "$USER_IDS" | sed 's/[][]//g' | tr ',' '\n' | tr -d ' "')
    
    if [ -z "$APP_ID" ] || [ -z "$APP_KEY" ]; then
        echo -e "${RED}错误：配置文件缺少必要的 app_id 或 app_key${NC}"
        exit 1
    fi
    
    # 默认值
    EXPIRE=${EXPIRE:-604800}
    ROOM_ID=${ROOM_ID:-test_room}
    USER_IDS=${USER_IDS:-user_001}
}

# 生成 Token
generate_token() {
    local user_id="$1"
    echo -e "${GREEN}正在为用户 $user_id 生成 Token...${NC}"
    
    python3 "$TOKEN_GENERATOR" \
        --app-id "$APP_ID" \
        --app-key "$APP_KEY" \
        --room-id "$ROOM_ID" \
        --user-id "$user_id" \
        --expire "$EXPIRE"
}

# 更新 Web SDK 配置
update_sdk_config() {
    local user_id="$1"
    local token="$2"
    
    echo -e "${GREEN}正在更新 SDK 配置...${NC}"
    
    # 使用 sed 替换配置
    sed -i "s/const appId = \".*\"/const appId = \"$APP_ID\"/" "$SDK_CONFIG_FILE"
    sed -i "s/const appKey = \".*\"/const appKey = \"$APP_KEY\"/" "$SDK_CONFIG_FILE"
    sed -i "s/const roomId = \".*\"/const roomId = \"$ROOM_ID\"/" "$SDK_CONFIG_FILE"
    sed -i "s/const userId = \".*\"/const userId = \"$user_id\"/" "$SDK_CONFIG_FILE")
    sed -i "s|const token = \".*\"|const token = \"$token\"|" "$SDK_CONFIG_FILE"
    
    echo -e "${GREEN}SDK 配置已更新！${NC}"
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
    echo -e "  Users: $USER_IDS"
    echo ""
    
    # 获取第一个用户
    FIRST_USER=$(echo "$USER_IDS" | head -n1)
    
    # 生成 Token
    TOKEN_OUTPUT=$(generate_token "$FIRST_USER")
    TOKEN=$(echo "$TOKEN_OUTPUT" | grep "Token:" | cut -d: -f2 | tr -d ' ')
    
    if [ -z "$TOKEN" ]; then
        echo -e "${RED}错误：Token 生成失败${NC}"
        echo "$TOKEN_OUTPUT"
        exit 1
    fi
    
    echo -e "${GREEN}Token 生成成功！${NC}"
    echo ""
    
    # 更新 SDK 配置
    update_sdk_config "$FIRST_USER" "$TOKEN"
    
    echo ""
    echo -e "${GREEN}==================================================${NC}"
    echo -e "${GREEN}配置更新完成！${NC}"
    echo -e "${GREEN}==================================================${NC}"
    echo ""
    echo -e "现在可以运行以下命令启动开发服务器："
    echo -e "  ${YELLOW}bash scripts/web/start.sh${NC}"
}

main "$@"
