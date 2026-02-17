"""
材料生成模块
Document Generator Module
生成报案材料和相关法律文档
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from .reasoner import LegalAnalysis


@dataclass
class Document:
    """文档"""
    title: str
    content: str
    document_type: str  # "report", "evidence_list", "claims", "complaint"
    created_at: str


class DocumentGenerator:
    """文档生成器"""

    def __init__(self):
        self.templates = {
            "complaint": self._complaint_template,
            "evidence_list": self._evidence_list_template,
            "claims": self._claims_template,
            "case_summary": self._case_summary_template
        }

    def generate_report(self, analysis: LegalAnalysis,
                        user_info: Dict[str, Any]) -> List[Document]:
        """生成完整报案材料"""
        documents = []

        # 1. 案情说明
        case_summary = self._generate_case_summary(analysis, user_info)
        documents.append(case_summary)

        # 2. 证据清单
        evidence_list = self._generate_evidence_list(analysis, user_info)
        documents.append(evidence_list)

        # 3. 诉求陈述
        claims = self._generate_claims(analysis, user_info)
        documents.append(claims)

        # 4. 起诉状（如果适用）
        if analysis.liability:
            complaint = self._generate_complaint(analysis, user_info)
            documents.append(complaint)

        return documents

    def _generate_case_summary(self, analysis: LegalAnalysis,
                                user_info: Dict[str, Any]) -> Document:
        """生成案情说明"""
        facts_text = "\n".join([
            f"• {fact.description}" for fact in analysis.facts
        ])

        laws_text = "\n\n".join([
            f"{law['law']} {law['category']} {law['article']}\n"
            f"内容：{law['content']}"
            for law in analysis.applicable_laws[:3]
        ])

        content = f"""# 案情说明

## 基本信息

**申请人姓名：** {user_info.get('name', '未填写')}
**联系电话：** {user_info.get('phone', '未填写')}
**案件类型：** {analysis.legal_relations[0].type if analysis.legal_relations else '民事纠纷'}
**发生时间：** {datetime.now().strftime('%Y年%m月%d日')}

## 案情描述

### 事实要素

{facts_text}

### 法律关系

根据案件描述，本案属于{analysis.legal_relations[0].type if analysis.legal_relations else '民事纠纷'}纠纷。

### 适用法律

{laws_text}

## 分析结论

**法律责任：**
- 责任主体：{analysis.liability.liable_party if analysis.liability else '待认定'}
- 责任类型：{analysis.liability.liability_type if analysis.liability else '待认定'}
- 责任依据：{analysis.liability.basis if analysis.liability else '待认定'}

**风险评估：**
- 成功概率：{analysis.risk_assessment.get('success_probability', '待评估')}
- 时间成本：{analysis.risk_assessment.get('time_cost', '待评估')}
- 经济成本：{analysis.risk_assessment.get('economic_cost', '待评估')}

## 重要提示

1. 本分析基于AI推理，仅供参考，不构成正式法律意见
2. 建议咨询专业律师进行案件评估
3. 注意保留相关证据材料

---

**生成时间：** {analysis.created_at.strftime('%Y年%m月%d日 %H:%M')}
**AI置信度：** {analysis.confidence:.2%}
"""

        return Document(
            title="案情说明",
            content=content,
            document_type="case_summary",
            created_at=analysis.created_at.strftime('%Y-%m-%d %H:%M:%S')
        )

    def _generate_evidence_list(self, analysis: LegalAnalysis,
                               user_info: Dict[str, Any]) -> Document:
        """生成证据清单"""
        content = """# 证据清单

## 已收集证据

根据案件情况，建议准备以下证据材料：

### 1. 身份证明
- [ ] 身份证复印件（正反面）
- [ ] 户口本复印件（如需要）
- [ ] 其他身份证明材料

### 2. 案件相关证据
"""

        case_type = analysis.legal_relations[0].type if analysis.legal_relations else ""

        if "肖像" in case_type:
            content += """
