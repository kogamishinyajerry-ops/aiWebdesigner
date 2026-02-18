#!/bin/bash
# AI Designer 服务启动脚本

set -e

echo "=========================================="
echo "AI Designer 服务启动"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# 进入项目目录
cd /workspace/ai_designer

# 停止现有服务
echo -e "${BLUE}[1/4] 停止现有服务...${NC}"
pkill -9 -f "uvicorn main:app" 2>/dev/null || true
pkill -9 -f "node.*next" 2>/dev/null || true
sleep 2
echo -e "${GREEN}✓ 服务已停止${NC}"

# 启动后端
echo ""
echo -e "${BLUE}[2/4] 启动后端服务...${NC}"
cd backend
mkdir -p logs
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info > logs/app.log 2>&1 &
BACKEND_PID=$!
cd ..
sleep 3

# 检查后端
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 后端服务已启动 (PID: $BACKEND_PID)${NC}"
else
    echo "✗ 后端服务启动失败"
    exit 1
fi

# 启动前端
echo ""
echo -e "${BLUE}[3/4] 启动前端服务...${NC}"
cd frontend
rm -rf .next  # 清理缓存
nohup npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# 等待前端编译
echo "等待前端编译..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 前端服务已启动 (PID: $FRONTEND_PID)${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "⚠ 前端服务可能还在编译中..."
    fi
    sleep 2
done

echo ""
echo -e "${BLUE}[4/4] 服务状态${NC}"
echo ""
echo "后端服务:"
echo "  - 状态: 运行中"
echo "  - 地址: http://localhost:8000"
echo "  - API 文档: http://localhost:8000/docs"
echo "  - 日志: /workspace/ai_designer/backend/logs/app.log"
echo ""
echo "前端服务:"
echo "  - 状态: 运行中 (可能还在编译)"
echo "  - 地址: http://localhost:3000"
echo "  - 日志: /tmp/frontend.log"
echo ""
echo -e "${GREEN}=========================================="
echo "✓ 服务启动完成"
echo "==========================================${NC}"
echo ""
echo "访问方式:"
echo "1. 在 Cloud Studio 中点击端口 3000 的预览按钮"
echo "2. 或通过 Cloud Studio 端口管理功能访问"
echo ""
echo "测试服务:"
echo "  ./test-full-flow.sh"
