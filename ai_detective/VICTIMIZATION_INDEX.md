# 职业碰瓷式维权案件 - 工具包索引

## 📦 工具包总览

基于专业警员视角开发的完整职业碰瓷式维权案件分析和管理系统。

---

## 🚀 快速导航

### 📖 深度分析报告

| 文件 | 大小 | 说明 |
|------|------|------|
| [PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md](PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md) | 27KB | **V2深度拓展版** - 14章完整分析，12,000字 |
| [PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT.md](PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT.md) | 16KB | V1基础版 |

### 🛠️ 工具脚本

| 文件 | 大小 | 功能 |
|------|------|------|
| [action_checklist_generator.py](action_checklist_generator.py) | 22KB | 行动检查清单生成器 |
| [speech_behavior_analyzer.py](speech_behavior_analyzer.py) | 17KB | 言语举动分析工具 |
| [victimization_case_manager.py](victimization_case_manager.py) | 22KB | 案件管理系统 |

### 📋 生成的清单和报告

| 文件 | 大小 | 类型 | 说明 |
|------|------|------|------|
| [action_checklist.md](action_checklist.md) | 8.8KB | MD | 行动检查清单（Markdown格式） |
| [action_checklist.json](action_checklist.json) | - | JSON | 行动检查清单（JSON格式） |
| [speech_behavior_analysis.md](speech_behavior_analysis.md) | 9.6KB | MD | 言语举动分析（Markdown格式） |
| [speech_behavior_analysis.json](speech_behavior_analysis.json) | - | JSON | 言语举动分析（JSON格式） |

### 📚 使用指南

| 文件 | 大小 | 说明 |
|------|------|------|
| [VICTIMIZATION_TOOLS_GUIDE.md](VICTIMIZATION_TOOLS_GUIDE.md) | 11KB | **详细使用指南** - 4个场景，完整说明 |
| [VICTIMIZATION_TOOLS_SUMMARY.md](VICTIMIZATION_TOOLS_SUMMARY.md) | 8.5KB | **项目总结** - 快速概览 |

### 📁 案例数据

| 文件 | 大小 | 类型 | 说明 |
|------|------|------|------|
| [cases/case_20260217_060737.json](cases/case_20260217_060737.json) | 6.6KB | JSON | 示例案件数据 |
| [cases/case_20260217_060737.md](cases/case_20260217_060737.md) | 5.5KB | MD | 示例案件报告 |

---

## 📖 按使用场景

### 场景1: 我想了解职业碰瓷的深度分析

👉 **阅读**: `PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md`

**包含内容**:
- 14章深度分析
- 行动路线分析
- 关键言语举动识别
- 举一反三的深度分析
- 5条完整证据链
- 50+项关键证据清单
- 三轨并行诉讼策略

---

### 场景2: 我需要一份可操作的行动清单

👉 **运行**: `python3 action_checklist_generator.py`

**输出**:
- `action_checklist.md` - Markdown 格式
- `action_checklist.json` - JSON 格式

**包含内容**:
- 立即行动（24小时内）- 6项
- 短期行动（1周内）- 6项
- 中期行动（1个月内）- 6项
- 长期行动（3-6个月）- 5项
- 证据清单 - 13项
- 文书清单 - 7项
- 言语分析 - 16项

---

### 场景3: 我需要分析监控录像中的言语和举动

👉 **运行**: `python3 speech_behavior_analyzer.py`

**输出**:
- `speech_behavior_analysis.md` - Markdown 格式
- `speech_behavior_analysis.json` - JSON 格式

**包含内容**:
- 言语记录 - 17项
- 行为记录 - 13项
- 高重要性项目 - 23项
- 完整时间线
- 统计分析

---

### 场景4: 我需要管理一个真实的案件

👉 **运行**: `python3 victimization_case_manager.py`

**输出**:
- `cases/case_[ID].json` - JSON 格式
- `cases/case_[ID].md` - Markdown 格式

**功能**:
- 案件基本信息管理
- 检查清单管理（带进度跟踪）
- 证据管理（带获取状态）
- 文书管理（带准备状态）
- 时间线管理
- 笔记管理
- 进度摘要
- 紧急项目提醒
- 高重要性项目筛选

---

### 场景5: 我想了解如何使用这些工具

👉 **阅读**: `VICTIMIZATION_TOOLS_GUIDE.md`

**包含内容**:
- 工具列表和功能说明
- 详细使用说明（4个场景）
- 文件结构说明
- 核心功能说明
- 预谋性/惯犯/团伙判断标准
- 言语/行为类别分析
- 进度跟踪说明
- 紧急提醒功能
- 高重要性项目筛选
- 导出格式说明
- 使用建议和注意事项

