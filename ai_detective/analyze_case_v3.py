"""
AI 侦探系统 V3 - 测试脚本
测试网络侵权案件和证据不充分案件的分析能力
"""

import sys
sys.path.append('/workspace/ai_detective/backend')

from reasoner_v3 import LegalReasonerV3
import json


def print_separator(title=""):
    """打印分隔线"""
    print("=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


def print_case_info(case_file: str):
    """打印案件信息"""
    print_separator("案件描述")
    with open(case_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    print()


def print_facts(facts):
    """打印事实要素"""
    print_separator("📌 事实要素提取")
    for i, fact in enumerate(facts, 1):
        status = "⚠️" if fact.confidence < 0.8 else "✅"
        print(f"{status} {i}. [{fact.category}] {fact.description}")
        print(f"     置信度: {fact.confidence:.2%}")
    print(f"\n共提取 {len(facts)} 个事实要素")
    print()


def print_dispute_focuses(focuses):
    """打印争议焦点"""
    print_separator("⚖️ 争议焦点识别")
    for i, focus in enumerate(focuses, 1):
        print(f"{i}. {focus.main_issue}")
        print(f"   详情:")
        for detail in focus.details:
            print(f"      • {detail}")
        print(f"   关键证据:")
        for evidence in focus.critical_evidence:
            print(f"      • {evidence}")
    print()


def print_laws(laws):
    """打印适用法律"""
    print_separator("📚 适用法律条文")
    for i, law in enumerate(laws, 1):
        print(f"{i}. {law['law']} {law['category']} {law['article']}")
        print(f"   {law['content']}")
        print(f"   适用: {law['application']}")
        print(f"   相关问题: {law['related_issue']}")
        print(f"   相关性: {law['relevance']:.2%}")
        print()


def print_evidence_gaps(gaps):
    """打印证据缺口分析"""
    print_separator("🔍 证据缺口分析")

    if not gaps:
        print("✅ 未发现明显证据缺口，证据较为完整")
    else:
        critical_count = sum(1 for g in gaps if g.importance == "critical")
        high_count = sum(1 for g in gaps if g.importance == "high")
        medium_count = sum(1 for g in gaps if g.importance == "medium")

        print(f"发现 {len(gaps)} 个证据缺口:")
        print(f"  • 关键证据: {critical_count} 个")
        print(f"  • 重要证据: {high_count} 个")
        print(f"  • 中等证据: {medium_count} 个")
        print()

        for i, gap in enumerate(gaps, 1):
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


def print_investigation_plan(plan):
    """打印调查计划"""
    print_separator("📋 调查计划")

    if plan.priority_tasks:
        print("【优先任务】")
        for task in plan.priority_tasks:
            print(f"  {task}")
        print()

    if plan.secondary_tasks:
        print("【重要任务】")
        for task in plan.secondary_tasks:
            print(f"  {task}")
        print()

    if plan.optional_tasks:
        print("【可选任务】")
        for task in plan.optional_tasks:
            print(f"  {task}")
        print()


def print_liability(liability):
    """打印责任认定"""
    print_separator("🎯 法律责任认定")
    print(f"责任主体: {liability['liable_party']}")
    print(f"责任类型: {liability['liability_type']}")
    print(f"责任依据:\n{liability['basis']}")
    print(f"严重程度: {liability['severity']}")
    print(f"损害类型: {liability['damages']['type']}")
    print(f"预估金额: {liability['damages']['estimated_amount']}")
    print(f"证据强度: {liability['damages']['evidence_level']}")
    print()


def print_risk(risk):
    """打印风险评估"""
    print_separator("📊 风险评估")
    print(f"成功概率: {risk['success_probability']}")
    print(f"时间成本: {risk['time_cost']}")
    print(f"经济成本: {risk['economic_cost']}")
    print(f"主要风险:")
    print(f"  • {risk['main_risk']}")
    print(f"证据强度: {risk['evidence_strength']}")
    print()


def print_suggestions(suggestions):
    """打印建议"""
    print_separator("💡 法律建议")
    for suggestion in suggestions:
        print(suggestion)
    print()


def print_litigation_strategy(strategy):
    """打印诉讼策略"""
    print_separator("⚔️ 诉讼策略")
    for item in strategy:
        print(item)
    print()


def analyze_case(case_file: str, case_name: str):
    """分析单个案例"""
    print_separator(f"开始分析案例: {case_name}")
    print()

    # 读取案件描述
    with open(case_file, 'r', encoding='utf-8') as f:
        description = f.read()

    # 创建推理引擎
    reasoner = LegalReasonerV3()

    # 执行分析
    print("🔍 AI 侦探 - 正在分析案件...")
    print()

    analysis = reasoner.analyze(description)

    # 打印分析结果
    print_facts(analysis.facts)
    print_dispute_focuses(analysis.dispute_focuses)
    print_evidence_gaps(analysis.evidence_gaps)
    print_investigation_plan(analysis.investigation_plan)
    print_laws(analysis.applicable_laws)
    print_liability(analysis.liability)
    print_risk(analysis.risk_assessment)
    print_litigation_strategy(analysis.litigation_strategy)
    print_suggestions(analysis.suggestions)

    print_separator(f"AI 置信度: {analysis.confidence:.2%}")
    print()

    return analysis


def main():
    """主函数"""
    print_separator("AI 侦探系统 V3 - 深度测试")
    print("测试网络侵权案件和证据不充分案件")
    print()

    # 测试案例1：小红书恶意发帖
    case1_file = "/workspace/ai_detective/test_cases/case_002_xiaohongshu.txt"
    analysis1 = analyze_case(case1_file, "小红书恶意发帖案件")

    print("\n" * 2)
    print_separator("=" * 20)
    print("\n" * 2)

    # 测试案例2：证据不充分
    case2_file = "/workspace/ai_detective/test_cases/case_003_incomplete_evidence.txt"
    analysis2 = analyze_case(case2_file, "证据不充分案件")

    # 保存分析结果
    print_separator("分析完成")
    print(f"✅ 案例1分析完成，置信度: {analysis1.confidence:.2%}")
    print(f"✅ 案例2分析完成，置信度: {analysis2.confidence:.2%}")
    print()


if __name__ == "__main__":
    main()
