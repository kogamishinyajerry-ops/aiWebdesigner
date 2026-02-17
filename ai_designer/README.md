# AI Designer - 艺术级前端AI设计师

> 以Gemini为标杆，具备极致艺术美学的AI前端设计系统

## 🎯 项目概览

AI Designer 是一个革命性的AI驱动前端设计系统，致力于为开发者和设计师提供：

- 🎨 **艺术级UI/UX设计** - AI驱动的美学引擎
- 🖼️ **智能图像生成** - Hero Banner、Icon集、背景纹理
- ✏️ **AI辅助矢量设计** - 文本描述生成SVG，草图转矢量
- 💻 **Design to Code 2.0** - 从艺术设计到优雅代码
- 🎭 **多风格支持** - Modern、Minimal、Glassmorphism等

## 🚀 快速开始

### 前置要求

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- CUDA 11.8+ (可选，用于GPU加速)

### 安装与运行

#### 1. 克隆仓库

```bash
git clone https://github.com/your-username/ai-designer.git
cd ai-designer
```

#### 2. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥

# 初始化数据库
python -c "from core.database import init_db; import asyncio; asyncio.run(init_db())"

# 启动后端
python main.py
```

后端将在 `http://localhost:8000` 启动

#### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.local.example .env.local

# 启动开发服务器
npm run dev
```

前端将在 `http://localhost:3000` 启动

### Docker 部署（推荐）

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📖 使用指南

### 图像生成

```bash
curl -X POST http://localhost:8000/api/v1/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "modern tech company hero banner",
    "style": "modern",
    "width": 1920,
    "height": 1080,
    "num_images": 1
  }'
```

### SVG生成

```bash
curl -X POST http://localhost:8000/api/v1/svg/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "a minimalist logo with a circle and triangle",
    "style": "minimal"
  }'
```

### 代码生成

```bash
curl -X POST http://localhost:8000/api/v1/code/generate \
  -H "Content-Type: application/json" \
  -d '{
    "design_description": "modern landing page with hero section",
    "framework": "react",
    "styling": "tailwind"
  }'
```

## 🏗️ 项目结构

```
ai_designer/
├── frontend/              # Next.js前端
│   ├── app/             # App Router页面
│   ├── components/      # React组件
│   ├── lib/            # 工具函数
│   ├── hooks/          # React Hooks
│   └── types/          # TypeScript类型
├── backend/              # FastAPI后端
│   ├── api/             # API路由
│   ├── models/          # 数据库模型
│   ├── services/        # 业务逻辑
│   ├── core/            # 核心配置
│   └── utils/           # 工具函数
├── shared/              # 共享代码
├── docs/                # 文档
├── data/                # 数据目录
└── logs/                # 日志文件
```

## 🛠️ 技术栈

### 前端
- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS + shadcn/ui
- **动画**: Framer Motion
- **状态**: Zustand
- **HTTP**: Axios

### 后端
- **框架**: FastAPI
- **语言**: Python 3.11
- **数据库**: PostgreSQL (asyncpg)
- **缓存**: Redis
- **ORM**: SQLAlchemy 2.0

### AI模型
- **图像生成**: FLUX.1, Stable Diffusion XL
- **设计理解**: Gemini 2.0
- **视觉分析**: CLIP ViT-L/14
- **代码生成**: GPT-4o

## 📊 API文档

访问 `http://localhost:8000/api/docs` 查看完整的API文档（Swagger UI）

### 主要端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/v1/image/generate` | POST | 生成图像 |
| `/api/v1/image/hero-banner` | POST | 生成Hero Banner |
| `/api/v1/svg/generate` | POST | 生成SVG |
| `/api/v1/code/generate` | POST | 生成代码 |
| `/health` | GET | 健康检查 |

## 🎨 支持的样式

### 图像样式
- **Modern** - 现代扁平化设计
- **Minimal** - 极简主义
- **Glassmorphism** - 玻璃态效果
- **Neumorphism** - 新拟态风格
- **Brutalism** - 粗野主义

### 代码框架
- React
- Vue
- Svelte
- Next.js
- Nuxt.js

## 🚀 开发计划

### Phase 1: MVP (4周) - 进行中 🚧
- [x] 项目初始化
- [ ] 图像生成模块
- [ ] SVG生成模块
- [ ] 简单代码生成
- [ ] 基础UI界面

### Phase 2: Beta (6周)
- [ ] 美学引擎
- [ ] Icon生成器
- [ ] 背景纹理生成
- [ ] Design to Code 2.0
- [ ] 性能优化

### Phase 3: Production (8周)
- [ ] 团队协作
- [ ] 版本控制
- [ ] 插件系统
- [ ] 企业级功能

详细开发计划请查看 [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)

## 📝 调研报告

完整的项目调研报告请查看 [AI_DESIGNER_RESEARCH.md](../AI_DESIGNER_RESEARCH.md)

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可证

MIT License

## 👥 作者

AI Design Team

## 🔗 相关链接

- [开发计划](DEVELOPMENT_PLAN.md)
- [调研报告](../AI_DESIGNER_RESEARCH.md)
- [API文档](http://localhost:8000/api/docs)
- [问题追踪](https://github.com/your-username/ai-designer/issues)

---

**注意**: 本项目目前处于开发阶段，预计4周后发布MVP版本。
