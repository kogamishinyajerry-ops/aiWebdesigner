#!/usr/bin/env python3
"""
Skills 和 Agents 系统使用示例

演示如何使用 Skills 和 Agents 系统完成各种任务
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))


def example_skills():
    """示例：使用 Skills"""
    print("=" * 60)
    print("Skills 使用示例")
    print("=" * 60)
    
    from skills import get_skill_manager
    
    # 获取技能管理器
    manager = get_skill_manager()
    
    # 发现技能
    print("\n1. 发现技能:")
    skills = manager.discover_skills()
    for skill in skills:
        print(f"   - {skill.name}: {skill.description}")
    
    # 加载代码分析技能
    print("\n2. 加载 code_analysis 技能:")
    if manager.load_skill("code_analysis"):
        print("   ✓ 技能加载成功")
        
        # 获取技能实例
        skill = manager.get_skill("code_analysis")
        
        # 执行技能动作
        print("\n3. 执行代码结构分析:")
        result = skill.execute("analyze_code_structure", file_path="/workspace/Codes/use_model.py")
        
        if "error" not in result:
            print(f"   文件: {result['file_path']}")
            print(f"   语言: {result['language']}")
            print(f"   行数: {result['lines']}")
            print(f"   类: {len(result['classes'])}")
            print(f"   函数: {len(result['functions'])}")
            print(f"   导入: {len(result['imports'])}")
        else:
            print(f"   ✗ 错误: {result['error']}")
        
        # 执行复杂度分析
        print("\n4. 执行复杂度分析:")
        result = skill.execute("analyze_complexity", file_path="/workspace/Codes/use_model.py")
        
        if "error" not in result:
            print(f"   总复杂度: {result['total_complexity']}")
            print(f"   平均复杂度: {result['average_complexity']}")
            print(f"   整体等级: {result['overall_level']}")
        else:
            print(f"   ✗ 错误: {result['error']}")
    else:
        print("   ✗ 技能加载失败")


def example_git_operations():
    """示例：使用 Git 操作技能"""
    print("\n" + "=" * 60)
    print("Git 操作技能示例")
    print("=" * 60)
    
    from skills import get_skill_manager
    
    manager = get_skill_manager()
    
    # 加载 Git 操作技能
    print("\n1. 加载 git_operations 技能:")
    if manager.load_skill("git_operations"):
        print("   ✓ 技能加载成功")
        
        skill = manager.get_skill("git_operations")
        
        # 获取 Git 状态
        print("\n2. 获取 Git 状态:")
        result = skill.execute("get_status", repo_path="/workspace")
        
        if "error" not in result:
            print(f"   当前分支: {result['current_branch']}")
            print(f"   已暂存: {result['summary']['staged_count']}")
            print(f"   未暂存: {result['summary']['unstaged_count']}")
            print(f"   未跟踪: {result['summary']['untracked_count']}")
        else:
            print(f"   ✗ 错误: {result['error']}")
    else:
        print("   ✗ 技能加载失败")


async def example_agents():
    """示例：使用 Agents"""
    print("\n" + "=" * 60)
    print("Agents 使用示例")
    print("=" * 60)
    
    from agents import AgentOrchestrator, AgentTask
    
    # 创建编排器
    orchestrator = AgentOrchestrator()
    
    # 注册代码探索代理
    print("\n1. 注册代码探索代理:")
    from agents.code_explorer import CodeExplorerAgent
    explorer = CodeExplorerAgent()
    orchestrator.register_agent(explorer)
    print("   ✓ 代理已注册")
    
    # 列出所有代理
    print("\n2. 列出所有代理:")
    agents = orchestrator.list_agents()
    for agent in agents:
        print(f"   - {agent['name']}: {agent['description']}")
    
    # 执行任务
    print("\n3. 执行搜索任务:")
    task = AgentTask(
        description="在当前目录搜索 Python 文件",
        params={"directory": "/workspace", "pattern": "*.py"}
    )
    
    result = await orchestrator.execute_task("code_explorer", task.description, task.params)
    
    print(f"   成功: {result.success}")
    print(f"   消息: {result.message}")
    print(f"   耗时: {result.execution_time:.2f} 秒")
    if result.steps:
        print(f"   步骤: {' -> '.join(result.steps)}")


async def example_parallel_execution():
    """示例：并行执行多个任务"""
    print("\n" + "=" * 60)
    print("并行执行示例")
    print("=" * 60)
    
    from agents import AgentOrchestrator
    from agents.code_explorer import CodeExplorerAgent
    from agents.file_processor import FileProcessorAgent
    
    # 创建编排器
    orchestrator = AgentOrchestrator()
    
    # 注册代理
    explorer = CodeExplorerAgent()
    processor = FileProcessorAgent()
    orchestrator.register_agent(explorer)
    orchestrator.register_agent(processor)
    
    # 定义多个任务
    tasks = [
        {
            "agent_name": "code_explorer",
            "description": "搜索 Python 文件",
            "params": {"directory": "/workspace", "pattern": "*.py"}
        },
        {
            "agent_name": "file_processor",
            "description": "筛选文件",
            "params": {
                "directory": "/workspace",
                "extensions": [".py", ".md"]
            }
        }
    ]
    
    print(f"\n并行执行 {len(tasks)} 个任务...")
    
    import time
    start_time = time.time()
    
    results = await orchestrator.execute_parallel(tasks)
    
    end_time = time.time()
    
    print(f"\n执行完成，总耗时: {end_time - start_time:.2f} 秒")
    for i, result in enumerate(results, 1):
        print(f"\n任务 {i}:")
        print(f"  成功: {result.success}")
        print(f"  消息: {result.message}")
        print(f"  耗时: {result.execution_time:.2f} 秒")


async def example_pipeline():
    """示例：任务管道执行"""
    print("\n" + "=" * 60)
    print("任务管道示例")
    print("=" * 60)
    
    from agents import AgentOrchestrator
    from agents.code_explorer import CodeExplorerAgent
    from agents.code_reviewer import CodeReviewerAgent
    
    # 创建编排器
    orchestrator = AgentOrchestrator()
    
    # 注册代理
    explorer = CodeExplorerAgent()
    reviewer = CodeReviewerAgent()
    orchestrator.register_agent(explorer)
    orchestrator.register_agent(reviewer)
    
    # 定义管道
    pipeline = [
        {
            "agent_name": "code_explorer",
            "description": "查找所有 Python 文件",
            "params": {"directory": "/workspace/Codes"}
        },
        {
            "agent_name": "code_reviewer",
            "description": "审查代码质量",
            "params": {}
        }
    ]
    
    print(f"\n执行包含 {len(pipeline)} 个步骤的管道...")
    
    result = await orchestrator.execute_pipeline(pipeline)
    
    print(f"\n管道执行完成:")
    print(f"  成功: {result.success}")
    print(f"  消息: {result.message}")
    print(f"  耗时: {result.execution_time:.2f} 秒")


async def main():
    """主函数"""
    # 运行 Skills 示例
    example_skills()
    example_git_operations()
    
    # 运行 Agents 示例
    await example_agents()
    
    # 运行高级示例
    await example_parallel_execution()
    await example_pipeline()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    # 运行所有示例
    asyncio.run(main())
