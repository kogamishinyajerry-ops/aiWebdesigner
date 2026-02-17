"""
Context Manager - Manage AI coding session context
管理AI编码会话的上下文，包括记忆和重建
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import json

from loguru import logger

from .memory_store import MemoryStore


class ContextManager:
    """上下文管理器"""
    
    def __init__(self):
        self.memory_store = MemoryStore()
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def capture_context(
        self,
        session_id: str,
        request_id: str
    ) -> Dict[str, Any]:
        """
        捕获当前上下文
        
        Args:
            session_id: 会话ID
            request_id: 请求ID
            
        Returns:
            上下文快照
        """
        try:
            # Get session state
            session = self.active_sessions.get(session_id, {})
            
            # Capture key information
            context = {
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "active_files": list(session.get("snapshots", {}).keys()),
                "recent_changes": self._get_recent_changes(session_id),
                "decisions_made": self._get_recent_decisions(session_id),
                "constraints": session.get("constraints", {}),
                "language": session.get("language", "python")
            }
            
            logger.info(f"Context captured for request {request_id}")
            
            return context
            
        except Exception as e:
            logger.error(f"Error capturing context: {e}")
            raise
    
    async def get_context(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        获取当前上下文
        
        Args:
            session_id: 会话ID
            
        Returns:
            当前上下文
        """
        try:
            session = self.active_sessions.get(session_id, {})
            
            # Get current context from memory
            current_context = await self.memory_store.get_current_context(session_id)
            
            return {
                "session_id": session_id,
                "language": session.get("language", "python"),
                "active_files": list(session.get("snapshots", {}).keys()),
                "current_context": current_context,
                "session_stats": {
                    "snapshots_count": len(session.get("snapshots", {})),
                    "requests_count": len(session.get("ai_requests", [])),
                    "responses_count": len(session.get("ai_responses", []))
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting context: {e}")
            raise
    
    async def reconstruct_context(
        self,
        session_id: str,
        target_step: int
    ) -> Dict[str, Any]:
        """
        重建上下文到指定步骤
        
        Args:
            session_id: 会话ID
            target_step: 目标步骤（AI响应索引）
            
        Returns:
            重建的上下文
        """
        try:
            # Get session history
            session = self.active_sessions.get(session_id, {})
            responses = session.get("ai_responses", [])
            
            if target_step >= len(responses):
                raise ValueError(f"Target step {target_step} out of range")
            
            # Reconstruct context up to target step
            relevant_responses = responses[:target_step + 1]
            
            # Extract key information
            reconstructed = {
                "session_id": session_id,
                "target_step": target_step,
                "timestamp": datetime.utcnow().isoformat(),
                "code_state": self._extract_code_state(relevant_responses),
                "decisions": self._extract_decisions(relevant_responses),
                "constraints": self._extract_constraints(session, target_step),
                "context_summary": self._generate_context_summary(relevant_responses)
            }
            
            logger.info(f"Context reconstructed to step {target_step}")
            
            return reconstructed
            
        except Exception as e:
            logger.error(f"Error reconstructing context: {e}")
            raise
    
    async def update_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any]
    ):
        """
        更新上下文
        
        Args:
            session_id: 会话ID
            context_updates: 上下文更新
        """
        try:
            session = self.active_sessions.get(session_id, {})
            
            # Update session context
            if "context" not in session:
                session["context"] = {}
            
            session["context"].update(context_updates)
            
            # Store in memory
            await self.memory_store.update_context(session_id, context_updates)
            
            logger.debug(f"Context updated for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error updating context: {e}")
            raise
    
    def _get_recent_changes(
        self,
        session_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """获取最近的代码变更"""
        session = self.active_sessions.get(session_id, {})
        responses = session.get("ai_responses", [])
        
        recent_changes = []
        for response in reversed(responses[-limit:]):
            for change in response.get("code_changes", []):
                recent_changes.append({
                    "file_path": change.get("file_path"),
                    "timestamp": response.get("timestamp"),
                    "change_type": self._classify_change(change)
                })
        
        return recent_changes[:limit]
    
    def _get_recent_decisions(
        self,
        session_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """获取最近的决策"""
        session = self.active_sessions.get(session_id, {})
        responses = session.get("ai_responses", [])
        
        decisions = []
        for response in reversed(responses[-limit:]):
            decisions.append({
                "response_id": response.get("response_id"),
                "timestamp": response.get("timestamp"),
                "summary": self._summarize_response(response)
            })
        
        return decisions[:limit]
    
    def _extract_code_state(
        self,
        responses: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """从响应中提取代码状态"""
        code_state = {}
        
        for response in responses:
            for change in response.get("code_changes", []):
                file_path = change.get("file_path")
                content = change.get("content")
                if file_path and content:
                    code_state[file_path] = content
        
        return code_state
    
    def _extract_decisions(
        self,
        responses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """提取决策历史"""
        decisions = []
        
        for response in responses:
            decisions.append({
                "response_id": response.get("response_id"),
                "timestamp": response.get("timestamp"),
                "changes_count": len(response.get("code_changes", [])),
                "summary": self._summarize_response(response)
            })
        
        return decisions
    
    def _extract_constraints(
        self,
        session: Dict[str, Any],
        target_step: int
    ) -> Dict[str, Any]:
        """提取约束条件"""
        return session.get("constraints", {})
    
    def _generate_context_summary(
        self,
        responses: List[Dict[str, Any]]
    ) -> str:
        """生成上下文摘要"""
        total_changes = sum(len(r.get("code_changes", [])) for r in responses)
        
        return f"""
        工作会话摘要:
        - AI响应数量: {len(responses)}
        - 总代码变更数: {total_changes}
        - 修改的文件数: {len(set(c['file_path'] for r in responses for c in r.get('code_changes', []))}
        """
    
    def _classify_change(
        self,
        change: Dict[str, Any]
    ) -> str:
        """分类变更类型"""
        content = change.get("content", "")
        
        if "def " in content or "class " in content:
            return "function/class"
        elif "import " in content:
            return "import"
        elif "=" in content and "==" not in content:
            return "assignment"
        else:
            return "modification"
    
    def _summarize_response(
        self,
        response: Dict[str, Any]
    ) -> str:
        """总结响应"""
        changes = response.get("code_changes", [])
        return f"Modified {len(changes)} file(s)"
