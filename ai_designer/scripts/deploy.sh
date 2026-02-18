#!/bin/bash

# ==========================================
# AI Designer - 一键部署脚本
# ==========================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查环境
check_environment() {
    log_info "检查部署环境..."

    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    log_success "Docker 已安装: $(docker --version)"

    # 检查 Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    log_success "Docker Compose 已安装: $(docker-compose --version)"

    # 检查环境变量文件
    if [ ! -f .env ]; then
        log_warning ".env 文件不存在，从 .env.example 复制..."
        if [ -f .env.example ]; then
            cp .env.example .env
            log_success ".env 文件已创建，请编辑并填入正确的配置"
            log_warning "请编辑 .env 文件后重新运行此脚本"
            exit 0
        else
            log_error ".env.example 文件不存在"
            exit 1
        fi
    fi
    log_success ".env 文件存在"
}

# 构建镜像
build_images() {
    log_info "构建 Docker 镜像..."
    docker-compose build --no-cache
    log_success "Docker 镜像构建完成"
}

# 启动服务
start_services() {
    log_info "启动服务..."
    docker-compose up -d
    log_success "服务启动完成"
}

# 等待服务健康
wait_for_health() {
    log_info "等待服务健康检查..."

    local max_attempts=30
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            log_success "后端服务健康检查通过"
            return 0
        fi
        attempt=$((attempt + 1))
        echo -n "."
        sleep 2
    done

    echo ""
    log_error "后端服务健康检查超时"
    return 1
}

# 显示状态
show_status() {
    log_info "服务状态:"
    docker-compose ps

    echo ""
    log_info "访问地址:"
    echo "  - 前端: http://localhost:3000"
    echo "  - 后端 API: http://localhost:8000"
    echo "  - API 文档: http://localhost:8000/api/docs"
    echo ""
}

# 显示日志
show_logs() {
    log_info "显示日志 (按 Ctrl+C 退出):"
    docker-compose logs -f
}

# 停止服务
stop_services() {
    log_info "停止服务..."
    docker-compose down
    log_success "服务已停止"
}

# 清理
cleanup() {
    log_info "清理容器和镜像..."
    docker-compose down -v --rmi all
    log_success "清理完成"
}

# 主函数
main() {
    case "${1:-deploy}" in
        deploy)
            log_info "开始部署 AI Designer..."
            check_environment
            build_images
            start_services
            wait_for_health
            show_status
            log_success "部署完成！"
            ;;
        start)
            log_info "启动服务..."
            start_services
            wait_for_health
            show_status
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            start_services
            wait_for_health
            show_status
            ;;
        logs)
            show_logs
            ;;
        status)
            show_status
            ;;
        cleanup)
            cleanup
            ;;
        *)
            echo "用法: $0 {deploy|start|stop|restart|logs|status|cleanup}"
            echo ""
            echo "命令说明:"
            echo "  deploy    - 完整部署 (构建 + 启动)"
            echo "  start     - 启动服务"
            echo "  stop      - 停止服务"
            echo "  restart   - 重启服务"
            echo "  logs      - 查看日志"
            echo "  status    - 查看状态"
            echo "  cleanup   - 清理所有资源"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
