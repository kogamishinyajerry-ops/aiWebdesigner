#!/usr/bin/env python3
"""
项目集成示例

演示如何在你的 Python 项目中使用已安装的 Skills 和 Agents 系统
"""

import asyncio
from pathlib import Path

# 方式 1: 如果已经配置了 PYTHONPATH，直接导入
try:
    from skills import get_skill_manager
    from agents import AgentOrchestrator, AgentTask
    from agents.code_explorer import CodeExplorerAgent
    from agents.code_reviewer import CodeReviewerAgent
    from agents.file_processor import FileProcessorAgent
    print("✓ 已从系统导入 Skills 和 Agents")
except ImportError:
    # 方式 2: 如果未配置 PYTHONPATH，手动添加路径
    import sys
    sys.path.insert(0, str(Path.home() / ".codebuddy_skills_agents"))
    
    from skills import get_skill_manager
    from agents import AgentOrchestrator, AgentTask
    from agents.code_explorer import CodeExplorerAgent
    from agents.code_reviewer import CodeReviewerAgent
    from agents.file_processor import FileProcessorAgent
    print("✓ 已手动添加路径并导入 Skills 和 Agents")


class ProjectAssistant:
    """项目助手 - 集成 Skills 和 Agents 到你的项目中"""
    
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.skill_manager = get_skill_manager()
        self.orchestrator = AgentOrchestrator()
        self._initialized = False
    
    def initialize(self):
        """初始化 - 加载需要的技能和代理"""
        if self._initialized:
            return
        
        print("初始化项目助手...")
        
        # 加载技能
        print("  - 加载技能...")
        self.skill_manager.discover_skills()
        self.skill_manager.load_skill("code_analysis")
        self.skill_manager.load_skill("git_operations")
        
        # 注册代理
        print("  - 注册代理...")
        self.orchestrator.register_agent(CodeExplorerAgent())
        self.orchestrator.register_agent(FileProcessorAgent())
        self.orchestrator.register_agent(CodeReviewerAgent())
        
        print("✓ 项目助手初始化完成")
        self._initialized = True
    
    def analyze_file(self, file_path):
        """分析单个文件"""
        print(f"\n分析文件: {file_path}")
        
        if not self._initialized:
            self.initialize()
        
        skill = self.skill_manager.get_skill("code_analysis")
        
        # 结构分析
        structure = skill.execute("analyze_code_structure", file_path=file_path)
        if "error" not in structure:
            print(f"  语言: {structure['language']}")
            print(f"  行数: {structure['lines']}")
            print(f"  类: {len(structure['classes'])}")
            print(f"  函数: {len(structure['functions'])}")
        
        # 复杂度分析
        complexity = skill.execute("analyze_complexity", file_path=file_path)
        if "error" not in complexity:
            print(f"  复杂度: {complexity['total_complexity']} (等级: {complexity['overall_level']})")
        
        # Bug 检测
        from agents.code_reviewer import CodeReviewerAgent
        reviewer = CodeReviewerAgent()
        task = AgentTask(f"检测 {file_path} 的 bug", {"file_path": file_path})

        # 在事件循环中直接 await（不使用 asyncio.run）
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果在异步上下文中，创建任务
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, reviewer.execute(task))
                result = future.result()
        else:
            result = asyncio.run(reviewer.execute(task))
        if result.success and "bugs" in result.data:
            bugs = result.data["bugs"]
            if bugs:
                print(f"  ⚠️  发现 {len(bugs)} 个潜在问题")
    
    def review_project(self):
        """审查整个项目"""
        print(f"\n审查项目: {self.project_root}")
        
        if not self._initialized:
            self.initialize()
        
        # 查找所有 Python 文件
        python_files = list(self.project_root.rglob("*.py"))
        print(f"  找到 {len(python_files)} 个 Python 文件")
        
        # 使用代理审查
        task = AgentTask(
            "审查项目代码质量",
            {"directory": str(self.project_root)}
        )
        
        # 同步执行异步任务
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    self.orchestrator.execute_task(
                        "code_reviewer",
                        task.description,
                        task.params
                    )
                )
                result = future.result()
        else:
            result = asyncio.run(
                self.orchestrator.execute_task(
                    "code_reviewer",
                    task.description,
                    task.params
                )
            )
        
        if result.success:
            print(f"  ✓ 审查完成")
            if "summary" in result.data:
                summary = result.data["summary"]
                print(f"  文件数: {summary.get('total_files', 0)}")
                print(f"  问题数: {summary.get('total_issues', 0)}")
                print(f"  警告数: {summary.get('total_warnings', 0)}")
    
    def check_git_status(self):
        """检查 Git 状态"""
        print(f"\n检查 Git 状态: {self.project_root}")
        
        if not self._initialized:
            self.initialize()
        
        skill = self.skill_manager.get_skill("git_operations")
        status = skill.execute("get_status", repo_path=str(self.project_root))
        
        if "error" not in status:
            print(f"  当前分支: {status['current_branch']}")
            print(f"  已暂存: {status['summary']['staged_count']}")
            print(f"  未暂存: {status['summary']['unstaged_count']}")
            print(f"  未跟踪: {status['summary']['untracked_count']}")
    
    def find_implementation(self, feature):
        """查找功能实现"""
        print(f"\n查找功能: {feature}")
        
        if not self._initialized:
            self.initialize()
        
        # 同步执行异步任务
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    self.orchestrator.execute_with_best_agent(
                        f"在当前目录查找 {feature} 的实现"
                    )
                )
                result = future.result()
        else:
            result = asyncio.run(
                self.orchestrator.execute_with_best_agent(
                    f"在当前目录查找 {feature} 的实现"
                )
            )
        
        print(f"  {result.message}")
        if result.data and "locations" in result.data:
            for loc in result.data["locations"]:
                print(f"    - {loc}")
    
    def get_git_history(self, limit=10):
        """获取 Git 历史"""
        print(f"\n获取最近 {limit} 次提交:")
        
        if not self._initialized:
            self.initialize()
        
        skill = self.skill_manager.get_skill("git_operations")
        history = skill.execute("view_history", limit=limit)
        
        if "error" not in history:
            for commit in history["commits"]:
                short_hash = commit["hash"][:8]
                print(f"  {short_hash} - {commit['author']}: {commit['message']}")


