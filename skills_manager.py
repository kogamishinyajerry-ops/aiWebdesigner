#!/usr/bin/env python3
"""
Skills 和 Agents 管理工具

提供命令行界面来管理和使用 Skills 和 Agents 系统
"""

import sys
import argparse
import asyncio
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from skills import SkillManager, create_skill
from agents import AgentOrchestrator, AgentRegistry, create_agent_template


def list_skills():
    """列出所有技能"""
    print("=" * 60)
    print("技能列表 (Skills)")
    print("=" * 60)
    
    manager = SkillManager()
    skills = manager.discover_skills()
    
    if not skills:
        print("未找到任何技能")
        return
    
    for skill in skills:
        status_icon = "✓" if skill.name in [s['name'] for s in manager.list_skills() if s['loaded']] else "○"
        print(f"\n{status_icon} {skill.name} v{skill.version}")
        print(f"  描述: {skill.description}")
        print(f"  分类: {skill.category}")
        print(f"  能力: {', '.join(skill.capabilities[:3])}{'...' if len(skill.capabilities) > 3 else ''}")
        if skill.required_tools:
            print(f"  依赖工具: {', '.join(skill.required_tools)}")


def load_skill(skill_name):
    """加载指定技能"""
    print(f"正在加载技能: {skill_name}")
    
    manager = SkillManager()
    manager.discover_skills()
    
    if manager.load_skill(skill_name):
        print(f"✓ 成功加载技能: {skill_name}")
    else:
        print(f"✗ 加载技能失败: {skill_name}")


def unload_skill(skill_name):
    """卸载指定技能"""
    print(f"正在卸载技能: {skill_name}")
    
    manager = SkillManager()
    if manager.unload_skill(skill_name):
        print(f"✓ 成功卸载技能: {skill_name}")
    else:
        print(f"✗ 卸载技能失败: {skill_name}")


def create_new_skill(name, description, **kwargs):
    """创建新技能模板"""
    print(f"正在创建技能模板: {name}")
    create_skill(name, description, **kwargs)
    print(f"✓ 技能模板创建完成")


def list_agents():
    """列出所有代理"""
    print("=" * 60)
    print("代理列表 (Agents)")
    print("=" * 60)
    
    orchestrator = AgentOrchestrator()
    registry = AgentRegistry()
    configs = registry.discover_agents()
    
    if not configs:
        print("未找到任何代理")
        return
    
    for config in configs:
        status = "✓ 已注册" if config['name'] in [a['name'] for a in orchestrator.list_agents()] else "○ 未注册"
        print(f"\n{status} {config['name']} v{config.get('version', '1.0.0')}")
        print(f"  描述: {config['description']}")
        print(f"  分类: {config.get('category', 'general')}")
        print(f"  能力: {', '.join(config['capabilities'][:3])}{'...' if len(config['capabilities']) > 3 else ''}")
        if config.get('required_tools'):
            print(f"  依赖工具: {', '.join(config['required_tools'])}")


def create_new_agent(name, description, **kwargs):
    """创建新代理模板"""
    print(f"正在创建代理模板: {name}")
    create_agent_template(name, description, **kwargs)
    print(f"✓ 代理模板创建完成")


async def run_agent_task(agent_name, task_description, params):
    """运行代理任务"""
    print(f"使用代理 '{agent_name}' 执行任务: {task_description}")
    
    orchestrator = AgentOrchestrator()
    registry = AgentRegistry()
    
    # 发现并注册代理
    configs = registry.discover_agents()
    for config in configs:
        # 这里需要实现动态加载代理
        # 实际使用时需要根据配置加载代理类
        pass
    
    result = await orchestrator.execute_task(agent_name, task_description, params)
    
    print(f"\n执行结果:")
    print(f"  成功: {result.success}")
    print(f"  消息: {result.message}")
    print(f"  耗时: {result.execution_time:.2f} 秒")
    if result.steps:
        print(f"  步骤: {' -> '.join(result.steps)}")
    
    return result


async def run_parallel_tasks(tasks):
    """并行运行多个任务"""
    print(f"并行执行 {len(tasks)} 个任务")
    
    orchestrator = AgentOrchestrator()
    results = await orchestrator.execute_parallel(tasks)
    
    print(f"\n执行结果:")
    for i, result in enumerate(results, 1):
        print(f"\n任务 {i}:")
        print(f"  成功: {result.success}")
        print(f"  消息: {result.message}")
        print(f"  耗时: {result.execution_time:.2f} 秒")
    
    return results


