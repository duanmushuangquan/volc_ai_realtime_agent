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
WEB_DIR="$SCRIPT_DIR/../../src/web/volc_web_sdk"

# 打印标题
print_header() {
    printf "${CYAN}"
    printf "╔══════════════════════════════════════════════════════════╗\n"
    printf "║          火山 RTC Web 开发工具                           ║\n"
    printf "╚══════════════════════════════════════════════════════════╝\n"
    printf "${NC}"
}

# 打印菜单
print_menu() {
    printf "${GREEN}请选择操作：${NC}\n"
    echo ""
    printf "  ${YELLOW}[1]${NC} 更新配置 - 读取 config/token.conf 生成 Token 并更新 SDK\n"
    printf "  ${YELLOW}[2]${NC} 启动服务 - 启动 Web 开发服务器\n"
    printf "  ${YELLOW}[3]${NC} 安装依赖 - 安装 npm/pnpm 依赖\n"
    printf "  ${YELLOW}[4]${NC} 构建项目 - 构建生产版本\n"
    printf "  ${YELLOW}[5]${NC} 停止服务 - 优雅停止 Web 服务\n"
    printf "  ${YELLOW}[6]${NC} 清理进程 - 强制清理后台 node 进程\n"
    echo ""
    printf "  ${YELLOW}[0]${NC} 退出\n"
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
    cd "$WEB_DIR"
    if command -v pnpm &> /dev/null; then
        pnpm install
    else
        npm install
    fi
}

# 执行构建
do_build() {
    echo -e "${BLUE}==> 构建项目...${NC}"
    cd "$WEB_DIR"
    if command -v pnpm &> /dev/null; then
        pnpm build
    else
        npm run build
    fi
}

# 停止服务
do_stop() {
    echo -e "${BLUE}==> 停止服务...${NC}"
    bash "$SCRIPT_DIR/stop.sh"
}

# 清理进程
do_kill() {
    echo -e "${BLUE}==> 清理进程...${NC}"
    bash "$SCRIPT_DIR/kill.sh"
}

# 主循环
main() {
    while true; do
        clear
        print_header
        print_menu
        
        read -p "请输入选项 [0-6]: " choice
        
        case $choice in
            1)
                do_update_config
                echo ""
                read -p "按 Enter 键继续..." _
                ;;
            2)
                do_start
                read -p "按 Enter 键继续..." _
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
            5)
                do_stop
                echo ""
                read -p "按 Enter 键继续..." _
                ;;
            6)
                do_kill
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
