#!/bin/bash
# cli.sh - 火山 RTC Web 开发工具 CLI
# 交互式终端入口

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 路径配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 打印标题
print_header() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║          火山 RTC Web 开发工具                           ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 打印菜单
print_menu() {
    echo -e "${GREEN}请选择操作：${NC}"
    echo ""
    echo "  ${YELLOW}1${NC}) 更新配置 - 读取 config/token.conf 生成 Token 并更新 SDK"
    echo "  ${YELLOW}2${NC}) 启动服务 - 启动 Web 开发服务器"
    echo "  ${YELLOW}3${NC}) 安装依赖 - 安装 npm/pnpm 依赖"
    echo "  ${YELLOW}4${NC}) 构建项目 - 构建生产版本"
    echo ""
    echo "  ${YELLOW}0${NC}) 退出"
    echo ""
}

# 执行更新配置
do_update_config() {
    echo -e "${BLUE}==> 执行更新配置...${NC}"
    bash "$SCRIPT_DIR/update_config.sh"
}

# 执行启动服务
do_start() {
    echo -e "${BLUE}==> 启动服务...${NC}"
    bash "$SCRIPT_DIR/start.sh"
}

# 执行安装依赖
do_install() {
    echo -e "${BLUE}==> 安装依赖...${NC}"
    cd "$SCRIPT_DIR/../../src/web/volc_web_sdk"
    if command -v pnpm &> /dev/null; then
        pnpm install
    else
        npm install
    fi
}

# 执行构建
do_build() {
    echo -e "${BLUE}==> 构建项目...${NC}"
    cd "$SCRIPT_DIR/../../src/web/volc_web_sdk"
    if command -v pnpm &> /dev/null; then
        pnpm build
    else
        npm run build
    fi
}

# 主循环
main() {
    while true; do
        clear
        print_header
        print_menu
        
        read -p "请输入选项 [0-4]: " choice
        
        case $choice in
            1)
                do_update_config
                echo ""
                read -p "按 Enter 键继续..." _
                ;;
            2)
                do_start
                break
                ;;
            3)
                do_install
                echo ""
                read -p "按 Enter 键继续..." _
                ;;
            4)
                do_build
                echo ""
                read -p "按 Enter 键继续..." _
                ;;
            0)
                echo -e "${GREEN}再见！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}无效选项，请重新选择${NC}"
                sleep 1
                ;;
        esac
    done
}

main
