#!/bin/bash
# Robot Control System - 部署脚本

set -e

echo "=========================================="
echo "Robot Control System - 部署脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker未安装${NC}"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: docker-compose未安装${NC}"
    exit 1
fi

# 创建环境变量文件
create_env_file() {
    echo "创建环境变量配置文件..."
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# 火山引擎配置
VOLC_APP_ID=your_volc_app_id_here
VOLC_TOKEN=your_volc_token_here
COZE_API_KEY=your_coze_api_key_here
COZE_SPACE_ID=your_coze_space_id_here

# RTC配置（可选）
RTC_APP_ID=your_rtc_app_id_here
RTC_TOKEN=your_rtc_token_here

# 应用配置
APP_DEBUG=false
LOG_LEVEL=INFO
EOF
        echo -e "${YELLOW}请编辑 .env 文件填入您的配置${NC}"
    else
        echo -e "${GREEN}环境变量文件已存在${NC}"
    fi
}

# 构建Docker镜像
build_image() {
    echo -e "\n${YELLOW}构建Docker镜像...${NC}"
    docker-compose build --no-cache
    echo -e "${GREEN}镜像构建成功！${NC}"
}

# 启动服务
start_service() {
    echo -e "\n${YELLOW}启动服务...${NC}"
    docker-compose up -d
    echo -e "${GREEN}服务已启动！${NC}"
}

# 停止服务
stop_service() {
    echo -e "\n${YELLOW}停止服务...${NC}"
    docker-compose down
    echo -e "${GREEN}服务已停止${NC}"
}

# 查看日志
view_logs() {
    echo -e "\n${YELLOW}查看日志 (Ctrl+C 退出)...${NC}"
    docker-compose logs -f
}

# 显示状态
show_status() {
    echo -e "\n${YELLOW}服务状态:${NC}"
    docker-compose ps
}

# 初始化
init() {
    echo -e "\n${YELLOW}初始化项目...${NC}"
    create_env_file
    echo -e "${GREEN}初始化完成！${NC}"
    echo -e "\n下一步:"
    echo -e "1. 编辑 .env 文件填入您的配置"
    echo -e "2. 运行 ./deploy.sh build 构建镜像"
    echo -e "3. 运行 ./deploy.sh start 启动服务"
    echo -e "4. 访问 http://localhost:5000 查看Web界面"
}

# 帮助信息
show_help() {
    echo ""
    echo "使用方法: ./deploy.sh [命令]"
    echo ""
    echo "可用命令:"
    echo "  init       - 初始化项目（创建配置文件）"
    echo "  build      - 构建Docker镜像"
    echo "  start      - 启动服务"
    echo "  stop       - 停止服务"
    echo "  restart    - 重启服务"
    echo "  logs       - 查看日志"
    echo "  status     - 查看状态"
    echo "  help       - 显示帮助信息"
    echo ""
}

# 主逻辑
case "${1:-help}" in
    init)
        init
        ;;
    build)
        create_env_file
        build_image
        ;;
    start)
        create_env_file
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        start_service
        ;;
    logs)
        view_logs
        ;;
    status)
        show_status
        ;;
    help)
        show_help
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac

echo ""
