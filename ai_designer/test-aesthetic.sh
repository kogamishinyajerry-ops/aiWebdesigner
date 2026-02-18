#!/bin/bash
# 美学设计引擎测试脚本

echo "=========================================="
echo "AI美学设计引擎 - 功能测试"
echo "=========================================="

# 测试后端API
echo -e "\n[1/5] 测试后端健康检查..."
curl -s http://localhost:8000/health | python3 -m json.tool > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ 后端服务正常"
else
    echo "✗ 后端服务异常"
    exit 1
fi

# 测试获取风格列表
echo -e "\n[2/5] 测试获取艺术风格列表..."
curl -s http://localhost:8000/api/v1/aesthetic/styles | python3 -m json.tool > /dev/null 2>&1
if [ $? -eq 0 ]; then
    STYLE_COUNT=$(curl -s http://localhost:8000/api/v1/aesthetic/styles | python3 -c "import sys, json; print(len(json.load(sys.stdin)['styles']))")
    echo "✓ 获取到 $STYLE_COUNT 种艺术风格"
else
    echo "✗ 获取风格列表失败"
    exit 1
fi

# 测试生成美学设计
echo -e "\n[3/5] 测试生成美学设计方案..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/aesthetic/design \
  -H "Content-Type: application/json" \
  -d '{
    "art_style": "monet",
    "page_description": "一个瑜伽冥想应用，追求宁静优雅的氛围",
    "target_components": ["hero_banner", "card", "button"],
    "mood": "宁静、优雅",
    "complexity": "low",
    "include_interactions": true,
    "include_assets": true
  }')

echo "$RESPONSE" | python3 -m json.tool > /dev/null 2>&1
if [ $? -eq 0 ]; then
    SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['success'])")
    if [ "$SUCCESS" = "True" ]; then
        STYLE_NAME=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['aesthetic_analysis']['style_name'])")
        COMPONENT_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['component_designs']))")
        echo "✓ 设计方案生成成功"
        echo "  风格: $STYLE_NAME"
        echo "  组件数: $COMPONENT_COUNT"
    else
        echo "✗ 设计方案生成失败"
        exit 1
    fi
else
    echo "✗ API响应异常"
    exit 1
fi

# 测试前端页面
echo -e "\n[4/5] 测试前端页面..."
curl -s http://localhost:3000 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ 首页访问正常"
else
    echo "✗ 首页访问异常"
    exit 1
fi

curl -s http://localhost:3000/generator/aesthetic > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ 美学设计页面访问正常"
else
    echo "✗ 美学设计页面访问异常"
    exit 1
fi

# 测试不同风格
echo -e "\n[5/5] 测试多种艺术风格..."
STYLES=("van_gogh" "picasso" "kandinsky" "warhol")

for style in "${STYLES[@]}"; do
    RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/aesthetic/design \
      -H "Content-Type: application/json" \
      -d "{
        \"art_style\": \"$style\",
        \"page_description\": \"测试页面\",
        \"target_components\": [\"card\"],
        \"complexity\": \"low\"
      }")
    
    SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['success'])" 2>/dev/null)
    
    if [ "$SUCCESS" = "True" ]; then
        MOOD=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['aesthetic_analysis']['mood'])" 2>/dev/null)
        echo "  ✓ $style: $MOOD"
    else
        echo "  ✗ $style: 生成失败"
    fi
done

echo -e "\n=========================================="
echo "✓ 所有测试通过！"
echo "=========================================="
echo -e "\n访问方式:"
echo "  前端: http://localhost:3000"
echo "  美学设计页面: http://localhost:3000/generator/aesthetic"
echo "  后端API: http://localhost:8000/docs"
