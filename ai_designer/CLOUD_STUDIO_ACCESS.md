# Cloud Studio 访问指南

## 当前服务状态

✅ 后端服务运行在: http://localhost:8000
✅ 前端服务运行在: http://localhost:3000

## 如何在 Cloud Studio 中访问应用

### 方法 1: 使用 Cloud Studio 端口预览（推荐）

**访问前端界面：**

1. 在 Cloud Studio 右侧面板找到"端口"（Ports）标签
2. 点击"添加端口"或查找已监听的端口
3. 找到端口 **3000**
4. 点击"打开预览"或"浏览器打开"按钮

**访问后端 API 文档：**

1. 在"端口"标签页中找到端口 **8000**
2. 点击"打开预览"
3. 访问 http://localhost:8000/docs 查看 API 文档

### 方法 2: 使用 Cloud Studio 内置 URL

Cloud Studio 会自动为每个端口生成公开访问的 URL，格式类似：

```
前端: https://xxx-3000.preview.cloudstudio.work
后端: https://xxx-8000.preview.cloudstudio.work
```

您可以在"端口"标签页中找到这些链接。

## 如果无法访问，请按以下步骤排查

### 步骤 1: 检查服务是否运行

在终端中运行：

```bash
# 检查后端服务
curl http://localhost:8000/health

# 检查前端服务
curl http://localhost:3000
```

如果都返回正常响应，说明服务运行正常，问题出在 Cloud Studio 预览配置。

### 步骤 2: 重新添加端口预览

1. 在"端口"标签页，找到对应的端口（3000 或 8000）
2. 点击端口旁边的"删除"或"停止"按钮
3. 点击"添加端口"
4. 输入端口号
5. 确认添加
6. 点击"打开预览"

### 步骤 3: 清除浏览器缓存

1. 按 `Ctrl + Shift + R` (Windows/Linux) 或 `Cmd + Shift + R` (Mac) 强制刷新页面
2. 或者在浏览器开发者工具中（F12）右键点击刷新按钮，选择"清空缓存并硬性重新加载"

### 步骤 4: 检查浏览器控制台

1. 按 F12 打开开发者工具
2. 切换到 Console（控制台）标签
3. 查看是否有红色错误信息
4. 切换到 Network（网络）标签
5. 刷新页面，查看哪些请求失败

### 步骤 5: 检查防火墙或网络限制

如果您在某些网络环境下（如公司内网），Cloud Studio 的预览端口可能被防火墙阻止。尝试：
- 使用个人网络（如手机热点）
- 联系网络管理员开放相关端口

## API 调用问题

在 Cloud Studio 环境中，前端（3000端口）调用后端（8000端口）的 API 时可能会遇到跨域问题。

### 解决方案：

前端配置中已经设置了 `http://localhost:8000` 作为 API 地址。在 Cloud Studio 的预览环境中：

1. **确保后端服务已通过端口 8000 暴露**
2. **在浏览器中访问前端时，API 请求应该能够正确路由**

如果仍然遇到 CORS 错误，可以：

1. 检查后端 CORS 配置（`/workspace/ai_designer/backend/core/config.py`）
2. 确认 `CORS_ORIGINS` 包含 Cloud Studio 的预览域名

## 快速测试命令

在 Cloud Studio 终端中运行以下命令测试服务：

```bash
# 测试后端健康检查
curl http://localhost:8000/health

# 测试图像生成 API
curl -X POST http://localhost:8000/api/v1/image/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"test","width":512,"height":512,"style":"modern_minimal","num_images":1}'

# 测试前端首页
curl -I http://localhost:3000

# 查看服务日志
ps aux | grep -E "(next|uvicorn)"
```

## 重新启动服务

如果服务停止，使用以下命令重启：

```bash
# 进入项目目录
cd /workspace/ai_designer

# 重启后端
cd backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info > logs/app.log 2>&1 &

# 重启前端
cd ../frontend
npm run dev
```

## 常见问题

### Q: 预览页面显示空白或加载中
**A:** 等待几秒钟，Next.js 首次编译需要时间。如果长时间空白，检查浏览器控制台错误。

### Q: 预览页面显示 "This site can't be reached"
**A:** 端口可能未正确暴露，重新添加端口预览。

### Q: API 调用失败（network error）
**A:** 确保后端服务（8000端口）也已通过 Cloud Studio 预览端口暴露。

### Q: 前端页面显示正常但功能无法使用
**A:** 检查浏览器控制台的网络请求，确认 API 请求是否成功。

## 获取帮助

如果以上方法都无法解决问题，请：

1. 在 Cloud Studio 终端中运行：`tail -f /workspace/ai_designer/backend/logs/app.log` 查看后端日志
2. 检查前端终端输出
3. 截图浏览器控制台错误信息
4. 记录具体错误信息以便进一步排查

## 备用方案：直接在本地运行

如果 Cloud Studio 环境无法访问，可以将代码克隆到本地运行：

```bash
# 克隆代码到本地
git clone <your-repo-url>

# 启动后端
cd ai_designer/backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# 启动前端（新终端）
cd ai_designer/frontend
npm install
npm run dev
```

然后访问 http://localhost:3000
