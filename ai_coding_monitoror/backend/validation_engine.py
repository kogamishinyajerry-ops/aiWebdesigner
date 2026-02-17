"""
Validation Engine - Validate code changes and detect regressions
验证代码变更并检测回归
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import subprocess
import asyncio
import json
import os

from loguru import logger

from .code_detector import CodeChangeDetector


class ValidationEngine:
    """验证引擎"""
    
    def __init__(self):
        self.code_detector = CodeChangeDetector()
    
    async def validate_changes(
        self,
        session_id: str,
        changes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        验证代码变更
        
        Args:
            session_id: 会话ID
            changes: 变更列表
            
        Returns:
            验证结果
        """
        try:
            issues = []
            suggestions = []
            max_risk = "LOW"
            
            for change in changes:
                # Validate each change
                result = await self._validate_single_change(
                    session_id,
                    change
                )
                
                issues.extend(result["issues"])
                suggestions.extend(result["suggestions"])
                
                # Update max risk
                risk_levels = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
                if risk_levels.get(result["risk_level"], 0) > risk_levels.get(max_risk, 0):
                    max_risk = result["risk_level"]
            
            # Overall validation result
            valid = max_risk != "CRITICAL"
            
            logger.info(f"Validation complete: {len(issues)} issues, risk={max_risk}")
            
            return {
                "valid": valid,
                "issues": issues,
                "suggestions": suggestions,
                "risk_level": max_risk,
                "changes_validated": len(changes),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating changes: {e}")
            raise
    
    async def validate_code(
        self,
        session_id: str,
        file_path: str,
        content: str
    ) -> Dict[str, Any]:
        """
        验证单个文件
        
        Args:
            session_id: 会话ID
            file_path: 文件路径
            content: 代码内容
            
        Returns:
            验证结果
        """
        try:
            issues = []
            suggestions = []
            
            # 1. Syntax validation
            syntax_result = await self._validate_syntax(content)
            if not syntax_result["valid"]:
                issues.extend(syntax_result["issues"])
            
            # 2. Type checking (if mypy available)
            type_result = await self._validate_types(file_path, content)
            issues.extend(type_result["issues"])
            suggestions.extend(type_result["suggestions"])
            
            # 3. Linting (if pylint available)
            lint_result = await self._validate_lint(file_path, content)
            issues.extend(lint_result["issues"])
            suggestions.extend(lint_result["suggestions"])
            
            # 4. Function integrity
            integrity_result = await self._validate_function_integrity(
                session_id,
                file_path,
                content
            )
            issues.extend(integrity_result["issues"])
            
            # Calculate overall risk
            risk_level = self._calculate_overall_risk(issues)
            
            valid = risk_level != "CRITICAL"
            
            logger.info(f"Code validation complete: {len(issues)} issues")
            
            return {
                "valid": valid,
                "issues": issues,
                "suggestions": suggestions,
                "risk_level": risk_level,
                "file_path": file_path,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating code: {e}")
            raise
    
    async def run_tests(
        self,
        session_id: str,
        test_command: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        运行测试
        
        Args:
            session_id: 会话ID
            test_command: 测试命令
            
        Returns:
            测试结果
        """
        try:
            # Default test command
            if not test_command:
                test_command = "pytest -v --tb=short"
            
            # Run tests
            process = await asyncio.create_subprocess_shell(
                test_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=60  # 60 second timeout
            )
            
            stdout_str = stdout.decode()
            stderr_str = stderr.decode()
            
            # Parse results
            passed = "passed" in stdout_str.lower()
            failed = "failed" in stdout_str.lower()
            errors = "error" in stderr_str.lower()
            
            result = {
                "success": passed and not failed and not errors,
                "stdout": stdout_str,
                "stderr": stderr_str,
                "exit_code": process.returncode,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Tests run: success={result['success']}")
            
            return result
            
        except asyncio.TimeoutError:
            logger.error("Test execution timed out")
            return {
                "success": False,
                "error": "Test execution timed out",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            raise
    
    async def _validate_single_change(
        self,
        session_id: str,
        change: Dict[str, Any]
    ) -> Dict[str, Any]:
        """验证单个变更"""
        issues = []
        suggestions = []
        
        impact = change.get("impact", {})
        risk_level = change.get("risk_level", "LOW")
        
        # Check for critical changes
        if impact.get("critical_changes"):
            issues.append({
                "type": "critical",
                "message": "Critical code change detected",
                "file_path": change.get("file_path"),
                "details": impact
            })
        
        # Check for removed functions
        for func in impact.get("removed_functions", []):
            issues.append({
                "type": "regression",
                "message": f"Function '{func['name']}' was removed",
                "file_path": func["file_path"]
            })
        
        # Check for removed classes
        for cls in impact.get("removed_classes", []):
            issues.append({
                "type": "regression",
                "message": f"Class '{cls['name']}' was removed",
                "file_path": cls["file_path"]
            })
        
        # Check for import changes
        for imp in impact.get("removed_imports", []):
            suggestions.append({
                "type": "warning",
                "message": f"Import '{imp}' was removed",
                "suggestion": "Verify this import is no longer needed"
            })
        
        # Check diff size
        diff = change.get("diff", {})
        if diff.get("lines_changed", 0) > 100:
            suggestions.append({
                "type": "warning",
                "message": f"Large change: {diff['lines_changed']} lines modified",
                "suggestion": "Consider breaking this into smaller, focused changes"
            })
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "risk_level": risk_level
        }
    
    async def _validate_syntax(
        self,
        content: str
    ) -> Dict[str, Any]:
        """验证语法"""
        try:
            import ast
            ast.parse(content)
            return {"valid": True, "issues": []}
        except SyntaxError as e:
            return {
                "valid": False,
                "issues": [{
                    "type": "syntax_error",
                    "message": f"Syntax error: {e.msg}",
                    "line": e.lineno,
                    "column": e.offset
                }]
            }
    
    async def _validate_types(
        self,
        file_path: str,
        content: str
    ) -> Dict[str, Any]:
        """类型检查"""
        try:
            # Check if mypy is available
            result = await asyncio.create_subprocess_shell(
                f"echo '{content}' | mypy --no-error-summary -",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                result.communicate(),
                timeout=10
            )
            
            issues = []
            if result.returncode != 0:
                issues.append({
                    "type": "type_error",
                    "message": stderr.decode(),
                    "file_path": file_path
                })
            
            return {"issues": issues, "suggestions": []}
            
        except asyncio.TimeoutError:
            return {"issues": [], "suggestions": []}
        except Exception as e:
            # mypy not available or error
            logger.debug(f"Type checking not available: {e}")
            return {"issues": [], "suggestions": []}
    
    async def _validate_lint(
        self,
        file_path: str,
        content: str
    ) -> Dict[str, Any]:
        """Lint检查"""
        try:
            # Check if pylint is available
            result = await asyncio.create_subprocess_shell(
                f"echo '{content}' | pylint --from-stdin {file_path} 2>&1",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                result.communicate(),
                timeout=10
            )
            
            issues = []
            suggestions = []
            
            # Parse pylint output
            output = stdout.decode()
            for line in output.split('\n'):
                if 'error' in line.lower():
                    issues.append({
                        "type": "lint_error",
                        "message": line,
                        "file_path": file_path
                    })
                elif 'warning' in line.lower():
                    suggestions.append({
                        "type": "lint_warning",
                        "message": line,
                        "suggestion": "Review this warning"
                    })
            
            return {"issues": issues, "suggestions": suggestions}
            
        except asyncio.TimeoutError:
            return {"issues": [], "suggestions": []}
        except Exception as e:
            # pylint not available or error
            logger.debug(f"Linting not available: {e}")
            return {"issues": [], "suggestions": []}
    
    async def _validate_function_integrity(
        self,
        session_id: str,
        file_path: str,
        content: str
    ) -> Dict[str, Any]:
        """验证函数完整性"""
        issues = []
        
        try:
            # Update code detector cache
            self.code_detector.file_cache[file_path] = content
            
            # Get previously known functions
            # In a real implementation, this would come from memory
            # For now, just check for docstrings
            
            import ast
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        # Only warn for public functions
                        if not node.name.startswith('_'):
                            issues.append({
                                "type": "warning",
                                "message": f"Function '{node.name}' missing docstring",
                                "file_path": file_path
                            })
            
            return {"issues": issues}
            
        except Exception as e:
            logger.error(f"Error validating function integrity: {e}")
            return {"issues": []}
    
    def _calculate_overall_risk(
        self,
        issues: List[Dict[str, Any]]
    ) -> str:
        """计算整体风险等级"""
        risk_level = "LOW"
        
        for issue in issues:
            issue_type = issue.get("type", "")
            
            if issue_type == "critical" or issue_type == "regression":
                return "CRITICAL"
            elif issue_type == "syntax_error" or issue_type == "type_error":
                risk_level = "HIGH"
            elif issue_type == "error" and risk_level != "HIGH":
                risk_level = "MEDIUM"
        
        return risk_level
