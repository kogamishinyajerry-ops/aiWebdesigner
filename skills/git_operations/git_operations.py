"""
Git 操作技能

提供 Git 版本控制相关的功能
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

from skills import Skill, SkillMetadata


class GitOperationsSkill(Skill):
    """Git 操作技能"""
    
    def _on_load(self):
        """加载时的初始化"""
        print(f"加载 {self.metadata.name} 技能...")
        self._check_git_available()
    
    def _on_unload(self):
        """卸载时的清理"""
        print(f"卸载 {self.metadata.name} 技能...")
    
    def _check_git_available(self):
        """检查 Git 是否可用"""
        try:
            result = subprocess.run(['git', '--version'], 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=5)
            if result.returncode == 0:
                print(f"Git 可用: {result.stdout.strip()}")
            else:
                print("警告: Git 不可用")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("警告: Git 未安装或不在 PATH 中")
    
    def _action_get_status(self, **kwargs) -> Dict[str, Any]:
        """获取 Git 状态
        
        Args:
            repo_path: 仓库路径（可选，默认当前目录）
            
        Returns:
            Git 状态信息
        """
        repo_path = kwargs.get('repo_path', '.')
        repo = Path(repo_path)
        
        if not (repo / '.git').exists():
            return {"error": f"不是 Git 仓库: {repo_path}"}
        
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {"error": f"获取状态失败: {result.stderr}"}
            
            # 解析状态
            staged = []
            unstaged = []
            untracked = []
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                status = line[:2]
                filename = line[3:].strip()
                
                if status in ('M ', 'MM', 'AM', 'RM', 'CM'):
                    staged.append({
                        "file": filename,
                        "status": status,
                        "change": "已暂存"
                    })
                
                if status[1] == 'M':
                    unstaged.append({
                        "file": filename,
                        "status": status,
                        "change": "未暂存的修改"
                    })
                
                if status == '??':
                    untracked.append({
                        "file": filename,
                        "status": status,
                        "change": "未跟踪"
                    })
            
            # 获取当前分支
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=10
            )
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
            
            return {
                "repo_path": str(repo),
                "current_branch": current_branch,
                "staged": staged,
                "unstaged": unstaged,
                "untracked": untracked,
                "summary": {
                    "staged_count": len(staged),
                    "unstaged_count": len(unstaged),
                    "untracked_count": len(untracked)
                }
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "命令执行超时"}
        except Exception as e:
            return {"error": f"获取状态失败: {str(e)}"}
    
    def _action_create_commit(self, **kwargs) -> Dict[str, Any]:
        """创建提交
        
        Args:
            message: 提交消息（必需）
            add_all: 是否添加所有更改（可选，默认 False）
            files: 要添加的文件列表（可选）
            repo_path: 仓库路径（可选，默认当前目录）
            
        Returns:
            提交结果
        """
        message = kwargs.get('message')
        if not message:
            return {"error": "缺少 message 参数"}
        
        repo_path = kwargs.get('repo_path', '.')
        repo = Path(repo_path)
        add_all = kwargs.get('add_all', False)
        files = kwargs.get('files', [])
        
        try:
            # 添加文件
            if add_all:
                subprocess.run(['git', 'add', '.'], cwd=repo, check=True, timeout=60)
            elif files:
                for file in files:
                    subprocess.run(['git', 'add', file], cwd=repo, check=True, timeout=30)
            
            # 创建提交
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return {"error": f"提交失败: {result.stderr}"}
            
            # 获取提交哈希
            hash_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=10
            )
            commit_hash = hash_result.stdout.strip() if hash_result.returncode == 0 else "unknown"
            
            return {
                "success": True,
                "commit_hash": commit_hash,
                "message": message
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "命令执行超时"}
        except subprocess.CalledProcessError as e:
            return {"error": f"命令执行失败: {str(e)}"}
        except Exception as e:
            return {"error": f"提交失败: {str(e)}"}
    
    def _action_create_branch(self, **kwargs) -> Dict[str, Any]:
        """创建分支
        
        Args:
            branch_name: 分支名称（必需）
            checkout: 是否切换到新分支（可选，默认 False）
            repo_path: 仓库路径（可选，默认当前目录）
            
        Returns:
            创建结果
        """
        branch_name = kwargs.get('branch_name')
        if not branch_name:
            return {"error": "缺少 branch_name 参数"}
        
        repo_path = kwargs.get('repo_path', '.')
        repo = Path(repo_path)
        checkout = kwargs.get('checkout', False)
        
        try:
            # 创建分支
            result = subprocess.run(
                ['git', 'branch', branch_name],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {"error": f"创建分支失败: {result.stderr}"}
            
            # 切换分支（如果需要）
            if checkout:
                checkout_result = subprocess.run(
                    ['git', 'checkout', branch_name],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if checkout_result.returncode != 0:
                    return {"error": f"切换分支失败: {checkout_result.stderr}"}
            
            return {
                "success": True,
                "branch_name": branch_name,
                "checked_out": checkout
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "命令执行超时"}
        except Exception as e:
            return {"error": f"创建分支失败: {str(e)}"}
    
    def _action_view_history(self, **kwargs) -> Dict[str, Any]:
        """查看提交历史
        
        Args:
            limit: 返回的提交数量（可选，默认 10）
            repo_path: 仓库路径（可选，默认当前目录）
            
        Returns:
            提交历史
        """
        limit = kwargs.get('limit', 10)
        repo_path = kwargs.get('repo_path', '.')
        repo = Path(repo_path)
        
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', '-n', str(limit), 
                 '--pretty=format:%H|%an|%ae|%ad|%s', 
                 '--date=iso'],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {"error": f"获取历史失败: {result.stderr}"}
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split('|', 4)
                if len(parts) == 5:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    })
            
            return {
                "repo_path": str(repo),
                "commits": commits,
                "total": len(commits)
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "命令执行超时"}
        except Exception as e:
            return {"error": f"获取历史失败: {str(e)}"}
    
    def _action_merge_branches(self, **kwargs) -> Dict[str, Any]:
        """合并分支
        
        Args:
            source_branch: 源分支（必需）
            target_branch: 目标分支（可选，默认当前分支）
            repo_path: 仓库路径（可选，默认当前目录）
            
        Returns:
            合并结果
        """
        source_branch = kwargs.get('source_branch')
        if not source_branch:
            return {"error": "缺少 source_branch 参数"}
        
        repo_path = kwargs.get('repo_path', '.')
        repo = Path(repo_path)
        target_branch = kwargs.get('target_branch')
        
        try:
            # 如果指定了目标分支，先切换
            if target_branch:
                subprocess.run(
                    ['git', 'checkout', target_branch],
                    cwd=repo,
                    check=True,
                    timeout=30
                )
            
            # 合并分支
            result = subprocess.run(
                ['git', 'merge', source_branch, '--no-edit'],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return {
                    "error": f"合并失败",
                    "details": result.stderr,
                    "conflicts": True if "conflict" in result.stderr.lower() else False
                }
            
            return {
                "success": True,
                "source_branch": source_branch,
                "target_branch": target_branch or "current"
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "命令执行超时"}
        except Exception as e:
            return {"error": f"合并失败: {str(e)}"}
    
    def _action_resolve_conflicts(self, **kwargs) -> Dict[str, Any]:
        """列出冲突文件（不自动解决冲突）
        
        Args:
            repo_path: 仓库路径（可选，默认当前目录）
            
        Returns:
            冲突信息
        """
        repo_path = kwargs.get('repo_path', '.')
        repo = Path(repo_path)
        
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', '--diff-filter=U'],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {"error": f"查找冲突失败: {result.stderr}"}
            
            conflict_files = [f for f in result.stdout.strip().split('\n') if f]
            
            return {
                "conflict_files": conflict_files,
                "count": len(conflict_files),
                "message": f"发现 {len(conflict_files)} 个冲突文件"
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "命令执行超时"}
        except Exception as e:
            return {"error": f"查找冲突失败: {str(e)}"}
