#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职业碰瓷式维权案件 - 案件管理系统

整合所有功能：
1. 行动检查清单生成
2. 言语举动分析
3. 证据管理
4. 文书管理
5. 进度跟踪
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class VictimCaseManager:
    """职业碰瓷案件管理器"""
    
    def __init__(self, case_id: str = None):
        self.case_id = case_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.case_info = {}
        self.checklist = []
        self.evidence = []
        self.documents = []
        self.timeline = []
        self.notes = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def set_case_info(self, shop_name: str, location: str, date: str,
                     amount: str, opposing_party: str, description: str = ""):
        """设置案件基本信息"""
        self.case_info = {
            "店铺名称": shop_name,
            "发生地点": location,
            "发生时间": date,
            "涉及金额": amount,
            "对方身份": opposing_party,
            "案件描述": description,
            "创建时间": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        self._mark_updated()
    
    def add_checklist_item(self, action: str, category: str, priority: int,
                           deadline: str = "", completed: bool = False,
                           notes: str = ""):
        """添加检查清单项"""
        self.checklist.append({
            "行动": action,
            "类别": category,  # 立即/短期/中期/长期
            "优先级": priority,  # 1-5
            "截止时间": deadline,
            "是否完成": completed,
            "备注": notes,
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._mark_updated()
    
    def add_evidence(self, name: str, category: str, importance: int,
                     difficulty: str, how_to_obtain: str,
                     obtained: bool = False, location: str = "",
                     notes: str = ""):
        """添加证据"""
        self.evidence.append({
            "证据名称": name,
            "类别": category,
            "重要性": importance,  # 1-5
            "获取难度": difficulty,
            "获取方式": how_to_obtain,
            "是否已获取": obtained,
            "存放位置": location,
            "备注": notes,
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._mark_updated()
    
    def add_document(self, name: str, category: str, status: str = "未准备",
                     notes: str = ""):
        """添加文书"""
        self.documents.append({
            "文书名称": name,
            "类别": category,  # 行政/民事/刑事
            "状态": status,  # 未准备/准备中/已完成
            "备注": notes,
            "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._mark_updated()
    
    def add_timeline_event(self, time_str: str, event_type: str, 
                           description: str, category: str = "",
                           importance: int = 3, notes: str = ""):
        """添加时间线事件"""
        self.timeline.append({
            "时间": time_str,
            "类型": event_type,  # 言语/行为/事件
            "描述": description,
            "类别": category,
            "重要性": importance,
            "备注": notes
        })
        self.timeline.sort(key=lambda x: self._parse_time(x["时间"]))
        self._mark_updated()
    
    def add_note(self, note: str, category: str = "通用"):
        """添加笔记"""
        self.notes.append({
            "内容": note,
            "类别": category,
            "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._mark_updated()
    
    def _parse_time(self, time_str: str) -> int:
        """解析时间字符串为秒数"""
        try:
            parts = time_str.split(':')
            if len(parts) == 3:
                h, m, s = map(int, parts)
                return h * 3600 + m * 60 + s
            elif len(parts) == 2:
                m, s = map(int, parts)
                return m * 60 + s
            else:
                return 0
        except:
            return 0
    
    def _mark_updated(self):
        """标记更新时间"""
        self.updated_at = datetime.now()
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """获取进度摘要"""
        total_items = len(self.checklist)
        completed_items = sum(1 for item in self.checklist if item["是否完成"])
        
        total_evidence = len(self.evidence)
        obtained_evidence = sum(1 for ev in self.evidence if ev["是否已获取"])
        
        total_documents = len(self.documents)
        completed_documents = sum(1 for doc in self.documents if doc["状态"] == "已完成")
        
        return {
            "检查清单进度": {
                "总项数": total_items,
                "已完成": completed_items,
                "完成率": f"{completed_items/total_items*100:.1f}%" if total_items > 0 else "0%"
            },
            "证据收集进度": {
                "总项数": total_evidence,
                "已获取": obtained_evidence,
                "获取率": f"{obtained_evidence/total_evidence*100:.1f}%" if total_evidence > 0 else "0%"
            },
            "文书准备进度": {
                "总项数": total_documents,
                "已完成": completed_documents,
                "完成率": f"{completed_documents/total_documents*100:.1f}%" if total_documents > 0 else "0%"
            },
            "更新时间": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_urgent_items(self, days: int = 1) -> List[Dict]:
        """获取紧急项目（即将到期）"""
        today = datetime.now()
        deadline = today + timedelta(days=days)
        urgent_items = []
        
        for item in self.checklist:
            if not item["是否完成"] and item["截止时间"]:
                try:
                    item_deadline = datetime.strptime(item["截止时间"], "%Y-%m-%d")
                    if item_deadline <= deadline:
                        urgent_items.append(item)
                except:
                    pass
        
        return sorted(urgent_items, key=lambda x: x["截止时间"])
    
    def get_high_importance_items(self, threshold: int = 4, 
                                   item_type: str = "all") -> List[Dict]:
        """获取高重要性项目"""
        items = []
        
        if item_type in ["all", "checklist"]:
            for item in self.checklist:
                if item["优先级"] >= threshold:
                    items.append({**item, "类型": "检查清单"})
        
        if item_type in ["all", "evidence"]:
            for ev in self.evidence:
                if ev["重要性"] >= threshold:
                    items.append({**ev, "类型": "证据"})
        
        if item_type in ["all", "timeline"]:
            for ev in self.timeline:
                if ev["重要性"] >= threshold:
                    items.append({**ev, "类型": "时间线"})
        
        return sorted(items, key=lambda x: x.get("重要性", 0), reverse=True)
    
    def generate_report(self) -> str:
        """生成完整报告"""
        md = []
        
        # 标题
        md.append("# 职业碰瓷式维权案件 - 案件管理报告\n")
        md.append(f"**案件ID**: {self.case_id}\n")
        
        # 案件基本信息
        md.append("## 📌 案件基本信息\n")
        for key, value in self.case_info.items():
            md.append(f"- **{key}**: {value}")
        md.append("")
        
        # 进度摘要
        summary = self.get_progress_summary()
        md.append("## 📊 进度摘要\n")
        md.append(f"**更新时间**: {summary['更新时间']}\n")
        
        md.append("### 检查清单进度")
        md.append(f"- 总项数: {summary['检查清单进度']['总项数']}")
        md.append(f"- 已完成: {summary['检查清单进度']['已完成']}")
        md.append(f"- 完成率: {summary['检查清单进度']['完成率']}\n")
        
        md.append("### 证据收集进度")
        md.append(f"- 总项数: {summary['证据收集进度']['总项数']}")
        md.append(f"- 已获取: {summary['证据收集进度']['已获取']}")
        md.append(f"- 获取率: {summary['证据收集进度']['获取率']}\n")
        
        md.append("### 文书准备进度")
        md.append(f"- 总项数: {summary['文书准备进度']['总项数']}")
        md.append(f"- 已完成: {summary['文书准备进度']['已完成']}")
        md.append(f"- 完成率: {summary['文书准备进度']['完成率']}\n")
        
        # 紧急项目
        urgent = self.get_urgent_items(1)
        if urgent:
            md.append("## 🚨 紧急项目（即将到期）\n")
            for i, item in enumerate(urgent, 1):
                md.append(f"### {i}. {item['行动']}")
                md.append(f"- 截止时间: {item['截止时间']}")
                md.append(f"- 优先级: {'⭐' * item['优先级']}")
                if item["备注"]:
                    md.append(f"- 备注: {item['备注']}")
                md.append("")
        
        # 高重要性项目
        high_importance = self.get_high_importance_items(4, "all")
        if high_importance:
            md.append("## ⭐ 高重要性项目（重要性 ≥ 4）\n")
            for i, item in enumerate(high_importance, 1):
                item_type = item.get("类型", "")
                stars = "⭐" * item.get("重要性", item.get("优先级", 0))
                
                if item_type == "检查清单":
                    md.append(f"### {i}. {item['行动']} [{item_type}] {stars}")
                elif item_type == "证据":
                    md.append(f"### {i}. {item['证据名称']} [{item_type}] {stars}")
                elif item_type == "时间线":
                    md.append(f"### {i}. [{item['时间']}] {item['描述']} [{item_type}] {stars}")
                
                md.append("")
        
        # 检查清单
        if self.checklist:
            md.append("## 📋 检查清单\n")
            categories = ["立即", "短期", "中期", "长期"]
            for category in categories:
                items = [item for item in self.checklist if category in item["类别"]]
                if items:
                    md.append(f"### {category}行动\n")
                    sorted_items = sorted(items, key=lambda x: x["优先级"], reverse=True)
                    for i, item in enumerate(sorted_items, 1):
                        status = "✅" if item["是否完成"] else "⬜"
                        stars = "⭐" * item["优先级"]
                        md.append(f"{status} **{i}. {item['行动']}** {stars}")
                        if item["截止时间"]:
                            md.append(f"   - 截止时间: {item['截止时间']}")
                        if item["备注"]:
                            md.append(f"   - 备注: {item['备注']}")
                        md.append("")
        
        # 证据清单
        if self.evidence:
            md.append("## 🔍 证据清单\n")
            sorted_evidence = sorted(self.evidence, key=lambda x: x["重要性"], reverse=True)
            for i, ev in enumerate(sorted_evidence, 1):
                status = "✅" if ev["是否已获取"] else "⬜"
                stars = "⭐" * ev["重要性"]
                md.append(f"{status} **{i}. {ev['证据名称']}** {stars}")
                md.append(f"   - 类别: {ev['类别']}")
                md.append(f"   - 获取难度: {ev['获取难度']}")
                md.append(f"   - 获取方式: {ev['获取方式']}")
                if ev["存放位置"]:
                    md.append(f"   - 存放位置: {ev['存放位置']}")
                if ev["备注"]:
                    md.append(f"   - 备注: {ev['备注']}")
                md.append("")
        
        # 文书清单
        if self.documents:
            md.append("## 📄 文书清单\n")
            for i, doc in enumerate(self.documents, 1):
                status_icon = "✅" if doc["状态"] == "已完成" else "🔄" if doc["状态"] == "准备中" else "⬜"
                md.append(f"{status_icon} **{i}. {doc['文书名称']}** [{doc['类别']}]")
                md.append(f"   - 状态: {doc['状态']}")
                if doc["备注"]:
                    md.append(f"   - 备注: {doc['备注']}")
                md.append("")
        
        # 时间线
        if self.timeline:
            md.append("## 📅 时间线\n")
            for i, event in enumerate(self.timeline, 1):
                icon = "💬" if event["类型"] == "言语" else "🎬" if event["类型"] == "行为" else "📌"
                stars = "⭐" * event["重要性"]
                md.append(f"{icon} **{i}. [{event['时间']}] {event['描述']}** {stars}")
                md.append(f"   - 类型: {event['类型']}")
                if event["类别"]:
                    md.append(f"   - 类别: {event['类别']}")
                if event["备注"]:
                    md.append(f"   - 备注: {event['备注']}")
                md.append("")
        
        # 笔记
        if self.notes:
            md.append("## 📝 笔记\n")
            for i, note in enumerate(self.notes, 1):
                md.append(f"### {i}. {note['类别']} - {note['时间']}\n")
                md.append(f"{note['内容']}\n")
        
        # 页脚
        md.append("---")
        md.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"**案件创建时间**: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"**最后更新时间**: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(md)
    
    def save_to_file(self, directory: str = ""):
        """保存到文件"""
        if not directory:
            directory = "/workspace/ai_detective/cases"
        
        # 创建目录
        os.makedirs(directory, exist_ok=True)
        
        # 保存 JSON
        json_file = os.path.join(directory, f"case_{self.case_id}.json")
        data = {
            "case_id": self.case_id,
            "case_info": self.case_info,
            "checklist": self.checklist,
            "evidence": self.evidence,
            "documents": self.documents,
            "timeline": self.timeline,
            "notes": self.notes,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 保存 Markdown 报告
        md_file = os.path.join(directory, f"case_{self.case_id}.md")
        report = self.generate_report()
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return json_file, md_file


def create_sample_case():
    """创建示例案件"""
    manager = VictimCaseManager()
    
    # 设置案件信息
    manager.set_case_info(
        shop_name="豫园某店铺",
        location="上海豫园",
        date="2026年2月17日",
        amount="400余元",
        opposing_party="某女性游客",
        description="职业碰瓷式维权案件，对方通过软暴力诱发冲突，利用舆论绑架行政决策。"
    )
    
    # 添加检查清单项
    immediate_actions = [
        ("固定完整监控录像（包括冲突前1小时）", "立即行动（24小时内）", 5, 
         (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"), False, "防止证据丢失"),
        ("收集左右摊主的证人证言", "立即行动（24小时内）", 5,
         (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"), False, "侧面印证"),
        ("截图对方小红书主页的历史发帖", "立即行动（24小时内）", 4,
         (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"), False, "证明惯犯"),
        ("准备行政复议申请书", "立即行动（24小时内）", 5,
         (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"), False, "核心文书"),
        ("提交行政复议申请", "立即行动（24小时内）", 5,
         (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"), False, "优先行动")
    ]
    
    for action, category, priority, deadline, completed, notes in immediate_actions:
        manager.add_checklist_item(action, category, priority, deadline, completed, notes)
    
    # 添加证据
    evidences = [
        ("完整监控录像（包括冲突前1小时）", "预谋性", 5, "容易", "调取店铺监控", False, ""),
        ("豫园入口监控录像", "预谋性", 5, "中等", "协助警方调取", False, ""),
        ("左右摊主的证人证言", "侧面印证", 5, "容易", "书面证言", False, ""),
        ("对方小红书主页截图", "惯犯", 5, "容易", "截图保存", False, ""),
        ("对方历史发帖截图", "惯犯", 5, "容易", "截图保存", False, ""),
        ("退款记录截图", "反驳指控", 4, "容易", "截图保存", False, "")
    ]
    
    for ev in evidences:
        manager.add_evidence(*ev)
    
    # 添加文书
    documents = [
        ("行政复议申请书", "行政", "未准备", "核心文书"),
        ("民事起诉状", "民事", "未准备", "核心文书"),
        ("刑事报案材料", "刑事", "未准备", "核心文书"),
        ("证人证言模板", "通用", "未准备", "辅助文书")
    ]
    
    for doc in documents:
        manager.add_document(*doc)
    
    # 添加时间线事件
    timeline_events = [
        ("00:05:00", "言语", "对方说：你们店就这样做生意的？", "挑衅性", 3, "暗示商户服务质量差"),
        ("00:10:00", "言语", "对方说：我看你们就是欺负外地人", "挑衅性", 4, "标签化攻击"),
        ("01:05:00", "言语", "对方说：你们不给赠品就退款", "挑衅性", 4, "制造交易障碍"),
        ("01:10:00", "言语", "对方说：你刚才说什么？再说一遍！", "取证性", 5, "引导商户重复"),
        ("01:13:00", "行为", "对方对着手机录像说：这家店在威胁我", "取证性", 5, "取证话术"),
        ("01:15:00", "言语", "对方说：我要让你们这店开不下去", "威胁性", 5, "直接威胁"),
        ("06:47:00", "行为", "对方发布小红书博文", "时间精确", 5, "黄金早高峰发帖")
    ]
    
    for time_str, event_type, description, category, importance, notes in timeline_events:
        manager.add_timeline_event(time_str, event_type, description, category, importance, notes)
    
    # 添加笔记
    notes = [
        ("对方行为具有明显的预谋性，需要调查其行动路线。", "关键发现"),
        ("对方可能在其他地方也有类似行为，需要调查其历史发帖。", "调查方向"),
        ("建议优先处理行政复议，这是最快的维权途径。", "策略建议")
    ]
    
    for note, category in notes:
        manager.add_note(note, category)
    
    return manager


if __name__ == "__main__":
    # 创建示例案件
    print("正在创建示例案件...")
    manager = create_sample_case()
    
    # 保存到文件
    json_file, md_file = manager.save_to_file()
    print(f"✅ JSON 格式已保存: {json_file}")
    print(f"✅ Markdown 报告已保存: {md_file}")
    
    # 显示摘要
    summary = manager.get_progress_summary()
    print("\n" + "="*60)
    print("案件管理报告生成完成！")
    print("="*60)
    print(f"案件ID: {manager.case_id}")
    print(f"\n进度摘要:")
    print(f"检查清单: {summary['检查清单进度']['已完成']}/{summary['检查清单进度']['总项数']} ({summary['检查清单进度']['完成率']})")
    print(f"证据收集: {summary['证据收集进度']['已获取']}/{summary['证据收集进度']['总项数']} ({summary['证据收集进度']['获取率']})")
    print(f"文书准备: {summary['文书准备进度']['已完成']}/{summary['文书准备进度']['总项数']} ({summary['文书准备进度']['完成率']})")
    
    # 显示紧急项目
    urgent = manager.get_urgent_items(1)
    if urgent:
        print(f"\n🚨 紧急项目（{len(urgent)}项）:")
        for item in urgent:
            print(f"  - {item['行动']} (截止: {item['截止时间']})")
    
    # 显示高重要性项目
    high_importance = manager.get_high_importance_items(4, "all")
    print(f"\n⭐ 高重要性项目（{len(high_importance)}项）:")
    for item in high_importance[:5]:  # 只显示前5个
        item_type = item.get("类型", "")
        if item_type == "检查清单":
            print(f"  - {item['行动']} [{item_type}]")
        elif item_type == "证据":
            print(f"  - {item['证据名称']} [{item_type}]")
        elif item_type == "时间线":
            print(f"  - [{item['时间']}] {item['描述']} [{item_type}]")
    
    print("="*60)
