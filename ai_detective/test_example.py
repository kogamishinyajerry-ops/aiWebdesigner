"""
AI 侦探 - 测试示例
Test Examples for AI Detective
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get(f"{API_BASE}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()

def test_analyze():
    """测试案件分析"""
    print("🔍 测试案件分析...")
    test_case = {
        "description": """
        未经本人同意，某互联网公司在2023年12月使用我的肖像照片用于商业广告宣传。
        照片是在朋友圈发布的个人照片，该公司未经我允许就下载并使用在他们的产品宣传中。
        我发现后联系该公司要求删除和道歉，但对方拒绝。
        我的肖像权受到了严重侵害，造成了精神损害。
        """,
        "context": {}
    }

    response = requests.post(f"{API_BASE}/analyze", json=test_case)
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print("\n=== 分析结果 ===")
        print(f"\n事实要素 ({len(result['facts'])}):")
        for fact in result['facts']:
            print(f"  • {fact['description']}")

        if result['legal_relations']:
            print(f"\n法律关系:")
            for rel in result['legal_relations']:
                print(f"  • 类型: {rel['type']}")
                print(f"    当事人: {rel['parties']}")

        if result['applicable_laws']:
            print(f"\n适用法律 ({len(result['applicable_laws'])}):")
            for law in result['applicable_laws']:
                print(f"  • {law['law']} {law['article']}")
                print(f"    {law['content'][:80]}...")

        if result['liability']:
            print(f"\n法律责任:")
            print(f"  • 责任主体: {result['liability']['liable_party']}")
            print(f"  • 责任类型: {result['liability']['liability_type']}")
            print(f"  • 责任依据: {result['liability']['basis']}")

        if result['risk_assessment']:
            print(f"\n风险评估:")
            print(f"  • 成功概率: {result['risk_assessment']['success_probability']}")
            print(f"  • 时间成本: {result['risk_assessment']['time_cost']}")
            print(f"  • 经济成本: {result['risk_assessment']['economic_cost']}")

        if result['suggestions']:
            print(f"\n建议:")
            for suggestion in result['suggestions']:
                print(f"  • {suggestion}")

        print(f"\nAI 置信度: {result['confidence']:.2%}")
    else:
        print(f"错误: {response.text}")

    print()

def test_generate_documents():
    """测试材料生成"""
    print("🔍 测试材料生成...")
    request = {
        "description": "未经本人同意，某公司使用我的肖像照片进行商业广告宣传。",
        "user_info": {
            "name": "张三",
            "phone": "13800138000",
            "address": "北京市朝阳区某街道"
        }
    }

    response = requests.post(f"{API_BASE}/documents/generate", json=request)
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n生成了 {len(result['documents'])} 份文档:")
        for doc in result['documents']:
            print(f"\n  📄 {doc['title']}")
            print(f"     类型: {doc['document_type']}")
            print(f"     预览: {doc['content'][:100]}...")
    else:
        print(f"错误: {response.text}")

    print()

def test_evidence_suggest():
    """测试证据建议"""
    print("🔍 测试证据建议...")
    case_type = "肖像权侵权"

    response = requests.get(f"{API_BASE}/evidence/suggest/{case_type}")
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n案件类型: {result['case_type']}")
        print(f"\n建议证据:")
        for evidence in result['suggested_evidences']:
            print(f"  • {evidence}")
    else:
        print(f"错误: {response.text}")

    print()

def test_intent_detect():
    """测试意图检测"""
    print("🔍 测试意图检测...")
    message = "我想报案，对方侵犯了我的肖像权"

    response = requests.get(f"{API_BASE}/intent/detect", params={"message": message})
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\n检测到的意图: {result['intent']}")
        print(f"置信度: {result['confidence']:.2%}")
        print(f"实体: {result['entities']}")
    else:
        print(f"错误: {response.text}")

    print()

if __name__ == "__main__":
    print("=" * 60)
    print("AI 侦探 - 功能测试")
    print("=" * 60)
    print()

    # 测试各个功能
    try:
        test_health()
        test_analyze()
        test_generate_documents()
        test_evidence_suggest()
        test_intent_detect()

        print("=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("❌ 错误: 无法连接到服务器")
        print("请确保后端服务已启动: cd ai_detective/backend && python main.py")
    except Exception as e:
        print(f"❌ 错误: {e}")
