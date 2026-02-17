# AI 阅读助手 - MVP 项目

> 一个小而美的 AI 阅读助手，让长文变短文，快速获取信息

## ✨ 核心功能

1. **文本摘要** - 一键提炼长文精华
2. **关键信息提取** - 提取重要观点和数据
3. **思维导图** - 可视化内容结构
4. **多语言翻译** - 支持多语言
5. **本地存储** - 保护隐私

## 🚀 快速开始

### 安装依赖

```bash
cd ai_reading_helper
pip install -r requirements.txt
```

### 运行项目

```bash
python app.py
```

访问: http://localhost:8000

## 📱 功能演示

### 1. 文本摘要
输入长文本，AI 自动生成简洁摘要

### 2. 思维导图
自动生成文章结构的思维导图

### 3. 关键词提取
提取文章核心关键词和概念

## 🛠️ 技术栈

- **前端**: React + Vite + Tailwind CSS + shadcn/ui
- **后端**: Python FastAPI
- **AI**: OpenAI API 或本地 LLM
- **可视化**: D3.js

## 📁 项目结构

```
ai_reading_helper/
├── frontend/          # 前端代码
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/           # 后端代码
│   ├── main.py
│   ├── ai_service.py
│   └── models.py
├── requirements.txt
└── README.md
```

## 🎯 使用场景

- 快速阅读长篇文章
- 学习笔记整理
- 会议记录提炼
- 研究论文总结

## 💡 未来规划

- [ ] 浏览器插件版本
- [ ] PDF/Word 文件支持
- [ ] 导出 Notion/Obsidian
- [ ] 本地 LLM 支持
- [ ] 离线模式

## 📄 许可证

MIT License
