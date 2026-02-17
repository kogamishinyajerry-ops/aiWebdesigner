"""
代码分析技能

提供代码结构分析、依赖检测、复杂度分析等功能
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict, Counter
import json

from skills import Skill, SkillMetadata


class CodeAnalysisSkill(Skill):
    """代码分析技能"""
    
    def _on_load(self):
        """加载时的初始化"""
        print(f"加载 {self.metadata.name} 技能...")
        self._cache = {}
    
    def _on_unload(self):
        """卸载时的清理"""
        print(f"卸载 {self.metadata.name} 技能...")
        self._cache.clear()
    
    def _action_analyze_code_structure(self, **kwargs) -> Dict[str, Any]:
        """分析代码结构
        
        Args:
            file_path: 文件路径（必需）
            
        Returns:
            代码结构分析结果
        """
        file_path = kwargs.get('file_path')
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            result = {
                "file_path": str(path),
                "language": self._detect_language(path),
                "lines": content.count('\n') + 1,
                "imports": self._extract_imports(tree),
                "classes": self._extract_classes(tree),
                "functions": self._extract_functions(tree),
                "complexity": self._calculate_complexity(tree)
            }
            
            return result
            
        except SyntaxError as e:
            return {"error": f"语法错误: {str(e)}"}
        except Exception as e:
            return {"error": f"分析失败: {str(e)}"}
    
    def _action_detect_code_smells(self, **kwargs) -> List[Dict[str, Any]]:
        """检测代码异味
        
        Args:
            file_path: 文件路径（必需）
            
        Returns:
            检测到的代码异味列表
        """
        file_path = kwargs.get('file_path')
        if not file_path:
            return [{"error": "缺少 file_path 参数"}]
        
        path = Path(file_path)
        if not path.exists():
            return [{"error": f"文件不存在: {file_path}"}]
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            smells = []
            
            # 检测长函数
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    lines = node.end_lineno - node.lineno if node.end_lineno else 0
                    if lines > 50:
                        smells.append({
                            "type": "long_function",
                            "severity": "warning",
                            "message": f"函数 {node.name} 过长 ({lines} 行)",
                            "location": f"{node.lineno}:{node.col_offset}"
                        })
            
            # 检测重复代码（简单版）
            lines = content.split('\n')
            line_counts = Counter(lines)
            for line, count in line_counts.items():
                if count > 3 and len(line.strip()) > 20:
                    smells.append({
                        "type": "duplicate_code",
                        "severity": "info",
                        "message": f"重复的代码行 (出现 {count} 次)",
                        "location": line.strip()[:50] + "..."
                    })
            
            return smells
            
        except Exception as e:
            return [{"error": f"检测失败: {str(e)}"}]
    
    def _action_find_dependencies(self, **kwargs) -> Dict[str, Any]:
        """查找依赖关系
        
        Args:
            file_path: 文件路径（必需）
            include_external: 是否包含外部依赖（可选，默认 False）
            
        Returns:
            依赖关系结果
        """
        file_path = kwargs.get('file_path')
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        include_external = kwargs.get('include_external', False)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            internal_deps = set()
            external_deps = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name.split('.')[0]
                        external_deps.add(module)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module.split('.')[0]
                        if not include_external:
                            external_deps.add(module)
                        else:
                            internal_deps.add(module)
            
            return {
                "file_path": str(path),
                "internal_dependencies": sorted(internal_deps),
                "external_dependencies": sorted(external_deps),
                "total_dependencies": len(internal_deps) + len(external_deps)
            }
            
        except Exception as e:
            return {"error": f"查找失败: {str(e)}"}
    
    def _action_analyze_complexity(self, **kwargs) -> Dict[str, Any]:
        """分析代码复杂度
        
        Args:
            file_path: 文件路径（必需）
            
        Returns:
            复杂度分析结果
        """
        file_path = kwargs.get('file_path')
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            function_complexity = {}
            total_complexity = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    complexity = self._calculate_cyclomatic_complexity(node)
                    function_complexity[node.name] = {
                        "complexity": complexity,
                        "line": node.lineno,
                        "level": self._get_complexity_level(complexity)
                    }
                    total_complexity += complexity
            
            avg_complexity = total_complexity / len(function_complexity) if function_complexity else 0
            
            return {
                "file_path": str(path),
                "total_complexity": total_complexity,
                "average_complexity": round(avg_complexity, 2),
                "function_complexity": function_complexity,
                "overall_level": self._get_complexity_level(avg_complexity)
            }
            
        except Exception as e:
            return {"error": f"分析失败: {str(e)}"}
    
    def _action_generate_documentation(self, **kwargs) -> Dict[str, Any]:
        """生成代码文档
        
        Args:
            file_path: 文件路径（必需）
            
        Returns:
            生成的文档
        """
        file_path = kwargs.get('file_path')
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            doc = {
                "file": str(path),
                "description": f"自动生成的文档: {path.name}",
                "classes": [],
                "functions": []
            }
            
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node),
                        "methods": []
                    }
                    
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            class_info["methods"].append({
                                "name": item.name,
                                "line": item.lineno,
                                "docstring": ast.get_docstring(item)
                            })
                    
                    doc["classes"].append(class_info)
                
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    doc["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node)
                    })
            
            return doc
            
        except Exception as e:
            return {"error": f"生成失败: {str(e)}"}
    
    def _detect_language(self, path: Path) -> str:
        """检测文件语言"""
        ext = path.suffix.lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust'
        }
        return lang_map.get(ext, 'unknown')
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """提取导入语句"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                imports.append(module)
        return list(set(imports))
    
    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """提取类定义"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = [self._get_node_name(base) for base in node.bases]
                methods = []
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)
                
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "bases": bases,
                    "methods": methods,
                    "docstring": ast.get_docstring(node)
                })
        return classes
    
    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """提取函数定义"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [arg.arg for arg in node.args.args]
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": args,
                    "docstring": ast.get_docstring(node)
                })
        return functions
    
    def _calculate_complexity(self, tree: ast.AST) -> Dict[str, int]:
        """计算复杂度"""
        return {
            "classes": len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]),
            "functions": len([n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]),
            "imports": len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))])
        }
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """计算圈复杂度"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
        
        return complexity
    
    def _get_complexity_level(self, complexity: float) -> str:
        """获取复杂度等级"""
        if complexity <= 5:
            return "low"
        elif complexity <= 10:
            return "moderate"
        elif complexity <= 20:
            return "high"
        else:
            return "very_high"
    
    def _get_node_name(self, node: ast.AST) -> str:
        """获取节点名称"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_node_name(node.value)}.{node.attr}"
        return ""
