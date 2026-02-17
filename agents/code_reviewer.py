"""
代码审查代理

用于自动化代码审查和质量检查
"""

import asyncio
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import ast

from agents import Agent, AgentTask, AgentResult, AgentCapability


class CodeReviewerAgent(Agent):
    """代码审查代理"""
    
    def __init__(self):
        super().__init__(
            name="code_reviewer",
            description="代码审查代理，用于自动化代码审查和质量检查"
        )
        self._capabilities = [
            AgentCapability(
                name="review_code",
                description="审查代码质量和最佳实践",
                category="code_quality",
                required_tools=[]
            ),
            AgentCapability(
                name="check_quality",
                description="检查代码质量指标",
                category="code_quality",
                required_tools=[]
            ),
            AgentCapability(
                name="detect_bugs",
                description="检测潜在的错误和问题",
                category="code_quality",
                required_tools=[]
            ),
            AgentCapability(
                name="suggest_improvements",
                description="提供改进建议",
                category="code_quality",
                required_tools=[]
            ),
            AgentCapability(
                name="check_style",
                description="检查代码风格",
                category="code_quality",
                required_tools=[]
            ),
            AgentCapability(
                name="verify_tests",
                description="验证测试覆盖率和质量",
                category="code_quality",
                required_tools=[]
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
            
            if task_type == "review_code":
                result = await self._review_code(params)
            elif task_type == "check_quality":
                result = await self._check_quality(params)
            elif task_type == "detect_bugs":
                result = await self._detect_bugs(params)
            elif task_type == "suggest_improvements":
                result = await self._suggest_improvements(params)
            elif task_type == "check_style":
                result = await self._check_style(params)
            elif task_type == "verify_tests":
                result = await self._verify_tests(params)
            else:
                result = await self._general_review(task.description, params)
            
            steps.append("完成审查")
            
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
        
        if "审查" in description_lower or "review" in description_lower:
            return "review_code"
        elif "质量" in description_lower or "quality" in description_lower:
            return "check_quality"
        elif "bug" in description_lower or "错误" in description_lower or "问题" in description_lower:
            return "detect_bugs"
        elif "改进" in description_lower or "优化" in description_lower or "建议" in description_lower:
            return "suggest_improvements"
        elif "风格" in description_lower or "style" in description_lower:
            return "check_style"
        elif "测试" in description_lower or "test" in description_lower:
            return "verify_tests"
        else:
            return "review_code"
    
    async def _review_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """审查代码"""
        file_path = params.get("file_path")
        directory = params.get("directory", ".")
        
        results = {
            "file_path": file_path,
            "directory": directory,
            "review": {
                "issues": [],
                "warnings": [],
                "suggestions": [],
                "score": 0
            }
        }
        
        if file_path:
            # 审查单个文件
            file_results = await self._review_single_file(file_path)
            results["review"] = file_results
        else:
            # 审查目录
            dir_results = await self._review_directory(directory)
            results["review"] = dir_results
        
        return results
    
    async def _check_quality(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """检查代码质量"""
        file_path = params.get("file_path")
        
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            metrics = {
                "total_lines": len(content.split('\n')),
                "code_lines": len([l for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]),
                "comment_lines": len([l for l in content.split('\n') if l.strip().startswith('#')]),
                "blank_lines": len([l for l in content.split('\n') if not l.strip()]),
                "functions": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
                "classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
                "imports": len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
            }
            
            # 计算质量分数
            score = self._calculate_quality_score(metrics)
            
            return {
                "file_path": str(path),
                "metrics": metrics,
                "score": score,
                "level": self._get_quality_level(score)
            }
            
        except Exception as e:
            return {"error": f"质量检查失败: {str(e)}"}
    
    async def _detect_bugs(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """检测潜在 bug"""
        file_path = params.get("file_path")
        
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        bugs = []
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # 检测未使用的变量
            used_names = set()
            defined_names = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    used_names.add(node.id)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    defined_names.add(node.id)
            
            for name in defined_names - used_names:
                bugs.append({
                    "type": "unused_variable",
                    "severity": "warning",
                    "message": f"变量 '{name}' 被定义但未使用"
                })
            
            # 检测空 except 块
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    if node.type is None or node.name is None:
                        bugs.append({
                            "type": "bare_except",
                            "severity": "error",
                            "message": "使用了空的 except 块，可能隐藏异常"
                        })
            
            # 检测硬编码的密钥或密码
            sensitive_patterns = [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']'
            ]
            
            for i, line in enumerate(content.split('\n'), 1):
                for pattern in sensitive_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        bugs.append({
                            "type": "hardcoded_secret",
                            "severity": "critical",
                            "message": f"行 {i}: 疑似硬编码的敏感信息",
                            "line": i
                        })
            
            return {
                "file_path": str(path),
                "bugs_found": len(bugs),
                "bugs": bugs
            }
            
        except Exception as e:
            return {"error": f"Bug 检测失败: {str(e)}"}
    
    async def _suggest_improvements(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """提供改进建议"""
        file_path = params.get("file_path")
        
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        suggestions = []
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否缺少文档字符串
            if not content.startswith('"""') and not content.startswith("'''"):
                suggestions.append({
                    "type": "documentation",
                    "priority": "medium",
                    "message": "建议在文件开头添加模块文档字符串"
                })
            
            # 检查函数是否有文档字符串
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        suggestions.append({
                            "type": "documentation",
                            "priority": "medium",
                            "message": f"函数 '{node.name}' 缺少文档字符串",
                            "line": node.lineno
                        })
            
            # 检查行长度
            for i, line in enumerate(content.split('\n'), 1):
                if len(line) > 100:
                    suggestions.append({
                        "type": "style",
                        "priority": "low",
                        "message": f"行 {i} 过长 ({len(line)} 字符)，建议拆分",
                        "line": i
                    })
            
            return {
                "file_path": str(path),
                "suggestions_count": len(suggestions),
                "suggestions": suggestions
            }
            
        except Exception as e:
            return {"error": f"建议生成失败: {str(e)}"}
    
    async def _check_style(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """检查代码风格"""
        file_path = params.get("file_path")
        
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        style_issues = []
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 检查缩进一致性
            for i, line in enumerate(lines, 1):
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    if indent % 4 != 0:
                        style_issues.append({
                            "type": "indentation",
                            "severity": "warning",
                            "message": f"行 {i}: 缩进不是 4 的倍数",
                            "line": i
                        })
            
            # 检查尾随空格
            for i, line in enumerate(lines, 1):
                if line.endswith(' \n') or line.endswith(' \r\n'):
                    style_issues.append({
                        "type": "trailing_whitespace",
                        "severity": "info",
                        "message": f"行 {i}: 存在尾随空格",
                        "line": i
                    })
            
            # 检查多余空行
            blank_count = 0
            for i, line in enumerate(lines, 1):
                if not line.strip():
                    blank_count += 1
                else:
                    if blank_count > 2:
                        style_issues.append({
                            "type": "extra_blank_lines",
                            "severity": "info",
                            "message": f"行 {i-blank_count-1}: 存在 {blank_count} 个连续空行"
                        })
                    blank_count = 0
            
            return {
                "file_path": str(path),
                "style_issues_count": len(style_issues),
                "style_issues": style_issues
            }
            
        except Exception as e:
            return {"error": f"风格检查失败: {str(e)}"}
    
    async def _verify_tests(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """验证测试"""
        directory = params.get("directory", ".")
        test_pattern = params.get("test_pattern", "test_*.py")
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        test_files = list(dir_path.glob(test_pattern))
        
        results = {
            "directory": directory,
            "test_files": [],
            "total_tests": 0,
            "coverage": {}
        }
        
        for test_file in test_files:
            if test_file.is_file():
                try:
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    tree = ast.parse(content)
                    test_functions = [
                        node.name for node in ast.walk(tree)
                        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')
                    ]
                    
                    results["test_files"].append({
                        "file": str(test_file),
                        "test_functions": test_functions,
                        "test_count": len(test_functions)
                    })
                    
                    results["total_tests"] += len(test_functions)
                    
                except Exception as e:
                    results["test_files"].append({
                        "file": str(test_file),
                        "error": str(e)
                    })
        
        return results
    
    async def _review_single_file(self, file_path: str) -> Dict[str, Any]:
        """审查单个文件"""
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        results = {
            "issues": [],
            "warnings": [],
            "suggestions": [],
            "score": 0
        }
        
        try:
            # 检查质量
            quality = await self._check_quality({"file_path": file_path})
            if "metrics" in quality:
                results["score"] = quality.get("score", 0)
            
            # 检测 bug
            bugs = await self._detect_bugs({"file_path": file_path})
            if "bugs" in bugs:
                results["issues"].extend(bugs["bugs"])
            
            # 获取建议
            improvements = await self._suggest_improvements({"file_path": file_path})
            if "suggestions" in improvements:
                results["suggestions"].extend(improvements["suggestions"])
            
            # 检查风格
            style = await self._check_style({"file_path": file_path})
            if "style_issues" in style:
                results["warnings"].extend(style["style_issues"])
            
        except Exception as e:
            results["issues"].append({
                "type": "error",
                "message": f"审查失败: {str(e)}"
            })
        
        return results
    
    async def _review_directory(self, directory: str) -> Dict[str, Any]:
        """审查目录"""
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        results = {
            "files": [],
            "summary": {}
        }
        
        # 查找所有 Python 文件
        python_files = list(dir_path.rglob("*.py"))
        
        for file_path in python_files:
            file_results = await self._review_single_file(str(file_path))
            results["files"].append({
                "file_path": str(file_path),
                "review": file_results
            })
        
        # 汇总
        total_issues = sum(len(f["review"].get("issues", [])) for f in results["files"])
        total_warnings = sum(len(f["review"].get("warnings", [])) for f in results["files"])
        avg_score = sum(f["review"].get("score", 0) for f in results["files"]) / len(results["files"]) if results["files"] else 0
        
        results["summary"] = {
            "total_files": len(results["files"]),
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "average_score": round(avg_score, 2)
        }
        
        return results
    
    async def _general_review(self, description: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """通用审查"""
        return await self._review_code(params)
    
    def _calculate_quality_score(self, metrics: Dict[str, int]) -> int:
        """计算质量分数"""
        score = 100
        
        # 根据指标调整分数
        if metrics.get("comment_lines", 0) == 0:
            score -= 10
        
        if metrics.get("code_lines", 0) > 100 and metrics.get("functions", 0) == 0:
            score -= 20
        
        return max(0, min(100, score))
    
    def _get_quality_level(self, score: int) -> str:
        """获取质量等级"""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        else:
            return "poor"
    
    def can_handle(self, task_description: str) -> bool:
        """判断是否可以处理该任务"""
        keywords = [
            "审查", "review", "质量", "quality", "bug", "错误",
            "问题", "改进", "优化", "建议", "风格", "style",
            "测试", "test", "代码", "code"
        ]
        return any(keyword in task_description.lower() for keyword in keywords)
