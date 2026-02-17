"""
Code Change Detector - Detect and analyze code changes
检测和分析代码变更，包括AST分析和影响分析
"""

from typing import Dict, List, Any, Optional, Set
import ast
import difflib
from datetime import datetime

from loguru import logger


class CodeChangeDetector:
    """代码变更检测器"""
    
    def __init__(self):
        self.file_cache: Dict[str, str] = {}
        self.ast_cache: Dict[str, ast.AST] = {}
    
    async def analyze_change(
        self,
        session_id: str,
        file_path: str,
        new_content: str
    ) -> List[Dict[str, Any]]:
        """
        分析代码变更
        
        Args:
            session_id: 会话ID
            file_path: 文件路径
            new_content: 新的代码内容
            
        Returns:
            检测到的变更列表
        """
        try:
            changes = []
            
            # Get previous content
            old_content = self.file_cache.get(file_path, "")
            
            if old_content == new_content:
                return []  # No changes
            
            # Calculate diff
            diff = self._calculate_diff(old_content, new_content)
            
            # Parse AST for both versions
            old_ast = self._parse_ast(old_content)
            new_ast = self._parse_ast(new_content)
            
            # Analyze impact
            impact = self._analyze_impact(old_ast, new_ast, file_path)
            
            # Update cache
            self.file_cache[file_path] = new_content
            self.ast_cache[file_path] = new_ast
            
            changes.append({
                "file_path": file_path,
                "change_type": "modification",
                "diff": diff,
                "impact": impact,
                "timestamp": datetime.utcnow().isoformat(),
                "risk_level": self._calculate_risk_level(impact)
            })
            
            logger.info(f"Change detected in {file_path}: {len(diff.lines_changed)} lines changed")
            
            return changes
            
        except Exception as e:
            logger.error(f"Error analyzing change: {e}")
            raise
    
    def _parse_ast(
        self,
        code: str
    ) -> Optional[ast.AST]:
        """解析AST"""
        try:
            return ast.parse(code)
        except SyntaxError as e:
            logger.warning(f"Syntax error parsing AST: {e}")
            return None
    
    def _calculate_diff(
        self,
        old_content: str,
        new_content: str
    ) -> Dict[str, Any]:
        """计算差异"""
        diff_lines = list(difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            lineterm="",
            fromfile="old",
            tofile="new"
        ))
        
        added_lines = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
        removed_lines = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
        
        return {
            "diff_lines": diff_lines,
            "lines_added": added_lines,
            "lines_removed": removed_lines,
            "lines_changed": added_lines + removed_lines
        }
    
    def _analyze_impact(
        self,
        old_ast: Optional[ast.AST],
        new_ast: Optional[ast.AST],
        file_path: str
    ) -> Dict[str, Any]:
        """分析变更影响"""
        impact = {
            "modified_functions": [],
            "added_functions": [],
            "removed_functions": [],
            "modified_classes": [],
            "added_classes": [],
            "removed_classes": [],
            "modified_imports": [],
            "added_imports": [],
            "removed_imports": [],
            "critical_changes": False
        }
        
        if not old_ast or not new_ast:
            return impact
        
        # Extract functions and classes
        old_functions = self._extract_functions(old_ast)
        new_functions = self._extract_functions(new_ast)
        old_classes = self._extract_classes(old_ast)
        new_classes = self._extract_classes(new_ast)
        old_imports = self._extract_imports(old_ast)
        new_imports = self._extract_imports(new_ast)
        
        # Analyze function changes
        for name in old_functions:
            if name not in new_functions:
                impact["removed_functions"].append({
                    "name": name,
                    "file_path": file_path
                })
                impact["critical_changes"] = True
        
        for name in new_functions:
            if name not in old_functions:
                impact["added_functions"].append({
                    "name": name,
                    "file_path": file_path
                })
            else:
                # Function modified
                impact["modified_functions"].append({
                    "name": name,
                    "file_path": file_path
                })
        
        # Analyze class changes
        for name in old_classes:
            if name not in new_classes:
                impact["removed_classes"].append({
                    "name": name,
                    "file_path": file_path
                })
                impact["critical_changes"] = True
        
        for name in new_classes:
            if name not in old_classes:
                impact["added_classes"].append({
                    "name": name,
                    "file_path": file_path
                })
            else:
                # Class modified
                impact["modified_classes"].append({
                    "name": name,
                    "file_path": file_path
                })
        
        # Analyze import changes
        for imp in old_imports:
            if imp not in new_imports:
                impact["removed_imports"].append(imp)
        
        for imp in new_imports:
            if imp not in old_imports:
                impact["added_imports"].append(imp)
            else:
                impact["modified_imports"].append(imp)
        
        return impact
    
    def _extract_functions(
        self,
        tree: ast.AST
    ) -> Set[str]:
        """提取函数名"""
        functions = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.add(node.name)
            elif isinstance(node, ast.AsyncFunctionDef):
                functions.add(node.name)
        
        return functions
    
    def _extract_classes(
        self,
        tree: ast.AST
    ) -> Set[str]:
        """提取类名"""
        classes = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.add(node.name)
        
        return classes
    
    def _extract_imports(
        self,
        tree: ast.AST
    ) -> Set[str]:
        """提取导入"""
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    full_import = f"{module}.{alias.name}" if module else alias.name
                    imports.add(full_import)
        
        return imports
    
    def _calculate_risk_level(
        self,
        impact: Dict[str, Any]
    ) -> str:
        """计算风险等级"""
        if impact["critical_changes"]:
            return "CRITICAL"
        elif (
            impact["modified_functions"] or
            impact["modified_classes"]
        ):
            return "HIGH"
        elif (
            impact["added_imports"] or
            impact["removed_imports"]
        ):
            return "MEDIUM"
        else:
            return "LOW"
    
    def check_function_integrity(
        self,
        session_id: str,
        file_path: str,
        function_name: str
    ) -> Dict[str, Any]:
        """
        检查函数完整性
        
        Args:
            session_id: 会话ID
            file_path: 文件路径
            function_name: 函数名
            
        Returns:
            完整性检查结果
        """
        try:
            content = self.file_cache.get(file_path, "")
            ast_tree = self._parse_ast(content)
            
            if not ast_tree:
                return {
                    "function_name": function_name,
                    "exists": False,
                    "status": "error",
                    "message": "Syntax error in file"
                }
            
            # Find function
            function_node = None
            for node in ast.walk(ast_tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name == function_name:
                        function_node = node
                        break
            
            if not function_node:
                return {
                    "function_name": function_name,
                    "exists": False,
                    "status": "missing",
                    "message": "Function not found"
                }
            
            # Check function structure
            has_return = any(
                isinstance(node, ast.Return)
                for node in ast.walk(function_node)
            )
            
            has_docstring = ast.get_docstring(function_node) is not None
            
            return {
                "function_name": function_name,
                "exists": True,
                "status": "valid",
                "has_return": has_return,
                "has_docstring": has_docstring,
                "args": [arg.arg for arg in function_node.args.args],
                "decorators": [self._get_decorator_name(d) for d in function_node.decorator_list]
            }
            
        except Exception as e:
            logger.error(f"Error checking function integrity: {e}")
            raise
    
    def _get_decorator_name(self, decorator: ast.expr) -> Optional[str]:
        """获取装饰器名称"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
        return None