- [ ] 被侵权的肖像照片（原版和电子版）
- [ ] 肖像使用证据（截图、照片等）
- [ ] 未经同意使用证明
- [ ] 损失证明（如有）
"""
        elif "合同" in case_type:
            content += """
- [ ] 合同原件及复印件
- [ ] 合同履行证据（付款凭证、交付凭证等）
- [ ] 违约证据（违约通知、拒付凭证等）
- [ ] 损失证明（费用发票、账单等）
"""
        elif "租赁" in case_type:
            content += """
- [ ] 租赁合同
- [ ] 付款记录（租金、押金等）
- [ ] 房屋验收记录
- [ ] 违约证据
- [ ] 物品损坏证明（如有）
"""
        else:
            content += """
- [ ] 相关协议或合同
- [ ] 沟通记录（短信、微信、邮件等）
- [ ] 付款凭证
- [ ] 损失证明
- [ ] 其他相关材料
"""

        content += """

### 3. 损失证明
- [ ] 经济损失证明（发票、收据、账单等）
- [ ] 误工证明（单位证明、工资流水等）
- [ ] 医疗费用（如涉及人身损害）
- [ ] 精神损害证明（如有）

### 4. 证据整理建议

1. **原件保存**：所有证据原件需妥善保管
2. **复印件备份**：准备至少3套复印件
3. **电子备份**：重要材料进行电子扫描
4. **证据链**：确保证据之间能够相互印证
5. **时间标注**：标注证据的取得时间

## 证据有效性评估

| 证据类型 | 有效性 | 说明 |
|---------|--------|------|
| 书证原件 | 高 | 最有力的证据形式 |
| 电子证据 | 中高 | 需确保真实性和完整性 |
| 证人证言 | 中 | 需证人出庭作证 |
| 鉴定结论 | 高 | 需有资质的鉴定机构出具 |

## 注意事项

1. 证据应当真实、合法、有效
2. 不得伪造、变造证据
3. 证据取得方式应当合法
4. 及时提交证据，避免举证期限届满

---

**重要提示：**
- 证据是诉讼成功的关键
- 建议在律师指导下准备证据
- 证据材料需清晰、完整、有序
"""

        return Document(
            title="证据清单",
            content=content,
            document_type="evidence_list",
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def _generate_claims(self, analysis: LegalAnalysis,
                        user_info: Dict[str, Any]) -> Document:
        """生成诉求陈述"""
        claims = []

        # 基于案件类型生成典型诉求
        case_type = analysis.legal_relations[0].type if analysis.legal_relations else ""

        if "肖像" in case_type:
            claims = [
                "停止侵害，立即停止使用申请人肖像的行为",
                "赔礼道歉，消除影响",
                "赔偿损失，包括但不限于精神损害赔偿、经济收益损失等"
            ]
        elif "合同" in case_type:
            claims = [
                "继续履行合同义务",
                "支付违约金",
                "赔偿因违约造成的损失"
            ]
        elif "租赁" in case_type:
            claims = [
                "退还押金",
                "支付违约金",
                "赔偿损失"
            ]
        else:
            claims = [
                "停止侵害行为",
                "恢复原状（如适用）",
                "赔偿损失"
            ]

        claims_text = "\n".join([f"{i+1}. {claim}" for i, claim in enumerate(claims)])

        content = f"""# 诉求陈述

## 申请人信息

**姓名：** {user_info.get('name', '未填写')}
**身份证号：** {user_info.get('id_number', '未填写')}
**联系电话：** {user_info.get('phone', '未填写')}
**地址：** {user_info.get('address', '未填写')}

## 诉讼请求

根据案件事实和法律规定，提出以下诉讼请求：

{claims_text}

## 事实与理由

### 案件事实
{(chr(10) + chr(10)).join([fact.description for fact in analysis.facts[:10]])}

### 法律依据
{(chr(10) + chr(10)).join([
    f"{law['law']} {law['category']} {law['article']}"
    for law in analysis.applicable_laws[:3]
])}

