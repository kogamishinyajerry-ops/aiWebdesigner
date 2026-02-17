"""
AI 阅读助手 - 后端服务

FastAPI 后端，提供文本摘要、关键信息提取等功能
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re
from collections import Counter

app = FastAPI(title="AI 阅读助手 API", version="1.0.0")

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 数据模型
class SummaryRequest(BaseModel):
    text: str
    max_length: Optional[int] = 300
    language: Optional[str] = "zh"


class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]
    keywords: List[str]
    reading_time: int


class MindMapNode(BaseModel):
    id: str
    label: str
    children: Optional[List["MindMapNode"]] = None


class MindMapResponse(BaseModel):
    root: MindMapNode


# 模拟 AI 服务（实际项目中调用 OpenAI API）
class AIService:
    """AI 服务类"""

    @staticmethod
    def summarize_text(text: str, max_length: int = 300) -> str:
        """文本摘要"""
        # 这里是简化版本，实际应该调用 AI API
        sentences = re.split(r'[。！？!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # 取前几句话作为摘要
        summary_sentences = sentences[:3]
        summary = "。".join(summary_sentences) + "。"

        # 限制长度
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary

    @staticmethod
    def extract_key_points(text: str, count: int = 5) -> List[str]:
        """提取关键观点"""
        sentences = re.split(r'[。！？!?]', text)
        sentences = [s.strip() for s in sentences if len(s) > 20]

        # 按句子长度排序，取最长的几个
        sentences.sort(key=len, reverse=True)
        return sentences[:count]

    @staticmethod
    def extract_keywords(text: str, count: int = 10) -> List[str]:
        """提取关键词"""
        # 简单的词频统计（实际应该使用 NLP）
        words = re.findall(r'[\w\u4e00-\u9fa5]{2,}', text)
        word_freq = Counter(words)

        # 常用词过滤
        stop_words = {'的', '是', '在', '了', '和', '有', '我', '他', '她', '它',
                    '这', '那', '一个', '我们', '你们', '他们', '就是', '这个',
                    'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                    'could', 'should', 'may', 'might', 'must', 'shall', 'can'}

        for word in stop_words:
            if word in word_freq:
                del word_freq[word]

        return [word for word, _ in word_freq.most_common(count)]

    @staticmethod
    def generate_mind_map(text: str) -> dict:
        """生成思维导图"""
        # 简化版：根据段落生成树状结构
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        root = {
            "id": "root",
            "label": "文章主题",
            "children": []
        }

        for i, para in enumerate(paragraphs[:5]):
            # 提取段落主题
            sentences = re.split(r'[。！？!?]', para)
            title = sentences[0][:20] if sentences else f"段落 {i+1}"

            node = {
                "id": f"node_{i}",
                "label": title,
                "children": []
            }

            # 添加子节点
            for j, sentence in enumerate(sentences[1:4]):
                if sentence.strip():
                    node["children"].append({
                        "id": f"node_{i}_{j}",
                        "label": sentence[:30] + "..." if len(sentence) > 30 else sentence
                    })

            root["children"].append(node)

        return {"root": root}


# API 路由

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI 阅读助手 API",
        "version": "1.0.0",
        "endpoints": {
            "summary": "/api/v1/summary",
            "mindmap": "/api/v1/mindmap",
            "keywords": "/api/v1/keywords"
        }
    }


@app.post("/api/v1/summary", response_model=SummaryResponse)
async def summarize(request: SummaryRequest):
    """文本摘要 API"""
    try:
        ai_service = AIService()

        summary = ai_service.summarize_text(request.text, request.max_length)
        key_points = ai_service.extract_key_points(request.text)
        keywords = ai_service.extract_keywords(request.text)

        # 估算阅读时间（中文 400 字/分钟，英文 200 词/分钟）
        if request.language == "en":
            word_count = len(request.text.split())
            reading_time = max(1, word_count // 200)
        else:
            char_count = len(request.text)
            reading_time = max(1, char_count // 400)

        return SummaryResponse(
            summary=summary,
            key_points=key_points,
            keywords=keywords,
            reading_time=reading_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/mindmap", response_model=MindMapResponse)
async def mindmap(text: str):
    """生成思维导图 API"""
    try:
        ai_service = AIService()
        mind_map = ai_service.generate_mind_map(text)
        return mind_map

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/keywords")
async def extract_keywords(text: str, count: int = 10):
    """提取关键词 API"""
    try:
        ai_service = AIService()
        keywords = ai_service.extract_keywords(text, count)
        return {"keywords": keywords}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    print("🚀 AI 阅读助手后端启动中...")
    print("📖 访问 http://localhost:8000")
    print("📖 API 文档 http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
