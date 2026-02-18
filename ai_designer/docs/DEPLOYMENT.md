# AI Designer - 部署指南

## 📋 目录

- [前置要求](#前置要求)
- [快速部署](#快速部署)
- [Docker 部署](#docker-部署)
- [本地开发部署](#本地开发部署)
- [生产环境部署](#生产环境部署)
- [环境变量配置](#环境变量配置)
- [故障排除](#故障排除)

---

## 前置要求

### 系统要求

- **操作系统**: Linux (Ubuntu 22.04+ 推荐), macOS, Windows (WSL2)
- **内存**: 最低 8GB，推荐 16GB+
- **存储**: 最低 20GB 可用空间
- **GPU**: CUDA 11.8+ (可选，用于GPU加速)

### 软件要求

| 软件 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Docker | 20.10+ | 24.0+ |
| Docker Compose | 2.0+ | 2.20+ |
| Node.js | 18.x | 20.x |
| Python | 3.11 | 3.11+ |
| PostgreSQL | 15+ | 16+ |
| Redis | 7+ | 7.2+ |

---

## 快速部署

### 一键部署 (Docker Compose)

```bash
# 克隆仓库
git clone https://github.com/kogamishinyajerry-ops/ai-designer.git
cd ai-designer

# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置必要的环境变量
# 必须配置: DATABASE_URL, REDIS_URL, GEMINI_API_KEY

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 访问服务

- 前端: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/api/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## Docker 部署

### 后端 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/ .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 前端 Dockerfile

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY frontend/ .

# 构建应用
RUN npm run build

# 生产镜像
FROM node:20-alpine

WORKDIR /app

# 复制构建产物
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["npm", "start"]
```

### Docker Compose 配置

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: ai-designer-db
    environment:
      POSTGRES_DB: ai_designer
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: ai-designer-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: ai-designer-backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/ai_designer
      REDIS_URL: redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - model_cache:/app/models
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    container_name: ai-designer-frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: ai-designer-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  model_cache:
```

---

## 本地开发部署

### 后端部署

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 初始化数据库
python -c "from core.database import init_db; import asyncio; asyncio.run(init_db())"

# 启动开发服务器
python main.py

# 或使用 uvicorn 直接启动（带自动重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端部署

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.local.example .env.local
# 编辑 .env.local 文件

# 启动开发服务器
npm run dev

# 或构建生产版本
npm run build
npm start
```

---

## 生产环境部署

### 使用 Nginx 反向代理

```nginx
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name your-domain.com;

    # HTTP to HTTPS 重定向
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL 证书配置
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # 前端路由
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 后端 API
    location /api {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # API 文档
    location /api/docs {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }

    # 静态文件
    location /static {
        proxy_pass http://backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 使用 PM2 管理 Node.js 进程

```bash
# 安装 PM2
npm install -g pm2

# 启动前端
cd frontend
pm2 start npm --name "ai-designer-frontend" -- start

# 查看 PM2 状态
pm2 status

# 查看日志
pm2 logs ai-designer-frontend

# 重启服务
pm2 restart ai-designer-frontend

# 停止服务
pm2 stop ai-designer-frontend

# 设置开机自启
pm2 startup
pm2 save
```

### 使用 Systemd 管理 Python 进程

创建 `/etc/systemd/system/ai-designer-backend.service`:

```ini
[Unit]
Description=AI Designer Backend
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/ai-designer/backend
Environment="PATH=/path/to/ai-designer/backend/venv/bin"
ExecStart=/path/to/ai-designer/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务:

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ai-designer-backend

# 查看状态
sudo systemctl status ai-designer-backend

# 设置开机自启
sudo systemctl enable ai-designer-backend
```

---

## 环境变量配置

### 后端环境变量 (.env)

```bash
# === 应用配置 ===
APP_NAME=AI Designer
APP_ENV=production
DEBUG=false
SECRET_KEY=your-secret-key-change-this

# === 数据库配置 ===
DATABASE_URL=postgresql://user:password@localhost:5432/ai_designer
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# === Redis 配置 ===
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=20

# === AI 模型配置 ===
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash-exp

IMAGE_MODEL_ID=black-forest-labs/FLUX.1-schnell
CLIP_MODEL_ID=laion/CLIP-ViT-L-14-DataComp.XL-s13B-b90k

# === Qdrant 向量数据库 ===
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-api-key

# === CORS 配置 ===
CORS_ORIGINS=http://localhost:3000,https://your-domain.com

# === 速率限制 ===
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# === 缓存配置 ===
CACHE_ENABLED=true
CACHE_TTL=3600

# === 日志配置 ===
LOG_LEVEL=info
LOG_FILE=/var/log/ai-designer/app.log
```

### 前端环境变量 (.env.local)

```bash
# === API 配置 ===
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_V1_URL=http://localhost:8000/api/v1

# === 应用配置 ===
NEXT_PUBLIC_APP_NAME=AI Designer
NEXT_PUBLIC_APP_URL=http://localhost:3000

# === 第三方服务 ===
NEXT_PUBLIC_GA_ID=your-google-analytics-id
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
```

---

## 故障排除

### 常见问题

#### 1. 数据库连接失败

```bash
# 检查 PostgreSQL 状态
docker-compose ps postgres

# 查看日志
docker-compose logs postgres

# 重启 PostgreSQL
docker-compose restart postgres

# 检查连接
docker-compose exec postgres psql -U postgres -d ai_designer -c "SELECT 1;"
```

#### 2. Redis 连接失败

```bash
# 检查 Redis 状态
docker-compose ps redis

# 测试连接
docker-compose exec redis redis-cli ping

# 清除所有缓存
docker-compose exec redis redis-cli FLUSHALL
```

#### 3. AI 模型加载失败

```bash
# 检查磁盘空间
df -h

# 清理未使用的 Docker 镜像
docker system prune -a

# 手动下载模型
python -c "from services.ai_models import ModelManager; ModelManager().load_all_models()"
```

#### 4. 前端构建失败

```bash
# 清除缓存
rm -rf .next node_modules

# 重新安装依赖
npm install

# 检查 Node.js 版本
node --version

# 重新构建
npm run build
```

#### 5. 端口被占用

```bash
# 查找占用端口的进程
sudo lsof -i :3000
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>
```

### 健康检查

```bash
# 后端健康检查
curl http://localhost:8000/health

# API 文档检查
curl http://localhost:8000/api/docs

# 数据库连接检查
docker-compose exec postgres psql -U postgres -d ai_designer -c "SELECT version();"

# Redis 连接检查
docker-compose exec redis redis-cli ping
```

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 查看最近 100 行日志
docker-compose logs --tail=100 backend
```

---

## 性能优化

### 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_designs_project_id ON designs(project_id);

-- 分析查询性能
EXPLAIN ANALYZE SELECT * FROM projects WHERE user_id = 'xxx';
```

### Redis 缓存优化

```bash
# 配置 Redis 最大内存
maxmemory 2gb
maxmemory-policy allkeys-lru
```

### Nginx 优化

```nginx
# 启用 gzip 压缩
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript;

# 启用缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;
```

---

## 安全建议

1. **更改默认密码**: 修改所有默认数据库和 Redis 密码
2. **使用强密钥**: 生成安全的 SECRET_KEY
3. **启用 HTTPS**: 使用 Let's Encrypt 获取免费 SSL 证书
4. **配置防火墙**: 限制不必要的端口访问
5. **定期更新**: 保持系统和依赖包更新
6. **监控日志**: 设置日志监控和告警

---

## 备份与恢复

### 数据库备份

```bash
# 备份数据库
docker-compose exec postgres pg_dump -U postgres ai_designer > backup.sql

# 恢复数据库
docker-compose exec -T postgres psql -U postgres ai_designer < backup.sql
```

### Redis 备份

```bash
# 备份 Redis 数据
docker-compose exec redis redis-cli SAVE
docker cp ai-designer-redis:/data/dump.rdb ./redis_backup.rdb

# 恢复 Redis 数据
docker cp ./redis_backup.rdb ai-designer-redis:/data/dump.rdb
docker-compose restart redis
```

---

## 更新部署

```bash
# 拉取最新代码
git pull origin main

# 重新构建 Docker 镜像
docker-compose build --no-cache

# 重启服务
docker-compose down
docker-compose up -d

# 查看启动日志
docker-compose logs -f
```

---

## 监控

### 基础监控

```bash
# 系统资源监控
htop

# Docker 容器监控
docker stats

# 应用日志监控
docker-compose logs -f --tail=100
```

### 推荐监控工具

- **Prometheus + Grafana**: 指标收集和可视化
- **Sentry**: 错误追踪
- **ELK Stack**: 日志分析
- **UptimeRobot**: 服务可用性监控

---

**文档版本**: v1.0  
**最后更新**: 2026-02-18
