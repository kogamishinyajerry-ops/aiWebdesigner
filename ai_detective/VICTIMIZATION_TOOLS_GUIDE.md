# 职业碰瓷式维权案件 - 工具使用指南

## 📚 概述

本工具包基于《职业碰瓷式维权案件 - 深度拓展分析报告》（PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md）开发，提供了一套完整的案件管理和分析工具。

---

## 🛠️ 工具列表

### 1. **深度分析报告** (V2)

**文件**: `PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md`

**内容**:
- 14章深度分析内容
- 行动路线分析
- 关键言语举动识别
- 举一反三的深度分析
- 5条完整证据链
- 50+项关键证据清单
- 三轨并行诉讼策略

**使用方式**: 直接阅读 Markdown 文件

---

### 2. **行动检查清单生成器**

**文件**: `action_checklist_generator.py`

**功能**:
- 生成立即/短期/中期/长期行动清单
- 生成证据清单
- 生成文书清单
- 包含预谋性/惯犯/团伙判断标准
- 支持导出为 Markdown 和 JSON 格式

**使用方式**:
```bash
cd /workspace/ai_detective
python3 action_checklist_generator.py
```

**输出文件**:
- `action_checklist.md` - Markdown 格式检查清单
- `action_checklist.json` - JSON 格式检查清单

---

### 3. **言语举动分析工具**

**文件**: `speech_behavior_analyzer.py`

**功能**:
- 分析监控录像中的关键言语
- 分析监控录像中的关键行为
- 生成时间戳分析表
- 按类别筛选（挑衅性/取证性/威胁性）
- 统计分析（次数、类别分布）

**使用方式**:
```bash
cd /workspace/ai_detective
python3 speech_behavior_analyzer.py
```

**输出文件**:
- `speech_behavior_analysis.md` - Markdown 格式分析报告
- `speech_behavior_analysis.json` - JSON 格式分析报告

---

### 4. **案件管理系统**

**文件**: `victimization_case_manager.py`

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
- 自动生成完整报告

**使用方式**:
```bash
cd /workspace/ai_detective
python3 victimization_case_manager.py
```

**输出文件**:
- `cases/case_[ID].json` - JSON 格式案件数据
- `cases/case_[ID].md` - Markdown 格式案件报告

---

## 📖 详细使用说明

### 场景1: 快速开始

如果您是新用户，建议按以下顺序使用：

1. **阅读深度分析报告**
   ```
   打开: PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md
   了解: 14章深度分析内容
   ```

2. **生成行动检查清单**
   ```bash
   cd /workspace/ai_detective
   python3 action_checklist_generator.py
   打开: action_checklist.md
   ```

3. **分析言语举动**
   ```bash
   cd /workspace/ai_detective
   python3 speech_behavior_analyzer.py
   打开: speech_behavior_analysis.md
   ```

4. **创建案件**
   ```bash
   cd /workspace/ai_detective
   python3 victimization_case_manager.py
   打开: cases/case_[ID].md
   ```

---

### 场景2: 管理真实案件

如果您正在处理真实的职业碰瓷案件，建议按以下步骤：

#### 第1步: 初始化案件

```python
from victimization_case_manager import VictimCaseManager

# 创建案件管理器
manager = VictimCaseManager()

# 设置案件信息
manager.set_case_info(
    shop_name="您的店铺名称",
    location="发生地点",
    date="发生时间",
    amount="涉及金额",
    opposing_party="对方身份",
    description="案件描述"
)
```

#### 第2步: 添加检查清单项

```python
# 添加立即行动
manager.add_checklist_item(
    action="固定完整监控录像",
    category="立即行动（24小时内）",
    priority=5,  # 1-5，5为最高
    deadline="2026-02-18 23:59",
    completed=False,
    notes="防止证据丢失"
)
```

#### 第3步: 添加证据

```python
# 添加证据
manager.add_evidence(
    name="完整监控录像",
    category="预谋性",
    importance=5,  # 1-5，5为最高
    difficulty="容易",
    how_to_obtain="调取店铺监控",
    obtained=False,
    location="",
    notes=""
)
```

#### 第4步: 添加时间线事件

```python
# 添加言语事件
manager.add_timeline_event(
    time_str="01:10:00",
    event_type="言语",
    description="对方说：你刚才说什么？再说一遍！",
    category="取证性",
    importance=5,
    notes="引导商户重复激烈言语"
)
```

#### 第5步: 生成报告

```python
# 保存到文件
json_file, md_file = manager.save_to_file()

# 或者生成报告字符串
report = manager.generate_report()
print(report)
```

---

### 场景3: 分析监控录像

如果您需要分析监控录像中的言语和举动：

```python
from speech_behavior_analyzer import SpeechBehaviorAnalyzer

# 创建分析器
analyzer = SpeechBehaviorAnalyzer()

# 添加言语
analyzer.add_speech(
    time_str="01:10:00",
    speaker="对方",
    content="你刚才说什么？再说一遍！",
    category="取证性",
    analysis="引导商户重复激烈言语",
    importance=5
)

# 添加行为
analyzer.add_behavior(
    time_str="01:13:00",
    actor="对方",
    action="对着手机录像说：这家店在威胁我",
    category="取证性",
    analysis="取证话术",
    importance=5
)

# 筛选高重要性项目
high_importance = analyzer.get_high_importance_items(4)

# 生成报告
analyzer.save_to_file("my_case_analysis")
```

---

### 场景4: 自定义检查清单

如果您需要自定义检查清单：

