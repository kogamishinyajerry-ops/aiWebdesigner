#!/bin/bash

# AI 侦探启动脚本

echo "🔍 AI 侦探 - 启动中..."
echo ""

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python 版本: $python_version"

# 检查是否安装了依赖
echo ""
echo "📦 检查依赖..."
if python3 -c "import fastapi" 2>/dev/null; then
    echo "✓ FastAPI 已安装"
else
    echo "✗ FastAPI 未安装"
    echo "请运行: pip install -r requirements.txt"
    exit 1
fi

# 启动后端服务
echo ""
echo "🚀 启动后端服务..."
cd "$(dirname "$0")/backend"
python3 main.py &
BACKEND_PID=$!

echo "✓ 后端服务已启动 (PID: $BACKEND_PID)"
echo "📍 API 地址: http://localhost:8000"
echo "📚 API 文档: http://localhost:8000/docs"
echo ""
echo "🌐 请在浏览器中打开: frontend/index.html"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待用户中断
wait $BACKEND_PID
