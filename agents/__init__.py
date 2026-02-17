"""
Agents System - 智能代理管理系统

这个模块提供了管理智能代理（Agents）的基础架构，每个 Agent 是一个专门化的子代理，
用于处理特定的、复杂的多步骤任务。

Agents 可以：
- 自主完成复杂的、多步骤的任务
- 协作完成跨领域的任务
- 提供专门化的分析和处理能力
- 扩展主助手的能力边界
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import time


class AgentStatus(Enum):
    """代理状态枚举"""
    IDLE = "idle"               # 空闲
    RUNNING = "running"         # 运行中
    COMPLETED = "completed"     # 已完成
    ERROR = "error"            # 错误
    PAUSED = "paused"          # 暂停


@dataclass
class AgentCapability:
    """代理能力描述"""
    name: str                           # 能力名称
    description: str                    # 能力描述
    category: str                       # 能力分类
    required_tools: List[str] = field(default_factory=list)  # 需要的工具


@dataclass
class AgentResult:
    """代理执行结果"""
    success: bool                      # 是否成功
    data: Any                         # 结果数据
    message: str                      # 结果消息
    execution_time: float             # 执行时间
    steps: List[str] = field(default_factory=list)  # 执行步骤


class AgentTask:
    """代理任务"""
    
    def __init__(self, description: str, params: Dict[str, Any] = None):
        self.description = description
        self.params = params or {}
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        self.status = AgentStatus.IDLE
        self.result: Optional[AgentResult] = None
    
    def start(self):
        """开始任务"""
        self.status = AgentStatus.RUNNING
        self.started_at = time.time()
    
    def complete(self, result: AgentResult):
        """完成任务"""
        self.status = AgentStatus.COMPLETED
        self.completed_at = time.time()
        self.result = result
    
    def fail(self, error_message: str):
        """任务失败"""
        self.status = AgentStatus.ERROR
        self.completed_at = time.time()
        self.result = AgentResult(
            success=False,
            data=None,
            message=error_message,
            execution_time=self.completed_at - (self.started_at or self.created_at)
        )


class Agent(ABC):
    """代理基类
    
    所有自定义代理都应继承此类并实现相应方法。
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = AgentStatus.IDLE
        self.current_task: Optional[AgentTask] = None
        self._capabilities: List[AgentCapability] = []
        self._history: List[AgentResult] = []
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """获取代理能力列表
        
        Returns:
            能力列表
        """
        pass
    
    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """执行任务
        
        Args:
            task: 要执行的任务
            
        Returns:
            执行结果
        """
        pass
    
    def can_handle(self, task_description: str) -> bool:
        """判断是否可以处理该任务
        
        Args:
            task_description: 任务描述
            
        Returns:
            是否可以处理
        """
        # 子类可以重写此方法以实现更智能的任务匹配
        return any(cap.name.lower() in task_description.lower() 
                  for cap in self.get_capabilities())
    
    def get_status(self) -> Dict[str, Any]:
        """获取代理状态"""
        return {
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'current_task': self.current_task.description if self.current_task else None,
            'capabilities': [cap.name for cap in self.get_capabilities()]
        }
    
    def get_history(self, limit: int = 10) -> List[AgentResult]:
        """获取执行历史
        
        Args:
            limit: 返回的最大历史记录数
            
        Returns:
            历史结果列表
        """
        return self._history[-limit:] if self._history else []
    
    def _add_to_history(self, result: AgentResult):
        """添加到历史记录"""
        self._history.append(result)
        # 限制历史记录数量
        if len(self._history) > 100:
            self._history = self._history[-50:]


