#!/bin/bash

# AI Designer - 备份脚本
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

backup_database() {
    log_info "备份数据库..."
    docker-compose exec -T postgres pg_dump -U postgres ai_designer > "$BACKUP_DIR/database.sql"
    log_success "数据库备份完成: $BACKUP_DIR/database.sql"
}

backup_redis() {
    log_info "备份 Redis..."
    docker-compose exec redis redis-cli SAVE
    docker cp ai-designer-redis:/data/dump.rdb "$BACKUP_DIR/redis_dump.rdb"
    log_success "Redis 备份完成: $BACKUP_DIR/redis_dump.rdb"
}

backup_models() {
    log_info "备份模型缓存..."
    docker run --rm -v ai-designer_model_cache:/data -v "$BACKUP_DIR":/backup alpine tar czf /backup/models_cache.tar.gz -C /data .
    log_success "模型缓存备份完成: $BACKUP_DIR/models_cache.tar.gz"
}

backup_uploads() {
    log_info "备份上传文件..."
    if [ -d "./data/uploads" ]; then
        cp -r ./data/uploads "$BACKUP_DIR/"
        log_success "上传文件备份完成: $BACKUP_DIR/uploads"
    else
        log_warning "上传文件目录不存在，跳过"
    fi
}

compress_backup() {
    log_info "压缩备份文件..."
    cd backups
    tar czf "$(basename $BACKUP_DIR).tar.gz" "$(basename $BACKUP_DIR)"
    cd ..
    log_success "备份压缩完成: backups/$(basename $BACKUP_DIR).tar.gz"
}

cleanup_old_backups() {
    log_info "清理 7 天前的备份..."
    find ./backups -name "*.tar.gz" -mtime +7 -delete
    log_success "旧备份清理完成"
}

main() {
    log_info "开始备份 AI Designer..."
    backup_database
    backup_redis
    backup_models
    backup_uploads
    compress_backup
    cleanup_old_backups
    log_success "备份完成！"
}

main
