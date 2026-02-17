"""
Alert System - Monitor for issues and send alerts
监控系统并发送告警
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid

from loguru import logger

from .memory_store import MemoryStore


class Alert:
    """告警数据结构"""
    
    def __init__(
        self,
        alert_type: str,
        severity: str,
        message: str,
        suggestion: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.alert_id = str(uuid.uuid4())
        self.type = alert_type
        self.severity = severity
        self.message = message
        self.suggestion = suggestion
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()
        self.resolved = False
    
    def dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "alert_id": self.alert_id,
            "type": self.type,
            "severity": self.severity,
            "message": self.message,
            "suggestion": self.suggestion,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved
        }


class AlertSystem:
    """告警系统"""
    
    def __init__(self):
        self.memory_store = MemoryStore()
        self.active_alerts: Dict[str, Dict[str, List[Alert]]] = {}
    
    async def check_regressions(
        self,
        session_id: str,
        changes: List[Dict[str, Any]]
    ) -> List[Alert]:
        """
        检查代码回归
        
        Args:
            session_id: 会话ID
            changes: 变更列表
            
        Returns:
            告警列表
        """
        alerts = []
        
        for change in changes:
            impact = change.get("impact", {})
            file_path = change.get("file_path")
            
            # Check for removed functions
            for func in impact.get("removed_functions", []):
                alert = Alert(
                    alert_type="REGRESSION",
                    severity="CRITICAL",
                    message=f"Function '{func['name']}' was removed",
                    suggestion=f"Restore function '{func['name']}' or update all references",
                    metadata={
                        "file_path": file_path,
                        "function_name": func["name"]
                    }
                )
                alerts.append(alert)
            
            # Check for removed classes
            for cls in impact.get("removed_classes", []):
                alert = Alert(
                    alert_type="REGRESSION",
                    severity="CRITICAL",
                    message=f"Class '{cls['name']}' was removed",
                    suggestion=f"Restore class '{cls['name']}' or update all references",
                    metadata={
                        "file_path": file_path,
                        "class_name": cls["name"]
                    }
                )
                alerts.append(alert)
            
            # Check for critical changes
            if impact.get("critical_changes"):
                alert = Alert(
                    alert_type="REGRESSION",
                    severity="HIGH",
                    message="Critical code structure changed",
                    suggestion="Review changes carefully and run comprehensive tests",
                    metadata={
                        "file_path": file_path,
                        "impact": impact
                    }
                )
                alerts.append(alert)
        
        # Store alerts
        if alerts:
            await self._store_alerts(session_id, alerts)
            logger.warning(f"{len(alerts)} regression alerts for session {session_id}")
        
        return alerts
    
    async def check_context_drift(
        self,
        session_id: str,
        response_id: str
    ) -> List[Alert]:
        """
        检查上下文漂移
        
        Args:
            session_id: 会话ID
            response_id: 响应ID
            
        Returns:
            告警列表
        """
        alerts = []
        
        try:
            # Get original intent
            original_intent = await self.memory_store.get_original_intent(session_id)
            
            if not original_intent:
                return alerts
            
            # Get current context
            current_context = await self.memory_store.get_current_context(session_id)
            
            # Calculate drift (simplified version)
            # In production, this would use embeddings and semantic similarity
            drift_score = self._calculate_drift_score(original_intent, current_context)
            
            if drift_score > 0.7:  # High drift
                alert = Alert(
                    alert_type="CONTEXT_DRIFT",
                    severity="WARNING",
                    message=f"Context drift detected: {drift_score*100:.1f}%",
                    suggestion=f"Review current work against original intent: '{original_intent}'",
                    metadata={
                        "drift_score": drift_score,
                        "original_intent": original_intent
                    }
                )
                alerts.append(alert)
            
            elif drift_score > 0.5:  # Medium drift
                alert = Alert(
                    alert_type="CONTEXT_DRIFT",
                    severity="INFO",
                    message=f"Potential context drift: {drift_score*100:.1f}%",
                    suggestion="Ensure current work aligns with original goals",
                    metadata={
                        "drift_score": drift_score,
                        "original_intent": original_intent
                    }
                )
                alerts.append(alert)
            
            # Store alerts
            if alerts:
                await self._store_alerts(session_id, alerts)
                logger.info(f"{len(alerts)} drift alerts for session {session_id}")
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking context drift: {e}")
            return []
    
    async def check_memory_loss(
        self,
        session_id: str
    ) -> List[Alert]:
        """
        检查记忆丢失
        
        Args:
            session_id: 会话ID
            
        Returns:
            告警列表
        """
        alerts = []
        
        try:
            # Check if important context has been lost
            session_history = await self.memory_store.get_session_history(session_id)
            
            if not session_history or len(session_history) < 3:
                # Not enough history to determine
                return alerts
            
            # Check if recent AI responses are inconsistent with earlier ones
            # This is a simplified check
            recent_responses = session_history[-3:]
            early_responses = session_history[:3]
            
            # Look for repetitive or contradictory patterns
            contradictions = self._detect_contradictions(early_responses, recent_responses)
            
            for contradiction in contradictions:
                alert = Alert(
                    alert_type="MEMORY_LOSS",
                    severity="WARNING",
                    message="Potential memory loss detected",
                    suggestion=contradiction["suggestion"],
                    metadata={
                        "contradiction": contradiction
                    }
                )
                alerts.append(alert)
            
            # Store alerts
            if alerts:
                await self._store_alerts(session_id, alerts)
                logger.warning(f"{len(alerts)} memory loss alerts for session {session_id}")
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking memory loss: {e}")
            return []
    
    async def check_test_failures(
        self,
        session_id: str,
        test_results: Dict[str, Any]
    ) -> List[Alert]:
        """
        检查测试失败
        
        Args:
            session_id: 会话ID
            test_results: 测试结果
            
        Returns:
            告警列表
        """
        alerts = []
        
        if not test_results.get("success"):
            alert = Alert(
                alert_type="TEST_FAILURE",
                severity="ERROR",
                message="Tests failed",
                suggestion="Review test output and fix failing tests before proceeding",
                metadata={
                    "exit_code": test_results.get("exit_code"),
                    "stderr": test_results.get("stderr", "")[:500]  # Limit length
                }
            )
            alerts.append(alert)
        
        # Store alerts
        if alerts:
            await self._store_alerts(session_id, alerts)
            logger.error(f"{len(alerts)} test failure alerts for session {session_id}")
        
        return alerts
    
    async def get_session_alerts(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Alert]:
        """
        获取会话告警
        
        Args:
            session_id: 会话ID
            limit: 返回数量限制
            
        Returns:
            告警列表
        """
        try:
            # Get from memory store
            stored_alerts = await self.memory_store.get_alerts(session_id, limit)
            
            # Convert to Alert objects
            alerts = []
            for alert_data in stored_alerts:
                alert = Alert(
                    alert_type=alert_data["type"],
                    severity=alert_data["severity"],
                    message=alert_data["message"],
                    suggestion=alert_data.get("suggestion"),
                    metadata=alert_data.get("metadata")
                )
                alert.alert_id = alert_data["alert_id"]
                alert.timestamp = datetime.fromisoformat(alert_data["timestamp"])
                alert.resolved = alert_data.get("resolved", False)
                alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting session alerts: {e}")
            return []
    
    async def resolve_alert(
        self,
        session_id: str,
        alert_id: str
    ) -> bool:
        """
        解决告警
        
        Args:
            session_id: 会话ID
            alert_id: 告警ID
            
        Returns:
            是否成功
        """
        try:
            await self.memory_store.resolve_alert(session_id, alert_id)
            logger.info(f"Alert {alert_id} resolved")
            return True
        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
            return False
    
    async def _store_alerts(
        self,
        session_id: str,
        alerts: List[Alert]
    ):
        """存储告警"""
        try:
            # Store in memory
            if session_id not in self.active_alerts:
                self.active_alerts[session_id] = {"all": [], "unresolved": []}
            
            for alert in alerts:
                self.active_alerts[session_id]["all"].append(alert)
                self.active_alerts[session_id]["unresolved"].append(alert)
            
            # Store in persistent storage
            await self.memory_store.add_alerts(session_id, alerts)
            
        except Exception as e:
            logger.error(f"Error storing alerts: {e}")
    
    def _calculate_drift_score(
        self,
        original_intent: str,
        current_context: Dict[str, Any]
    ) -> float:
        """
        计算漂移分数
        
        Args:
            original_intent: 原始意图
            current_context: 当前上下文
            
        Returns:
            漂移分数 (0-1)
        """
        # Simplified implementation
        # In production, this would use embeddings and semantic similarity
        
        # Check if key terms from original intent are present
        key_terms = self._extract_key_terms(original_intent)
        context_str = str(current_context)
        
        matches = sum(1 for term in key_terms if term.lower() in context_str.lower())
        
        # Calculate drift as inverse of match ratio
        if len(key_terms) == 0:
            return 0.0
        
        match_ratio = matches / len(key_terms)
        drift = 1.0 - match_ratio
        
        return min(max(drift, 0.0), 1.0)
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """提取关键术语"""
        # Simple extraction: words that are not common stopwords
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'should', 'could', 'may', 'might', 'must', 'can', 'to', 'from',
                     'in', 'on', 'at', 'by', 'for', 'with', 'about', 'of', 'and',
                     'or', 'but', 'if', 'then', 'else', 'when', 'while', 'because'}
        
        words = text.lower().split()
        key_terms = [word.strip('.,!?;:()[]{}"\'') for word in words 
                     if len(word) > 3 and word.strip('.,!?;:()[]{}"\'') not in stopwords]
        
        return key_terms[:10]  # Return top 10 terms
    
    def _detect_contradictions(
        self,
        early_responses: List[Dict[str, Any]],
        recent_responses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        检测矛盾
        
        Args:
            early_responses: 早期响应
            recent_responses: 最近响应
            
        Returns:
            矛盾列表
        """
        contradictions = []
        
        # Look for contradictory patterns
        # This is a simplified implementation
        early_code = [r.get("code", "") for r in early_responses]
        recent_code = [r.get("code", "") for r in recent_responses]
        
        # Check if code is being reverted
        for early in early_code:
            for recent in recent_code:
                if recent in early and len(recent) < len(early):
                    contradictions.append({
                        "type": "code_reversion",
                        "message": "Recent code appears to be reverting earlier changes",
                        "suggestion": "Review whether the reversion is intentional"
                    })
                    break
        
        return contradictions