---

## 📊 按功能模块

### 1. 深度分析模块

**文件**: `PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md`

**功能**:
- ✅ 行动路线分析
- ✅ 关键言语举动识别
- ✅ 举一反三的深度分析
- ✅ 证据链完整构建
- ✅ 立案可能性评估
- ✅ 诉讼策略优化

---

### 2. 检查清单模块

**文件**: `action_checklist_generator.py`

**功能**:
- ✅ 生成立即/短期/中期/长期行动清单
- ✅ 生成证据清单
- ✅ 生成文书清单
- ✅ 包含预谋性/惯犯/团伙判断标准
- ✅ 支持导出 Markdown 和 JSON 格式

---

### 3. 言语举动分析模块

**文件**: `speech_behavior_analyzer.py`

**功能**:
- ✅ 分析监控录像中的关键言语
- ✅ 分析监控录像中的关键行为
- ✅ 生成时间戳分析表
- ✅ 按类别筛选（挑衅性/取证性/威胁性）
- ✅ 统计分析（次数、类别分布）

---

### 4. 案件管理模块

**文件**: `victimization_case_manager.py`

**功能**:
- ✅ 案件基本信息管理
- ✅ 检查清单管理（带进度跟踪）
- ✅ 证据管理（带获取状态）
- ✅ 文书管理（带准备状态）
- ✅ 时间线管理
- ✅ 笔记管理
- ✅ 进度摘要
- ✅ 紧急项目提醒
- ✅ 高重要性项目筛选

---

## 🎯 核心判断标准

### 预谋性判断

✅ **高度可疑**:
- 直接从某点进入豫园，直奔本店铺（中间无逗留）
- 进入店铺前在店外停留观察超过2分钟
- 全程手机录像或频繁拍照
- 未购买其他任何商品

---

### 惯犯判断

✅ **高度可能是惯犯**:
- 历史发帖中有3次以上类似"维权"
- 文案结构高度相似（都有"诈骗"、"中国警察"等关键词）
- 专门在旅游景区发生
- 发帖时间都在早高峰（6:00-7:00）
- 有多次行政投诉记录

---

### 团伙作案判断

✅ **高度可能是团伙**:
- 有同伴但未进入店铺（在外观望）
- 冲突后有人接应
- 行为有明确分工（一人缠斗、一人取证、一人发帖）
- 有多个账号参与舆论攻击

---

## 📈 数据统计

### 深度分析报告

- 章节数: 14 章
- 总字数: 约12,000字
- 证据链: 5 条
- 证据项: 50+ 项

### 检查清单生成器

- 立即行动项: 6 项
- 短期行动项: 6 项
- 中期行动项: 6 项
- 长期行动项: 5 项
- 证据项: 13 项
- 文书项: 7 项

### 言语举动分析

- 言语总数: 17 项
- 行为总数: 13 项
- 高重要性项目: 23 项

---

## 💡 快速命令参考

```bash
# 查看深度分析报告
cat PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md

# 生成行动检查清单
python3 action_checklist_generator.py

# 分析言语举动
python3 speech_behavior_analyzer.py

# 管理案件
python3 victimization_case_manager.py

# 查看使用指南
cat VICTIMIZATION_TOOLS_GUIDE.md

# 查看项目总结
cat VICTIMIZATION_TOOLS_SUMMARY.md
```

---

## 📞 获取帮助

| 问题 | 解决方案 |
|------|---------|
| 如何使用工具？ | 查看 `VICTIMIZATION_TOOLS_GUIDE.md` |
| 工具有哪些功能？ | 查看 `VICTIMIZATION_TOOLS_SUMMARY.md` |
| 如何判断预谋性？ | 查看 `PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md` 第1章 |
| 如何分析言语举动？ | 运行 `python3 speech_behavior_analyzer.py` |
| 如何管理案件？ | 运行 `python3 victimization_case_manager.py` |
| 如何生成检查清单？ | 运行 `python3 action_checklist_generator.py` |

---

## ⚠️ 重要提示

1. **仅供参考** - 本工具仅供参考，不构成正式法律意见
2. **咨询律师** - 重要案件请咨询专业律师
3. **证据收集** - 优先收集和固定证据
4. **诉讼时效** - 民事诉讼时效一般为3年
5. **数据安全** - 保护个人隐私，不要泄露敏感信息

---

## 📝 版本信息

**版本**: 1.0
**发布日期**: 2026年2月17日
**状态**: ✅ 完成并可用

---

**祝您维权顺利！** 🎉