```python
from action_checklist_generator import ActionChecklistGenerator

# 创建生成器
generator = ActionChecklistGenerator()

# 初始化案件信息
generator.initialize_case_info(
    shop_name="您的店铺名称",
    location="发生地点",
    date="发生时间",
    amount="涉及金额",
    opposing_party="对方身份"
)

# 添加行动项
generator.add_immediate_action(
    action="您的自定义行动",
    priority=5,
    completed=False,
    notes="备注"
)

# 保存
generator.save_to_file("my_checklist")
```

---

## 📊 文件结构

```
ai_detective/
├── PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md  # 深度分析报告（V2）
├── action_checklist_generator.py                    # 行动检查清单生成器
├── speech_behavior_analyzer.py                      # 言语举动分析工具
├── victimization_case_manager.py                    # 案件管理系统
├── action_checklist.md                              # 生成的检查清单（MD）
├── action_checklist.json                            # 生成的检查清单（JSON）
├── speech_behavior_analysis.md                      # 生成的言语分析（MD）
├── speech_behavior_analysis.json                    # 生成的言语分析（JSON）
└── cases/                                           # 案件目录
    ├── case_[ID].json                               # 案件数据
    └── case_[ID].md                                 # 案件报告
```

---

## 🎯 核心功能说明

### 1. 预谋性判断

判断对方是否为职业碰瓷的关键指标：

✅ **高度可疑**:
- 直接从某点进入豫园，直奔本店铺（中间无逗留）
- 进入店铺前在店外停留观察超过2分钟
- 全程手机录像或频繁拍照
- 未购买其他任何商品

⚠️ **需要注意**:
- 在其他店铺有短暂停留但未消费
- 有同伴但未进入店铺

❌ **不太可能是预谋**:
- 随意逛了多家店铺后进入本店
- 在其他店铺有正常消费记录

---

### 2. 惯犯判断

判断对方是否为惯犯的关键指标：

✅ **高度可能是惯犯**:
- 历史发帖中有3次以上类似"维权"
- 文案结构高度相似（都有"诈骗"、"中国警察"等关键词）
- 专门在旅游景区发生
- 发帖时间都在早高峰（6:00-7:00）
- 有多次行政投诉记录

---

### 3. 团伙作案判断

判断对方是否有同伙的关键指标：

✅ **高度可能是团伙**:
- 有同伴但未进入店铺（在外观望）
- 冲突后有人接应
- 行为有明确分工（一人缠斗、一人取证、一人发帖）
- 有多个账号参与舆论攻击

---

### 4. 言语类别分析

**挑衅性言语** - 证明其故意激怒:
- "你们店就这样做生意的？"
- "我看你们就是欺负外地人"
- "你们不给赠品就退款"

**取证性言语** - 证明其执行预案:
- "你刚才说什么？再说一遍！"
- "你敢不敢再说一遍？"
- "（对着手机录像说）这家店在威胁我"

**威胁性言语** - 证明其恶意报复:
- "我要让你们这店开不下去"
- "我会让大家都知道你们店的样子"
- "我要发到网上去"

---

### 5. 行为类别分析

**异常冷静行为** - 证明其经过训练:
- 原地拍照
- 冷静截图
- 现场报警
- 不逃跑

**制造场景行为** - 证明其表演性质:
- 站在门口不走
- 阻碍其他顾客进入
- 大声说话吸引注意
- 对着手机哭诉

**时间精确行为** - 证明其专业性:
- 6:47发布博文
- 支付后立即要求赠品
- 缠斗1小时后支付

---

## 📈 进度跟踪

### 检查清单进度

- 总项数
- 已完成数
- 完成率

### 证据收集进度

- 总项数
- 已获取数
- 获取率

### 文书准备进度

- 总项数
- 已完成数
- 完成率

---

## 🚨 紧急提醒

系统会自动识别即将到期的项目（默认24小时内）：

```python
# 获取紧急项目
urgent = manager.get_urgent_items(days=1)

for item in urgent:
    print(f"紧急: {item['行动']} (截止: {item['截止时间']})")
```

---

## ⭐ 高重要性项目

系统会自动筛选高重要性项目（重要性 ≥ 4）：

```python
# 获取高重要性项目
high_importance = manager.get_high_importance_items(threshold=4)

for item in high_importance:
    print(f"重要: {item}")
```

---

## 📤 导出格式

### Markdown 格式

适合阅读和打印
- 结构清晰
- 格式美观
- 可直接分享

### JSON 格式

适合程序处理
- 结构化数据
- 易于解析
- 可自动化处理

---

## 💡 使用建议

1. **立即行动**: 优先处理紧急和高重要性项目
2. **证据收集**: 尽快固定证据，防止丢失
3. **时间标注**: 准确标注时间戳，便于分析
4. **持续更新**: 随时更新进度，保持最新状态
5. **定期检查**: 定期查看进度摘要，了解整体情况

---

## ⚠️ 注意事项

1. **法律建议**: 本工具仅供参考，重要案件请咨询专业律师
2. **证据固定**: 尽快固定证据，考虑进行公证
3. **诉讼时效**: 民事诉讼时效一般为3年
4. **数据安全**: 保护个人隐私，不要泄露敏感信息

---

## 📞 获取帮助

- 查看深度分析报告: `PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md`
- 查看示例输出: `action_checklist.md`, `speech_behavior_analysis.md`, `cases/`
- 查看代码文档: 每个工具文件都有详细的 docstring

---

## 📝 更新日志

**版本**: 1.0
**日期**: 2026年2月17日
**内容**: 初始版本

- ✅ 深度分析报告（V2）
- ✅ 行动检查清单生成器
- ✅ 言语举动分析工具
- ✅ 案件管理系统
- ✅ 示例数据和输出

---

**最后更新**: 2026年2月17日
**工具版本**: 1.0
**状态**: ✅ 可用
