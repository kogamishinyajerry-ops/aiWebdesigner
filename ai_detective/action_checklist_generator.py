#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职业碰瓷式维权案件 - 行动检查清单生成器

基于 PROFESSIONAL_VICTIMIZATION_ANALYSIS_REPORT_V2.md 生成可操作的检查清单
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

class ActionChecklistGenerator:
    """行动检查清单生成器"""
    
    def __init__(self):
        self.checklist = {
            "案件基本信息": {},
            "立即行动（24小时内）": [],
            "短期行动（1周内）": [],
            "中期行动（1个月内）": [],
            "长期行动（3-6个月内）": [],
            "证据清单": [],
            "文书清单": [],
            "关键言语举动分析": {
                "挑衅性言语": [],
                "取证性言语": [],
                "威胁性言语": []
            },
            "关键行为分析": {
                "异常冷静行为": [],
                "制造场景行为": [],
                "时间精确行为": []
            },
            "预谋性判断标准": {
                "高度可疑": [],
                "需要注意": [],
                "不太可能": []
            },
            "惯犯判断标准": {
                "高度可能是惯犯": [],
                "可能是惯犯": [],
                "不太可能是惯犯": []
            },
            "团伙作案判断标准": {
                "高度可能是团伙": [],
                "可能是团伙": [],
                "不太可能是团伙": []
            }
        }
    
    def initialize_case_info(self, shop_name: str, location: str, date: str, 
                            amount: str, opposing_party: str):
        """初始化案件基本信息"""
        self.checklist["案件基本信息"] = {
            "店铺名称": shop_name,
            "发生地点": location,
            "发生时间": date,
            "涉及金额": amount,
            "对方身份": opposing_party,
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def add_immediate_action(self, action: str, priority: int = 5, 
                            completed: bool = False, notes: str = ""):
        """添加立即行动项"""
        self.checklist["立即行动（24小时内）"].append({
            "行动": action,
            "优先级": priority,  # 1-5，5为最高
            "是否完成": completed,
            "备注": notes,
            "截止时间": (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
        })
    
    def add_short_term_action(self, action: str, priority: int = 4,
                            completed: bool = False, notes: str = ""):
        """添加短期行动项"""
        self.checklist["短期行动（1周内）"].append({
            "行动": action,
            "优先级": priority,
            "是否完成": completed,
            "备注": notes,
            "截止时间": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        })
    
    def add_medium_term_action(self, action: str, priority: int = 3,
                             completed: bool = False, notes: str = ""):
        """添加中期行动项"""
        self.checklist["中期行动（1个月内）"].append({
            "行动": action,
            "优先级": priority,
            "是否完成": completed,
            "备注": notes,
            "截止时间": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        })
    
    def add_long_term_action(self, action: str, priority: int = 2,
                            completed: bool = False, notes: str = ""):
        """添加长期行动项"""
        self.checklist["长期行动（3-6个月内）"].append({
            "行动": action,
            "优先级": priority,
            "是否完成": completed,
            "备注": notes,
            "截止时间": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")
        })
    
    def add_evidence(self, evidence_name: str, importance: int, 
                    difficulty: str, how_to_obtain: str,
                    obtained: bool = False, location: str = ""):
        """添加证据项"""
        self.checklist["证据清单"].append({
            "证据名称": evidence_name,
            "重要性": importance,  # 1-5，5为最高
            "获取难度": difficulty,  # 容易/中等/困难/极难
            "获取方式": how_to_obtain,
            "是否已获取": obtained,
            "存放位置": location
        })
    
    def add_document(self, document_name: str, document_type: str,
                    status: str = "未准备", notes: str = ""):
        """添加文书项"""
        self.checklist["文书清单"].append({
            "文书名称": document_name,
            "文书类型": document_type,  # 行政/民事/刑事
            "状态": status,  # 未准备/准备中/已完成
            "备注": notes
        })
    
    def add_speech_analysis(self, category: str, time: str, content: str,
                           analysis: str, value: int):
        """添加言语分析"""
        self.checklist["关键言语举动分析"][category].append({
            "时间": time,
            "言语内容": content,
            "专业分析": analysis,
            "立案价值": value  # 1-5，5为最高
        })
    
    def add_behavior_analysis(self, category: str, time: str, behavior: str,
                             analysis: str, value: int):
        """添加行为分析"""
        self.checklist["关键行为分析"][category].append({
            "时间": time,
            "行为": behavior,
            "专业分析": analysis,
            "立案价值": value  # 1-5，5为最高
        })
    
    def generate_markdown(self) -> str:
        """生成 Markdown 格式的检查清单"""
        md = []
        
        # 标题
        md.append("# 职业碰瓷式维权案件 - 行动检查清单\n")
        
        # 案件基本信息
        md.append("## 📌 案件基本信息\n")
        for key, value in self.checklist["案件基本信息"].items():
            md.append(f"- **{key}**: {value}")
        md.append("\n")
        
        # 立即行动
        md.append("## 🔥 立即行动（24小时内）\n")
        immediate = sorted(self.checklist["立即行动（24小时内）"], 
                          key=lambda x: x["优先级"], reverse=True)
        for i, action in enumerate(immediate, 1):
            status = "✅" if action["是否完成"] else "⬜"
            stars = "⭐" * action["优先级"]
            md.append(f"{status} **{i}. {action['行动']}** {stars}")
            md.append(f"   - 截止时间: {action['截止时间']}")
            if action["备注"]:
                md.append(f"   - 备注: {action['备注']}")
            md.append("")
        
        # 短期行动
        md.append("## 📅 短期行动（1周内）\n")
        short = sorted(self.checklist["短期行动（1周内）"], 
                      key=lambda x: x["优先级"], reverse=True)
        for i, action in enumerate(short, 1):
            status = "✅" if action["是否完成"] else "⬜"
            stars = "⭐" * action["优先级"]
            md.append(f"{status} **{i}. {action['行动']}** {stars}")
            md.append(f"   - 截止时间: {action['截止时间']}")
            if action["备注"]:
                md.append(f"   - 备注: {action['备注']}")
            md.append("")
        
        # 中期行动
        md.append("## 📆 中期行动（1个月内）\n")
        medium = sorted(self.checklist["中期行动（1个月内）"], 
                       key=lambda x: x["优先级"], reverse=True)
        for i, action in enumerate(medium, 1):
            status = "✅" if action["是否完成"] else "⬜"
            stars = "⭐" * action["优先级"]
            md.append(f"{status} **{i}. {action['行动']}** {stars}")
            md.append(f"   - 截止时间: {action['截止时间']}")
            if action["备注"]:
                md.append(f"   - 备注: {action['备注']}")
            md.append("")
        
        # 长期行动
        md.append("## 📋 长期行动（3-6个月内）\n")
        long_term = sorted(self.checklist["长期行动（3-6个月内）"], 
                          key=lambda x: x["优先级"], reverse=True)
        for i, action in enumerate(long_term, 1):
            status = "✅" if action["是否完成"] else "⬜"
            stars = "⭐" * action["优先级"]
            md.append(f"{status} **{i}. {action['行动']}** {stars}")
            md.append(f"   - 截止时间: {action['截止时间']}")
            if action["备注"]:
                md.append(f"   - 备注: {action['备注']}")
            md.append("")
        
        # 证据清单
        md.append("## 🔍 证据清单\n")
        evidence = sorted(self.checklist["证据清单"], 
                         key=lambda x: x["重要性"], reverse=True)
        for i, ev in enumerate(evidence, 1):
            status = "✅" if ev["是否已获取"] else "⬜"
            stars = "⭐" * ev["重要性"]
            md.append(f"{status} **{i}. {ev['证据名称']}** {stars}")
            md.append(f"   - 获取难度: {ev['获取难度']}")
            md.append(f"   - 获取方式: {ev['获取方式']}")
            if ev["存放位置"]:
                md.append(f"   - 存放位置: {ev['存放位置']}")
            md.append("")
        
        # 文书清单
        md.append("## 📄 文书清单\n")
        for i, doc in enumerate(self.checklist["文书清单"], 1):
            md.append(f"**{i}. {doc['文书名称']}** [{doc['文书类型']}]")
            md.append(f"   - 状态: {doc['状态']}")
            if doc["备注"]:
                md.append(f"   - 备注: {doc['备注']}")
            md.append("")
        
        # 关键言语举动分析
        md.append("## 💬 关键言语举动分析\n")
        
        for category, speeches in self.checklist["关键言语举动分析"].items():
            if speeches:
                md.append(f"### {category}\n")
                for speech in speeches:
                    stars = "⭐" * speech["立案价值"]
                    md.append(f"- **时间**: {speech['时间']}")
                    md.append(f"  **内容**: {speech['言语内容']}")
                    md.append(f"  **分析**: {speech['专业分析']}")
                    md.append(f"  **立案价值**: {stars}")
                    md.append("")
        
        # 预谋性判断标准
        md.append("## 🎯 预谋性判断标准\n")
        for level, items in self.checklist["预谋性判断标准"].items():
            if items:
                icon = "✅" if "高度" in level else "⚠️" if "注意" in level else "❌"
                md.append(f"{icon} **{level}**:")
                for item in items:
                    md.append(f"  - {item}")
                md.append("")
        
        # 惯犯判断标准
        md.append("## 🔄 惯犯判断标准\n")
        for level, items in self.checklist["惯犯判断标准"].items():
            if items:
                icon = "✅" if "高度" in level else "⚠️" if "可能" in level else "❌"
                md.append(f"{icon} **{level}**:")
                for item in items:
                    md.append(f"  - {item}")
                md.append("")
        
        # 团伙作案判断标准
        md.append("## 👥 团伙作案判断标准\n")
        for level, items in self.checklist["团伙作案判断标准"].items():
            if items:
                icon = "✅" if "高度" in level else "⚠️" if "可能" in level else "❌"
                md.append(f"{icon} **{level}**:")
                for item in items:
                    md.append(f"  - {item}")
                md.append("")
        
        return "\n".join(md)
    
    def generate_json(self) -> str:
        """生成 JSON 格式的检查清单"""
        return json.dumps(self.checklist, ensure_ascii=False, indent=2)
    
    def save_to_file(self, filename: str, format: str = "markdown"):
        """保存到文件"""
        if format == "markdown":
            content = self.generate_markdown()
            ext = ".md"
        elif format == "json":
            content = self.generate_json()
            ext = ".json"
        else:
            raise ValueError("格式必须是 'markdown' 或 'json'")
        
        full_filename = filename + ext
        with open(full_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return full_filename


def create_sample_checklist():
    """创建示例检查清单"""
    generator = ActionChecklistGenerator()
    
    # 初始化案件信息
    generator.initialize_case_info(
        shop_name="豫园某店铺",
        location="上海豫园",
        date="2026年2月",
        amount="400余元",
        opposing_party="某女性游客"
    )
    
    # 添加立即行动
    immediate_actions = [
        ("固定完整监控录像（包括冲突前1小时）", 5, False, "防止证据丢失"),
        ("收集左右摊主的证人证言", 5, False, "侧面印证"),
        ("截图对方小红书主页的历史发帖", 4, False, "证明惯犯"),
        ("截图对方博文的编辑记录（6:47）", 4, False, "证明专业性"),
        ("准备行政复议申请书", 5, False, "核心文书"),
        ("提交行政复议申请", 5, False, "优先行动")
    ]
    for action, priority, completed, notes in immediate_actions:
        generator.add_immediate_action(action, priority, completed, notes)
    
    # 添加短期行动
    short_actions = [
        ("调取豫园入口监控录像", 4, False, "证明预谋性"),
        ("调取周边店铺监控录像", 4, False, "证明预谋性"),
        ("调取对方进入豫园后的消费记录", 3, False, "证明预谋性"),
        ("分析监控录像中的言语举动（标注时间戳）", 5, False, "核心证据"),
        ("准备民事诉讼起诉状", 4, False, "核心文书"),
        ("发布初步澄清声明", 3, False, "应对舆论")
    ]
    for action, priority, completed, notes in short_actions:
        generator.add_short_term_action(action, priority, completed, notes)
    
    # 添加中期行动
    medium_actions = [
        ("协助警方查询对方的投诉记录", 4, False, "证明惯犯"),
        ("协助警方查询对方的纠纷记录", 4, False, "证明惯犯"),
        ("联系可能的同伙受害者", 3, False, "寻找其他受害者"),
        ("准备刑事报案材料", 5, False, "核心文书"),
        ("发起民事诉讼", 5, False, "核心行动"),
        ("推动刑事立案", 4, False, "打击惯犯")
    ]
    for action, priority, completed, notes in medium_actions:
        generator.add_medium_term_action(action, priority, completed, notes)
    
    # 添加长期行动
    long_actions = [
        ("配合行政复议审理", 5, False, "3-6个月"),
        ("配合民事诉讼审理", 5, False, "6-12个月"),
        ("配合刑事侦查（如立案）", 4, False, "1-3个月"),
        ("跟进对方的历史发帖删除情况", 3, False, "持续跟进"),
        ("跟进对方的道歉和赔偿情况", 3, False, "持续跟进")
    ]
    for action, priority, completed, notes in long_actions:
        generator.add_long_term_action(action, priority, completed, notes)
    
    # 添加证据
    evidences = [
        ("完整监控录像（包括冲突前1小时）", 5, "容易", "调取店铺监控"),
        ("豫园入口监控录像", 5, "中等", "协助警方调取"),
        ("周边店铺监控录像", 4, "容易", "调取周边监控"),
        ("左右摊主的证人证言", 5, "容易", "书面证言"),
        ("对方小红书主页截图", 5, "容易", "截图保存"),
        ("对方历史发帖截图", 5, "容易", "截图保存"),
        ("对方博文编辑记录截图", 5, "容易", "截图保存"),
        ("退款记录截图", 4, "容易", "截图保存"),
        ("小红书博文传播数据截图", 4, "容易", "截图保存"),
        ("行政处罚决定书", 5, "容易", "已有"),
        ("停业通知", 5, "容易", "已有"),
        ("罚款单据", 5, "容易", "已有"),
        ("过往营业额数据", 3, "容易", "统计整理")
    ]
    for ev in evidences:
        generator.add_evidence(*ev)
    
    # 添加文书
    documents = [
        ("行政复议申请书", "行政", "未准备", "核心文书"),
        ("民事起诉状", "民事", "未准备", "核心文书"),
        ("刑事报案材料", "刑事", "未准备", "核心文书"),
        ("证人证言模板", "通用", "未准备", "辅助文书"),
        ("澄清声明模板", "舆论", "未准备", "辅助文书"),
        ("言语举动分析表", "证据", "未准备", "辅助文书"),
        ("证据清单模板", "通用", "未准备", "辅助文书")
    ]
    for doc in documents:
        generator.add_document(*doc)
    
    # 添加言语分析
    speeches_provocative = [
        ("缠斗期", "你们店就这样做生意的？", "暗示商户服务质量差", 3),
        ("缠斗期", "我看你们就是欺负外地人", "标签化攻击，制造矛盾", 4),
        ("缠斗期", "我都等你这么久了", "强调'受害者'身份", 2),
        ("交易期", "行吧，就当我倒霉", "暗示被迫交易", 3),
        ("爆破期", "你们不给赠品就退款", "制造交易障碍", 4),
        ("爆破期", "我看你们就是不想卖", "指责商户违约", 4)
    ]
    for time, content, analysis, value in speeches_provocative:
        generator.add_speech_analysis("挑衅性言语", time, content, analysis, value)
    
    speeches_evidentiary = [
        ("冲突期", "你刚才说什么？再说一遍！", "引导商户重复激烈言语", 5),
        ("冲突期", "你敢不敢再说一遍？", "进一步引导，获取更激烈言语", 5),
        ("冲突期", "大家看看，这就是这家店的态度", "制造舆论场景", 4),
        ("冲突期", "我要报警了，你们等着", "威胁，为后续投诉做铺垫", 3),
        ("冲突期", "（对着手机录像说）这家店在威胁我", "取证话术", 5)
    ]
    for time, content, analysis, value in speeches_evidentiary:
        generator.add_speech_analysis("取证性言语", time, content, analysis, value)
    
    speeches_threatening = [
        ("冲突期", "我要让你们这店开不下去", "直接威胁", 5),
        ("冲突期", "我会让大家都知道你们店的样子", "威胁曝光", 4),
        ("冲突期", "我要去投诉你们", "行政威胁", 3),
        ("冲突期", "我要发到网上去", "舆论威胁", 4),
        ("冲突期", "你们等着，不会就这么算了", "继续威胁", 4)
    ]
    for time, content, analysis, value in speeches_threatening:
        generator.add_speech_analysis("威胁性言语", time, content, analysis, value)
    
    # 添加预谋性判断标准
    generator.checklist["预谋性判断标准"]["高度可疑"] = [
        "直接从某点进入豫园，直奔本店铺（中间无逗留）",
        "进入店铺前在店外停留观察超过2分钟",
        "全程手机录像或频繁拍照",
        "未购买其他任何商品"
    ]
    generator.checklist["预谋性判断标准"]["需要注意"] = [
        "在其他店铺有短暂停留但未消费",
        "有同伴但未进入店铺"
    ]
    generator.checklist["预谋性判断标准"]["不太可能"] = [
        "随意逛了多家店铺后进入本店",
        "在其他店铺有正常消费记录"
    ]
    
    # 添加惯犯判断标准
    generator.checklist["惯犯判断标准"]["高度可能是惯犯"] = [
        "历史发帖中有3次以上类似'维权'",
        "文案结构高度相似（都有'诈骗'、'中国警察'等关键词）",
        "专门在旅游景区发生",
        "发帖时间都在早高峰（6:00-7:00）",
        "有多次行政投诉记录"
    ]
    generator.checklist["惯犯判断标准"]["可能是惯犯"] = [
        "历史发帖中有1-2次类似'维权'",
        "部分文案结构相似",
        "发帖时间在特定时段"
    ]
    generator.checklist["惯犯判断标准"]["不太可能是惯犯"] = [
        "历史发帖中无类似内容",
        "这是第一次发帖"
    ]
    
    # 添加团伙作案判断标准
    generator.checklist["团伙作案判断标准"]["高度可能是团伙"] = [
        "有同伴但未进入店铺（在外观望）",
        "冲突后有人接应",
        "行为有明确分工（一人缠斗、一人取证、一人发帖）",
        "有多个账号参与舆论攻击"
    ]
    generator.checklist["团伙作案判断标准"]["可能是团伙"] = [
        "有同伴但未明显参与",
        "行为有部分分工"
    ]
    generator.checklist["团伙作案判断标准"]["不太可能是团伙"] = [
        "独自一人"
    ]
    
    return generator


if __name__ == "__main__":
    # 创建示例检查清单
    print("正在生成行动检查清单...")
    generator = create_sample_checklist()
    
    # 保存为 Markdown 格式
    md_file = generator.save_to_file("/workspace/ai_detective/action_checklist", "markdown")
    print(f"✅ Markdown 格式已保存: {md_file}")
    
    # 保存为 JSON 格式
    json_file = generator.save_to_file("/workspace/ai_detective/action_checklist", "json")
    print(f"✅ JSON 格式已保存: {json_file}")
    
    # 显示摘要
    print("\n" + "="*60)
    print("行动检查清单生成完成！")
    print("="*60)
    print(f"立即行动项: {len(generator.checklist['立即行动（24小时内）'])} 项")
    print(f"短期行动项: {len(generator.checklist['短期行动（1周内）'])} 项")
    print(f"中期行动项: {len(generator.checklist['中期行动（1个月内）'])} 项")
    print(f"长期行动项: {len(generator.checklist['长期行动（3-6个月内）'])} 项")
    print(f"证据项: {len(generator.checklist['证据清单'])} 项")
    print(f"文书项: {len(generator.checklist['文书清单'])} 项")
    print(f"言语分析: {sum(len(v) for v in generator.checklist['关键言语举动分析'].values())} 项")
    print("="*60)
