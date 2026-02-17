# Skills 和 Agents 系统 - 快速参考

## 📦 安装位置

系统已安装到：`~/.codebuddy_skills_agents`

## 🚀 快速开始

### 命令行使用

```bash
# 查看技能
sa --list-skills

# 查看代理
sa --list-agents

# 交互模式
sa --interactive
```

### Python 代码使用

```python
# 方式 1: 已配置 PYTHONPATH（推荐）
from skills import get_skill_manager
from agents import get_orchestrator

# 方式 2: 手动添加路径
import sys
sys.path.append('~/.codebuddy_skills_agents')
from skills import get_skill_manager
from agents import get_orchestrator

# 方式 3: 使用项目助手
from project_integration import ProjectAssistant
assistant = ProjectAssistant(".")
assistant.analyze_file("main.py")
```

## 📚 内置 Skills

### code_analysis（代码分析）
```python
manager = get_skill_manager()
manager.load_skill("code_analysis")
skill = manager.get_skill("code_analysis")

# 分析代码结构
result = skill.execute("analyze_code_structure", file_path="file.py")

# 检测代码异味
result = skill.execute("detect_code_smells", file_path="file.py")

# 查找依赖
result = skill.execute("find_dependencies", file_path="file.py")

# 分析复杂度
result = skill.execute("analyze_complexity", file_path="file.py")

# 生成文档
result = skill.execute("generate_documentation", file_path="file.py")
```

### git_operations（Git 操作）
```python
manager.load_skill("git_operations")
skill = manager.get_skill("git_operations")

# 获取状态
result = skill.execute("get_status", repo_path=".")

# 创建提交
result = skill.execute("create_commit",
    message="feat: add new feature",
    add_all=True
)

# 创建分支
result = skill.execute("create_branch",
    branch_name="feature/new-feature",
    checkout=True
)

# 查看历史
result = skill.execute("view_history", limit=10)

# 合并分支
result = skill.execute("merge_branches",
    source_branch="feature",
    target_branch="main"
)
```

## 🤖 内置 Agents

### code_explorer（代码探索）
```python
import asyncio
from agents import get_orchestrator

async def explore():
    orchestrator = get_orchestrator()
    result = await orchestrator.execute_with_best_agent(
        "搜索所有 Python 文件中的类定义"
    )
    print(result)

asyncio.run(explore())
```

### file_processor（文件处理）
```python
async def process_files():
    orchestrator = get_orchestrator()
    result = await orchestrator.execute_with_best_agent(
        "批量重命名文件"
    )
    print(result)

asyncio.run(process_files())
```

### code_reviewer（代码审查）
```python
async def review():
    orchestrator = get_orchestrator()
    result = await orchestrator.execute_with_best_agent(
        "审查当前目录的代码质量"
    )
    print(result)

asyncio.run(review())
```

## 🎯 常用场景

### 场景 1: 分析新文件
```python
from skills import get_skill_manager

manager = get_skill_manager()
manager.load_skill("code_analysis")
skill = manager.get_skill("code_analysis")

# 分析文件
result = skill.execute("analyze_code_structure", file_path="new_file.py")
print(f"类: {len(result['classes'])}, 函数: {len(result['functions'])}")
```

### 场景 2: 提交前检查
```python
from skills import get_skill_manager

manager = get_skill_manager()
manager.load_skill("git_operations")
skill = skill_manager.get_skill("git_operations")

# 检查状态
status = skill.execute("get_status", repo_path=".")
print(f"待提交: {status['summary']['staged_count']}")
```

### 场景 3: 项目代码审查
```python
import asyncio
from agents import get_orchestrator

async def review_project():
    orchestrator = get_orchestrator()
    result = await orchestrator.execute_with_best_agent(
        "审查项目代码质量"
    )
    if result.success and "summary" in result.data:
        summary = result.data["summary"]
        print(f"文件数: {summary['total_files']}")
        print(f"问题数: {summary['total_issues']}")

asyncio.run(review_project())
```

