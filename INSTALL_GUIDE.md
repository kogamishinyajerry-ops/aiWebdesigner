# 本地环境安装指南

本指南将帮助你将 Skills 和 Agents 系统安装到本地环境，让你在未来的编码工作中都能使用这些强大的功能。

## 📋 安装方式

### 方式一：一键配置（推荐）

运行自动配置脚本：

```bash
cd /workspace
python setup_local.py
```

这个脚本会自动：
1. 在 `~/.codebuddy_skills_agents` 创建本地安装目录
2. 复制所有 Skills 和 Agents 文件
3. 创建便捷命令 `sa`
4. 更新你的 shell 配置

配置完成后，在**新的终端**中执行：

```bash
# 重启终端后，直接使用便捷命令
sa --list-skills
sa --list-agents
sa --interactive
```

### 方式二：手动配置

#### 1. 复制文件到本地

```bash
# 创建本地目录
mkdir -p ~/.codebuddy_skills_agents

# 复制文件
cp -r /workspace/skills ~/.codebuddy_skills_agents/
cp -r /workspace/agents ~/.codebuddy_skills_agents/
cp /workspace/skills_manager.py ~/.codebuddy_skills_agents/
```

#### 2. 创建环境变量

编辑你的 shell 配置文件（`.zshrc` 或 `.bashrc`）：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export PYTHONPATH="$PYTHONPATH:$HOME/.codebuddy_skills_agents"
```

使配置生效：

```bash
source ~/.zshrc  # 或 source ~/.bashrc
```

### 方式三：作为 Python 包安装

#### 1. 创建 `setup.py`

```bash
cd /workspace
python setup_local.py  # 这会创建 setup.py
```

#### 2. 可编辑安装

```bash
pip install -e .
```

安装后，你可以在任何 Python 项目中导入：

```python
from skills import get_skill_manager
from agents import get_orchestrator
```

## 🚀 验证安装

### 测试 Skills 系统

```bash
# 使用便捷命令
sa --list-skills

# 或者直接运行脚本
python ~/.codebuddy_skills_agents/skills_manager.py --list-skills
```

预期输出：
```
============================================================
技能列表 (Skills)
============================================================

○ code_analysis v1.0.0
  描述: 代码分析技能，用于理解、分析和优化代码结构
  分类: development

○ git_operations v1.0.0
  描述: Git 操作技能，提供版本控制相关的功能
  分类: development
```

### 测试 Agents 系统

```bash
sa --list-agents
```

预期输出：
```
============================================================
代理列表 (Agents)
============================================================

○ code_explorer v1.0.0
  描述: 代码探索代理，用于在代码库中搜索、理解和分析代码结构

○ file_processor v1.0.0
  描述: 文件处理代理，用于批量处理、转换和操作文件

○ code_reviewer v1.0.0
  描述: 代码审查代理，用于自动化代码审查和质量检查
```

## 💡 在代码中使用

### 使用 Skills

```python
from skills import get_skill_manager

# 获取技能管理器
manager = get_skill_manager()

# 加载技能
manager.load_skill("code_analysis")

# 获取技能实例
skill = manager.get_skill("code_analysis")

# 执行技能动作
result = skill.execute("analyze_code_structure", file_path="your_file.py")
print(result)
```

### 使用 Agents

```python
import asyncio
from agents import get_orchestrator

async def main():
    orchestrator = get_orchestrator()

    # 执行任务
    result = await orchestrator.execute_with_best_agent(
        "分析当前目录的代码质量"
    )
    print(result)

asyncio.run(main())
```

## 📝 在项目中集成

### 方式一：直接导入

在你的项目代码中：

```python
# 你的项目脚本
from skills import get_skill_manager
from agents import AgentOrchestrator, AgentTask

async def analyze_project():
    # 使用 Skills
    skill_manager = get_skill_manager()
    skill_manager.load_skill("code_analysis")

    skill = skill_manager.get_skill("code_analysis")
    result = skill.execute("analyze_code_structure", file_path="main.py")

    # 使用 Agents
    orchestrator = AgentOrchestrator()
    # ... 配置和执行
