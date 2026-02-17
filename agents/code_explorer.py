"""
代码探索代理

用于在代码库中搜索、理解和分析代码结构
"""

import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
import re

from agents import Agent, AgentTask, AgentResult, AgentCapability


class CodeExplorerAgent(Agent):
    """代码探索代理"""
    
    def __init__(self):
        super().__init__(
            name="code_explorer",
            description="代码探索代理，用于在代码库中搜索、理解和分析代码结构"
        )
        self._capabilities = [
            AgentCapability(
                name="search_across_files",
                description="在多个文件中搜索代码",
                category="code_analysis",
                required_tools=["search_file", "search_content"]
            ),
            AgentCapability(
                name="find_definitions",
                description="查找函数、类、变量的定义",
                category="code_analysis",
                required_tools=["search_content", "read_file"]
            ),
            AgentCapability(
                name="find_references",
                description="查找代码的引用位置",
                category="code_analysis",
                required_tools=["search_content"]
            ),
            AgentCapability(
                name="analyze_codebase",
                description="分析代码库整体结构",
                category="code_analysis",
                required_tools=["list_files", "read_file"]
            ),
            AgentCapability(
                name="navigate_dependencies",
                description="导航和理解依赖关系",
                category="code_analysis",
                required_tools=["read_file", "search_content"]
            ),
            AgentCapability(
                name="locate_features",
                description="定位特定功能的实现位置",
                category="code_analysis",
                required_tools=["search_file", "search_content"]
            )
        ]
    
    def get_capabilities(self) -> List[AgentCapability]:
        """获取代理能力列表"""
        return self._capabilities
    
    async def execute(self, task: AgentTask) -> AgentResult:
        """执行任务"""
        import time
        start_time = time.time()
        steps = ["开始任务"]
        
        try:
            task_type = self._detect_task_type(task.description)
            params = task.params
            
            steps.append(f"检测到任务类型: {task_type}")
            
            if task_type == "search_pattern":
                result = await self._search_pattern(params)
            elif task_type == "find_definition":
                result = await self._find_definition(params)
            elif task_type == "analyze_structure":
                result = await self._analyze_structure(params)
            elif task_type == "find_references":
                result = await self._find_references(params)
            elif task_type == "locate_feature":
                result = await self._locate_feature(params)
            else:
                result = await self._general_explore(task.description, params)
            
            steps.append("完成分析")
            
            execution_time = time.time() - start_time
            return AgentResult(
                success=result.get("success", True),
                data=result,
                message="任务执行成功",
                execution_time=execution_time,
                steps=steps
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            steps.append(f"执行失败: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                message=f"任务执行失败: {str(e)}",
                execution_time=execution_time,
                steps=steps
            )
    
    def _detect_task_type(self, description: str) -> str:
        """检测任务类型"""
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ["搜索", "search", "查找", "find"]):
            if "定义" in description_lower or "definition" in description_lower:
                return "find_definition"
            elif "引用" in description_lower or "reference" in description_lower:
                return "find_references"
            elif "功能" in description_lower or "feature" in description_lower or "实现" in description_lower:
                return "locate_feature"
            else:
                return "search_pattern"
        elif any(keyword in description_lower for keyword in ["分析", "analyze", "结构", "structure"]):
            return "analyze_structure"
        else:
            return "general_explore"
    
    async def _search_pattern(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """搜索模式"""
        directory = params.get("directory", ".")
        pattern = params.get("pattern")
        file_pattern = params.get("file_pattern", "*")
        
        if not pattern:
            return {"error": "缺少 pattern 参数"}
        
        results = {
            "pattern": pattern,
            "directory": directory,
            "matches": []
        }
        
        # 模拟搜索结果（实际应该调用工具）
        # 这里返回示例数据
        results["matches"] = [
            {
                "file": f"{directory}/example.py",
                "line": 10,
                "content": f"def {pattern}():"
            }
        ]
        
        return results
    
    async def _find_definition(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """查找定义"""
        symbol = params.get("symbol")
        directory = params.get("directory", ".")
        
        if not symbol:
            return {"error": "缺少 symbol 参数"}
        
        results = {
            "symbol": symbol,
            "directory": directory,
            "definitions": []
        }
        
        # 模拟查找结果
        results["definitions"] = [
            {
                "file": f"{directory}/example.py",
                "line": 15,
                "type": "function",
                "name": symbol
            }
        ]
        
        return results
    
    async def _analyze_structure(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """分析结构"""
        directory = params.get("directory", ".")
        depth = params.get("depth", 3)
        
        results = {
            "directory": directory,
            "structure": {},
            "summary": {}
        }
        
        # 模拟结构分析
        results["structure"] = {
            "files": ["example.py", "test.py"],
            "directories": ["src", "tests"]
        }
        results["summary"] = {
            "total_files": 2,
            "total_directories": 2,
            "languages": ["python"]
        }
        
        return results
    
    async def _find_references(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """查找引用"""
        symbol = params.get("symbol")
        directory = params.get("directory", ".")
        
        if not symbol:
            return {"error": "缺少 symbol 参数"}
        
        results = {
            "symbol": symbol,
            "directory": directory,
            "references": []
        }
        
        # 模拟引用结果
        results["references"] = [
            {
                "file": f"{directory}/example.py",
                "lines": [20, 35, 50],
                "count": 3
            }
        ]
        
        return results
    
    async def _locate_feature(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """定位功能"""
        feature = params.get("feature")
        directory = params.get("directory", ".")
        
        if not feature:
            return {"error": "缺少 feature 参数"}
        
        results = {
            "feature": feature,
            "directory": directory,
            "locations": []
        }
        
        # 模拟功能定位
        results["locations"] = [
            {
                "file": f"{directory}/example.py",
                "function": f"implement_{feature}",
                "line": 100,
                "description": f"实现了 {feature} 功能"
            }
        ]
        
        return results
    
    async def _general_explore(self, description: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """通用探索"""
        directory = params.get("directory", ".")
        
        results = {
            "description": description,
            "directory": directory,
            "findings": []
        }
        
        # 模拟通用探索
        results["findings"] = [
            {
                "type": "info",
                "message": f"在 {directory} 中进行探索"
            }
        ]
        
        return results
    
    def can_handle(self, task_description: str) -> bool:
        """判断是否可以处理该任务"""
        keywords = [
            "搜索", "search", "查找", "find", "分析", "analyze",
            "代码", "code", "结构", "structure", "定义", "definition",
            "引用", "reference", "功能", "feature", "实现", "implement"
        ]
        return any(keyword in task_description.lower() for keyword in keywords)
