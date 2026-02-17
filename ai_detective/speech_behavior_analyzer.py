#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职业碰瓷式维权案件 - 言语举动分析工具

用于分析监控录像中的关键言语和举动，生成时间戳分析表
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import json


class SpeechBehaviorAnalyzer:
    """言语举动分析器"""
    
    def __init__(self):
        self.speeches = []
        self.behaviors = []
        self.timeline = []
    
    def add_speech(self, time_str: str, speaker: str, content: str,
                   category: str, analysis: str, importance: int):
        """添加言语记录
        
        Args:
            time_str: 时间字符串（如 "00:05:30"）
            speaker: 说话人（对方/我方/双方）
            content: 言语内容
            category: 类别（挑衅性/取证性/威胁性/正常）
            analysis: 专业分析
            importance: 重要性（1-5，5为最高）
        """
        self.speeches.append({
            "时间": time_str,
            "说话人": speaker,
            "内容": content,
            "类别": category,
            "专业分析": analysis,
            "重要性": importance,
            "时间戳": self._parse_time(time_str)
        })
    
    def add_behavior(self, time_str: str, actor: str, action: str,
                     category: str, analysis: str, importance: int):
        """添加行为记录
        
        Args:
            time_str: 时间字符串（如 "00:05:30"）
            actor: 行为人（对方/我方/双方）
            action: 行为描述
            category: 类别（异常冷静/制造场景/时间精确/正常）
            analysis: 专业分析
            importance: 重要性（1-5，5为最高）
        """
        self.behaviors.append({
            "时间": time_str,
            "行为人": actor,
            "行为": action,
            "类别": category,
            "专业分析": analysis,
            "重要性": importance,
            "时间戳": self._parse_time(time_str)
        })
    
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
    
    def generate_timeline(self):
        """生成完整时间线"""
        self.timeline = []
        
        # 合并言语和行为
        for speech in self.speeches:
            self.timeline.append({
                "类型": "言语",
                **speech
            })
        
        for behavior in self.behaviors:
            self.timeline.append({
                "类型": "行为",
                **behavior
            })
        
        # 按时间排序
        self.timeline.sort(key=lambda x: x["时间戳"])
    
    def filter_by_category(self, category: str, item_type: str = None):
        """按类别筛选
        
        Args:
            category: 类别（如 "挑衅性"、"取证性"、"威胁性"）
            item_type: 项目类型（"言语"/"行为"/None表示全部）
        """
        results = []
        
        if item_type is None or item_type == "言语":
            for speech in self.speeches:
                if category in speech["类别"]:
                    results.append(speech)
        
        if item_type is None or item_type == "行为":
            for behavior in self.behaviors:
                if category in behavior["类别"]:
                    results.append(behavior)
        
        return sorted(results, key=lambda x: x["时间戳"])
    
    def get_high_importance_items(self, threshold: int = 4):
        """获取高重要性项目"""
        results = []
        
        for speech in self.speeches:
            if speech["重要性"] >= threshold:
                results.append(speech)
        
        for behavior in self.behaviors:
            if behavior["重要性"] >= threshold:
                results.append(behavior)
        
        return sorted(results, key=lambda x: x["时间戳"])
    
    def generate_summary(self) -> Dict[str, Any]:
        """生成统计摘要"""
        summary = {
            "言语总数": len(self.speeches),
            "行为总数": len(self.behaviors),
            "言语类别统计": {},
            "行为类别统计": {},
            "高重要性项目数": len(self.get_high_importance_items(4)),
            "对方说话次数": len([s for s in self.speeches if s["说话人"] == "对方"]),
            "我方说话次数": len([s for s in self.speeches if s["说话人"] == "我方"])
        }
        
        # 统计言语类别
        for speech in self.speeches:
            category = speech["类别"]
            summary["言语类别统计"][category] = summary["言语类别统计"].get(category, 0) + 1
        
        # 统计行为类别
        for behavior in self.behaviors:
            category = behavior["类别"]
            summary["行为类别统计"][category] = summary["行为类别统计"].get(category, 0) + 1
        
        return summary
    
    def generate_markdown(self) -> str:
        """生成 Markdown 格式的分析报告"""
        md = []
        
        # 标题
        md.append("# 言语举动分析报告\n")
        md.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 统计摘要
        summary = self.generate_summary()
        md.append("## 📊 统计摘要\n")
        md.append(f"- **言语总数**: {summary['言语总数']}")
        md.append(f"- **行为总数**: {summary['行为总数']}")
        md.append(f"- **高重要性项目**: {summary['高重要性项目数']}")
        md.append(f"- **对方说话次数**: {summary['对方说话次数']}")
        md.append(f"- **我方说话次数**: {summary['我方说话次数']}\n")
        
        # 言语类别统计
        md.append("### 言语类别统计")
        for category, count in summary["言语类别统计"].items():
            md.append(f"- **{category}**: {count} 次")
        md.append("")
        
        # 行为类别统计
        md.append("### 行为类别统计")
        for category, count in summary["行为类别统计"].items():
            md.append(f"- **{category}**: {count} 次")
        md.append("")
        
        # 高重要性项目
        md.append("## ⭐ 高重要性项目（重要性 ≥ 4）\n")
        high_importance = self.get_high_importance_items(4)
        for i, item in enumerate(high_importance, 1):
            icon = "💬" if "内容" in item else "🎬"
            stars = "⭐" * item["重要性"]
            md.append(f"{icon} **{i}. [{item['时间']}] {item.get('内容', item.get('行为', ''))}** {stars}")
            md.append(f"   - 类型: {item['类别']}")
            md.append(f"   - 专业分析: {item['专业分析']}")
            md.append("")
        
        # 按类别分类
        md.append("## 📋 按类别分类\n")
        
        # 挑衅性言语
        provocative_speeches = self.filter_by_category("挑衅性", "言语")
        if provocative_speeches:
            md.append("### 💥 挑衅性言语\n")
            for speech in provocative_speeches:
                stars = "⭐" * speech["重要性"]
                md.append(f"**[{speech['时间']}] {speech['说话人']}**: \"{speech['内容']}\" {stars}")
                md.append(f"> {speech['专业分析']}\n")
        
        # 取证性言语
        evidentiary_speeches = self.filter_by_category("取证性", "言语")
        if evidentiary_speeches:
            md.append("### 📸 取证性言语\n")
            for speech in evidentiary_speeches:
                stars = "⭐" * speech["重要性"]
                md.append(f"**[{speech['时间']}] {speech['说话人']}**: \"{speech['内容']}\" {stars}")
                md.append(f"> {speech['专业分析']}\n")
        
        # 威胁性言语
        threatening_speeches = self.filter_by_category("威胁性", "言语")
        if threatening_speeches:
            md.append("### ⚠️ 威胁性言语\n")
            for speech in threatening_speeches:
                stars = "⭐" * speech["重要性"]
                md.append(f"**[{speech['时间']}] {speech['说话人']}**: \"{speech['内容']}\" {stars}")
                md.append(f"> {speech['专业分析']}\n")
        
        # 异常冷静行为
        calm_behaviors = self.filter_by_category("异常冷静", "行为")
        if calm_behaviors:
            md.append("### 😶 异常冷静行为\n")
            for behavior in calm_behaviors:
                stars = "⭐" * behavior["重要性"]
                md.append(f"**[{behavior['时间']}] {behavior['行为人']}**: {behavior['行为']} {stars}")
                md.append(f"> {behavior['专业分析']}\n")
        
        # 制造场景行为
        scene_behaviors = self.filter_by_category("制造场景", "行为")
        if scene_behaviors:
            md.append("### 🎭 制造场景行为\n")
            for behavior in scene_behaviors:
                stars = "⭐" * behavior["重要性"]
                md.append(f"**[{behavior['时间']}] {behavior['行为人']}**: {behavior['行为']} {stars}")
                md.append(f"> {behavior['专业分析']}\n")
        
        # 时间精确行为
        time_behaviors = self.filter_by_category("时间精确", "行为")
        if time_behaviors:
            md.append("### ⏰ 时间精确行为\n")
            for behavior in time_behaviors:
                stars = "⭐" * behavior["重要性"]
                md.append(f"**[{behavior['时间']}] {behavior['行为人']}**: {behavior['行为']} {stars}")
                md.append(f"> {behavior['专业分析']}\n")
        
        # 完整时间线
        md.append("## 📅 完整时间线\n")
        self.generate_timeline()
        for i, item in enumerate(self.timeline, 1):
            icon = "💬" if item["类型"] == "言语" else "🎬"
            content = item.get("内容", item.get("行为", ""))
            speaker = item.get("说话人", item.get("行为人", ""))
            md.append(f"{icon} **{i}. [{item['时间']}] {speaker}**: {content}")
            md.append(f"   - 类别: {item['类别']}")
            md.append(f"   - 重要性: {'⭐' * item['重要性']}")
            md.append("")
        
        return "\n".join(md)
    
    def generate_json(self) -> str:
        """生成 JSON 格式的分析报告"""
        data = {
            "生成时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "统计摘要": self.generate_summary(),
            "言语记录": self.speeches,
            "行为记录": self.behaviors,
            "完整时间线": self.timeline
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
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


def create_sample_analysis():
    """创建示例分析"""
    analyzer = SpeechBehaviorAnalyzer()
    
    # 添加言语记录（模拟职业碰瓷案例）
    speeches = [
        # 缠斗期（0-60分钟）
        ("00:05:00", "对方", "你们店就这样做生意的？", "挑衅性", "暗示商户服务质量差", 3),
        ("00:10:00", "对方", "我看你们就是欺负外地人", "挑衅性", "标签化攻击，制造矛盾", 4),
        ("00:20:00", "对方", "我都等你这么久了", "挑衅性", "强调'受害者'身份", 2),
        ("00:45:00", "对方", "能不能便宜点？", "正常", "正常议价", 1),
        ("01:00:00", "对方", "行吧，就当我倒霉", "挑衅性", "暗示被迫交易", 3),
        
        # 爆破期（交易后即刻）
        ("01:05:00", "对方", "你们不给赠品就退款", "挑衅性", "制造交易障碍", 4),
        ("01:06:00", "对方", "我看你们就是不想卖", "挑衅性", "指责商户违约", 4),
        
        # 冲突期（商户爆发时）
        ("01:10:00", "对方", "你刚才说什么？再说一遍！", "取证性", "引导商户重复激烈言语", 5),
        ("01:10:30", "对方", "你敢不敢再说一遍？", "取证性", "进一步引导，获取更激烈言语", 5),
        ("01:11:00", "对方", "大家看看，这就是这家店的态度", "取证性", "制造舆论场景", 4),
        ("01:12:00", "对方", "我要报警了，你们等着", "威胁性", "威胁，为后续投诉做铺垫", 3),
        ("01:13:00", "对方", "（对着手机录像说）这家店在威胁我", "取证性", "取证话术", 5),
        ("01:15:00", "对方", "我要让你们这店开不下去", "威胁性", "直接威胁", 5),
        ("01:16:00", "对方", "我会让大家都知道你们店的样子", "威胁性", "威胁曝光", 4),
        ("01:17:00", "对方", "我要去投诉你们", "威胁性", "行政威胁", 3),
        ("01:18:00", "对方", "我要发到网上去", "威胁性", "舆论威胁", 4),
        ("01:19:00", "对方", "你们等着，不会就这么算了", "威胁性", "继续威胁", 4)
    ]
    
    for time_str, speaker, content, category, analysis, importance in speeches:
        analyzer.add_speech(time_str, speaker, content, category, analysis, importance)
    
    # 添加行为记录
    behaviors = [
        # 缠斗期（0-60分钟）
        ("00:03:00", "对方", "站在店铺门口不动", "制造场景", "制造'店大欺客'视觉假象", 4),
        ("00:05:00", "对方", "拿出手机开始录像", "异常冷静", "职业取证习惯", 4),
        ("00:10:00", "对方", "频繁拍照", "异常冷静", "全程取证", 4),
        ("00:15:00", "对方", "阻碍其他顾客进入店铺", "制造场景", "扩大冲突影响范围", 5),
        ("00:30:00", "对方", "反复试用商品", "正常", "正常消费行为", 1),
        
        # 冲突期
        ("01:08:00", "对方", "原地拍照", "异常冷静", "正常反应是逃跑或惊慌，而不是取证", 5),
        ("01:09:00", "对方", "冷静截图", "异常冷静", "极度符合受过训练的特征", 5),
        ("01:11:00", "对方", "大声说话吸引注意", "制造场景", "制造围观者", 4),
        ("01:12:00", "对方", "现场报警", "异常冷静", "不是在求助，而是在执行预案", 5),
        ("01:13:00", "对方", "对着手机哭诉", "制造场景", "强化'女性弱势受害者'人设", 4),
        ("01:14:00", "对方", "不逃跑", "异常冷静", "等待商户'凶狠'画面", 4),
        ("01:15:00", "对方", "对着手机说'我好害怕'", "制造场景", "表演技艺", 4),
        
        # 次日清晨
        ("06:47:00", "对方", "发布小红书博文", "时间精确", "社交媒体算法推荐的'黄金早高峰'", 5)
    ]
    
    for time_str, actor, action, category, analysis, importance in behaviors:
        analyzer.add_behavior(time_str, actor, action, category, analysis, importance)
    
    return analyzer


if __name__ == "__main__":
    # 创建示例分析
    print("正在生成言语举动分析...")
    analyzer = create_sample_analysis()
    
    # 保存为 Markdown 格式
    md_file = analyzer.save_to_file("/workspace/ai_detective/speech_behavior_analysis", "markdown")
    print(f"✅ Markdown 格式已保存: {md_file}")
    
    # 保存为 JSON 格式
    json_file = analyzer.save_to_file("/workspace/ai_detective/speech_behavior_analysis", "json")
    print(f"✅ JSON 格式已保存: {json_file}")
    
    # 显示摘要
    summary = analyzer.generate_summary()
    print("\n" + "="*60)
    print("言语举动分析生成完成！")
    print("="*60)
    print(f"言语总数: {summary['言语总数']}")
    print(f"行为总数: {summary['行为总数']}")
    print(f"高重要性项目: {summary['高重要性项目数']}")
    print(f"对方说话次数: {summary['对方说话次数']}")
    print(f"我方说话次数: {summary['我方说话次数']}")
    print(f"\n言语类别统计:")
    for category, count in summary["言语类别统计"].items():
        print(f"  - {category}: {count} 次")
    print(f"\n行为类别统计:")
    for category, count in summary["行为类别统计"].items():
        print(f"  - {category}: {count} 次")
    print("="*60)
