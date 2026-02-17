"""
AI Coding Monitoror - Main Application
监控AI coding过程，防止记忆丢失和功能破坏
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import asyncio
from datetime import datetime
import uuid

from loguru import logger

from .context_manager import ContextManager
from .code_detector import CodeChangeDetector
from .validation_engine import ValidationEngine
from .alert_system import AlertSystem
from .memory_store import MemoryStore

# Initialize FastAPI app
app = FastAPI(
    title="AI Coding Monitoror",
    description="Monitor AI coding sessions and prevent code regressions",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
sessions: Dict[str, Dict[str, Any]] = {}

# Initialize core components
context_manager = ContextManager()
code_detector = CodeChangeDetector()
validation_engine = ValidationEngine()
alert_system = AlertSystem()
memory_store = MemoryStore()


# ============== Data Models ==============

class SessionInit(BaseModel):
    """会话初始化请求"""
    project_path: str
    language: str = "python"
    session_id: Optional[str] = None


class CodeSnapshot(BaseModel):
    """代码快照"""
    file_path: str
    content: str
    timestamp: Optional[datetime] = None


class AIRequest(BaseModel):
    """AI请求记录"""
    request_id: str
    prompt: str
    context: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()


class AIResponse(BaseModel):
    """AI响应记录"""
    response_id: str
    request_id: str
    code_changes: List[Dict[str, str]]
    timestamp: datetime = datetime.utcnow()


class ValidationResult(BaseModel):
    """验证结果"""
    valid: bool
    issues: List[str] = []
    suggestions: List[str] = []
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL


class Alert(BaseModel):
    """告警信息"""
    alert_id: str
    type: str  # BREAKAGE, DRIFT, MEMORY_LOSS
    severity: str  # INFO, WARNING, ERROR, CRITICAL
    message: str
    timestamp: datetime = datetime.utcnow()
    suggestion: Optional[str] = None


# ============== API Endpoints ==============

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "AI Coding Monitoror",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "sessions": "/sessions",
            "analyze": "/analyze",
            "validate": "/validate",
            "context": "/context"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "context_manager": "ok",
            "code_detector": "ok",
            "validation_engine": "ok",
            "alert_system": "ok",
            "memory_store": "ok"
        }
    }


@app.post("/sessions/init")
async def init_session(session: SessionInit):
    """初始化监控会话"""
    try:
        session_id = session.session_id or str(uuid.uuid4())
        
        # Initialize session state
        sessions[session_id] = {
            "project_path": session.project_path,
            "language": session.language,
            "created_at": datetime.utcnow(),
            "snapshots": {},
            "ai_requests": [],
            "ai_responses": [],
            "context": {},
            "status": "active"
        }
        
        # Initialize memory for this session
        await memory_store.create_session(session_id, {
            "project_path": session.project_path,
            "language": session.language
        })
        
        logger.info(f"Session {session_id} initialized")
        
        return {
            "session_id": session_id,
            "status": "initialized",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error initializing session: {e}")
        raise


@app.post("/sessions/{session_id}/snapshot")
async def save_snapshot(session_id: str, snapshot: CodeSnapshot):
    """保存代码快照"""
    try:
        if session_id not in sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Save snapshot
        snapshot.timestamp = snapshot.timestamp or datetime.utcnow()
        sessions[session_id]["snapshots"][snapshot.file_path] = snapshot.dict()
        
        # Analyze changes
        changes = await code_detector.analyze_change(
            session_id,
            snapshot.file_path,
            snapshot.content
        )
        
        # Store in memory
        await memory_store.add_code_snapshot(
            session_id,
            snapshot.file_path,
            snapshot.content,
            snapshot.timestamp
        )
        
        logger.info(f"Snapshot saved for {snapshot.file_path}")
        
        return {
            "session_id": session_id,
            "snapshot_id": str(uuid.uuid4()),
            "changes_detected": len(changes),
            "changes": changes
        }
    except Exception as e:
        logger.error(f"Error saving snapshot: {e}")
        raise


@app.post("/analyze/ai-request")
async def analyze_ai_request(session_id: str, request: AIRequest):
    """分析AI请求"""
    try:
        if session_id not in sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Record request
        sessions[session_id]["ai_requests"].append(request.dict())
        
        # Capture context before AI makes changes
        context_snapshot = await context_manager.capture_context(
            session_id,
            request.request_id
        )
        
        # Store in memory
        await memory_store.add_ai_request(
            session_id,
            request.request_id,
            request.prompt,
            request.context
        )
        
        logger.info(f"AI request {request.request_id} recorded")
        
        return {
            "request_id": request.request_id,
            "context_snapshot": context_snapshot,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing AI request: {e}")
        raise


@app.post("/analyze/ai-response")
async def analyze_ai_response(session_id: str, response: AIResponse):
    """分析AI响应"""
    try:
        if session_id not in sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Record response
        sessions[session_id]["ai_responses"].append(response.dict())
        
        # Detect code changes
        detected_changes = []
        for change in response.code_changes:
            change_analysis = await code_detector.analyze_change(
                session_id,
                change["file_path"],
                change["content"]
            )
            detected_changes.extend(change_analysis)
        
        # Validate changes
        validation_result = await validation_engine.validate_changes(
            session_id,
            detected_changes
        )
        
        # Check for regressions
        regression_alerts = await alert_system.check_regressions(
            session_id,
            detected_changes
        )
        
        # Check for context drift
        drift_alerts = await alert_system.check_context_drift(
            session_id,
            response.response_id
        )
        
        # Store in memory
        await memory_store.add_ai_response(
            session_id,
            response.response_id,
            response.request_id,
            response.code_changes
        )
        
        logger.info(f"AI response {response.response_id} analyzed")
        
        return {
            "response_id": response.response_id,
            "validation": validation_result.dict(),
            "alerts": {
                "regressions": [a.dict() for a in regression_alerts],
                "drift": [a.dict() for a in drift_alerts]
            },
            "changes_detected": len(detected_changes),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing AI response: {e}")
        raise


@app.get("/sessions/{session_id}/context")
async def get_session_context(session_id: str, include_history: bool = True):
    """获取会话上下文"""
    try:
        if session_id not in sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Get current context
        current_context = await context_manager.get_context(session_id)
        
        # Get historical context if requested
        history = None
        if include_history:
            history = await memory_store.get_session_history(session_id)
        
        return {
            "session_id": session_id,
            "current_context": current_context,
            "history": history,
            "stats": {
                "snapshots_count": len(sessions[session_id]["snapshots"]),
                "ai_requests_count": len(sessions[session_id]["ai_requests"]),
                "ai_responses_count": len(sessions[session_id]["ai_responses"])
            }
        }
    except Exception as e:
        logger.error(f"Error getting session context: {e}")
        raise


@app.post("/sessions/{session_id}/reconstruct")
async def reconstruct_context(session_id: str, target_step: int):
    """重建上下文到指定步骤"""
    try:
        if session_id not in sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Reconstruct context from memory
        reconstructed = await context_manager.reconstruct_context(
            session_id,
            target_step
        )
        
        logger.info(f"Context reconstructed for session {session_id} to step {target_step}")
        
        return {
            "session_id": session_id,
            "target_step": target_step,
            "reconstructed_context": reconstructed,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error reconstructing context: {e}")
        raise


@app.post("/validate/code")
async def validate_code(
    session_id: str,
    file_path: str,
    content: str
):
    """验证代码"""
    try:
        if session_id not in sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Run validation
        result = await validation_engine.validate_code(
            session_id,
            file_path,
            content
        )
        
        return result.dict()
    except Exception as e:
        logger.error(f"Error validating code: {e}")
        raise


@app.get("/alerts/{session_id}")
async def get_alerts(session_id: str, limit: int = 50):
    """获取告警"""
    try:
        alerts = await alert_system.get_session_alerts(session_id, limit)
        
        return {
            "session_id": session_id,
            "alerts": [a.dict() for a in alerts],
            "count": len(alerts)
        }
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise


# ============== WebSocket Endpoint ==============

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket连接用于实时监控"""
    await websocket.accept()
    
    logger.info(f"WebSocket connection established for session {session_id}")
    
    try:
        if session_id not in sessions:
            await websocket.close(code=4000, reason="Session not found")
            return
        
        # Send initial state
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            message_type = data.get("type")
            
            if message_type == "heartbeat":
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            elif message_type == "snapshot":
                # Handle code snapshot
                snapshot_data = data.get("data")
                result = await save_snapshot(session_id, CodeSnapshot(**snapshot_data))
                await websocket.send_json({
                    "type": "snapshot_saved",
                    "data": result
                })
            
            elif message_type == "ai_request":
                # Handle AI request
                request_data = data.get("data")
                result = await analyze_ai_request(session_id, AIRequest(**request_data))
                await websocket.send_json({
                    "type": "request_analyzed",
                    "data": result
                })
            
            elif message_type == "ai_response":
                # Handle AI response
                response_data = data.get("data")
                result = await analyze_ai_response(session_id, AIResponse(**response_data))
                
                # Send alerts immediately if any
                if result["alerts"]["regressions"] or result["alerts"]["drift"]:
                    await websocket.send_json({
                        "type": "alert",
                        "data": result["alerts"]
                    })
                
                await websocket.send_json({
                    "type": "response_analyzed",
                    "data": result
                })
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=4001, reason=str(e))


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting AI Coding Monitoror...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
