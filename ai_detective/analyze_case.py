#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析案件描述"""

from backend.reasoner import LegalReasoner
import json

def main():
    # 创建推理引擎
    reasoner = LegalReasoner()

    # 读取案件描述
    with open('test_cases/case_001_chaos.txt', 'r', encoding='utf-8') as f:
        description = f.read()

    print('🔍 AI 侦探 - 正在分析案件...')
    print('=' * 60)
    print()

    # 执行分析
    analysis = reasoner.analyze(description)

    print('📌 事实要素提取:')
    for fact in analysis.facts:
        print(f'  [{fact.category}] {fact.description}')
        print(f'     置信度: {fact.confidence:.2f}')
    print()

    print('⚖️ 案件类型识别:')
    for relation in analysis.legal_relations:
        print(f'  类型: {relation.type}')
        print(f'  当事人: {relation.parties}')
    print()

    print('📚 适用法律:')
    for i, law in enumerate(analysis.applicable_laws[:3], 1):
        print(f'  {i}. {law["law"]} {law["category"]} {law["article"]}')
        print(f'     {law["content"][:80]}...')
    print()

    print('🎯 法律责任认定:')
    if analysis.liability:
        print(f'  责任主体: {analysis.liability.liable_party}')
        print(f'  责任类型: {analysis.liability.liability_type}')
        print(f'  责任依据: {analysis.liability.basis}')
        print(f'  严重程度: {analysis.liability.severity}')
    print()

    print('📊 风险评估:')
    print(f'  成功概率: {analysis.risk_assessment["success_probability"]}')
    print(f'  时间成本: {analysis.risk_assessment["time_cost"]}')
    print(f'  经济成本: {analysis.risk_assessment["economic_cost"]}')
    print()

    print('💡 建议:')
    for suggestion in analysis.suggestions:
        print(f'  {suggestion}')
    print()

    print('🔬 AI 置信度: {:.2%}'.format(analysis.confidence))

if __name__ == '__main__':
    main()