# 使用示例
async def main():
    print("=" * 60)
    print("Skills 和 Agents 项目集成示例")
    print("=" * 60)
    
    # 创建项目助手
    assistant = ProjectAssistant("/workspace/Codes")
    
    # 示例 1: 分析文件
    print("\n" + "=" * 60)
    print("示例 1: 分析单个文件")
    print("=" * 60)
    assistant.analyze_file("/workspace/Codes/use_model.py")
    
    # 示例 2: 检查 Git 状态
    print("\n" + "=" * 60)
    print("示例 2: 检查 Git 状态")
    print("=" * 60)
    assistant.check_git_status()
    
    # 示例 3: 审查项目
    print("\n" + "=" * 60)
    print("示例 3: 审查项目")
    print("=" * 60)
    assistant.review_project()
    
    # 示例 4: 查找功能
    print("\n" + "=" * 60)
    print("示例 4: 查找功能实现")
    print("=" * 60)
    assistant.find_implementation("OllamaClient")
    
    # 示例 5: Git 历史
    print("\n" + "=" * 60)
    print("示例 5: Git 历史记录")
    print("=" * 60)
    assistant.get_git_history(limit=5)
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())
    
    print("\n" + "=" * 60)
    print("现在你可以在自己的项目中使用这个助手了！")
    print("=" * 60)
    print("\n在你的项目代码中:")
    print("""
from project_integration import ProjectAssistant

# 创建助手
assistant = ProjectAssistant(".")

# 使用功能
assistant.analyze_file("main.py")
assistant.check_git_status()
await assistant.review_project()
""")
