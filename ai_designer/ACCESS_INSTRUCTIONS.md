# Cloud Studio 访问说明

## 当前服务状态

后端服务运行在: http://localhost:8000
前端服务运行在: http://localhost:3000

## 在 Cloud Studio 中访问

### 方法 1: 使用 Cloud Studio 预览端口

1. 在 Cloud Studio 界面右侧找到"端口"标签
2. 点击"添加端口"按钮
3. 输入端口号: `3000`
4. 点击"打开预览"

### 方法 2: 使用 Cloud Studio 内置代理

Cloud Studio 会自动将服务通过特定 URL 暴露，格式通常为:

```
https://<workspace-id>-3000.cloudstudio.work
```

### 方法 3: 直接在终端测试

```bash
# 测试后端 API
curl http://localhost:8000/health

# 测试前端页面
curl http://localhost:3000
```

## 可能的问题

### 如果预览页面空白:

1. 检查浏览器控制台是否有错误 (F12)
2. 检查网络请求是否失败
3. 尝试刷新页面 (Ctrl+F5 或 Cmd+Shift+R)

### 如果 API 调用失败:

前端配置的 API 地址是 `http://localhost:8000`，在某些环境下可能需要修改为 Cloud Studio 的代理地址。

查看 `/workspace/ai_designer/frontend/.env.local` 修改配置:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 服务日志

查看实时日志:
```bash
# 后端日志 (在后台运行)
tail -f /workspace/ai_designer/backend/logs/app.log

# 前端日志
# 前端在当前终端运行，直接查看输出
```

## 重启服务

如果需要重启服务:

```bash
# 停止服务
pkill -f "uvicorn main:app"
pkill -f "next dev"

# 重新启动
cd /workspace/ai_designer/backend
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info > logs/app.log 2>&1 &

cd /workspace/ai_designer/frontend
npm run dev
```