### 理由说明

{analysis.liability.basis if analysis.liability else '根据案件事实和法律规定，被告应当承担相应的法律责任。'}

## 金额计算

**损失明细：**
- 直接损失：待评估
- 间接损失：待评估
- 精神损害：待评估
- 其他损失：待评估

**总计：待评估**

（具体金额需根据实际损失和相关证据确定）

## 送达地址

**申请人地址：** {user_info.get('address', '未填写')}
**联系电话：** {user_info.get('phone', '未填写')}
**邮政编码：** {user_info.get('zip_code', '未填写')}

## 承诺

本人承诺上述所提供的信息和材料真实、合法、有效，如有虚假，愿承担相应的法律责任。

---

**申请人签名：** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**日期：** \_\_\_\_\_\_\_\_\_年\_\_\_\_\_月\_\_\_\_\_日
"""

        return Document(
            title="诉求陈述",
            content=content,
            document_type="claims",
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def _generate_complaint(self, analysis: LegalAnalysis,
                           user_info: Dict[str, Any]) -> Document:
        """生成民事起诉状"""
        content = f"""# 民事起诉状

## 原告信息

**姓名：** {user_info.get('name', '未填写')}
**性别：** {user_info.get('gender', '未填写')}
**民族：** {user_info.get('ethnicity', '未填写')}
**出生日期：** {user_info.get('birth_date', '未填写')}
**身份证号：** {user_info.get('id_number', '未填写')}
**住址：** {user_info.get('address', '未填写')}
**联系电话：** {user_info.get('phone', '未填写')}

## 被告信息

**姓名/名称：** 未填写（请根据实际情况填写）
**住址/地址：** 未填写（请根据实际情况填写）
**联系电话：** 未填写（请根据实际情况填写）

## 诉讼请求

1. 判令被告立即停止侵害行为；
2. 判令被告赔偿原告损失，具体金额待司法鉴定后确定；
3. 判令被告承担本案全部诉讼费用。

## 事实与理由

### 基本事实

{(chr(10) + chr(10)).join([fact.description for fact in analysis.facts[:8]])}

### 法律关系

本案属于{analysis.legal_relations[0].type if analysis.legal_relations else '民事纠纷'}，根据相关法律规定，被告应当承担相应的法律责任。

### 法律依据

{(chr(10) + chr(10)).join([
    f"{law['law']} {law['category']} {law['article']}: {law['content']}"
    for law in analysis.applicable_laws[:3]
])}

### 请求理由

根据以上事实和法律依据，被告的行为已构成侵权/违约，给原告造成了相应的损失。为维护原告的合法权益，特向贵院提起诉讼，请求依法裁判。

## 证据和证据来源

1. 身份证明（身份证复印件）
2. 相关协议/合同（如有）
3. 沟通记录（短信、微信、邮件等）
4. 损失证明（发票、收据等）
5. 其他相关证据

（具体证据请根据实际情况补充）

## 此致

\_\_\_\_\_\_\_\_\_\_\_\_\_\_人民法院

## 具状人

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**日期：** {datetime.now().strftime('%Y年%m月%d日')}

---

**附件：**
1. 身份证复印件 1 份
2. 证据清单 1 份
3. 其他材料

**重要提示：**
- 本起诉状为模板，需根据实际情况修改
- 建议咨询专业律师审查
- 注意诉讼时效（一般为3年）
"""

        return Document(
            title="民事起诉状",
            content=content,
            document_type="complaint",
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

    def export_markdown(self, document: Document) -> str:
        """导出为 Markdown 格式"""
        return document.content

    def export_html(self, document: Document) -> str:
        """导出为 HTML 格式"""
        import markdown
        html = markdown.markdown(document.content)
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{document.title}</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1a365d; border-bottom: 2px solid #1a365d; padding-bottom: 10px; }}
        h2 {{ color: #2c5282; margin-top: 30px; }}
        .metadata {{ background: #f7fafc; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    {html}
</body>
</html>
"""
