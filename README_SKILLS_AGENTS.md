# Skills 和 Agents 系统

一个对标 Claude Code 的技能和代理管理系统，提供可扩展的领域特定能力和智能代理框架。

## 概述

这个系统包含两个核心组件：

### Skills（技能）
- **定义**：领域特定的扩展包，提供专业知识和标准化工作流（SOPs）
- **用途**：为特定领域提供专门的能力，如代码分析、Git 操作等
- **特点**：可加载/卸载、有状态管理、支持依赖检查

### Agents（代理）
- **定义**：专门化的子代理，用于处理复杂的多步骤任务
- **用途**：自主完成任务、协作处理跨领域任务
- **特点**：异步执行、支持并行和管道编排、状态跟踪

## 项目结构

```
workspace/
├── skills/                      # Skills 系统
│   ├── __init__.py             # Skills 核心框架
│   ├── code_analysis/          # 代码分析技能
│   │   ├── skill_config.json   # 技能配置
│   │   └── code_analysis.py    # 技能实现
│   └── git_operations/         # Git 操作技能
│       ├── skill_config.json
│       └── git_operations.py
├── agents/                      # Agents 系统
│   ├── __init__.py             # Agents 核心框架
│   ├── code_explorer.py        # 代码探索代理
│   ├── code_explorer.json      # 代理配置
│   ├── file_processor.py       # 文件处理代理
│   ├── file_processor.json
│   ├── code_reviewer.py        # 代码审查代理
│   └── code_reviewer.json
├── skills_manager.py           # 命令行管理工具
└── README_SKILLS_AGENTS.md     # 本文档
```

## 快速开始

### 1. 使用命令行工具

```bash
# 查看所有可用技能
python skills_manager.py --list-skills

# 查看所有可用代理
python skills_manager.py --list-agents

# 进入交互式模式
python skills_manager.py --interactive
```

### 2. 交互式模式命令

```
> skills                      # 列出所有技能
> agents                      # 列出所有代理
> load code_analysis          # 加载代码分析技能
> unload code_analysis        # 卸载代码分析技能
> create-skill my_skill "描述"  # 创建新技能
> create-agent my_agent "描述"  # 创建新代理
> run code_explorer "搜索函数"   # 运行代理任务
> help                        # 显示帮助
> quit                        # 退出
```

## 内置 Skills

### 1. code_analysis（代码分析）

**能力**：
- `analyze_code_structure` - 分析代码结构
- `detect_code_smells` - 检测代码异味
- `find_dependencies` - 查找依赖关系
- `analyze_complexity` - 分析复杂度
- `generate_documentation` - 生成文档

**使用示例**：
```python
from skills import get_skill_manager

manager = get_skill_manager()
manager.load_skill("code_analysis")

skill = manager.get_skill("code_analysis")
result = skill.execute("analyze_code_structure", file_path="example.py")
```

### 2. git_operations（Git 操作）

**能力**：
- `get_status` - 获取 Git 状态
- `create_commit` - 创建提交
- `create_branch` - 创建分支
- `view_history` - 查看历史
- `merge_branches` - 合并分支
- `resolve_conflicts` - 解决冲突

**使用示例**：
```python
from skills import get_skill_manager

manager = get_skill_manager()
manager.load_skill("git_operations")

skill = manager.get_skill("git_operations")
result = skill.execute("get_status", repo_path=".")
```

## 内置 Agents

### 1. code_explorer（代码探索）

**能力**：
- 在代码库中搜索代码
- 查找函数、类的定义
- 查找代码引用
- 分析代码库结构
- 导航依赖关系
- 定位特定功能

**使用示例**：
```python
import asyncio
from agents import get_orchestrator, AgentTask

async def main():
    orchestrator = get_orchestrator()
    result = await orchestrator.execute_with_best_agent(
        "在当前目录搜索所有 Python 文件"
    )
    print(result)

asyncio.run(main())
```

### 2. file_processor（文件处理）

**能力**：
- 批量重命名文件
- 批量转换文件格式
- 按条件筛选文件
- 批量处理文件
- 验证目录结构

### 3. code_reviewer（代码审查）

**能力**：
- 审查代码质量
- 检查代码指标
- 检测潜在 bug
- 提供改进建议
- 检查代码风格
- 验证测试覆盖

## 创建自定义 Skill

### 方法 1：使用命令行工具

```bash
python skills_manager.py --create-skill my_skill "我的自定义技能"
```

### 方法 2：手动创建

1. 创建技能目录：
```bash
mkdir -p skills/my_skill
```

2. 创建配置文件 `skills/my_skill/skill_config.json`：
```json
{
  "name": "my_skill",
  "description": "我的自定义技能",
  "version": "1.0.0",
  "author": "Your Name",
  "category": "general",
  "dependencies": [],
  "capabilities": [
    "execute_task",
    "analyze_data"
  ],
  "required_tools": [],
  "base_directory": "skills/my_skill"
}
```

3. 创建技能实现 `skills/my_skill/my_skill.py`：
```python
from skills import Skill, SkillMetadata

class MySkillSkill(Skill):
    def _on_load(self):
        print(f"加载 {self.metadata.name} 技能...")
    
    def _action_execute_task(self, **kwargs):
        print(f"执行任务: {kwargs}")
        return {"status": "success"}
    
    def _action_analyze_data(self, **kwargs):
        # 实现你的逻辑
        return {"result": "分析完成"}
```

## 创建自定义 Agent

### 方法 1：使用命令行工具

```bash
python skills_manager.py --create-agent my_agent "我的自定义代理"
```

### 方法 2：手动创建