### 场景 4: 并行处理多个任务
```python
import asyncio
from agents import get_orchestrator

async def parallel_process():
    orchestrator = get_orchestrator()

    tasks = [
        {
            "agent_name": "code_explorer",
            "description": "搜索 Python 文件",
            "params": {"directory": ".", "pattern": "*.py"}
        },
        {
            "agent_name": "file_processor",
            "description": "筛选文件",
            "params": {"extensions": [".py"]}
        }
    ]

    results = await orchestrator.execute_parallel(tasks)
    for result in results:
        print(result.success)

asyncio.run(parallel_process())
```

### 场景 5: 任务管道
```python
import asyncio
from agents import get_orchestrator

async def pipeline():
    orchestrator = get_orchestrator()

    pipeline = [
        {
            "agent_name": "code_explorer",
            "description": "查找所有测试文件",
            "params": {"pattern": "test_*.py"}
        },
        {
            "agent_name": "code_reviewer",
            "description": "审查测试代码",
            "params": {}
        }
    ]

    result = await orchestrator.execute_pipeline(pipeline)
    print(result)

asyncio.run(pipeline())
```

## 🛠️ 创建自定义 Skill

```bash
# 使用命令行
sa --create-skill my_skill "我的技能"

# 或使用 Python
from skills import create_skill
create_skill("my_skill", "我的技能描述", version="1.0.0")
```

然后编辑生成的文件：

```python
# skills/my_skill/my_skill.py
from skills import Skill

class MySkillSkill(Skill):
    def _on_load(self):
        print("加载中...")

    def _action_execute(self, **kwargs):
        # 实现你的逻辑
        return {"result": "成功"}
```

## 🤖 创建自定义 Agent

```bash
# 使用命令行
sa --create-agent my_agent "我的代理"
```

然后编辑生成的文件：

```python
# agents/my_agent.py
from agents import Agent

class MyAgentAgent(Agent):
    def get_capabilities(self):
        # 定义能力
        pass

    async def execute(self, task):
        # 实现你的逻辑
        pass
```

## 📋 交互式命令

```bash
sa --interactive

# 然后可以使用:
skills                      # 列出技能
agents                      # 列出代理
load code_analysis          # 加载技能
unload code_analysis        # 卸载技能
run code_explorer "搜索"    # 运行代理
help                        # 帮助
quit                        # 退出
```

## ⚡ 快捷技巧

### 1. 快速分析当前目录
```bash
sa --interactive
> load code_analysis
> run code_explorer "分析当前目录的 Python 文件"
```

### 2. 快速检查 Git
```python
from skills import get_skill_manager
manager = get_skill_manager()
manager.load_skill("git_operations")
skill = manager.get_skill("git_operations")
print(skill.execute("get_status"))
```

### 3. 一键代码审查
```python
from project_integration import ProjectAssistant
assistant = ProjectAssistant(".")
assistant.review_project()
```

## 🔧 故障排除

### 问题: 找不到模块
```bash
export PYTHONPATH="$PYTHONPATH:$HOME/.codebuddy_skills_agents"
```

### 问题: 命令不可用
```bash
export PATH="$PATH:$HOME/bin"
```

### 问题: 技能加载失败
```bash
# 检查技能配置
sa --list-skills
```

## 📖 更多信息

- **完整文档**: `README_SKILLS_AGENTS.md`
- **安装指南**: `INSTALL_GUIDE.md`
- **使用示例**: `example_usage.py`
- **项目集成**: `project_integration.py`

## ✅ 安装验证

```bash
# 验证命令行
sa --list-skills
sa --list-agents

# 验证 Python 导入
python -c "from skills import get_skill_manager; print('OK')"
python -c "from agents import get_orchestrator; print('OK')"
```

---

现在你可以在任何项目中使用这些强大的技能和代理了！🚀