async def run_pipeline(pipeline):
    """运行任务管道"""
    print(f"执行包含 {len(pipeline)} 个步骤的管道")
    
    orchestrator = AgentOrchestrator()
    result = await orchestrator.execute_pipeline(pipeline)
    
    print(f"\n管道执行结果:")
    print(f"  成功: {result.success}")
    print(f"  消息: {result.message}")
    print(f"  耗时: {result.execution_time:.2f} 秒")
    
    return result


def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("Skills 和 Agents 管理工具 - 交互式模式")
    print("=" * 60)
    print("\n可用命令:")
    print("  skills        - 列出所有技能")
    print("  agents        - 列出所有代理")
    print("  load <name>   - 加载技能")
    print("  unload <name> - 卸载技能")
    print("  create-skill <name> <description> - 创建新技能")
    print("  create-agent <name> <description> - 创建新代理")
    print("  run <agent> <task> - 运行代理任务")
    print("  help          - 显示帮助")
    print("  quit / exit   - 退出")
    print()
    
    while True:
        try:
            command = input("> ").strip()
            if not command:
                continue
            
            parts = command.split(maxsplit=2)
            cmd = parts[0].lower()
            
            if cmd in ('quit', 'exit'):
                print("再见！")
                break
            
            elif cmd == 'skills':
                list_skills()
            
            elif cmd == 'agents':
                list_agents()
            
            elif cmd == 'load' and len(parts) > 1:
                load_skill(parts[1])
            
            elif cmd == 'unload' and len(parts) > 1:
                unload_skill(parts[1])
            
            elif cmd == 'create-skill' and len(parts) > 2:
                create_new_skill(parts[1], parts[2])
            
            elif cmd == 'create-agent' and len(parts) > 2:
                create_new_agent(parts[1], parts[2])
            
            elif cmd == 'run' and len(parts) > 2:
                # 异步运行任务
                asyncio.run(run_agent_task(parts[1], parts[2], {}))
            
            elif cmd == 'help':
                print("可用命令:")
                print("  skills        - 列出所有技能")
                print("  agents        - 列出所有代理")
                print("  load <name>   - 加载技能")
                print("  unload <name> - 卸载技能")
                print("  create-skill <name> <description> - 创建新技能")
                print("  create-agent <name> <description> - 创建新代理")
                print("  run <agent> <task> - 运行代理任务")
                print("  help          - 显示帮助")
                print("  quit / exit   - 退出")
            
            else:
                print(f"未知命令: {cmd} (输入 'help' 查看帮助)")
        
        except KeyboardInterrupt:
            print("\n使用 'quit' 或 'exit' 退出")
        except Exception as e:
            print(f"错误: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Skills 和 Agents 管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出所有技能
  python skills_manager.py --list-skills
  
  # 列出所有代理
  python skills_manager.py --list-agents
  
  # 加载技能
  python skills_manager.py --load-skill code_analysis
  
  # 卸载技能
  python skills_manager.py --unload-skill code_analysis
  
  # 创建新技能
  python skills_manager.py --create-skill my_skill "我的自定义技能"
  
  # 创建新代理
  python skills_manager.py --create-agent my_agent "我的自定义代理"
  
  # 交互式模式
  python skills_manager.py --interactive
        """
    )
    
    parser.add_argument('--list-skills', action='store_true',
                        help='列出所有技能')
    parser.add_argument('--load-sill', dest='load_skill', metavar='NAME',
                        help='加载指定技能')
    parser.add_argument('--unload-skill', metavar='NAME',
                        help='卸载指定技能')
    parser.add_argument('--create-skill', nargs=2, metavar=('NAME', 'DESCRIPTION'),
                        help='创建新技能模板')
    parser.add_argument('--list-agents', action='store_true',
                        help='列出所有代理')
    parser.add_argument('--create-agent', nargs=2, metavar=('NAME', 'DESCRIPTION'),
                        help='创建新代理模板')
    parser.add_argument('--interactive', action='store_true',
                        help='启动交互式模式')
    
    args = parser.parse_args()
    
    # 如果没有参数，默认进入交互式模式
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    if args.list_skills:
        list_skills()
    
    if args.load_skill:
        load_skill(args.load_skill)
    
    if args.unload_skill:
        unload_skill(args.unload_skill)
    
    if args.create_skill:
        create_new_skill(args.create_skill[0], args.create_skill[1])
    
    if args.list_agents:
        list_agents()
    
    if args.create_agent:
        create_new_agent(args.create_agent[0], args.create_agent[1])
    
    if args.interactive:
        interactive_mode()


if __name__ == "__main__":
    main()
