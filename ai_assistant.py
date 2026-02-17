#!/usr/bin/env python3
"""
AI 助手集成脚本

让我在对话中直接使用 Skills 和 Agents 系统
"""

import sys
import json
from pathlib import Path

# 添加系统路径
sys.path.insert(0, str(Path.home() / ".codebuddy_skills_agents"))

from skills import get_skill_manager
from agents import AgentOrchestrator, AgentTask
from agents.code_explorer import CodeExplorerAgent
from agents.code_reviewer import CodeReviewerAgent
from agents.file_processor import FileProcessorAgent


class AIAssistant:
    """AI 助手 - 集成 Skills 和 Agents"""
    
    def __init__(self):
        self.skill_manager = get_skill_manager()
        self.orchestrator = AgentOrchestrator()
        self._initialized = False
    
    def init(self):
        """初始化系统"""
        if self._initialized:
            return
        
        # 加载技能
        self.skill_manager.discover_skills()
        self.skill_manager.load_skill("code_analysis")
        self.skill_manager.load_skill("git_operations")
        
        # 注册代理
        self.orchestrator.register_agent(CodeExplorerAgent())
        self.orchestrator.register_agent(FileProcessorAgent())
        self.orchestrator.register_agent(CodeReviewerAgent())
        
        self._initialized = True
    
    def analyze_file(self, file_path):
        """分析文件"""
        self.init()
        skill = self.skill_manager.get_skill("code_analysis")
        return skill.execute("analyze_code_structure", file_path=file_path)
    
    def get_git_status(self, repo_path="."):
        """获取 Git 状态"""
        self.init()
        skill = self.skill_manager.get_skill("git_operations")
        return skill.execute("get_status", repo_path=repo_path)
    
    def find_dependencies(self, file_path):
        """查找依赖"""
        self.init()
        skill = self.skill_manager.get_skill("code_analysis")
        return skill.execute("find_dependencies", file_path=file_path)
    
    def analyze_complexity(self, file_path):
        """分析复杂度"""
        self.init()
        skill = self.skill_manager.get_skill("code_analysis")
        return skill.execute("analyze_complexity", file_path=file_path)
    
    def detect_bugs(self, file_path):
        """检测 Bug"""
        import asyncio
        self.init()
        
        reviewer = CodeReviewerAgent()
        task = AgentTask(f"检测 {file_path} 的 bug", {"file_path": file_path})
        
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, reviewer.execute(task))
                return future.result().data
        else:
            return asyncio.run(reviewer.execute(task)).data
    
    def review_code(self, file_path):
        """审查代码"""
        import asyncio
        self.init()
        
        reviewer = CodeReviewerAgent()
        task = AgentTask(f"审查 {file_path}", {"file_path": file_path})
        
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, reviewer.execute(task))
                return future.result().data
        else:
            return asyncio.run(reviewer.execute(task)).data
    
    def search_code(self, query, directory="."):
        """搜索代码"""
        import asyncio
        self.init()
        
        result = asyncio.run(
            self.orchestrator.execute_with_best_agent(
                f"在 {directory} 中搜索: {query}"
            )
        )
        return result.data
    
    def process_files(self, operation, directory=".", **params):
        """处理文件"""
        import asyncio
        self.init()
        
        result = asyncio.run(
            self.orchestrator.execute_task(
                "file_processor",
                operation,
                {**params, "directory": directory}
            )
        )
        return result.data


# 创建全局实例
assistant = AIAssistant()


def analyze_file(file_path):
    """快捷函数：分析文件"""
    result = assistant.analyze_file(file_path)
    print(f"\n📄 文件分析: {file_path}")
    print(f"  语言: {result.get('language', 'unknown')}")
    print(f"  行数: {result.get('lines', 0)}")
    print(f"  类: {len(result.get('classes', []))}")
    print(f"  函数: {len(result.get('functions', []))}")
    print(f"  导入: {len(result.get('imports', []))}")
    return result


def git_status(repo_path="."):
    """快捷函数：Git 状态"""
    result = assistant.get_git_status(repo_path)
    print(f"\n📊 Git 状态: {repo_path}")
    print(f"  分支: {result.get('current_branch', 'unknown')}")
    print(f"  已暂存: {result['summary'].get('staged_count', 0)}")
    print(f"  未暂存: {result['summary'].get('unstaged_count', 0)}")
    print(f"  未跟踪: {result['summary'].get('untracked_count', 0)}")
    return result


def complexity(file_path):
    """快捷函数：复杂度分析"""
    result = assistant.analyze_complexity(file_path)
    print(f"\n🔍 复杂度分析: {file_path}")
    print(f"  总复杂度: {result.get('total_complexity', 0)}")
    print(f"  平均复杂度: {result.get('average_complexity', 0)}")
    print(f"  整体等级: {result.get('overall_level', 'unknown')}")
    return result


def detect_bugs(file_path):
    """快捷函数：检测 Bug"""
    result = assistant.detect_bugs(file_path)
    bugs = result.get('bugs', [])
    print(f"\n🐛 Bug 检测: {file_path}")
    print(f"  发现 {len(bugs)} 个潜在问题")
    for bug in bugs[:5]:  # 只显示前5个
        print(f"    - {bug.get('type', '')}: {bug.get('message', '')}")
    if len(bugs) > 5:
        print(f"    ... 还有 {len(bugs) - 5} 个")
    return result


def review_code(file_path):
    """快捷函数：代码审查"""
    result = assistant.review_code(file_path)
    print(f"\n✅ 代码审查: {file_path}")
    
    if "summary" in result:
        summary = result["summary"]
        print(f"  问题: {summary.get('total_issues', 0)}")
        print(f"  警告: {summary.get('total_warnings', 0)}")
        print(f"  建议: {summary.get('total_suggestions', 0)}")
    elif "suggestions" in result:
        suggestions = result.get("suggestions", [])
        print(f"  建议: {len(suggestions)}")
    
    return result


def dependencies(file_path):
    """快捷函数：查看依赖"""
    result = assistant.find_dependencies(file_path)
    print(f"\n🔗 依赖分析: {file_path}")
    print(f"  内部依赖: {result.get('internal_dependencies', [])}")
    print(f"  外部依赖: {result.get('external_dependencies', [])}")
    return result


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 助手命令")
    parser.add_argument("command", choices=["analyze", "git", "complexity", "bugs", "review", "deps"])
    parser.add_argument("path", nargs="?", default=".")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        analyze_file(args.path)
    elif args.command == "git":
        git_status(args.path)
    elif args.command == "complexity":
        complexity(args.path)
    elif args.command == "bugs":
        detect_bugs(args.path)
    elif args.command == "review":
        review_code(args.path)
    elif args.command == "deps":
        dependencies(args.path)
