"""
法律推理模块
Legal Reasoner Module
基于法律条文和逻辑推理的纠纷分析引擎
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import re


@dataclass
class Fact:
    """事实要素"""
    id: str
    description: str
    category: str  # "time", "location", "person", "action", "result", "amount"
    confidence: float = 1.0
    source: str = "user_input"


@dataclass
class LegalRelation:
    """法律关系"""
    type: str  # "contract", "tort", "property", "personality", "family"
    parties: List[str]
    subject: str
    content: str
    relevant_laws: List[str] = field(default_factory=list)


@dataclass
class Liability:
    """法律责任"""
    liable_party: str
    liability_type: str  # "civil", "criminal", "administrative"
    basis: str
    severity: str  # "minor", "moderate", "serious"
    damages: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LegalAnalysis:
    """法律分析结果"""
    facts: List[Fact]
    legal_relations: List[LegalRelation]
    applicable_laws: List[Dict[str, str]]
    liability: Optional[Liability]
    risk_assessment: Dict[str, Any]
    suggestions: List[str]
    confidence: float
    created_at: datetime = field(default_factory=datetime.now)


class LegalReasoner:
    """法律推理引擎"""

    def __init__(self):
        # 加载法律知识库（简化版）
        self.law_database = self._load_law_database()
        self.case_patterns = self._load_case_patterns()

    def _load_law_database(self) -> Dict[str, Any]:
        """加载法律数据库"""
        return {
            "民法典": {
                "人格权编": {
                    "第990条": {
                        "content": "人格权是民事主体享有的生命权、身体权、健康权、姓名权、名称权、肖像权、名誉权、荣誉权、隐私权等权利。",
                        "keywords": ["人格权", "生命权", "身体权", "健康权", "姓名权", "肖像权", "名誉权", "荣誉权", "隐私权"]
                    },
                    "第1019条": {
                        "content": "未经肖像权人同意，不得制作、使用、公开肖像权人的肖像，但是法律另有规定的除外。",
                        "keywords": ["肖像权", "肖像", "未经同意", "制作", "使用", "公开"]
                    }
                },
                "合同编": {
                    "第509条": {
                        "content": "当事人应当按照约定全面履行自己的义务。",
                        "keywords": ["合同", "履行", "义务", "约定"]
                    },
                    "第577条": {
                        "content": "当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。",
                        "keywords": ["违约", "不履行", "赔偿", "违约责任"]
                    }
                },
                "侵权责任编": {
                    "第1165条": {
                        "content": "行为人因过错侵害他人民事权益造成损害的，应当承担侵权责任。",
                        "keywords": ["侵权", "过错", "损害", "侵权责任"]
                    },
                    "第1179条": {
                        "content": "侵害他人造成人身损害的，应当赔偿医疗费、护理费、交通费、营养费、住院伙食补助费等为治疗和康复支出的合理费用。",
                        "keywords": ["人身损害", "赔偿", "医疗费", "护理费", "交通费", "营养费"]
                    }
                }
            }
        }

    def _load_case_patterns(self) -> Dict[str, Any]:
        """加载案例模式库"""
        return {
            "肖像权侵权": {
                "keywords": ["照片", "肖像", "未同意", "公开", "使用", "商用"],
                "typical_claims": ["停止侵害", "赔礼道歉", "赔偿损失"],
                "evidence_needed": ["照片使用证据", "肖像权证明", "损失证明"]
            },
            "合同违约": {
                "keywords": ["合同", "违约", "未履行", "不支付", "不交付"],
                "typical_claims": ["继续履行", "违约金", "赔偿损失"],
                "evidence_needed": ["合同原件", "履约证据", "违约证据", "损失证明"]
            },
            "人身损害": {
                "keywords": ["受伤", "医疗", "住院", "误工", "残疾"],
                "typical_claims": ["医疗费", "误工费", "护理费", "精神损害赔偿"],
                "evidence_needed": ["医疗记录", "费用票据", "误工证明", "伤情鉴定"]
            },
            "房屋租赁": {
                "keywords": ["租房", "房租", "押金", "违约", "退房"],
                "typical_claims": ["退还押金", "支付违约金", "赔偿损失"],
                "evidence_needed": ["租赁合同", "付款记录", "违约证据", "损失证明"]
            }
        }

    def extract_facts(self, description: str) -> List[Fact]:
        """提取事实要素"""
        facts = []
        fact_id = 1

        # 提取时间
        time_patterns = [
            r'(\d{4}年\d{1,2}月\d{1,2}日)',
            r'(\d{4}-\d{1,2}-\d{1,2})',
            r'(\d{1,2}月\d{1,2}日)',
            r'(今天|昨天|前天|本月|上月|今年|去年)'
        ]
        for pattern in time_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                facts.append(Fact(
                    id=f"fact_{fact_id}",
                    description=f"时间：{match}",
                    category="time",
                    confidence=0.9
                ))
                fact_id += 1

        # 提取地点
        location_patterns = [
            r'(\S+市\S+区)',
            r'(\S+省\S+市)',
            r'(\S+小区)',
            r'(\S+街道\S+号)'
        ]
        for pattern in location_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                facts.append(Fact(
                    id=f"fact_{fact_id}",
                    description=f"地点：{match}",
                    category="location",
                    confidence=0.85
                ))
                fact_id += 1

        # 提取人物（简化处理）
        person_patterns = []  # 简化处理，不使用复杂正则

        # 简化处理：使用常见姓氏进行匹配
        common_surnames = ["张", "李", "王", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
        for surname in common_surnames:
            if surname in description:
                # 查找包含姓氏的称呼
                patterns = [
                    f'{surname}阿姨',
                    f'{surname}先生',
                    f'{surname}女士',
                    f'{surname}姐',
                    f'{surname}哥'
                ]
                for pattern in patterns:
                    if pattern in description:
                        facts.append(Fact(
                            id=f"fact_{fact_id}",
                            description=f"人物：{pattern}",
                            category="person",
                            confidence=0.7
                        ))
                        fact_id += 1

        # 提取金额
        amount_patterns = [
            r'(\d+(?:\.\d+)?)\s*(元|万|千|百|万块|千块)',
            r'(\d+(?:\.\d+)?)\s*(人民币|钱)'
        ]
        for pattern in amount_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                facts.append(Fact(
                    id=f"fact_{fact_id}",
                    description=f"金额：{match[0]}{match[1]}",
                    category="amount",
                    confidence=0.95
                ))
                fact_id += 1

        # 提取行为和结果（简化版）
        action_patterns = [
            "未履行", "不支付", "不退还", "未经同意", "擅自",
            "拒绝", "延迟", "违反", "侵害", "损坏"
        ]
        for action in action_patterns:
            if action in description:
                # 提取上下文
                idx = description.find(action)
                context_start = max(0, idx - 20)
                context_end = min(len(description), idx + 30)
                context = description[context_start:context_end].strip()
                facts.append(Fact(
                    id=f"fact_{fact_id}",
                    description=f"行为：{context}",
                    category="action",
                    confidence=0.9
                ))
                fact_id += 1

        return facts

    def identify_case_type(self, facts: List[Fact], description: str) -> str:
        """识别案件类型"""
        description_lower = description.lower()

        # 匹配案件模式
        for case_type, pattern in self.case_patterns.items():
            match_count = 0
            for keyword in pattern["keywords"]:
                if keyword in description_lower:
                    match_count += 1

            if match_count >= 2:
                return case_type

        # 如果没有明确匹配，尝试推断
        if any("合同" in f.description for f in facts):
            return "合同纠纷"
        elif any("侵权" in f.description or "侵害" in f.description for f in facts):
            return "侵权责任"
        elif any("肖像" in f.description or "照片" in f.description for f in facts):
            return "肖像权侵权"
        elif any("租房" in f.description or "房租" in f.description for f in facts):
            return "房屋租赁"
        else:
            return "民事纠纷"

    def match_laws(self, case_type: str, description: str) -> List[Dict[str, str]]:
        """匹配适用法律"""
        matched_laws = []

        for law_name, law_content in self.law_database.items():
            for category_name, category_content in law_content.items():
                for article_num, article in category_content.items():
                    # 检查关键词匹配
                    keywords = article["keywords"]
                    match_count = sum(1 for kw in keywords if kw in description)

                    if match_count >= 1:
                        matched_laws.append({
                            "law": law_name,
                            "category": category_name,
                            "article": article_num,
                            "content": article["content"],
                            "relevance": match_count / len(keywords)
                        })

        # 按相关性排序
        matched_laws.sort(key=lambda x: x["relevance"], reverse=True)

        return matched_laws[:5]  # 返回最相关的5条

    def determine_liability(self, facts: List[Fact], case_type: str,
                           applicable_laws: List[Dict[str, str]]) -> Liability:
        """认定法律责任"""
        # 简化版：基于案件类型和法律匹配度推断

        liable_party = "待认定"
        liability_type = "民事责任"
        basis = ""
        severity = "moderate"

        if case_type == "肖像权侵权":
            liable_party = "肖像使用方"
            liability_type = "民事责任"
            basis = "未经肖像权人同意制作、使用、公开肖像"
            severity = "moderate"
        elif case_type == "合同违约":
            liable_party = "违约方"
            liability_type = "民事责任"
            basis = "未按照约定履行合同义务"
            severity = "moderate"
        elif case_type == "人身损害":
            liable_party = "加害方"
            liability_type = "民事责任"
            basis = "侵害他人造成人身损害"
            severity = "serious"

        # 估算赔偿
        damages = {"type": "待评估"}
        amount_facts = [f for f in facts if f.category == "amount"]
        if amount_facts:
            damages = {
                "type": "经济损失",
                "estimated_amount": amount_facts[0].description.split("：")[1],
                "evidence_level": "中等"
            }

        return Liability(
            liable_party=liable_party,
            liability_type=liability_type,
            basis=basis,
            severity=severity,
            damages=damages
        )

    def assess_risk(self, liability: Liability, applicable_laws: List[Dict[str, str]]) -> Dict[str, Any]:
        """评估风险"""
        return {
            "success_probability": "70%",  # 简化值
            "time_cost": "3-6个月",
            "economic_cost": "中等",
            "complexity": liability.severity,
            "evidence_requirement": "需要提供相关证据材料",
            "key_factors": [
                "证据链完整性",
                "法律责任认定清晰度",
                "对方配合程度",
                "损失可量化程度"
            ]
        }

    def generate_suggestions(self, case_type: str, facts: List[Fact],
                             liability: Liability) -> List[str]:
        """生成建议"""
        suggestions = []

        # 证据收集建议
        if case_type in self.case_patterns:
            pattern = self.case_patterns[case_type]
            suggestions.append("【证据收集】")
            for evidence in pattern["evidence_needed"]:
                suggestions.append(f"  • {evidence}")

        # 诉讼建议
        suggestions.append("\n【诉讼建议】")
        if liability.severity == "minor":
            suggestions.append("  • 建议先尝试协商解决")
            suggestions.append("  • 如协商不成，可向法院起诉")
        else:
            suggestions.append("  • 建议尽快咨询专业律师")
            suggestions.append("  • 准备充分的证据材料")
            suggestions.append("  • 评估诉讼成本与预期收益")

        # 时效提醒
        suggestions.append("\n【时效提醒】")
        if case_type == "合同违约":
            suggestions.append("  • 诉讼时效：3年")
        elif case_type == "人身损害":
            suggestions.append("  • 诉讼时效：3年")
        else:
            suggestions.append("  • 一般民事诉讼时效：3年")

        return suggestions

    def analyze(self, description: str, context: Optional[Dict[str, Any]] = None) -> LegalAnalysis:
        """完整的法律分析流程"""
        # Step 1: 提取事实
        facts = self.extract_facts(description)

        # Step 2: 识别案件类型
        case_type = self.identify_case_type(facts, description)

        # Step 3: 匹配法律
        applicable_laws = self.match_laws(case_type, description)

        # Step 4: 认定责任
        liability = self.determine_liability(facts, case_type, applicable_laws)

        # Step 5: 风险评估
        risk_assessment = self.assess_risk(liability, applicable_laws)

        # Step 6: 生成建议
        suggestions = self.generate_suggestions(case_type, facts, liability)

        return LegalAnalysis(
            facts=facts,
            legal_relations=[LegalRelation(
                type=case_type,
                parties=["原告", "被告"],
                subject=case_type,
                content=f"关于{case_type}的法律关系"
            )],
            applicable_laws=applicable_laws,
            liability=liability,
            risk_assessment=risk_assessment,
            suggestions=suggestions,
            confidence=0.75  # 基于简化规则的置信度
        )
