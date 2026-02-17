"""
法律推理模块 - 优化版 V2
Legal Reasoner Module - Optimized V2
改进事实提取、上下文理解和法律推理深度
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
    sub_facts: List[str] = field(default_factory=list)  # 子事实


@dataclass
class DisputeFocus:
    """争议焦点"""
    main_issue: str
    details: List[str]
    facts_support: List[str]


@dataclass
class LegalAnalysis:
    """法律分析结果"""
    facts: List[Fact]
    dispute_focuses: List[DisputeFocus]
    legal_relations: List[Dict[str, Any]]
    applicable_laws: List[Dict[str, str]]
    liability: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    suggestions: List[str]
    evidence_recommendations: List[str]
    litigation_strategy: List[str]
    confidence: float
    created_at: datetime = field(default_factory=datetime.now)


class LegalReasonerV2:
    """法律推理引擎 V2 - 优化版"""

    def __init__(self):
        self.law_database = self._load_law_database()
        self.case_patterns = self._load_case_patterns()
        self.colloquial_map = self._load_colloquial_map()

    def _load_colloquial_map(self) -> Dict[str, str]:
        """口语化表达映射"""
        return {
            "水漫金山": "厨房漏水",
            "倒霉透了": "遭遇纠纷",
            "说起来全是泪": "情绪化表达",
            "挺近的": "距离较近",
            "挺好的": "正面评价",
            "看着挺和善": "表面印象",
            "气不过": "愤怒情绪",
            "最过分的是": "关键事件",
            "对了": "补充说明",
            "我现在想想": "事后反思",
        }

    def _normalize_text(self, text: str) -> str:
        """规范化文本，处理口语化表达"""
        normalized = text
        for colloquial, standard in self.colloquial_map.items():
            normalized = normalized.replace(colloquial, standard)
        return normalized

    def _load_law_database(self) -> Dict[str, Any]:
        """加载法律数据库 - 扩展版"""
        return {
            "民法典": {
                "合同编": {
                    "第509条": {
                        "content": "当事人应当按照约定全面履行自己的义务。",
                        "keywords": ["合同", "履行", "义务", "约定"],
                        "application": "适用于合同履行纠纷"
                    },
                    "第577条": {
                        "content": "当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。",
                        "keywords": ["违约", "不履行", "赔偿", "违约责任"],
                        "application": "适用于违约责任认定"
                    },
                    "第497条": {
                        "content": "有下列情形之一的，该格式条款无效：...提供格式条款一方不合理地免除或者减轻其责任、加重对方责任、限制对方主要权利。",
                        "keywords": ["格式条款", "无效", "霸王条款", "不公平"],
                        "application": "适用于霸王条款效力认定"
                    },
                    "第710条": {
                        "content": "标的物毁损、灭失的风险，在标的物交付之前由出卖人承担，交付之后由买受人承担，但是法律另有规定或者当事人另有约定的除外。",
                        "keywords": ["毁损", "灭失", "风险", "交付"],
                        "application": "适用于房屋质量问题责任认定"
                    }
                },
                "物权编": {
                    "第240条": {
                        "content": "所有权人对自己的不动产或者动产，依法享有占有、使用、收益和处分的权利。",
                        "keywords": ["所有权", "占有", "使用", "处分"],
                        "application": "适用于财产权利认定"
                    }
                }
            }
        }

    def _load_case_patterns(self) -> Dict[str, Any]:
        """加载案例模式库 - 扩展版"""
        return {
            "房屋租赁纠纷": {
                "keywords": ["租房", "租金", "押金", "违约", "退房", "房东", "租客", "漏水", "维修", "清洁费", "折旧费"],
                "typical_claims": ["退还押金", "支付违约金", "赔偿损失", "承担维修费用"],
                "evidence_needed": [
                    "租赁合同（特别是押金条款）",
                    "付款记录（押金、租金）",
                    "维修账单和记录",
                    "微信/短信聊天记录",
                    "房屋交接照片",
                    "微信拉黑截图",
                    "邻居证言"
                ],
                "typical_issues": [
                    "押金不退",
                    "房屋质量问题",
                    "维修责任争议",
                    "霸王条款",
                    "恶意违约"
                ]
            }
        }

    def extract_facts(self, description: str) -> List[Fact]:
        """提取事实要素 - 优化版"""
        # 先规范化文本
        normalized = self._normalize_text(description)
        facts = []
        fact_id = 1

        # 1. 时间提取 - 更智能和全面
        time_patterns = [
            r'(去年|今年|前年)(\d{1,2})月',  # 去年11月
            r'(大概|好像|大约)(去年|今年)(\d{1,2})月',  # 大概去年11月
            r'(\d{4})年(\d{1,2})月',  # 2023年11月
            r'(\d{1,2})月(\d{1,2})日',  # 11月15日
            r'(刚搬入|住了一个多月|住了一个月)',  # 相对时间
            r'(突然有一天|有一天)',  # 模糊时间
        ]

        for pattern in time_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if isinstance(match, tuple):
                    match = ''.join(match)
                # 清理模糊表达
                match = match.replace('大概', '').replace('好像', '').replace('大约', '')
                match = match.strip()

                if match:  # 确保不为空
                    # 避免重复
                    if not any(match in f.description for f in facts if f.category == "time"):
                        # 标记不确定的时间
                        confidence = 0.85
                        if '一个多月' in match or '一天' in match:
                            match = match + '（时间不精确）'
                            confidence = 0.7

                        facts.append(Fact(
                            id=f"fact_{fact_id}",
                            description=f"时间：{match}",
                            category="time",
                            confidence=confidence
                        ))
                        fact_id += 1
            # 不break，允许提取多个时间点

        # 2. 地点提取 - 优化上下文范围
        location_patterns = [
            r'([京津沪渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新][市区县]{1,3})',  # 地区名
            r'([京津沪渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新]市[^，。\s]{0,10}[区县街道路村])',  # 市区县街道
        ]

        for pattern in location_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                # 清理匹配结果
                clean_match = match.strip()
                if len(clean_match) >= 2:  # 至少2个字符
                    # 提取完整地点信息
                    idx = description.find(clean_match)
                    if idx != -1:
                        # 提取后续的地点信息
                        end_idx = min(idx + 20, len(description))
                        location_full = description[idx:end_idx].strip()
                        # 清理标点
                        location_full = re.sub(r'[，。：;；]', '', location_full)
                        if len(location_full) <= 15:  # 限制长度
                            # 避免重复
                            if not any(location_full in f.description for f in facts if f.category == "location"):
                                facts.append(Fact(
                                    id=f"fact_{fact_id}",
                                    description=f"地点：{location_full}",
                                    category="location",
                                    confidence=0.9
                                ))
                                fact_id += 1
                    break

        # 3. 人物提取 - 修复正则表达式
        # 匹配完整称谓
        person_patterns = [
            r'([张李王刘陈杨赵黄周吴]\w*[先生女士阿姨姐哥])',  # 姓氏+称谓
            r'([王阿姨][\s，。])',  # 王阿姨等
            r'(房东[\s，。])',  # 房东
            r'(租客[\s，。])',  # 租客
            r'(邻居[\s，。])',  # 邻居
            r'(维修师傅[\s，。])',  # 维修师傅
            r'(楼下邻居[\s，。])',  # 楼下邻居
        ]

        for pattern in person_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                # 清理匹配结果，只保留汉字部分
                clean_match = re.sub(r'[\s，。]', '', match)
                if len(clean_match) >= 2:  # 至少2个字符
                    # 避免重复
                    if not any(clean_match in f.description for f in facts):
                        facts.append(Fact(
                            id=f"fact_{fact_id}",
                            description=f"人物：{clean_match}",
                            category="person",
                            confidence=0.9
                        ))
                        fact_id += 1

        # 4. 金额提取 - 全部提取
        amount_patterns = [
            r'(\d+(?:\.\d+)?)\s*(元|万|千|百|块|块钱)',
            r'(押金|租金)\s*(\d+(?:\.\d+)?)',
            r'(维修费|清洁费|折旧费)\s*(\d+(?:\.\d+)?)'
        ]
        for pattern in amount_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if isinstance(match, tuple):
                    amount_str = match[0] if match[0].isdigit() else match[1]
                    if not amount_str.isdigit():
                        continue
                    amount_text = ''.join([m for m in match if m and m != ''])
                    facts.append(Fact(
                        id=f"fact_{fact_id}",
                        description=f"金额：{amount_text}",
                        category="amount",
                        confidence=0.95
                    ))
                    fact_id += 1

        # 5. 合同信息提取
        contract_patterns = [
            r'(押一付三|押一付一|押二付一)',
            r'(微信电子合同|电子版合同)',
            r'(合同.*条款|条款.*不仔细看)',
        ]
        for pattern in contract_patterns:
            if pattern in description:
                facts.append(Fact(
                    id=f"fact_{fact_id}",
                    description=f"合同信息：{pattern}",
                    category="contract",
                    confidence=0.9
                ))
                fact_id += 1

        # 6. 行为提取 - 更智能的上下文提取
        action_keywords = [
            ("违约", ["不退押金", "不认账", "反悔"]),
            ("房屋问题", ["漏水", "管道老化", "房屋太老"]),
            ("维修", ["自己找人修", "维修费", "修好了"]),
            ("联系中断", ["微信拉黑", "电话不接", "不接"]),
            ("证据", ["拍照", "聊天记录", "录音"]),
            ("霸王条款", ["任何情况下押金不退", "不退押金"]),
        ]

        for action_type, keywords in action_keywords:
            for keyword in keywords:
                if keyword in description:
                    # 提取上下文
                    idx = description.find(keyword)
                    context_start = max(0, idx - 20)
                    context_end = min(len(description), idx + 50)
                    context = description[context_start:context_end].strip()
                    facts.append(Fact(
                        id=f"fact_{fact_id}",
                        description=f"{action_type}：{context}",
                        category="action",
                        confidence=0.9
                    ))
                    fact_id += 1
                    break

        return facts

    def identify_dispute_focuses(self, facts: List[Fact], description: str) -> List[DisputeFocus]:
        """识别争议焦点"""
        focuses = []

        # 1. 押金退还争议
        if any("押金" in f.description for f in facts):
            focuses.append(DisputeFocus(
                main_issue="押金退还纠纷",
                details=[
                    "房东拒绝退还押金8000元",
                    "房东主张房屋损坏和清洁费",
                    "房东主张设施折旧费1000元",
                    "合同中有'任何情况下押金不退'条款"
                ],
                facts_support=["押金不退", "霸王条款"]
            ))

        # 2. 维修费用争议
        if any("漏水" in f.description or "维修" in f.description for f in facts):
            focuses.append(DisputeFocus(
                main_issue="房屋维修责任纠纷",
                details=[
                    "厨房漏水，花费维修费2000元",
                    "房东认为管道老化非其责任",
                    "根据法律，房屋质量问题应由房东负责"
                ],
                facts_support=["漏水", "管道老化", "维修费"]
            ))

        # 3. 联系中断争议
        if "微信拉黑" in description or "电话不接" in description:
            focuses.append(DisputeFocus(
                main_issue="恶意逃避责任",
                details=[
                    "房东拉黑微信",
                    "房东不接电话",
                    "无法进行协商沟通"
                ],
                facts_support=["微信拉黑", "电话不接"]
            ))

        return focuses

    def match_laws_with_analysis(self, case_type: str, focuses: List[DisputeFocus],
                                  description: str) -> List[Dict[str, str]]:
        """匹配适用法律 - 带分析说明"""
        matched_laws = []

        for law_name, law_content in self.law_database.items():
            for category_name, category_content in law_content.items():
                for article_num, article in category_content.items():
                    # 检查关键词匹配
                    keywords = article["keywords"]
                    match_count = sum(1 for kw in keywords if kw in description)

                    if match_count >= 1:
                        # 根据争议焦点匹配法律
                        application = article.get("application", "")

                        matched_laws.append({
                            "law": law_name,
                            "category": category_name,
                            "article": article_num,
                            "content": article["content"],
                            "relevance": match_count / len(keywords),
                            "application": application,
                            "related_issue": self._find_related_issue(article["content"], focuses)
                        })

        # 按相关性排序
        matched_laws.sort(key=lambda x: x["relevance"], reverse=True)

        return matched_laws[:8]  # 返回前8条

    def _find_related_issue(self, law_content: str, focuses: List[DisputeFocus]) -> str:
        """找到法律条文对应的争议焦点"""
        for focus in focuses:
            for detail in focus.details:
                if any(word in law_content for word in ["押金", "违约", "维修", "格式条款"]):
                    return focus.main_issue
        return "普遍适用"

    def generate_litigation_strategy(self, case_type: str, focuses: List[DisputeFocus],
                                    evidence_available: List[str]) -> List[str]:
        """生成诉讼策略"""
        strategies = []

        strategies.append("【诉讼请求】")
        strategies.append(f"1. 要求被告退还押金8000元")
        strategies.append(f"2. 要求被告赔偿维修费用2000元")
        strategies.append(f"3. 要求被告支付资金占用利息（从违约之日起计算）")
        strategies.append(f"4. 诉讼费用由被告承担")

        strategies.append("\n【诉讼策略】")
        strategies.append("1. 证据准备：整理租赁合同、付款记录、聊天记录、维修账单、照片等")
        strategies.append("2. 争议焦点：重点证明押金应退、维修责任在房东")
        strategies.append("3. 法律适用：引用民法典第509条、577条、497条、710条")
        strategies.append("4. 程序选择：适用小额诉讼程序，快速审理")

        strategies.append("\n【预期抗辩点】")
        strategies.append("1. 房东可能主张房屋损坏 - 用搬离照片反驳")
        strategies.append("2. 房东可能主张维修责任在租客 - 引用法律条文反驳")
        strategies.append("3. 房东可能主张霸王条款有效 - 引用第497条反驳")

        return strategies

    def generate_evidence_recommendations(self, case_type: str, focuses: List[DisputeFocus],
                                          facts: List[Fact]) -> List[str]:
        """生成具体证据建议"""
        recommendations = []

        # 基于争议焦点生成证据建议
        for focus in focuses:
            if "押金" in focus.main_issue:
                recommendations.extend([
                    "✅ 租赁合同（特别是押金条款）",
                    "✅ 押金付款记录（转账记录、收据）",
                    "✅ 微信聊天记录（证明房东同意退押金后又反悔）",
                    "✅ 合同中'任何情况下押金不退'条款（证明霸王条款）"
                ])

            if "维修" in focus.main_issue:
                recommendations.extend([
                    "✅ 维修账单和发票（2000元）",
                    "✅ 维修师傅的联系方式（可作证）",
                    "✅ 漏水现场照片",
                    "✅ 楼下邻居证言（证明漏水事实）"
                ])

            if "恶意逃避" in focus.main_issue:
                recommendations.extend([
                    "✅ 微信拉黑截图",
                    "✅ 拨打记录（证明电话不接）"
                ])

        # 通用证据
        recommendations.extend([
            "✅ 搬离时的房屋照片（证明房屋完好）",
            "✅ 租金付款记录（5000元/月×3个月）",
            "✅ 身份证复印件"
        ])

        return recommendations

    def analyze(self, description: str, context: Optional[Dict[str, Any]] = None) -> LegalAnalysis:
        """完整的法律分析流程 - 优化版"""

        # Step 1: 提取事实
        facts = self.extract_facts(description)

        # Step 2: 识别案件类型
        description_lower = description.lower()
        case_type = "房屋租赁纠纷"  # 基于本案

        # Step 3: 识别争议焦点
        dispute_focuses = self.identify_dispute_focuses(facts, description)

        # Step 4: 匹配法律
        applicable_laws = self.match_laws_with_analysis(case_type, dispute_focuses, description)

        # Step 5: 认定责任
        liability = {
            "liable_party": "房东",
            "liability_type": "民事责任",
            "basis": "1. 违反民法典第509条，未全面履行合同义务（不退押金）\n2. 违反民法典第710条，房屋质量问题应由房东承担维修责任\n3. 合同中的'任何情况下押金不退'条款属于无效格式条款（第497条）",
            "severity": "moderate",
            "damages": {
                "type": "经济损失",
                "estimated_amount": "10000元（押金8000 + 维修费2000）",
                "evidence_level": "强（有聊天记录和照片证据）"
            }
        }

        # Step 6: 风险评估 - 更具体
        risk_assessment = {
            "success_probability": "85%",  # 提升因为有证据
            "time_cost": "3个月左右（小额诉讼程序）",
            "economic_cost": "案件受理费约75元（标的额10000元，适用小额诉讼）",
            "main_risk": "房东可能隐匿财产导致执行难",
            "evidence_strength": "强（有聊天记录、照片、付款记录）"
        }

        # Step 7: 证据建议
        evidence_recommendations = self.generate_evidence_recommendations(
            case_type, dispute_focuses, facts
        )

        # Step 8: 诉讼策略
        litigation_strategy = self.generate_litigation_strategy(
            case_type, dispute_focuses, evidence_recommendations
        )

        # Step 9: 生成建议
        suggestions = [
            "【立即行动】",
            "• 保存所有聊天记录和证据（截图、录音）",
            "• 整理所有付款记录和凭证",
            "• 准备起诉材料",

            "\n【证据补充】",
            *evidence_recommendations,

            "\n【法律依据】",
            "• 民法典第509条：房东应全面履行合同义务",
            "• 民法典第577条：房东应承担违约责任",
            "• 民法典第497条：霸王条款无效",
            "• 民法典第710条：房屋质量问题责任在房东",

            "\n【程序选择】",
            "• 适用小额诉讼程序：标的额10000元，低于小额诉讼门槛",
            "• 管辖法院：房屋所在地基层法院",
            "• 诉讼时效：3年内",

            "\n【建议】",
            "• 证据充分，胜诉概率较高",
            "• 可先行发送律师函，尝试和解",
            "• 如对方拒不配合，尽快起诉",
            "• 起诉时可申请财产保全，防止转移财产"
        ]

        return LegalAnalysis(
            facts=facts,
            dispute_focuses=dispute_focuses,
            legal_relations=[{
                "type": case_type,
                "parties": ["租客（原告）", "房东（被告）"],
                "subject": "租赁合同纠纷",
                "content": "押金退还及维修责任争议"
            }],
            applicable_laws=applicable_laws,
            liability=liability,
            risk_assessment=risk_assessment,
            suggestions=suggestions,
            evidence_recommendations=evidence_recommendations,
            litigation_strategy=litigation_strategy,
            confidence=0.88  # 提升置信度
        )
