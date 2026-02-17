# AI 侦探 (AI Detective)

> 基于深度法律推理的智能纠纷分析和报案材料生成系统

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 🎯 项目简介

AI 侦探是一个智能法律辅助系统，通过深度逻辑推理和民法法律条款匹配，为用户提供日常纠纷的分析指导和报案材料生成服务。

### 核心功能

- 🔍 **智能案情分析** - AI 提取事实要素，识别法律关系
- ⚖️ **法律条文匹配** - 自动匹配适用法律条款
- 📊 **风险评估** - 评估胜诉概率、时间成本、经济成本
- 📄 **材料生成** - 自动生成报案材料、证据清单、起诉状
- 💡 **专业建议** - 提供证据收集和诉讼建议

---

## 🏗️ 项目结构

```
ai_detective/
├── backend/              # 后端服务
│   ├── __init__.py      # 模块初始化
│   ├── main.py          # FastAPI 主应用
│   ├── conversation.py  # 对话管理
│   ├── reasoner.py      # 法律推理引擎
│   ├── generator.py     # 材料生成器
│   └── evidence.py      # 证据分析器
├── frontend/             # 前端界面
│   └── index.html       # Web UI
├── knowledge_base/       # 法律知识库
├── docs/                # 文档
├── requirements.txt     # Python 依赖
└── README.md           # 项目文档
```

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- pip 包管理器

### 安装步骤

1. **克隆项目**
```bash
cd ai_detective
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动后端服务**
```bash
cd backend
python main.py
```

后端将在 `http://localhost:8000` 启动

4. **访问前端**

在浏览器中打开 `frontend/index.html` 文件

---

## 📖 使用指南

### 1. 描述案情

在左侧表单中详细描述您遇到的问题，包括：
- 事件发生的时间和地点
- 涉及的人员
- 具体经过
- 损失情况

### 2. 开始分析

点击"开始分析"按钮，AI 将：
- 提取事实要素
- 识别法律关系
- 匹配适用法律
- 认定法律责任
- 评估风险

### 3. 生成材料

点击"生成材料"按钮，系统将自动生成：
- 📋 案情说明
- 📚 证据清单
- ✍️ 诉求陈述
- 📄 民事起诉状

### 4. 下载材料

点击"下载"按钮，将材料保存为 Markdown 格式

---

## 🔧 API 文档

启动服务后访问：http://localhost:8000/docs

### 主要端点

#### POST `/analyze`
分析案件

**请求体：**
```json
{
  "description": "案情描述",
  "context": {}
}
```

**响应：**
```json
{
  "facts": [...],
  "legal_relations": [...],
  "applicable_laws": [...],
  "liability": {...},
  "risk_assessment": {...},
  "suggestions": [...],
  "confidence": 0.75
}
```

#### POST `/documents/generate`
生成报案材料

**请求体：**
```json
{
  "description": "案情描述",
  "user_info": {
    "name": "姓名",
    "phone": "电话",
    "address": "地址"
  }
}
```

#### GET `/evidence/suggest/{case_type}`
建议证据类型

#### GET `/health`
健康检查

---

## 💡 支持的案件类型

- ✅ 肖像权侵权
- ✅ 合同违约
- ✅ 人身损害
- ✅ 房屋租赁纠纷
- ✅ 其他民事纠纷

---

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI
- **AI 引擎**: 基于规则的法律推理（可扩展接入 LLM）
- **数据**: Pydantic 数据验证
- **文档**: 自动生成 OpenAPI 文档

### 前端
- **框架**: 原生 JavaScript
- **样式**: Tailwind CSS
- **设计**: 玻璃拟态风格

---

## ⚠️ 免责声明

1. 本系统仅供参考，不构成正式法律意见
2. 重要案件请咨询专业律师
3. 法律条文更新需及时同步
4. 最终责任由用户自行承担

---

## 🔮 未来规划

- [ ] 接入真实 LLM（GPT-4 / DeepSeek）
- [ ] 向量数据库（Qdrant / Chroma）
- [ ] 案例库集成
- [ ] 多轮对话优化
- [ ] 证据上传功能
- [ ] PDF 导出
- [ ] 移动端适配
- [ ] 律师对接平台

---

## 📝 开发日志

### v1.0.0 (2025-02-17)
- ✅ 完成基础架构
- ✅ 对话管理模块
- ✅ 法律推理引擎
- ✅ 材料生成器
- ✅ 证据分析器
- ✅ Web UI
- ✅ API 文档

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 📞 联系方式

如有问题，请提交 Issue 或联系项目维护者。

---

**Made with ❤️ for legal AI**
