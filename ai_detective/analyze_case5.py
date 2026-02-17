"""
AI 侦探系统 V3 - 职业碰瓷式维权案件分析
结合专业警员视角的深度分析
"""

import sys
sys.path.append('/workspace/ai_detective/backend')

from reasoner_v3 import LegalReasonerV3


def print_separator(title=""):
    """打印分隔线"""
    print("=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


def main():
    """主函数"""
    case_file = "/workspace/ai_detective/test_cases/case_005_professional_victimization.txt"

    print_separator("AI 侦探系统 V3 - 职业碰瓷式维权案件分析")
    print("结合专业警员视角")
    print()

    # 读取案例
    with open(case_file, 'r', encoding='utf-8') as f:
        description = f.read()

    print_separator("案件描述")
    print(description)
    print()

    reasoner = LegalReasonerV3()
    analysis = reasoner.analyze(description)

    print_separator("📌 事实要素提取")
    for fact in analysis.facts[:10]:
        status = "⚠️" if fact.confidence < 0.8 else "✅"
        print(f"{status} [{fact.category}] {fact.description}")
    print(f"\n共提取 {len(analysis.facts)} 个事实要素")
    print()

    print_separator("⚖️ 争议焦点识别")
    if analysis.dispute_focuses:
        for i, focus in enumerate(analysis.dispute_focuses, 1):
            print(f"{i}. {focus.main_issue}")
            for detail in focus.details:
                print(f"   • {detail}")
    else:
        print("⚠️ 未识别到争议焦点")
    print()

    print_separator("🔍 证据缺口分析")
    for gap in analysis.evidence_gaps:
        icon = "🔴" if gap.importance == "critical" else "🟠" if gap.importance == "high" else "🟡"
        print(f"{icon} {gap.missing_evidence}")
        print(f"   重要程度: {gap.importance}")
        print(f"   获取方式: {gap.how_to_obtain}")
    print()

    print_separator("📊 风险评估")
    print(f"成功概率: {analysis.risk_assessment['success_probability']}")
    print(f"时间成本: {analysis.risk_assessment['time_cost']}")
    print(f"经济成本: {analysis.risk_assessment['economic_cost']}")
    print(f"主要风险: {analysis.risk_assessment['main_risk']}")
    print(f"证据强度: {analysis.risk_assessment['evidence_strength']}")
    print()

    print_separator("💡 关键建议（前15条）")
    for i, suggestion in enumerate(analysis.suggestions[:15], 1):
        print(f"{i}. {suggestion}")
    print()

    print_separator("📋 调查计划（优先任务）")
    for task in analysis.investigation_plan.priority_tasks[:12]:
        print(f"  {task}")
    print()

    print_separator(f"AI 置信度: {analysis.confidence:.2%}")


if __name__ == "__main__":
    main()
