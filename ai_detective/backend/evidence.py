"""
证据分析模块
Evidence Analyzer Module
分析和评估证据的有效性和完整性
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EvidenceType(Enum):
    """证据类型"""
    DOCUMENT = "书证"  # 合同、凭证等书面材料
    AUDIO_VIDEO = "视听资料"  # 录音、录像
    ELECTRONIC = "电子数据"  # 微信、邮件等电子记录
    TESTIMONY = "证人证言"  # 证人证言
    EXPERT_OPINION = "鉴定意见"  # 司法鉴定
    INSPECTION_RECORD = "勘验笔录"  # 现场勘验
    OTHER = "其他"  # 其他类型


class Validity(Enum):
    """有效性等级"""
    HIGH = "高"  # 证据力强，可直接采信
    MEDIUM = "中"  # 证据力一般，需补强
    LOW = "低"  # 证据力弱，难以采信
    INVALID = "无效"  # 无效证据


@dataclass
class Evidence:
    """证据"""
    id: str
    name: str
    evidence_type: EvidenceType
    description: str
    validity: Validity
    weight: float = 1.0  # 证据权重
    source: str = ""
    obtained_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceChain:
    """证据链"""
    evidences: List[Evidence]
    completeness: float  # 完整度 0-1
    consistency: float  # 一致性 0-1
    strength: str  # 强度 "strong", "moderate", "weak"
    gaps: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class EvidenceAnalyzer:
    """证据分析器"""

    def __init__(self):
        self.evaluation_rules = self._load_evaluation_rules()

    def _load_evaluation_rules(self) -> Dict[str, Any]:
        """加载证据评估规则"""
        return {
            "document": {
                "validity_factors": {
                    "original": Validity.HIGH,
                    "copy": Validity.MEDIUM,
                    "electronic": Validity.MEDIUM
                },
                "weight": 0.9
            },
            "audio_video": {
                "validity_factors": {
                    "original": Validity.MEDIUM,
                    "edited": Validity.LOW
                },
                "weight": 0.7
            },
            "electronic": {
                "validity_factors": {
                    "authenticated": Validity.MEDIUM,
                    "unverified": Validity.LOW
                },
                "weight": 0.6
            },
            "testimony": {
                "validity_factors": {
                    "multiple_witnesses": Validity.MEDIUM,
                    "single_witness": Validity.LOW
                },
                "weight": 0.5
            },
            "expert_opinion": {
                "validity_factors": {
                    "qualified": Validity.HIGH,
                    "unqualified": Validity.LOW
                },
                "weight": 0.85
            }
        }

    def analyze_evidence(self, evidence: Evidence) -> Dict[str, Any]:
        """分析单个证据"""
        analysis = {
            "id": evidence.id,
            "name": evidence.name,
            "type": evidence.evidence_type.value,
            "validity": evidence.validity.value,
            "weight": evidence.weight,
            "assessment": self._assess_validity(evidence),
            "weaknesses": self._identify_weaknesses(evidence),
            "improvements": self._suggest_improvements(evidence)
        }
        return analysis

    def build_evidence_chain(self, evidences: List[Evidence],
                             case_type: str) -> EvidenceChain:
        """构建证据链"""
        # 计算完整度
        completeness = self._calculate_completeness(evidences, case_type)

        # 计算一致性
        consistency = self._calculate_consistency(evidences)

        # 确定强度
        strength = self._determine_strength(completeness, consistency)

        # 识别证据链缺口
        gaps = self._identify_gaps(evidences, case_type)

        # 生成建议
        suggestions = self._generate_chain_suggestions(gaps, completeness, consistency)

        return EvidenceChain(
            evidences=evidences,
            completeness=completeness,
            consistency=consistency,
            strength=strength,
            gaps=gaps,
            suggestions=suggestions
        )

    def _assess_validity(self, evidence: Evidence) -> str:
        """评估证据有效性"""
        assessments = []

        if evidence.validity == Validity.HIGH:
            assessments.append("证据力强，可直接采信")
        elif evidence.validity == Validity.MEDIUM:
            assessments.append("证据力一般，建议补强")
        elif evidence.validity == Validity.LOW:
            assessments.append("证据力较弱，难以独立采信")
        else:
            assessments.append("证据无效，无法采信")

        # 根据证据类型补充评估
        if evidence.evidence_type == EvidenceType.DOCUMENT:
            assessments.append("书证是最有力的证据形式")
        elif evidence.evidence_type == EvidenceType.ELECTRONIC:
            assessments.append("电子证据需确保真实性和完整性")
        elif evidence.evidence_type == EvidenceType.TESTIMONY:
            assessments.append("证人证言需证人出庭作证")

        return "；".join(assessments)

    def _identify_weaknesses(self, evidence: Evidence) -> List[str]:
        """识别证据弱点"""
        weaknesses = []

        if evidence.validity == Validity.LOW:
            weaknesses.append("证据有效性较低")

        if evidence.weight < 0.5:
            weaknesses.append("证据权重较低")

        if evidence.evidence_type == EvidenceType.ELECTRONIC:
            if not evidence.metadata.get("authenticated"):
                weaknesses.append("电子证据未经过真实性验证")

        if evidence.evidence_type == EvidenceType.AUDIO_VIDEO:
            if evidence.metadata.get("edited"):
                weaknesses.append("视听资料经过编辑，影响证明力")

        if not evidence.description or len(evidence.description) < 10:
            weaknesses.append("证据描述不够详细")

        return weaknesses

    def _suggest_improvements(self, evidence: Evidence) -> List[str]:
        """提出证据改进建议"""
        suggestions = []

        if evidence.validity == Validity.MEDIUM:
            suggestions.append("建议提供原件或经过公证的复印件")

        if evidence.evidence_type == EvidenceType.ELECTRONIC:
            suggestions.append("建议对电子证据进行公证或鉴定")
            suggestions.append("保留完整的获取过程和来源信息")

        if evidence.evidence_type == EvidenceType.TESTIMONY:
            suggestions.append("建议提供多份证人证言相互印证")

        if evidence.evidence_type == EvidenceType.DOCUMENT:
            suggestions.append("确保证据材料的完整性和连续性")

        return suggestions

    def _calculate_completeness(self, evidences: List[Evidence],
                                case_type: str) -> float:
        """计算证据链完整度"""
        # 定义不同案件类型需要的证据类型
        required_evidence_types = {
            "肖像权侵权": [EvidenceType.DOCUMENT, EvidenceType.ELECTRONIC],
            "合同违约": [EvidenceType.DOCUMENT, EvidenceType.ELECTRONIC],
            "人身损害": [EvidenceType.DOCUMENT, EvidenceType.EXPERT_OPINION, EvidenceType.TESTIMONY],
            "房屋租赁": [EvidenceType.DOCUMENT, EvidenceType.ELECTRONIC]
        }

        required = required_evidence_types.get(case_type, [EvidenceType.DOCUMENT])
        present_types = set(ev.evidence_type for ev in evidences)

        completeness = len(present_types & set(required)) / len(required) if required else 0.5

        # 考虑证据数量
        if len(evidences) >= 3:
            completeness += 0.1

        return min(completeness, 1.0)

    def _calculate_consistency(self, evidences: List[Evidence]) -> float:
        """计算证据一致性"""
        if len(evidences) < 2:
            return 0.5

        # 简化版：检查证据描述中的关键词一致性
        descriptions = [ev.description.lower() for ev in evidences]
        common_words = set()

        if descriptions:
            # 提取所有中文词汇（简化处理）
            all_words = []
            for desc in descriptions:
                words = [desc[i:i+2] for i in range(0, len(desc)-1)]
                all_words.extend(words)

            # 找出出现次数多的词
            from collections import Counter
            word_counts = Counter(all_words)
            common_words = {word for word, count in word_counts.items() if count > 1}

        # 一致性基于证据之间的共同内容
        consistency = min(len(common_words) / 10, 0.9) if common_words else 0.5

        return consistency

    def _determine_strength(self, completeness: float, consistency: float) -> str:
        """确定证据链强度"""
        overall_score = (completeness + consistency) / 2

        if overall_score >= 0.8:
            return "strong"  # 强
        elif overall_score >= 0.6:
            return "moderate"  # 中等
        else:
            return "weak"  # 弱

    def _identify_gaps(self, evidences: List[Evidence], case_type: str) -> List[str]:
        """识别证据链缺口"""
        gaps = []
        present_types = set(ev.evidence_type for ev in evidences)

        # 检查书证
        if EvidenceType.DOCUMENT not in present_types:
            gaps.append("缺少书证（合同、凭证等）")

        # 检查电子证据
        if EvidenceType.ELECTRONIC not in present_types:
            gaps.append("缺少电子证据（沟通记录等）")

        # 检查特定案件类型的证据
        if case_type == "人身损害":
            if EvidenceType.EXPERT_OPINION not in present_types:
                gaps.append("缺少司法鉴定意见")
            if EvidenceType.INSPECTION_RECORD not in present_types:
                gaps.append("缺少勘验笔录")

        # 检查证据数量
        if len(evidences) < 3:
            gaps.append("证据数量较少")

        return gaps

    def _generate_chain_suggestions(self, gaps: List[str],
                                   completeness: float,
                                   consistency: float) -> List[str]:
        """生成证据链建议"""
        suggestions = []

        if completeness < 0.7:
            suggestions.append("建议补充更多类型的证据材料")

        if consistency < 0.6:
            suggestions.append("建议确保证据之间的逻辑一致性和相互印证")

        if gaps:
            suggestions.append("建议补充以下证据：")
            for gap in gaps:
                suggestions.append(f"  • {gap}")

        if completeness >= 0.8 and consistency >= 0.8:
            suggestions.append("证据链较为完整，可以提起诉讼")

        else:
            suggestions.append("建议在补充证据后再提起诉讼")

        return suggestions

    def suggest_evidence(self, case_type: str, facts: List[Any]) -> List[str]:
        """建议证据类型"""
        evidence_suggestions = {
            "肖像权侵权": [
                "被侵权的肖像照片（原版）",
                "肖像使用的证据（网页、广告等截图）",
                "未经同意使用的证明",
                "造成损失的证据（如侵权获利、精神损害）"
            ],
            "合同违约": [
                "合同原件",
                "合同履行证据（付款凭证、交付凭证等）",
                "违约证据（违约通知、拒付凭证等）",
                "损失证明（费用发票、账单等）"
            ],
            "人身损害": [
                "医疗记录（病历、诊断证明、医疗费用票据）",
                "现场照片或视频",
                "证人证言",
                "司法鉴定意见书",
                "误工证明（单位证明、工资流水等）"
            ],
            "房屋租赁": [
                "租赁合同",
                "付款记录（租金、押金等）",
                "房屋验收记录",
                "违约证据",
                "物品损坏证明（如有）"
            ]
        }

        return evidence_suggestions.get(case_type, [
            "相关合同或协议",
            "沟通记录（短信、微信、邮件等）",
            "付款凭证",
            "损失证明"
        ])
