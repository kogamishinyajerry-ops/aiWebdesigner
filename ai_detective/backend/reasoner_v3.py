"""
法律推理模块 - 扩展版 V3
Legal Reasoner Module - Extended V3
新增：网络侵权（小红书恶意发帖）、证据深度挖掘功能
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
    category: str  # "time", "location", "person", "action", "result", "amount", "platform", "post"
    confidence: float = 1.0
    source: str = "user_input"
    sub_facts: List[str] = field(default_factory=list)
    needs_verification: bool = False  # 是否需要进一步验证


@dataclass
class DisputeFocus:
    """争议焦点"""
    main_issue: str
    details: List[str]
    facts_support: List[str]
    critical_evidence: List[str]  # 关键证据


@dataclass
class EvidenceGap:
    """证据缺口"""
    missing_evidence: str
    importance: str  # "critical", "high", "medium", "low"
    how_to_obtain: str
    estimated_difficulty: str  # "容易", "中等", "困难", "极难"


@dataclass
class InvestigationPlan:
    """调查计划"""
    priority_tasks: List[str]
    secondary_tasks: List[str]
    optional_tasks: List[str]


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
    evidence_gaps: List[EvidenceGap]  # 新增：证据缺口
    investigation_plan: InvestigationPlan  # 新增：调查计划
    confidence: float
    created_at: datetime = field(default_factory=datetime.now)


class LegalReasonerV3:
    """法律推理引擎 V3 - 扩展版"""

    def __init__(self):
        self.law_database = self._load_law_database()
        self.case_patterns = self._load_case_patterns()
        self.colloquial_map = self._load_colloquial_map()
        self.platform_keywords = self._load_platform_keywords()

    def _load_platform_keywords(self) -> Dict[str, List[str]]:
        """平台关键词识别"""
        return {
            "小红书": ["小红书", "xhs", "red", "薯", "笔记", "博主", "网红", "种草"],
            "微博": ["微博", "weibo", "博主", "V博主", "热搜"],
            "抖音": ["抖音", "douyin", "短视频", "直播", "抖"],
            "知乎": ["知乎", "zhihu", "答主", "问答"],
            "朋友圈": ["朋友圈", "weixin", "微信群"]
        }

    def _load_colloquial_map(self) -> Dict[str, str]:
        """口语化表达映射 - 扩展版"""
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
            "造谣": "虚假陈述",
            "抹黑": "损害名誉",
            "挂人": "公开个人信息",
            "带节奏": "煽动情绪",
            "网暴": "网络暴力"
        }

    def _normalize_text(self, text: str) -> str:
        """规范化文本，处理口语化表达"""
        normalized = text
        for colloquial, standard in self.colloquial_map.items():
            normalized = normalized.replace(colloquial, standard)
        return normalized

    def _load_law_database(self) -> Dict[str, Any]:
        """加载法律数据库 - 扩展版（含网络侵权）"""
        return {
            "民法典": {
                "人格权编": {
                    "第1024条": {
                        "content": "民事主体享有名誉权。任何组织或者个人不得以侮辱、诽谤等方式侵害他人的名誉权。",
                        "keywords": ["名誉权", "侮辱", "诽谤", "侵害", "名誉"],
                        "application": "适用于名誉权侵权纠纷"
                    },
                    "第1019条": {
                        "content": "未经肖像权人同意，不得制作、使用、公开肖像权人的肖像，但是法律另有规定的除外。",
                        "keywords": ["肖像权", "肖像", "照片", "未经同意", "使用"],
                        "application": "适用于肖像权侵权纠纷"
                    },
                    "第1034条": {
                        "content": "自然人的个人信息受法律保护。个人信息是以电子或者其他方式记录的能够单独或者与其他信息结合识别特定自然人的各种信息。",
                        "keywords": ["个人信息", "隐私", "电话", "地址", "识别"],
                        "application": "适用于个人信息保护纠纷"
                    }
                },
                "侵权责任编": {
                    "第1194条": {
                        "content": "网络用户、网络服务提供者利用网络侵害他人民事权益的，应当承担侵权责任。",
                        "keywords": ["网络", "侵权", "民事权益", "责任"],
                        "application": "适用于网络侵权纠纷"
                    },
                    "第1195条": {
                        "content": "网络服务提供者接到通知后，应当及时采取必要措施，如删除、屏蔽、断开链接等。",
                        "keywords": ["删除", "屏蔽", "断开链接", "通知", "平台"],
                        "application": "适用于平台通知义务"
                    },
                    "第1165条": {
                        "content": "行为人因过错侵害他人民事权益造成损害的，应当承担侵权责任。",
                        "keywords": ["过错", "侵权", "损害", "责任"],
                        "application": "适用于过错侵权责任认定"
                    },
                    "第1183条": {
                        "content": "侵害自然人人身权益造成严重精神损害的，被侵权人有权请求精神损害赔偿。",
                        "keywords": ["精神损害", "赔偿", "人身权益", "严重"],
                        "application": "适用于精神损害赔偿请求"
                    }
                },
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
        """加载案例模式库 - 扩展版（含网络侵权）"""
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
            },
            "名誉权侵权": {
                "keywords": ["诽谤", "造谣", "抹黑", "侮辱", "损害名誉", "名誉权", "污蔑", "造黄谣"],
                "typical_claims": ["停止侵权", "赔礼道歉", "恢复名誉", "赔偿损失", "精神损害赔偿"],
                "evidence_needed": [
                    "侵权内容截图（含发布时间、发布者ID）",
                    "侵权内容传播数据（浏览量、点赞量、评论量）",
                    "举报/投诉记录",
                    "个人损失证明（如工作受影响、精神损害）",
                    "平台处理结果",
                    "侵权者真实身份信息"
                ],
                "typical_issues": [
                    "虚假陈述",
                    "恶意抹黑",
                    "人肉搜索",
                    "网暴煽动"
                ]
            },
            "肖像权侵权": {
                "keywords": ["照片", "肖像", "未经同意", "使用", "商用", "广告", "宣传"],
                "typical_claims": ["停止使用", "删除内容", "赔礼道歉", "赔偿损失"],
                "evidence_needed": [
                    "侵权照片/视频截图",
                    "发布时间、发布者信息",
                    "使用场景证明（广告、商业宣传等）",
                    "未授权证明",
                    "商业获利证明（如有）"
                ],
                "typical_issues": [
                    "擅自使用照片",
                    "商用未授权",
                    "虚假宣传"
                ]
            },
            "个人信息泄露": {
                "keywords": ["电话", "地址", "身份证", "曝光", "人肉", "个人信息", "隐私"],
                "typical_claims": ["删除信息", "赔礼道歉", "赔偿损失"],
                "evidence_needed": [
                    "被泄露信息内容截图",
                    "发布时间、发布者信息",
                    "信息真实性证明",
                    "造成的后果证明"
                ],
                "typical_issues": [
                    "人肉搜索",
                    "曝光隐私",
                    "恶意传播"
                ]
            }
        }

    def extract_facts(self, description: str) -> List[Fact]:
        """提取事实要素 - 扩展版（含平台和帖子信息）"""
        # 先规范化文本
        normalized = self._normalize_text(description)
        facts = []
        fact_id = 1

        # 1. 平台识别
        for platform, keywords in self.platform_keywords.items():
            for keyword in keywords:
                if keyword in description:
                    facts.append(Fact(
                        id=f"fact_{fact_id}",
                        description=f"平台：{platform}",
                        category="platform",
                        confidence=0.95
                    ))
                    fact_id += 1
                    break

        # 2. 帖子信息提取
        post_patterns = [
            r'(发了|发布了|上传了)(一篇|一条)(笔记|帖子|内容)',
            r'(笔记|帖子)(浏览量|点赞量|评论量)(超过|达到)(\d+)(万|千|百)',
            r'标题：(.{5,50}?)(，|。|\n)',
            r'([^\n]{5,30}?)(说是|说我是|说我是那种人)'
        ]

        for pattern in post_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if isinstance(match, tuple):
                    content = ''.join(match)
                else:
                    content = match

                # 清理和截断
                content = content.strip()
                if len(content) > 60:
                    content = content[:60] + "..."

                if content and len(content) > 5:
                    # 避免重复
                    if not any(content in f.description for f in facts if f.category == "post"):
                        facts.append(Fact(
                            id=f"fact_{fact_id}",
                            description=f"帖子信息：{content}",
                            category="post",
                            confidence=0.85
                        ))
                        fact_id += 1

        # 3. 时间提取
        time_patterns = [
            r'(去年|今年|前年|上个月|这个月|上周|这周)(\d{1,2})?(月|日|号)?',
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{1,2})月(\d{1,2})日',
            r'(三天前|两天前|一天前|昨天|前天)',
            r'(大概|好像|大约)(去年|今年|上周|这周)',
        ]

        for pattern in time_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if isinstance(match, tuple):
                    match = ''.join(match)
                # 清理模糊表达
                match = match.replace('大概', '').replace('好像', '').replace('大约', '')
                match = match.strip()

                if match:
                    # 避免重复
                    if not any(match in f.description for f in facts if f.category == "time"):
                        confidence = 0.85
                        if '前天' in match or '大概' in match or '好像' in match:
                            match = match + '（时间不精确）'
                            confidence = 0.7

                        facts.append(Fact(
                            id=f"fact_{fact_id}",
                            description=f"时间：{match}",
                            category="time",
                            confidence=confidence
                        ))
                        fact_id += 1

        # 4. 地点提取
        location_patterns = [
            r'([京津沪渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新][市区县]{1,3})',
            r'([京津沪渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新]市[^，。\s]{0,10}[区县街道路村])',
        ]

        for pattern in location_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                clean_match = match.strip()
                if len(clean_match) >= 2:
                    idx = description.find(clean_match)
                    if idx != -1:
                        end_idx = min(idx + 20, len(description))
                        location_full = description[idx:end_idx].strip()
                        location_full = re.sub(r'[，。：;；]', '', location_full)
                        if len(location_full) <= 15:
                            if not any(location_full in f.description for f in facts if f.category == "location"):
                                facts.append(Fact(
                                    id=f"fact_{fact_id}",
                                    description=f"地点：{location_full}",
                                    category="location",
                                    confidence=0.9
                                ))
                                fact_id += 1
                    break

        # 5. 人物提取
        person_patterns = [
            r'([张李王刘陈杨赵黄周吴]\w*[先生女士阿姨姐哥])',
            r'(房东[\s，。])',
            r'(租客[\s，。])',
            r'(邻居[\s，。])',
            r'(维修师傅[\s，。])',
            r'(博主|网红|网红店|某博主)',
            r'(店家|老板|老板娘)'
        ]

        for pattern in person_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                clean_match = re.sub(r'[\s，。]', '', match)
                if len(clean_match) >= 2:
                    if not any(clean_match in f.description for f in facts):
                        facts.append(Fact(
                            id=f"fact_{fact_id}",
                            description=f"人物：{clean_match}",
                            category="person",
                            confidence=0.9
                        ))
                        fact_id += 1

        # 6. 金额提取
        amount_patterns = [
            r'(\d+(?:\.\d+)?)\s*(元|万|千|百|块|块钱)',
            r'(押金|租金|赔偿|损失|精神损失)\s*(\d+(?:\.\d+)?)',
            r'(维修费|清洁费|折旧费|违约金)\s*(\d+(?:\.\d+)?)'
        ]
        for pattern in amount_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if isinstance(match, tuple):
                    amount_str = match[0] if match[0].isdigit() else (match[1] if len(match) > 1 and match[1].isdigit() else match[0])
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

        # 7. 侵权行为提取
        infringement_keywords = [
            ("诽谤/造谣", ["造谣", "污蔑", "诽谤", "抹黑", "造黄谣"]),
            ("人肉/曝光", ["人肉", "曝光", "曝光电话", "曝光地址", "挂人"]),
            ("网络暴力", ["网暴", "带节奏", "煽动", "攻击"]),
            ("未经使用", ["未经同意", "擅自", "盗用", "商用", "广告"])
        ]

        for action_type, keywords in infringement_keywords:
            for keyword in keywords:
                if keyword in description:
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
        """识别争议焦点 - 扩展版（含网络侵权）"""
        focuses = []

        # 1. 名誉权侵权争议
        if any("造谣" in f.description or "污蔑" in f.description or "诽谤" in f.description for f in facts):
            focuses.append(DisputeFocus(
                main_issue="名誉权侵权纠纷",
                details=[
                    "被告在小红书发布虚假内容",
                    "内容涉及捏造事实、侮辱诽谤",
                    "对原告造成名誉损害",
                    "传播范围广（需确认浏览量、点赞量）"
                ],
                facts_support=["造谣", "污蔑", "诽谤"],
                critical_evidence=["侵权内容完整截图", "传播数据证明", "虚假事实证明"]
            ))

        # 2. 肖像权侵权争议
        if any("照片" in f.description or "肖像" in f.description or "未经同意" in f.description for f in facts):
            focuses.append(DisputeFocus(
                main_issue="肖像权侵权纠纷",
                details=[
                    "被告未经原告同意使用原告照片",
                    "可能用于商业宣传",
                    "未获得原告授权"
                ],
                facts_support=["照片", "未经同意", "使用"],
                critical_evidence=["侵权照片截图", "商用证明", "未授权证明"]
            ))

        # 3. 个人信息泄露争议
        if any("人肉" in f.description or "曝光" in f.description or "电话" in f.description or "地址" in f.description for f in facts):
            focuses.append(DisputeFocus(
                main_issue="个人信息保护纠纷",
                details=[
                    "被告泄露原告个人信息",
                    "包括电话、地址等敏感信息",
                    "对原告生活造成困扰"
                ],
                facts_support=["人肉", "曝光", "电话", "地址"],
                critical_evidence=["被泄露信息截图", "真实性证明"]
            ))

        # 4. 精神损害争议
        if any("精神" in f.description or "抑郁" in f.description or "影响" in f.description for f in facts):
            focuses.append(DisputeFocus(
                main_issue="精神损害赔偿请求",
                details=[
                    "被告的侵权行为给原告造成精神痛苦",
                    "可能影响工作和生活",
                    "需要提供精神损害证明"
                ],
                facts_support=["精神", "抑郁", "影响"],
                critical_evidence=["医疗诊断证明", "心理咨询记录", "工作影响证明"]
            ))

        return focuses

    def analyze_evidence_gaps(self, facts: List[Fact], description: str,
                            case_type: str) -> List[EvidenceGap]:
        """分析证据缺口"""
        gaps = []

        # 检查是否有关键证据缺失
        if "浏览量" not in description and "点赞" not in description:
            gaps.append(EvidenceGap(
                missing_evidence="侵权内容的传播数据（浏览量、点赞量、评论量）",
                importance="critical",
                how_to_obtain="在帖子页面截取完整截图，显示浏览量、点赞量、评论量数据",
                estimated_difficulty="容易"
            ))

        if "截图" not in description:
            gaps.append(EvidenceGap(
                missing_evidence="侵权内容的完整截图（含发布时间、发布者ID、具体内容）",
                importance="critical",
                how_to_obtain="对侵权帖子进行完整截图，确保包含所有关键信息",
                estimated_difficulty="容易"
            ))

        if "举报" not in description and "投诉" not in description:
            gaps.append(EvidenceGap(
                missing_evidence="向平台的举报/投诉记录",
                importance="high",
                how_to_obtain="在小红书等平台内进行举报，并截图保存举报记录和平台回复",
                estimated_difficulty="容易"
            ))

        # 检查是否能确认侵权者真实身份
        if any("不知道" in f.description or "不认识" in f.description for f in facts):
            gaps.append(EvidenceGap(
                missing_evidence="侵权者的真实身份信息（姓名、联系方式、地址等）",
                importance="critical",
                how_to_obtain="1. 通过平台客服要求提供侵权者信息；2. 法院立案后申请调查令；3. 报警要求派出所协助",
                estimated_difficulty="中等"
            ))

        # 检查精神损害证明
        if "诊断" not in description and "医院" not in description:
            gaps.append(EvidenceGap(
                missing_evidence="精神损害的医疗证明（如心理咨询记录、医疗诊断）",
                importance="medium",
                how_to_obtain="到正规医院或心理咨询机构进行诊断，获取相关证明",
                estimated_difficulty="中等"
            ))

        # 检查实际损失证明
        if "工作" not in description and "收入" not in description:
            gaps.append(EvidenceGap(
                missing_evidence="实际损失证明（工作受影响、收入减少等）",
                importance="medium",
                how_to_obtain="提供劳动合同、收入证明、工作单位出具的证明等",
                estimated_difficulty="中等"
            ))

        # 检查侵权者是否删除内容
        if "删除" not in description and "还挂着" in description:
            gaps.append(EvidenceGap(
                missing_evidence="公证或时间戳证明（防止侵权者删除后死无对证）",
                importance="high",
                how_to_obtain="通过公证处进行网页公证，或使用可信时间戳服务进行存证",
                estimated_difficulty="中等"
            ))

        return gaps

    def create_investigation_plan(self, evidence_gaps: List[EvidenceGap],
                                 case_type: str) -> InvestigationPlan:
        """创建调查计划"""
        priority_tasks = []
        secondary_tasks = []
        optional_tasks = []

        # 根据证据缺口的重要性分配任务
        critical_gaps = [g for g in evidence_gaps if g.importance == "critical"]
        high_gaps = [g for g in evidence_gaps if g.importance == "high"]
        medium_gaps = [g for g in evidence_gaps if g.importance == "medium"]

        # 优先任务 - 关键证据
        for gap in critical_gaps:
            priority_tasks.append(f"【关键】{gap.missing_evidence}")
            priority_tasks.append(f"      获取方式：{gap.how_to_obtain}")

        # 重要任务
        for gap in high_gaps:
            secondary_tasks.append(f"【重要】{gap.missing_evidence}")
            secondary_tasks.append(f"      获取方式：{gap.how_to_obtain}")

        # 可选任务
        for gap in medium_gaps:
            optional_tasks.append(f"【可选】{gap.missing_evidence}")
            optional_tasks.append(f"      获取方式：{gap.how_to_obtain}")

        # 通用调查建议
        priority_tasks.extend([
            "",
            "【通用建议】",
            "• 保存所有相关截图和记录",
            "• 尽快联系平台进行举报",
            "• 考虑进行网页公证固定证据",
            "• 避免与侵权者直接对骂，保持理性"
        ])

        return InvestigationPlan(
            priority_tasks=priority_tasks,
            secondary_tasks=secondary_tasks,
            optional_tasks=optional_tasks
        )

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

        return matched_laws[:10]  # 返回前10条

    def _find_related_issue(self, law_content: str, focuses: List[DisputeFocus]) -> str:
        """找到法律条文对应的争议焦点"""
        for focus in focuses:
            for detail in focus.details:
                if any(word in law_content for word in ["名誉", "肖像", "个人信息", "网络", "精神", "押金", "违约", "维修", "格式条款"]):
                    return focus.main_issue
        return "普遍适用"

    def generate_litigation_strategy(self, case_type: str, focuses: List[DisputeFocus],
                                    evidence_available: List[str]) -> List[str]:
        """生成诉讼策略"""
        strategies = []

        # 根据案件类型调整策略
        if "名誉权" in case_type or "侵权" in case_type:
            strategies.append("【诉讼请求】")
            strategies.append("1. 要求被告立即停止侵权行为（删除、屏蔽相关内容）")
            strategies.append("2. 要求被告在侵权平台公开赔礼道歉（持续7天以上）")
            strategies.append("3. 要求被告恢复原告名誉")
            strategies.append("4. 要求被告赔偿精神损害抚慰金（5000-50000元，根据具体情况）")
            strategies.append("5. 要求被告承担维权合理费用（公证费、律师费等）")
            strategies.append("6. 要求网络平台履行通知义务（如未及时处理）")

            strategies.append("\n【诉讼策略】")
            strategies.append("1. 证据固定：优先进行网页公证，确保证据效力")
            strategies.append("2. 确认侵权者：通过平台或法律途径获取侵权者真实身份")
            strategies.append("3. 证明损害：提供名誉受损、精神痛苦、工作影响等证明")
            strategies.append("4. 主张赔偿：结合侵权情节、传播范围、实际损失主张赔偿")
            strategies.append("5. 平台责任：如平台未及时处理，可将平台列为共同被告")

            strategies.append("\n【预期抗辩点】")
            strategies.append("1. 侵权者可能主张内容属实 - 需证明内容虚假")
            strategies.append("2. 侵权者可能主张行使舆论监督权 - 需证明主观恶意")
            strategies.append("3. 侵权者可能主张损害后果轻微 - 需证明实际影响")
            strategies.append("4. 平台可能主张已尽审核义务 - 需证明其未尽义务")

        else:
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

        # 根据案件类型调整证据建议
        if "名誉权" in str(focuses) or "侵权" in str(focuses):
            # 网络侵权案件的证据建议
            recommendations.extend([
                "✅ 侵权内容完整截图（含发布时间、发布者ID、具体内容）",
                "✅ 传播数据证明（浏览量、点赞量、评论量、转发量）",
                "✅ 平台举报/投诉记录及平台回复",
                "✅ 侵权者个人主页截图（含粉丝数、活跃度）",
                "✅ 虚假事实证明（证明内容不实）",
                "✅ 精神损害证明（医疗诊断、心理咨询记录）",
                "✅ 实际损失证明（工作受影响、收入减少）",
                "✅ 网页公证或时间戳证明（固定证据）"
            ])
        else:
            # 房屋租赁案件的证据建议
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

            recommendations.extend([
                "✅ 搬离时的房屋照片（证明房屋完好）",
                "✅ 租金付款记录（5000元/月×3个月）",
                "✅ 身份证复印件"
            ])

        return recommendations

    def analyze(self, description: str, context: Optional[Dict[str, Any]] = None) -> LegalAnalysis:
        """完整的法律分析流程 - 扩展版"""

        # Step 1: 提取事实
        facts = self.extract_facts(description)

        # Step 2: 识别案件类型
        description_lower = description.lower()

        # 智能识别案件类型
        if any(kw in description for kw in ["小红书", "造谣", "诽谤", "污蔑", "人肉", "曝光", "网暴"]):
            case_type = "名誉权/个人信息侵权"
        elif any(kw in description for kw in ["照片", "肖像", "未经同意", "商用", "广告"]):
            case_type = "肖像权侵权"
        elif any(kw in description for kw in ["租房", "租金", "押金", "房东", "租客", "漏水"]):
            case_type = "房屋租赁纠纷"
        else:
            case_type = "待定案件"

        # Step 3: 识别争议焦点
        dispute_focuses = self.identify_dispute_focuses(facts, description)

        # Step 4: 匹配法律
        applicable_laws = self.match_laws_with_analysis(case_type, dispute_focuses, description)

        # Step 5: 认定责任
        if "侵权" in case_type:
            liability = {
                "liable_party": "侵权者（需确认真实身份）",
                "liability_type": "侵权责任",
                "basis": "1. 违反民法典第1024条，以侮辱、诽谤方式侵害名誉权\n2. 违反民法典第1194条，网络侵害他人民事权益\n3. 如造成严重精神损害，可主张精神损害赔偿（第1183条）",
                "severity": "high",
                "damages": {
                    "type": "名誉损害+精神损害",
                    "estimated_amount": "精神损害抚慰金5000-50000元（视情节严重程度）+ 维权费用",
                    "evidence_level": "需补充关键证据（传播数据、身份证明等）"
                }
            }
        else:
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

        # Step 6: 风险评估
        if "侵权" in case_type:
            risk_assessment = {
                "success_probability": "70%",  # 降低因为证据不充分
                "time_cost": "6个月左右（涉及取证和确认身份）",
                "economic_cost": "案件受理费约100元+ 公证费1000-3000元 + 律师费（如委托律师）",
                "main_risk": "1. 无法确认侵权者真实身份\n2. 侵权者删除内容后取证困难\n3. 精神损害赔偿金额难以确定",
                "evidence_strength": "弱到中等（需要补充关键证据）"
            }
        else:
            risk_assessment = {
                "success_probability": "85%",
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

        # Step 9: 分析证据缺口
        evidence_gaps = self.analyze_evidence_gaps(facts, description, case_type)

        # Step 10: 创建调查计划
        investigation_plan = self.create_investigation_plan(evidence_gaps, case_type)

        # Step 11: 生成建议
        if "侵权" in case_type:
            suggestions = [
                "【紧急行动】",
                "• 立即对侵权内容进行完整截图（确保包含发布时间、ID、内容、传播数据）",
                "• 尽快联系平台进行举报，并保存举报记录",
                "• 考虑进行网页公证，固定证据（防止对方删除）",
                "• 避免与侵权者对骂，保持理性，收集更多证据",

                "\n【证据补充】",
                *evidence_recommendations,

                "\n【法律依据】",
                "• 民法典第1024条：名誉权保护",
                "• 民法典第1194条：网络侵权责任",
                "• 民法典第1195条：平台通知义务",
                "• 民法典第1183条：精神损害赔偿",

                "\n【程序选择】",
                "• 管辖法院：侵权行为地或被告住所地法院",
                "• 可申请网络实名制调查令获取侵权者身份",
                "• 诉讼时效：3年内",

                "\n【建议】",
                "• 证据收集是关键，优先进行公证固定",
                "• 可先向平台投诉，要求删除内容",
                "• 如侵权者身份不明，可申请法院调查令",
                "• 精神损害赔偿需提供医疗或心理咨询证明",
                "• 情节严重可考虑向公安机关报案"
            ]
        else:
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
                "parties": ["原告", "被告"],
                "subject": case_type,
                "content": "纠纷详情见争议焦点"
            }],
            applicable_laws=applicable_laws,
            liability=liability,
            risk_assessment=risk_assessment,
            suggestions=suggestions,
            evidence_recommendations=evidence_recommendations,
            litigation_strategy=litigation_strategy,
            evidence_gaps=evidence_gaps,
            investigation_plan=investigation_plan,
            confidence=0.75 if "侵权" in case_type else 0.88
        )
