"""
Memory Store - Persistent storage for sessions, context, and alerts
持久化存储会话、上下文和告警
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import os

from loguru import logger


class MemoryStore:
    """记忆存储"""
    
    def __init__(self, storage_path: str = "./data"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # In-memory cache
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.alerts: Dict[str, List[Dict[str, Any]]] = {}
        
        logger.info(f"MemoryStore initialized with path: {storage_path}")
    
    async def create_session(
        self,
        session_id: str,
        metadata: Dict[str, Any]
    ):
        """创建新会话"""
        try:
            session_data = {
                "session_id": session_id,
                "created_at": datetime.utcnow().isoformat(),
                "metadata": metadata,
                "snapshots": {},
                "ai_requests": [],
                "ai_responses": [],
                "alerts": []
            }
            
            self.sessions[session_id] = session_data
            
            # Persist to disk
            await self._save_session(session_id)
            
            logger.info(f"Session {session_id} created")
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    async def add_code_snapshot(
        self,
        session_id: str,
        file_path: str,
        content: str,
        timestamp: datetime
    ):
        """添加代码快照"""
        try:
            if session_id not in self.sessions:
                await self.create_session(session_id, {})
            
            self.sessions[session_id]["snapshots"][file_path] = {
                "content": content,
                "timestamp": timestamp.isoformat()
            }
            
            await self._save_session(session_id)
            
        except Exception as e:
            logger.error(f"Error adding code snapshot: {e}")
    
    async def add_ai_request(
        self,
        session_id: str,
        request_id: str,
        prompt: str,
        context: Dict[str, Any]
    ):
        """添加AI请求"""
        try:
            if session_id not in self.sessions:
                await self.create_session(session_id, {})
            
            request_data = {
                "request_id": request_id,
                "prompt": prompt,
                "context": context,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.sessions[session_id]["ai_requests"].append(request_data)
            
            await self._save_session(session_id)
            
        except Exception as e:
            logger.error(f"Error adding AI request: {e}")
    
    async def add_ai_response(
        self,
        session_id: str,
        response_id: str,
        request_id: str,
        code_changes: List[Dict[str, str]]
    ):
        """添加AI响应"""
        try:
            if session_id not in self.sessions:
                await self.create_session(session_id, {})
            
            response_data = {
                "response_id": response_id,
                "request_id": request_id,
                "code_changes": code_changes,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.sessions[session_id]["ai_responses"].append(response_data)
            
            await self._save_session(session_id)
            
        except Exception as e:
            logger.error(f"Error adding AI response: {e}")
    
    async def update_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any]
    ):
        """更新上下文"""
        try:
            if session_id not in self.contexts:
                self.contexts[session_id] = {}
            
            self.contexts[session_id].update(context_updates)
            
            await self._save_context(session_id)
            
        except Exception as e:
            logger.error(f"Error updating context: {e}")
    
    async def get_current_context(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """获取当前上下文"""
        try:
            # Load from disk if not in memory
            if session_id not in self.contexts:
                await self._load_context(session_id)
            
            return self.contexts.get(session_id, {})
            
        except Exception as e:
            logger.error(f"Error getting current context: {e}")
            return {}
    
    async def get_original_intent(
        self,
        session_id: str
    ) -> Optional[str]:
        """获取原始意图"""
        try:
            if session_id not in self.sessions:
                await self._load_session(session_id)
            
            # Get the first AI request as original intent
            ai_requests = self.sessions.get(session_id, {}).get("ai_requests", [])
            
            if ai_requests:
                return ai_requests[0].get("prompt")
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting original intent: {e}")
            return None
    
    async def get_session_history(
        self,
        session_id: str
    ) -> List[Dict[str, Any]]:
        """获取会话历史"""
        try:
            if session_id not in self.sessions:
                await self._load_session(session_id)
            
            session = self.sessions.get(session_id, {})
            
            # Combine requests and responses
            history = []
            
            for i, request in enumerate(session.get("ai_requests", [])):
                history.append({
                    "type": "request",
                    "index": i * 2,
                    "data": request
                })
                
                # Add corresponding response if exists
                if i < len(session.get("ai_responses", [])):
                    history.append({
                        "type": "response",
                        "index": i * 2 + 1,
                        "data": session["ai_responses"][i]
                    })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting session history: {e}")
            return []
    
    async def add_alerts(
        self,
        session_id: str,
        alerts: List[Any]  # Alert objects from alert_system
    ):
        """添加告警"""
        try:
            if session_id not in self.alerts:
                self.alerts[session_id] = []
            
            # Convert Alert objects to dicts
            alert_dicts = [alert.dict() for alert in alerts]
            
            self.alerts[session_id].extend(alert_dicts)
            
            await self._save_alerts(session_id)
            
        except Exception as e:
            logger.error(f"Error adding alerts: {e}")
    
    async def get_alerts(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """获取告警"""
        try:
            if session_id not in self.alerts:
                await self._load_alerts(session_id)
            
            session_alerts = self.alerts.get(session_id, [])
            
            # Return most recent alerts
            return session_alerts[-limit:]
            
        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            return []
    
    async def resolve_alert(
        self,
        session_id: str,
        alert_id: str
    ):
        """解决告警"""
        try:
            if session_id not in self.alerts:
                return
            
            for alert in self.alerts[session_id]:
                if alert["alert_id"] == alert_id:
                    alert["resolved"] = True
                    alert["resolved_at"] = datetime.utcnow().isoformat()
                    break
            
            await self._save_alerts(session_id)
            
        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
    
    async def delete_session(
        self,
        session_id: str
    ):
        """删除会话"""
        try:
            # Remove from memory
            self.sessions.pop(session_id, None)
            self.contexts.pop(session_id, None)
            self.alerts.pop(session_id, None)
            
            # Remove from disk
            session_file = os.path.join(self.storage_path, f"{session_id}.json")
            context_file = os.path.join(self.storage_path, f"{session_id}_context.json")
            alerts_file = os.path.join(self.storage_path, f"{session_id}_alerts.json")
            
            for file_path in [session_file, context_file, alerts_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            logger.info(f"Session {session_id} deleted")
            
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
    
    async def _save_session(self, session_id: str):
        """保存会话到磁盘"""
        try:
            session_file = os.path.join(self.storage_path, f"{session_id}.json")
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions[session_id], f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error saving session: {e}")
    
    async def _load_session(self, session_id: str):
        """从磁盘加载会话"""
        try:
            session_file = os.path.join(self.storage_path, f"{session_id}.json")
            
            if os.path.exists(session_file):
                with open(session_file, 'r', encoding='utf-8') as f:
                    self.sessions[session_id] = json.load(f)
            
        except Exception as e:
            logger.error(f"Error loading session: {e}")
    
    async def _save_context(self, session_id: str):
        """保存上下文到磁盘"""
        try:
            context_file = os.path.join(self.storage_path, f"{session_id}_context.json")
            
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(self.contexts.get(session_id, {}), f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error saving context: {e}")
    
    async def _load_context(self, session_id: str):
        """从磁盘加载上下文"""
        try:
            context_file = os.path.join(self.storage_path, f"{session_id}_context.json")
            
            if os.path.exists(context_file):
                with open(context_file, 'r', encoding='utf-8') as f:
                    self.contexts[session_id] = json.load(f)
            
        except Exception as e:
            logger.error(f"Error loading context: {e}")
    
    async def _save_alerts(self, session_id: str):
        """保存告警到磁盘"""
        try:
            alerts_file = os.path.join(self.storage_path, f"{session_id}_alerts.json")
            
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump(self.alerts.get(session_id, []), f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Error saving alerts: {e}")
    
    async def _load_alerts(self, session_id: str):
        """从磁盘加载告警"""
        try:
            alerts_file = os.path.join(self.storage_path, f"{session_id}_alerts.json")
            
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r', encoding='utf-8') as f:
                    self.alerts[session_id] = json.load(f)
            
        except Exception as e:
            logger.error(f"Error loading alerts: {e}")