1. 创建代理配置 `agents/my_agent.json`：
```json
{
  "name": "my_agent",
  "description": "我的自定义代理",
  "version": "1.0.0",
  "author": "Your Name",
  "category": "general",
  "capabilities": [
    "process_data",
    "generate_report"
  ],
  "required_tools": [],
  "module": "agents.my_agent",
  "class_name": "MyAgentAgent"
}
```

2. 创建代理实现 `agents/my_agent.py`：
```python
from typing import List
from agents import Agent, AgentTask, AgentResult, AgentCapability

class MyAgentAgent(Agent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            description="我的自定义代理"
        )
        self._capabilities = [
            AgentCapability(
                name="process_data",
                description="处理数据",
                category="general",
                required_tools=[]
            )
        ]
    
    def get_capabilities(self) -> List[AgentCapability]:
        return self._capabilities
    
    async def execute(self, task: AgentTask) -> AgentResult:
        import time
        start_time = time.time()
        
        # 实现你的逻辑
        result_data = self._process_task(task.description, task.params)
        
        execution_time = time.time() - start_time
        return AgentResult(
            success=True,
            data=result_data,
            message="任务执行成功",
            execution_time=execution_time
        )
    
    def _process_task(self, description: str, params: dict):
        # 实现你的处理逻辑
        return {"description": description, "params": params}
```

## 高级用法

### 并行执行多个任务

```python
import asyncio
from agents import get_orchestrator

async def main():
    orchestrator = get_orchestrator()
    
    tasks = [
        {
            "agent_name": "file_processor",
            "description": "处理文件1",
            "params": {"file_path": "file1.py"}
        },
        {
            "agent_name": "file_processor",
            "description": "处理文件2",
            "params": {"file_path": "file2.py"}
        }
    ]
    
    results = await orchestrator.execute_parallel(tasks)
    for result in results:
        print(f"任务结果: {result.success}")

asyncio.run(main())
```

### 任务管道执行

```python
import asyncio
from agents import get_orchestrator

async def main():
    orchestrator = get_orchestrator()
    
    pipeline = [
        {
            "agent_name": "code_explorer",
            "description": "查找所有测试文件",
            "params": {"pattern": "test_*.py"}
        },
        {
            "agent_name": "code_reviewer",
            "description": "审查测试文件质量",
            "params": {}
        },
        {
            "agent_name": "code_reviewer",
            "description": "生成测试报告",
            "params": {}
        }
    ]
    
    result = await orchestrator.execute_pipeline(pipeline)
    print(f"管道执行结果: {result.data}")

asyncio.run(main())
```

### 自动选择最佳代理

```python
import asyncio
from agents import get_orchestrator

async def main():
    orchestrator = get_orchestrator()
    
    # 系统会自动选择最合适的代理
    result = await orchestrator.execute_with_best_agent(
        "分析当前目录下的代码质量"
    )
    print(result)

asyncio.run(main())
```

## 架构设计

### Skills 架构

```
Skill (抽象基类)
  ├── SkillMetadata (元数据)
  ├── _on_load() (加载回调)
  ├── _on_unload() (卸载回调)
  ├── execute(action, **kwargs) (执行动作)
  └── _action_{name}(**kwargs) (具体动作实现)

SkillManager (管理器)
  ├── discover_skills() (发现技能)
  ├── load_skill(name) (加载技能)
  ├── unload_skill(name) (卸载技能)
  └── get_skill(name) (获取技能)
```

### Agents 架构

```
Agent (抽象基类)
  ├── get_capabilities() (获取能力)
  ├── can_handle(task) (判断是否能处理)
  ├── execute(task) (执行任务)
  └── get_status() (获取状态)

AgentOrchestrator (编排器)
  ├── register_agent(agent) (注册代理)
  ├── find_best_agent(task) (查找最佳代理)
  ├── execute_task(name, task) (执行任务)
  ├── execute_parallel(tasks) (并行执行)
  └── execute_pipeline(pipeline) (管道执行)
```

## 最佳实践

### 1. Skill 设计

- 保持单一职责
- 提供清晰的文档字符串
- 实现适当的错误处理
- 添加必要的依赖检查
- 提供有意义的动作名称

### 2. Agent 设计

- 明确能力边界
- 实现智能的任务匹配
- 提供详细的执行步骤
- 支持参数化配置
- 记录执行历史

### 3. 性能优化

- 使用缓存避免重复计算
- 实现增量处理
- 合理设置超时
- 并行化独立任务

## 与 Claude Code 的对标特性

| 特性 | Claude Code | 本系统 |
|------|------------|--------|
| 扩展包系统 | ✓ Skills | ✓ Skills |
| 代理系统 | ✓ Agents | ✓ Agents |
| 领域特定能力 | ✓ | ✓ (code_analysis, git_operations) |
| 专用代理 | ✓ (code-explorer) | ✓ (code_explorer, file_processor, code_reviewer) |
| 并行执行 | ✓ | ✓ |
| 管道编排 | ✓ | ✓ |
| 交互式工具 | ✓ | ✓ (skills_manager.py) |
| 动态加载 | ✓ | ✓ |

## 扩展建议

以下是可以进一步扩展的方向：

### 更多 Skills

- `test_runner` - 测试运行和报告
- `dependency_manager` - 依赖管理
- `docker_operations` - Docker 操作
- `cloud_deploy` - 云部署
- `data_processing` - 数据处理
- `documentation_generator` - 文档生成

### 更多 Agents

- `test_generator` - 自动生成测试
- `refactoring_agent` - 代码重构
- `performance_optimizer` - 性能优化
- `security_scanner` - 安全扫描
- `migration_assistant` - 迁移助手
- `debugger_agent` - 调试助手

## 许可证

本系统基于 Claude Code 的概念构建，为学习和参考目的提供。

## 贡献

欢迎提交问题和拉取请求！
