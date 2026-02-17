"""
对话管理模块
Conversation Manager Module
管理用户对话、上下文和意图识别
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Message:
    """对话消息"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Session:
    """对话会话"""
    session_id: str
    messages: List[Message] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    case_info: Dict[str, Any] = field(default_factory=dict)


class ConversationManager:
    """对话管理器"""

    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.max_messages_per_session = 50

    def create_session(self) -> str:
        """创建新的对话会话"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        self.sessions[session_id] = Session(session_id=session_id)
        return session_id

    def add_message(self, session_id: str, role: str, content: str,
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """添加消息到会话"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        session.messages.append(message)
        session.updated_at = datetime.now()

        # 限制消息数量
        if len(session.messages) > self.max_messages_per_session:
            session.messages = session.messages[-self.max_messages_per_session:]

    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话"""
        return self.sessions.get(session_id)

    def get_context(self, session_id: str) -> Dict[str, Any]:
        """获取对话上下文"""
        session = self.get_session(session_id)
        if not session:
            return {}

        return session.context

    def update_context(self, session_id: str, context: Dict[str, Any]) -> None:
        """更新对话上下文"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        self.sessions[session_id].context.update(context)
        self.sessions[session_id].updated_at = datetime.now()

    def get_messages(self, session_id: str,
                     last_n: Optional[int] = None) -> List[Message]:
        """获取消息历史"""
        session = self.get_session(session_id)
        if not session:
            return []

        messages = session.messages
        if last_n:
            return messages[-last_n:]

        return messages

    def detect_intent(self, message: str) -> Dict[str, Any]:
        """检测用户意图"""
        message_lower = message.lower()

        # 意图分类
        intents = {
            "consult": ["咨询", "问", "怎么", "如何", "法律"],
            "report": ["报案", "起诉", "投诉", "举报", "维权"],
            "analyze": ["分析", "判断", "评估", "风险"],
            "generate": ["生成", "写", "材料", "文档"],
            "evidence": ["证据", "证明", "材料", "文件"],
        }

        detected_intent = "unknown"
        confidence = 0.0

        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > 0:
                current_confidence = matches / len(keywords)
                if current_confidence > confidence:
                    confidence = current_confidence
                    detected_intent = intent

        return {
            "intent": detected_intent,
            "confidence": confidence,
            "entities": self._extract_entities(message)
        }

    def _extract_entities(self, message: str) -> Dict[str, List[str]]:
        """提取实体信息"""
        entities = {
            "time": [],
            "location": [],
            "person": [],
            "amount": [],
            "organization": []
        }

        # 简单的关键词匹配（实际应使用 NER）
        import re

        # 提取金额
        amount_pattern = r'(\d+(?:\.\d+)?)\s*(元|万|千|百)'
        amounts = re.findall(amount_pattern, message)
        entities["amount"] = [f"{a[0]}{a[1]}" for a in amounts]

        # 提取日期
        date_pattern = r'(\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{1,2}-\d{1,2})'
        dates = re.findall(date_pattern, message)
        entities["time"] = dates

        return entities

    def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """获取对话摘要"""
        session = self.get_session(session_id)
        if not session:
            return {}

        user_messages = [msg for msg in session.messages if msg.role == "user"]
        assistant_messages = [msg for msg in session.messages if msg.role == "assistant"]

        return {
            "session_id": session_id,
            "message_count": len(session.messages),
            "user_message_count": len(user_messages),
            "assistant_message_count": len(assistant_messages),
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "has_case_info": bool(session.case_info),
            "context_keys": list(session.context.keys())
        }

    def cleanup_old_sessions(self, days: int = 7) -> int:
        """清理旧会话"""
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(days=days)
        to_remove = []

        for session_id, session in self.sessions.items():
            if session.updated_at < cutoff:
                to_remove.append(session_id)

        for session_id in to_remove:
            del self.sessions[session_id]

        return len(to_remove)
