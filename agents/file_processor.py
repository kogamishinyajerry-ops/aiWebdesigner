"""
文件处理代理

用于批量处理、转换和操作文件
"""

import asyncio
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import mimetypes

from agents import Agent, AgentTask, AgentResult, AgentCapability


class FileProcessorAgent(Agent):
    """文件处理代理"""
    
    def __init__(self):
        super().__init__(
            name="file_processor",
            description="文件处理代理，用于批量处理、转换和操作文件"
        )
        self._capabilities = [
            AgentCapability(
                name="batch_rename",
                description="批量重命名文件",
                category="file_operations",
                required_tools=[]
            ),
            AgentCapability(
                name="batch_convert",
                description="批量转换文件格式",
                category="file_operations",
                required_tools=[]
            ),
            AgentCapability(
                name="filter_files",
                description="按条件筛选文件",
                category="file_operations",
                required_tools=[]
            ),
            AgentCapability(
                name="process_files",
                description="批量处理文件",
                category="file_operations",
                required_tools=[]
            ),
            AgentCapability(
                name="validate_structure",
                description="验证目录结构",
                category="file_operations",
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
            
            if task_type == "batch_rename":
                result = await self._batch_rename(params)
            elif task_type == "batch_convert":
                result = await self._batch_convert(params)
            elif task_type == "filter_files":
                result = await self._filter_files(params)
            elif task_type == "process_files":
                result = await self._process_files(params)
            elif task_type == "validate_structure":
                result = await self._validate_structure(params)
            else:
                result = await self._general_process(task.description, params)
            
            steps.append("完成处理")
            
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
        
        if "重命名" in description_lower or "rename" in description_lower:
            return "batch_rename"
        elif "转换" in description_lower or "convert" in description_lower:
            return "batch_convert"
        elif "筛选" in description_lower or "filter" in description_lower:
            return "filter_files"
        elif "验证" in description_lower or "validate" in description_lower:
            return "validate_structure"
        else:
            return "process_files"
    
    async def _batch_rename(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """批量重命名文件"""
        directory = params.get("directory", ".")
        pattern = params.get("pattern", "*")
        replacement = params.get("replacement", "")
        dry_run = params.get("dry_run", True)
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        files = list(dir_path.glob(pattern))
        renamed = []
        errors = []
        
        for file_path in files:
            if file_path.is_file():
                old_name = file_path.name
                new_name = old_name.replace(pattern, replacement)
                
                if new_name != old_name:
                    renamed.append({
                        "old_path": str(file_path),
                        "new_path": str(file_path.parent / new_name),
                        "old_name": old_name,
                        "new_name": new_name
                    })
                    
                    if not dry_run:
                        try:
                            file_path.rename(file_path.parent / new_name)
                        except Exception as e:
                            errors.append({
                                "file": str(file_path),
                                "error": str(e)
                            })
        
        return {
            "success": True,
            "total_files": len(files),
            "renamed_count": len(renamed),
            "renamed": renamed,
            "errors": errors,
            "dry_run": dry_run
        }
    
    async def _batch_convert(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """批量转换文件格式"""
        directory = params.get("directory", ".")
        source_ext = params.get("source_ext")
        target_ext = params.get("target_ext")
        dry_run = params.get("dry_run", True)
        
        if not source_ext or not target_ext:
            return {"error": "缺少 source_ext 或 target_ext 参数"}
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        # 确保扩展名以点开头
        if not source_ext.startswith('.'):
            source_ext = '.' + source_ext
        if not target_ext.startswith('.'):
            target_ext = '.' + target_ext
        
        files = list(dir_path.glob(f"*{source_ext}"))
        converted = []
        errors = []
        
        for file_path in files:
            if file_path.is_file():
                new_path = file_path.with_suffix(target_ext)
                converted.append({
                    "source": str(file_path),
                    "target": str(new_path),
                    "source_ext": source_ext,
                    "target_ext": target_ext
                })
                
                if not dry_run:
                    try:
                        # 对于支持的格式进行转换
                        if source_ext == '.txt' and target_ext == '.md':
                            content = file_path.read_text(encoding='utf-8')
                            new_path.write_text(content, encoding='utf-8')
                        elif source_ext in ['.md', '.txt'] and target_ext in ['.md', '.txt']:
                            shutil.copy2(file_path, new_path)
                        else:
                            errors.append({
                                "file": str(file_path),
                                "error": "不支持的转换格式"
                            })
                    except Exception as e:
                        errors.append({
                            "file": str(file_path),
                            "error": str(e)
                        })
        
        return {
            "success": True,
            "total_files": len(files),
            "converted_count": len(converted),
            "converted": converted,
            "errors": errors,
            "dry_run": dry_run
        }
    
    async def _filter_files(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """筛选文件"""
        directory = params.get("directory", ".")
        extensions = params.get("extensions", [])
        pattern = params.get("pattern", "*")
        min_size = params.get("min_size", 0)
        max_size = params.get("max_size", float('inf'))
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        files = list(dir_path.glob(pattern))
        filtered = []
        
        for file_path in files:
            if not file_path.is_file():
                continue
            
            # 检查扩展名
            if extensions:
                if file_path.suffix.lower() not in [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]:
                    continue
            
            # 检查大小
            try:
                file_size = file_path.stat().st_size
                if file_size < min_size or file_size > max_size:
                    continue
            except OSError:
                continue
            
            # 检测文件类型
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            filtered.append({
                "path": str(file_path),
                "name": file_path.name,
                "extension": file_path.suffix,
                "size": file_path.stat().st_size,
                "mime_type": mime_type
            })
        
        return {
            "success": True,
            "total_files": len(files),
            "filtered_count": len(filtered),
            "files": filtered
        }
    
    async def _process_files(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """批量处理文件"""
        directory = params.get("directory", ".")
        pattern = params.get("pattern", "*")
        operation = params.get("operation", "read")
        dry_run = params.get("dry_run", True)
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        files = list(dir_path.glob(pattern))
        processed = []
        errors = []
        
        for file_path in files:
            if not file_path.is_file():
                continue
            
            try:
                result = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "operation": operation
                }
                
                if operation == "read":
                    content = file_path.read_text(encoding='utf-8')
                    result["preview"] = content[:200] if len(content) > 200 else content
                    result["size"] = len(content)
                
                elif operation == "delete" and not dry_run:
                    file_path.unlink()
                    result["deleted"] = True
                
                elif operation == "count_lines":
                    lines = file_path.read_text(encoding='utf-8').count('\n') + 1
                    result["lines"] = lines
                
                processed.append(result)
                
            except Exception as e:
                errors.append({
                    "file": str(file_path),
                    "error": str(e)
                })
        
        return {
            "success": True,
            "total_files": len(files),
            "processed_count": len(processed),
            "processed": processed,
            "errors": errors,
            "dry_run": dry_run
        }
    
    async def _validate_structure(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """验证目录结构"""
        directory = params.get("directory", ".")
        required_files = params.get("required_files", [])
        required_dirs = params.get("required_dirs", [])
        forbidden_patterns = params.get("forbidden_patterns", [])
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        results = {
            "directory": str(dir_path),
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        # 检查必需的文件
        for required_file in required_files:
            file_path = dir_path / required_file
            if not file_path.exists():
                results["issues"].append({
                    "type": "missing_file",
                    "path": required_file,
                    "message": f"缺少必需文件: {required_file}"
                })
                results["valid"] = False
        
        # 检查必需的目录
        for required_dir in required_dirs:
            dir_to_check = dir_path / required_dir
            if not dir_to_check.exists() or not dir_to_check.is_dir():
                results["issues"].append({
                    "type": "missing_directory",
                    "path": required_dir,
                    "message": f"缺少必需目录: {required_dir}"
                })
                results["valid"] = False
        
        # 检查禁止的模式
        for pattern in forbidden_patterns:
            matches = list(dir_path.glob(pattern))
            for match in matches:
                results["warnings"].append({
                    "type": "forbidden_pattern",
                    "path": str(match.relative_to(dir_path)),
                    "pattern": pattern,
                    "message": f"发现禁止的文件模式: {pattern}"
                })
        
        # 统计信息
        all_files = list(dir_path.rglob("*"))
        results["stats"] = {
            "total_items": len(all_files),
            "files": len([f for f in all_files if f.is_file()]),
            "directories": len([d for d in all_files if d.is_dir()])
        }
        
        return results
    
    async def _general_process(self, description: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """通用文件处理"""
        directory = params.get("directory", ".")
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"目录不存在: {directory}"}
        
        results = {
            "description": description,
            "directory": directory,
            "findings": []
        }
        
        # 收集基本信息
        files = [f for f in dir_path.iterdir() if f.is_file()]
        dirs = [d for d in dir_path.iterdir() if d.is_dir()]
        
        results["findings"] = [
            {"type": "info", "message": f"发现 {len(files)} 个文件"},
            {"type": "info", "message": f"发现 {len(dirs)} 个目录"}
        ]
        
        return results
    
    def can_handle(self, task_description: str) -> bool:
        """判断是否可以处理该任务"""
        keywords = [
            "文件", "file", "重命名", "rename", "转换", "convert",
            "筛选", "filter", "处理", "process", "批量", "batch",
            "目录", "directory", "结构", "structure", "验证", "validate"
        ]
        return any(keyword in task_description.lower() for keyword in keywords)
