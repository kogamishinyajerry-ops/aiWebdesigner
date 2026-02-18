#!/bin/bash

# ==========================================
# AI Designer - 更新脚本
# ==========================================

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# 拉取最新代码
pull_latest() {
    log_info "拉取最新代码..."
    git pull origin main
    log_success "代码已更新"
}

# 重新构建
rebuild() {
    log_info "重新构建镜像..."
    docker-compose build --no-cache
    log_success "镜像重建完成"
}

# 重启服务
restart_services() {
    log_info "重启服务..."
    docker-compose down
    docker-compose up -d
    log_success "服务已重启"
}

# 数据库迁移
run_migrations() {
    log_info "运行数据库迁移..."
    docker-compose exec backend alembic upgrade head
    log_success "数据库迁移完成"
}

# 清理旧镜像
cleanup_old_images() {
    log_info "清理旧的 Docker 镜像..."
    docker image prune -f
    log_success "清理完成"
}

# 主函数
main() {
    log_info "开始更新 AI Designer..."
    pull_latest
    rebuild
    run_migrations || echo "数据库迁移跳过 (可能不存在)"
    restart_services
    cleanup_old_images
    log_success "更新完成！"
}

main
