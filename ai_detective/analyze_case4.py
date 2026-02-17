"""
AI 侦探系统 V3 - 案例单独分析脚本
测试复杂混乱 + 证据不充分的案件
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
    # 读取案例4
    case_file = "/workspace/ai_detective/test_cases/case_004_complex_chaos.txt"

    print_separator("AI 侦探系统 V3 - 案例4分析")
    print("测试：复杂混乱 + 证据不充分的案件")
    print()

    # 打印案例描述
    print_separator("案件描述")
    with open(case_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    print()

    # 创建推理引擎
    reasoner = LegalReasonerV3()

    # 执行分析
    print("🔍 AI 侦探 - 正在分析案件...")
    print()

    analysis = reasoner.analyze(content)

    # 打印分析结果
    print_separator("📌 事实要素提取")
    for i, fact in enumerate(analysis.facts, 1):
        status = "⚠️" if fact.confidence < 0.8 else "✅"
        print(f"{status} {i}. [{fact.category}] {fact.description}")
        print(f"     置信度: {fact.confidence:.2%}")
    print(f"\n共提取 {len(analysis.facts)} 个事实要素")
    print()

    print_separator("⚖️ 争议焦点识别")
    if not analysis.dispute_focuses:
        print("⚠️ 未识别到争议焦点")
        print("   可能原因：案件描述混乱或证据不足")
    else:
        for i, focus in enumerate(analysis.dispute_focuses, 1):
            print(f"{i}. {focus.main_issue}")
            print(f"   详情:")
            for detail in focus.details:
                print(f"      • {detail}")
            print(f"   关键证据:")
            for evidence in focus.critical_evidence:
                print(f"      • {evidence}")
    print()

    print_separator("🔍 证据缺口分析")
    if not analysis.evidence_gaps:
        print("✅ 未发现明显证据缺口")
    else:
        critical_count = sum(1 for g in analysis.evidence_gaps if g.importance == "critical")
        high_count = sum(1 for g in analysis.evidence_gaps if g.importance == "high")
        medium_count = sum(1 for g in analysis.evidence_gaps if g.importance == "medium")

        print(f"发现 {len(analysis.evidence_gaps)} 个证据缺口:")
        print(f"  • 关键证据: {critical_count} 个")
        print(f"  • 重要证据: {high_count} 个")
        print(f"  • 中等证据: {medium_count} 个")
        print()

        for i, gap in enumerate(analysis.evidence_gaps, 1):
            if gap.importance == "critical":
                icon = "🔴"
            elif gap.importance == "high":
                icon = "🟠"
            else:
                icon = "🟡"

            print(f"{icon} {i}. {gap.missing_evidence}")
            print(f"   重要程度: {gap.importance}")
            print(f"   获取难度: {gap.estimated_difficulty}")
            print(f"   获取方式: {gap.how_to_obtain}")
            print()
    print()

    print_separator("🎯 法律责任认定")
    print(f"责任主体: {analysis.liability['liable_party']}")
    print(f"责任类型: {analysis.liability['liability_type']}")
    print(f"责任依据:")
    for line in analysis.liability['basis'].split('\n'):
        print(f"  {line}")
    print(f"严重程度: {analysis.liability['severity']}")
    print()

    print_separator("📊 风险评估")
    print(f"成功概率: {analysis.risk_assessment['success_probability']}")
    print(f"时间成本: {analysis.risk_assessment['time_cost']}")
    print(f"经济成本: {analysis.risk_assessment['economic_cost']}")
    print(f"主要风险: {analysis.risk_assessment['main_risk']}")
    print(f"证据强度: {analysis.risk_assessment['evidence_strength']}")
    print()

    print_separator("💡 关键建议（前10条）")
    for i, suggestion in enumerate(analysis.suggestions[:10], 1):
        print(f"{i}. {suggestion}")
    print()

    print_separator("📋 调查计划（优先任务）")
    for task in analysis.investigation_plan.priority_tasks[:10]:
        print(f"  {task}")
    print()

    print_separator(f"AI 置信度: {analysis.confidence:.2%}")
    print()


if __name__ == "__main__":
    main()
