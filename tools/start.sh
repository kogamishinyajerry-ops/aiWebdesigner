#!/bin/sh

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

# 启动Ollama服务
echo -e "${YELLOW}启动 Ollama 服务...${NC}"
ollama serve &
OLLAMA_PID=$!

# 启动OpenWebUI
echo -e "${YELLOW}启动 OpenWebUI...${NC}"
open-webui serve --port 8080 &
WEBUI_PID=$!

# 等待服务启动
sleep 3

# 显示状态
echo -e "\n=== 服务状态 ==="
if ps -p $OLLAMA_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Ollama 运行中 (PID: $OLLAMA_PID)"
    ollama_ok=1
else
    echo -e "${RED}✗${NC} Ollama 未运行"
    ollama_ok=0
fi

if ps -p $WEBUI_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} OpenWebUI 运行中 (PID: $WEBUI_PID)"
    webui_ok=1
else
    echo -e "${RED}✗${NC} OpenWebUI 未运行"
    webui_ok=0
fi

# 显示访问信息
if [ "$ollama_ok" = "1" ] && [ "$webui_ok" = "1" ]; then
    echo -e "\n${GREEN}服务已启动!${NC}"
    echo -e "访问 OpenWebUI: ${YELLOW}http://localhost:8080${NC}"
else
    echo -e "\n${RED}警告: 部分服务未能启动${NC}"
fi

echo -e "\n按 Ctrl+C 停止所有服务"

# 等待所有后台进程
wait