```

### 方式二：创建项目特定的配置

在项目中创建 `skills_config.py`：

```python
"""
项目特定的 Skills 和 Agents 配置
"""
from skills import get_skill_manager
from agents import AgentOrchestrator
from agents.code_explorer import CodeExplorerAgent
from agents.code_reviewer import CodeReviewerAgent

# 初始化
skill_manager = get_skill_manager()
orchestrator = AgentOrchestrator()

# 加载项目需要的技能
skill_manager.load_skill("code_analysis")
skill_manager.load_skill("git_operations")

# 注册项目需要的代理
orchestrator.register_agent(CodeExplorerAgent())
orchestrator.register_agent(CodeReviewerAgent())

# 导出为全局变量
SKILLS = skill_manager
AGENTS = orchestrator
```

然后在你的代码中使用：

```python
from skills_config import SKILLS, AGENTS

# 使用配置好的系统
skill = SKILLS.get_skill("code_analysis")
result = skill.execute("analyze_code_structure", file_path="main.py")
```

## 🎯 常用命令

### 交互式模式

```bash
sa --interactive
```

交互式命令：
```
skills                     # 列出所有技能
agents                     # 列出所有代理
load code_analysis         # 加载技能
unload code_analysis       # 卸载技能
run code_explorer "搜索"    # 运行代理任务
help                       # 显示帮助
quit                       # 退出
```

### 快速命令

```bash
# 查看技能
sa --list-skills

# 查看代理
sa --list-agents

# 创建新技能
sa --create-skill my_skill "我的技能"

# 创建新代理
sa --create-agent my_agent "我的代理"
```

## 🔧 故障排除

### 问题 1: 找不到模块

**错误**: `ModuleNotFoundError: No module named 'skills'`

**解决**:
```bash
# 确保 PYTHONPATH 包含安装目录
export PYTHONPATH="$PYTHONPATH:$HOME/.codebuddy_skills_agents"

# 或者使用完整路径
python ~/.codebuddy_skills_agents/skills_manager.py --list-skills
```

### 问题 2: 命令不可用

**错误**: `command not found: sa`

**解决**:
```bash
# 手动创建符号链接
ln -s ~/.codebuddy_skills_agents/sa.py ~/bin/sa
chmod +x ~/bin/sa

# 确保 bin 目录在 PATH 中
echo $PATH
```

### 问题 3: 权限问题

**错误**: `Permission denied`

**解决**:
```bash
# 添加执行权限
chmod +x ~/.codebuddy_skills_agents/sa.py
chmod +x ~/bin/sa
```

### 问题 4: 依赖缺失

如果使用了外部依赖：

```bash
pip install -r requirements.txt
```

## 📚 更多资源

- **完整文档**: 查看 `README_SKILLS_AGENTS.md`
- **使用示例**: 查看 `example_usage.py`
- **技能创建**: 查看 `skills/` 目录下的示例
- **代理创建**: 查看 `agents/` 目录下的示例

## 🎓 学习建议

1. **从简单开始**: 先使用内置的 Skills 和 Agents
2. **阅读示例**: 运行 `python example_usage.py` 查看实际使用
3. **自定义扩展**: 根据需求创建自己的 Skills 和 Agents
4. **集成到项目**: 将系统集成到你的日常工作流程中

## ✅ 安装检查清单

- [ ] 运行了 `python setup_local.py`
- [ ] 重启了终端或执行了 `source ~/.zshrc`
- [ ] 执行 `sa --list-skills` 成功
- [ ] 执行 `sa --list-agents` 成功
- [ ] 可以在 Python 代码中 `from skills import get_skill_manager`
- [ ] 运行了 `python example_usage.py` 无错误

完成以上检查后，你就可以在任何项目中使用 Skills 和 Agents 系统了！

## 🆘 获取帮助

如果遇到问题：

1. 查看日志输出
2. 检查文件路径是否正确
3. 确保 Python 版本 >= 3.8
4. 查看文档 `README_SKILLS_AGENTS.md`
5. 运行示例代码验证安装

祝你编码愉快！🚀
