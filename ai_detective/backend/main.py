"""
AI 侦探 - FastAPI 主应用
AI Detective Main Application
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from .conversation import ConversationManager
from .reasoner import LegalReasoner
from .generator import DocumentGenerator
from .evidence import EvidenceAnalyzer, EvidenceType, Evidence, Validity


app = FastAPI(
    title="AI 侦探 API",
    description="基于法律推理的纠纷分析和报案材料生成系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心模块
conversation_manager = ConversationManager()
legal_reasoner = LegalReasoner()
document_generator = DocumentGenerator()
evidence_analyzer = EvidenceAnalyzer()


# ===== 数据模型 =====

class Message(BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class CreateSessionResponse(BaseModel):
    session_id: str
    created_at: str


class AnalyzeRequest(BaseModel):
    description: str
    context: Optional[Dict[str, Any]] = None


class UserInfo(BaseModel):
    name: str = ""
    phone: str = ""
    address: str = ""
    id_number: str = ""
    gender: str = ""
    ethnicity: str = ""
    birth_date: str = ""
    zip_code: str = ""


class GenerateDocumentsRequest(BaseModel):
    description: str
    user_info: UserInfo
    session_id: Optional[str] = None


class EvidenceRequest(BaseModel):
    evidences: List[Dict[str, Any]]
    case_type: str


# ===== API 端点 =====

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI 侦探 API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/session/create", response_model=CreateSessionResponse)
async def create_session():
    """创建新的对话会话"""
    session_id = conversation_manager.create_session()
    return CreateSessionResponse(
        session_id=session_id,
        created_at=datetime.now().isoformat()
    )


@app.post("/session/{session_id}/message")
async def add_message(session_id: str, message: Message):
    """添加消息到会话"""
    try:
        conversation_manager.add_message(
            session_id=session_id,
            role=message.role,
            content=message.content,
            metadata=message.metadata
        )
        return {"status": "success", "message": "消息已添加"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """获取会话信息"""
    session = conversation_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    return {
        "session_id": session.session_id,
        "created_at": session.created_at.isoformat(),
        "updated_at": session.updated_at.isoformat(),
        "message_count": len(session.messages),
        "context": session.context,
        "case_info": session.case_info
    }


@app.get("/session/{session_id}/messages")
async def get_messages(session_id: str, last_n: Optional[int] = None):
    """获取消息历史"""
    messages = conversation_manager.get_messages(session_id, last_n)
    return {
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata
            }
            for msg in messages
        ]
    }


@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_case(request: AnalyzeRequest):
    """分析案件"""
    try:
        # 执行法律推理
        analysis = legal_reasoner.analyze(
            description=request.description,
            context=request.context
        )

        # 转换为可序列化的格式
        return {
            "facts": [
                {
                    "id": fact.id,
                    "description": fact.description,
                    "category": fact.category,
                    "confidence": fact.confidence
                }
                for fact in analysis.facts
            ],
            "legal_relations": [
                {
                    "type": relation.type,
                    "parties": relation.parties,
                    "subject": relation.subject,
                    "content": relation.content
                }
                for relation in analysis.legal_relations
            ],
            "applicable_laws": analysis.applicable_laws,
            "liability": {
                "liable_party": analysis.liability.liable_party if analysis.liability else None,
                "liability_type": analysis.liability.liability_type if analysis.liability else None,
                "basis": analysis.liability.basis if analysis.liability else None,
                "severity": analysis.liability.severity if analysis.liability else None,
                "damages": analysis.liability.damages if analysis.liability else None
            } if analysis.liability else None,
            "risk_assessment": analysis.risk_assessment,
            "suggestions": analysis.suggestions,
            "confidence": analysis.confidence,
            "created_at": analysis.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/generate")
async def generate_documents(request: GenerateDocumentsRequest):
    """生成报案材料"""
    try:
        # 执行分析
        analysis = legal_reasoner.analyze(
            description=request.description,
            context={}
        )

        # 生成文档
        user_info_dict = request.user_info.dict()
        documents = document_generator.generate_report(analysis, user_info_dict)

        # 转换为可序列化的格式
        return {
            "documents": [
                {
                    "title": doc.title,
                    "content": doc.content,
                    "document_type": doc.document_type,
                    "created_at": doc.created_at
                }
                for doc in documents
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evidence/analyze")
async def analyze_evidence(request: EvidenceRequest):
    """分析证据"""
    try:
        # 转换证据
        evidences = []
        for i, ev_dict in enumerate(request.evidences):
            evidence_type = EvidenceType(ev_dict.get("type", "document"))
            validity = Validity(ev_dict.get("validity", "medium"))

            evidence = Evidence(
                id=f"ev_{i}",
                name=ev_dict.get("name", f"证据{i+1}"),
                evidence_type=evidence_type,
                description=ev_dict.get("description", ""),
                validity=validity,
                weight=ev_dict.get("weight", 1.0),
                source=ev_dict.get("source", ""),
                obtained_date=datetime.fromisoformat(ev_dict["obtained_date"]) if ev_dict.get("obtained_date") else None,
                metadata=ev_dict.get("metadata", {})
            )
            evidences.append(evidence)

        # 构建证据链
        evidence_chain = evidence_analyzer.build_evidence_chain(
            evidences=evidences,
            case_type=request.case_type
        )

        # 分析单个证据
        individual_analyses = [
            evidence_analyzer.analyze_evidence(ev)
            for ev in evidences
        ]

        return {
            "evidence_chain": {
                "completeness": evidence_chain.completeness,
                "consistency": evidence_chain.consistency,
                "strength": evidence_chain.strength,
                "gaps": evidence_chain.gaps,
                "suggestions": evidence_chain.suggestions
            },
            "individual_analyses": individual_analyses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/evidence/suggest/{case_type}")
async def suggest_evidence(case_type: str):
    """建议证据类型"""
    suggestions = evidence_analyzer.suggest_evidence(case_type, [])
    return {
        "case_type": case_type,
        "suggested_evidences": suggestions
    }


@app.get("/intent/detect")
async def detect_intent(message: str):
    """检测用户意图"""
    intent = conversation_manager.detect_intent(message)
    return intent


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "conversation_manager": "active",
            "legal_reasoner": "active",
            "document_generator": "active",
            "evidence_analyzer": "active"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