class AgentOrchestrator:
    """代理编排器
    
    负责管理和协调多个代理的执行。
    """
    
    def __init__(self):
        self._agents: Dict[str, Agent] = {}
        self._task_queue: List[AgentTask] = []
    
    def register_agent(self, agent: Agent):
        """注册代理
        
        Args:
            agent: 要注册的代理
        """
        self._agents[agent.name] = agent
        print(f"已注册代理: {agent.name}")
    
    def unregister_agent(self, agent_name: str):
        """注销代理
        
        Args:
            agent_name: 代理名称
        """
        if agent_name in self._agents:
            del self._agents[agent_name]
            print(f"已注销代理: {agent_name}")
    
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """获取代理
        
        Args:
            agent_name: 代理名称
            
        Returns:
            代理实例或 None
        """
        return self._agents.get(agent_name)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有代理
        
        Returns:
            代理信息列表
        """
        return [agent.get_status() for agent in self._agents.values()]
    
    def find_best_agent(self, task_description: str) -> Optional[Agent]:
        """查找最适合处理任务的代理
        
        Args:
            task_description: 任务描述
            
        Returns:
            最适合的代理或 None
        """
        for agent in self._agents.values():
            if agent.can_handle(task_description):
                return agent
        return None
    
    async def execute_task(self, agent_name: str, task_description: str, 
                          params: Dict[str, Any] = None) -> AgentResult:
        """使用指定代理执行任务
        
        Args:
            agent_name: 代理名称
            task_description: 任务描述
            params: 任务参数
            
        Returns:
            执行结果
        """
        agent = self.get_agent(agent_name)
        if agent is None:
            return AgentResult(
                success=False,
                data=None,
                message=f"未找到代理: {agent_name}",
                execution_time=0.0
            )
        
        task = AgentTask(task_description, params)
        agent.current_task = task
        agent.status = AgentStatus.RUNNING
        task.start()
        
        try:
            result = await agent.execute(task)
            task.complete(result)
            agent._add_to_history(result)
            return result
        except Exception as e:
            error_msg = f"执行任务时发生错误: {str(e)}"
            task.fail(error_msg)
            agent._add_to_history(task.result)
            return task.result
        finally:
            agent.status = AgentStatus.IDLE
            agent.current_task = None
    
    async def execute_with_best_agent(self, task_description: str, 
                                      params: Dict[str, Any] = None) -> AgentResult:
        """自动选择最适合的代理执行任务
        
        Args:
            task_description: 任务描述
            params: 任务参数
            
        Returns:
            执行结果
        """
        agent = self.find_best_agent(task_description)
        if agent is None:
            return AgentResult(
                success=False,
                data=None,
                message=f"未找到可以处理该任务的代理: {task_description}",
                execution_time=0.0
            )
        
        print(f"使用代理 {agent.name} 处理任务: {task_description}")
        return await self.execute_task(agent.name, task_description, params)
    
    async def execute_parallel(self, tasks: List[Dict[str, Any]]) -> List[AgentResult]:
        """并行执行多个任务
        
        Args:
            tasks: 任务列表，每个任务是一个字典，包含:
                  - agent_name: 代理名称（可选，不指定则自动选择）
                  - description: 任务描述
                  - params: 任务参数（可选）
                  
        Returns:
            执行结果列表
        """
        async def execute_single(task: Dict[str, Any]) -> AgentResult:
            agent_name = task.get('agent_name')
            description = task['description']
            params = task.get('params')
            
            if agent_name:
                return await self.execute_task(agent_name, description, params)
            else:
                return await self.execute_with_best_agent(description, params)
        
        return await asyncio.gather(*[execute_single(task) for task in tasks])
    
    async def execute_pipeline(self, pipeline: List[Dict[str, Any]]) -> AgentResult:
        """按管道顺序执行任务
        
        Args:
            pipeline: 任务管道，每个任务是一个字典，包含:
                     - agent_name: 代理名称（可选）
                     - description: 任务描述
                     - params: 任务参数（可选）
                     
        Returns:
            最后一个任务的执行结果
        """
        previous_result = None
        
        for task in pipeline:
            # 如果参数中引用了前一个任务的结果，进行替换
            params = task.get('params', {})
            if previous_result and '{{previous}}' in json.dumps(params):
                params_str = json.dumps(params)
                params_str = params_str.replace('{{previous}}', json.dumps(previous_result.data))
                params = json.loads(params_str)
            
            agent_name = task.get('agent_name')
            description = task['description']
            
            if agent_name:
                result = await self.execute_task(agent_name, description, params)
            else:
                result = await self.execute_with_best_agent(description, params)
            
            if not result.success:
                return result
            
            previous_result = result
        
        return previous_result


class AgentRegistry:
    """代理注册表
    
    用于发现和加载代理配置。
    """
    
    def __init__(self, agents_directory: str = "agents"):
        self.agents_directory = Path(agents_directory)
        self._agent_configs: Dict[str, Dict] = {}
    
    def discover_agents(self) -> List[Dict[str, Any]]:
        """发现所有可用的代理
        
        Returns:
            代理配置列表
        """
        configs = []
        
        if not self.agents_directory.exists():
            return configs
        
        for agent_file in self.agents_directory.glob("*.json"):
            if agent_file.name == "registry.json":
                continue
            
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self._agent_configs[config['name']] = config
                    configs.append(config)
            except Exception as e:
                print(f"加载代理配置失败 {agent_file}: {e}")
        
        return configs
    
    def get_agent_config(self, agent_name: str) -> Optional[Dict]:
        """获取代理配置
        
        Args:
            agent_name: 代理名称
            
        Returns:
            代理配置或 None
        """
        return self._agent_configs.get(agent_name)


# 全局代理编排器实例
_global_orchestrator: Optional[AgentOrchestrator] = None


def get_orchestrator() -> AgentOrchestrator:
    """获取全局代理编排器实例"""
    global _global_orchestrator
    if _global_orchestrator is None:
        _global_orchestrator = AgentOrchestrator()
        
        # 发现并注册所有代理
        registry = AgentRegistry()
        configs = registry.discover_agents()
        for config in configs:
            # 这里需要根据配置动态加载代理类
            # 实际实现中应该使用动态导入
            print(f"发现代理配置: {config['name']}")
    
    return _global_orchestrator


def create_agent_template(name: str, description: str, **kwargs) -> None:
    """创建代理模板
    
    Args:
        name: 代理名称
        description: 代理描述
        **kwargs: 其他配置项
    """
    agents_dir = Path("agents")
    agents_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建配置文件
    config = {
        "name": name,
        "description": description,
        "version": kwargs.get('version', '1.0.0'),
        "author": kwargs.get('author', ''),
        "category": kwargs.get('category', 'general'),
        "capabilities": kwargs.get('capabilities', []),
        "required_tools": kwargs.get('required_tools', []),
        "module": f"agents.{name}",
        "class_name": name.capitalize() + 'Agent'
    }
    
    config_file = agents_dir / f"{name}.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # 创建代理实现文件模板
    agent_class_name = name.capitalize() + 'Agent'
    agent_template = f'''"""
{description}
"""

from typing import List
from agents import Agent, AgentTask, AgentResult, AgentCapability


class {agent_class_name}(Agent):
    """{description}"""
    
    def __init__(self):
        super().__init__(
            name="{name}",
            description="{description}"
        )
        self._capabilities = [
            AgentCapability(
                name="{kwargs.get('capabilities', ['general'])[0] if kwargs.get('capabilities') else 'execute'}",
                description="执行 {description} 相关任务",
                category="{kwargs.get('category', 'general')}",
                required_tools={kwargs.get('required_tools', [])}
            )
        ]
    
    def get_capabilities(self) -> List[AgentCapability]:
        """获取代理能力列表"""
        return self._capabilities
    
    async def execute(self, task: AgentTask) -> AgentResult:
        """执行任务
        
        Args:
            task: 要执行的任务
            
        Returns:
            执行结果
        """
        import time
        start_time = time.time()
        
        try:
            # 实现你的代理逻辑
            # 例如:
            # 1. 解析任务参数
            params = task.params
            
            # 2. 执行具体的处理逻辑
            result_data = self._process_task(task.description, params)
            
            # 3. 返回结果
            execution_time = time.time() - start_time
            return AgentResult(
                success=True,
                data=result_data,
                message="任务执行成功",
                execution_time=execution_time,
                steps=["开始任务", "处理任务", "完成任务"]
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return AgentResult(
                success=False,
                data=None,
                message=f"任务执行失败: {{str(e)}}",
                execution_time=execution_time,
                steps=["开始任务", "执行失败"]
            )
    
    def _process_task(self, description: str, params: dict) -> any:
        """处理任务的具体实现
        
        Args:
            description: 任务描述
            params: 任务参数
            
        Returns:
            处理结果
        """
        # 在这里实现你的具体逻辑
        print(f"处理任务: {{description}}")
        print(f"参数: {{params}}")
        
        # 示例: 返回处理结果
        return {{
            "description": description,
            "params": params,
            "result": "处理完成"
        }}
'''
    
    agent_file = agents_dir / f"{name}.py"
    with open(agent_file, 'w', encoding='utf-8') as f:
        f.write(agent_template)
    
    print(f"代理模板已创建: {agent_file}")


if __name__ == "__main__":
    # 示例：使用代理系统
    orchestrator = AgentOrchestrator()
    
    # 示例：创建代理模板
    # create_agent_template("example", "示例代理")
    
    # 列出代理
    print("代理列表:")
    agents = orchestrator.list_agents()
    for agent in agents:
        print(f"- {{agent['name']}}: {{agent['description']}}")
