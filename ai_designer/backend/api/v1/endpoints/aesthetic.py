"""
Aesthetic Engine Endpoints
美学引擎API - 风格识别、色彩推荐、审美评分
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from loguru import logger
from datetime import datetime

from services import aesthetic_engine

router = APIRouter()


class ColorRecommendationRequest(BaseModel):
    """色彩推荐请求"""
    description: Optional[str] = Field(None, description="设计描述")
    style: Optional[str] = Field(None, description="风格预设")
    mood: Optional[str] = Field(None, description="情绪/氛围")


class StyleAnalysisRequest(BaseModel):
    """风格分析请求"""
    description: str = Field(..., description="设计描述")


class AestheticScoreRequest(BaseModel):
    """美学评分请求"""
    description: str = Field(..., description="设计描述")
    style: Optional[str] = Field(None, description="设计风格")
    has_gradient: bool = Field(default=False, description="是否包含渐变")
    has_good_spacing: bool = Field(default=False, description="是否有良好间距")
    has_good_contrast: bool = Field(default=False, description="是否有良好对比度")


@router.post("/colors/recommend")
async def recommend_colors(request: ColorRecommendationRequest, http_request: Request):
    """
    推荐色彩方案
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")

        logger.info(f"[{request_id}] Recommending colors | Style: {request.style} | Mood: {request.mood}")

        result = aesthetic_engine.recommend_colors(
            description=request.description,
            style=request.style,
            mood=request.mood
        )

        logger.info(f"[{request_id}] Color palette recommended")

        return {
            "success": True,
            **result,
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Color recommendation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/style/analyze")
async def analyze_style(request: StyleAnalysisRequest, http_request: Request):
    """
    分析设计风格
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")

        logger.info(f"[{request_id}] Analyzing style: {request.description}")

        result = aesthetic_engine.analyze_style(request.description)

        logger.info(f"[{request_id}] Style analyzed: {result['primary_style']}")

        return {
            "success": True,
            **result,
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Style analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/score")
async def calculate_aesthetic_score(request: AestheticScoreRequest, http_request: Request):
    """
    计算美学评分
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")

        logger.info(f"[{request_id}] Calculating aesthetic score")

        result = aesthetic_engine.calculate_aesthetic_score(
            description=request.description,
            style=request.style,
            has_gradient=request.has_gradient,
            has_good_spacing=request.has_good_spacing,
            has_good_contrast=request.has_good_contrast
        )

        logger.info(f"[{request_id}] Aesthetic score: {result['total_score']:.2f} ({result['grade']})")

        return {
            "success": True,
            **result,
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Aesthetic score calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/palettes")
async def get_color_palettes():
    """
    获取所有可用色彩方案
    """
    return {
        "success": True,
        "palettes": aesthetic_engine.COLOR_PALETTES
    }


@router.get("/styles")
async def get_available_styles():
    """
    获取所有可用风格
    """
    styles = [
        {
            "id": style,
            "keywords": keywords
        }
        for style, keywords in aesthetic_engine.STYLE_KEYWORDS.items()
    ]

    return {
        "success": True,
        "styles": styles
    }


@router.get("/moods")
async def get_available_moods():
    """
    获取所有可用情绪预设
    """
    moods = [
        {"id": "calm", "name": "Calm", "description": "Peaceful and relaxing"},
        {"id": "energetic", "name": "Energetic", "description": "Dynamic and exciting"},
        {"id": "natural", "name": "Natural", "description": "Organic and fresh"},
        {"id": "luxury", "name": "Luxury", "description": "Premium and elegant"},
        {"id": "professional", "name": "Professional", "description": "Business-like and trustworthy"},
        {"id": "clean", "name": "Clean", "description": "Simple and uncluttered"}
    ]

    return {
        "success": True,
        "moods": moods
    }
