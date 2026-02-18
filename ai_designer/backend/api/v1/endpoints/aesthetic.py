"""
Aesthetic Design API Endpoints
美学设计API - 基于艺术巨匠风格的前端美学方案生成
"""

from fastapi import APIRouter, HTTPException, status
from loguru import logger
import time
import uuid

from schemas.aesthetic import (
    AestheticDesignRequest,
    AestheticDesignResponse,
    ArtStylePresetsResponse,
    ArtMasterStyle,
    UIComponent
)
from services.aesthetic_generation import aesthetic_service


router = APIRouter(prefix="", tags=["aesthetic"])


@router.post("/design", response_model=AestheticDesignResponse, status_code=status.HTTP_200_OK)
async def generate_aesthetic_design(request: AestheticDesignRequest):
    """
    生成完整的美学设计方案

    基于艺术巨匠的风格，为指定的页面和组件生成完整的美学方案，
    包括色彩方案、排版、组件样式、交互动效和视觉素材提示词。

    **输入:**
    - art_style: 参考的艺术风格 (如 van_gogh, picasso, dali等)
    - page_description: 页面描述（布局、功能、场景）
    - target_components: 需要设计的组件列表
    - color_preference: 可选，颜色偏好
    - mood: 可选，情感基调
    - complexity: 复杂度 (low, medium, high)
    - include_interactions: 是否包含交互设计
    - include_assets: 是否生成视觉素材提示词

    **输出:**
    - aesthetic_analysis: 艺术风格分析
    - global_color_palette: 全局色彩方案
    - global_typography: 全局排版方案
    - component_designs: 各组件的设计方案（含CSS和Tailwind类名）
    - interactions: 交互动效设计
    - visual_assets: 视觉素材AI生成提示词
    - design_summary: 完整设计摘要
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        logger.info(f"[{request_id}] Aesthetic design request | Style: {request.art_style} | Components: {len(request.target_components)}")

        # 调用服务生成设计
        result = aesthetic_service.generate_aesthetic_design(
            art_style=request.art_style.value,
            page_description=request.page_description,
            target_components=[comp.value for comp in request.target_components],
            color_preference=request.color_preference,
            mood=request.mood,
            complexity=request.complexity,
            include_interactions=request.include_interactions,
            include_assets=request.include_assets
        )

        generation_time = time.time() - start_time

        logger.info(f"[{request_id}] Aesthetic design generated in {generation_time:.2f}s")

        return AestheticDesignResponse(
            success=True,
            request_id=request_id,
            generation_time=generation_time,
            aesthetic_analysis=result["aesthetic_analysis"],
            global_color_palette=result["global_color_palette"],
            global_typography=result["global_typography"],
            component_designs=result["component_designs"],
            interactions=result["interactions"],
            visual_assets=result["visual_assets"],
            design_summary=result["design_summary"]
        )

    except Exception as e:
        logger.error(f"[{request_id}] Failed to generate aesthetic design: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate aesthetic design: {str(e)}"
        )


@router.get("/styles", response_model=ArtStylePresetsResponse)
async def get_art_style_presets():
    """
    获取可用的艺术风格列表

    返回所有可用的艺术巨匠风格及其描述，帮助用户选择合适的风格。
    """
    try:
        styles = []
        for style_key, style_info in aesthetic_service.ART_STYLES.items():
            styles.append({
                "value": style_key,
                "name": style_info["name"],
                "description": style_info["description"],
                "mood": style_info["mood"],
                "suitability": style_info["suitability"],
                "primary_colors": style_info["primary_colors"]
            })

        return ArtStylePresetsResponse(styles=styles)

    except Exception as e:
        logger.error(f"Failed to get art style presets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get art style presets: {str(e)}"
        )


@router.get("/components")
async def get_ui_components():
    """
    获取可用的UI组件列表

    返回所有支持设计的UI组件类型。
    """
    try:
        components = [
            {
                "value": comp.value,
                "name": comp.value.replace("_", " ").title(),
                "description": f"{comp.value.replace('_', ' ')} component design"
            }
            for comp in UIComponent
        ]

        return {"components": components}

    except Exception as e:
        logger.error(f"Failed to get UI components: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get UI components: {e}"
        )


@router.post("/analyze")
async def analyze_aesthetic_style(
    art_style: ArtMasterStyle,
    page_description: str
):
    """
    分析艺术风格适用性

    给定艺术风格和页面描述，分析该风格的适用性和建议。
    """
    try:
        style_info = aesthetic_service.ART_STYLES.get(art_style.value)

        if not style_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Art style {art_style.value} not found"
            )

        # 简单的适用性分析
        analysis = {
            "style": style_info["name"],
            "suitability_score": 0.85,  # 示例分数
            "recommendations": [
                f"Use {style_info['primary_colors'][0]} as primary color",
                f"Incorporate {style_info['key_characteristics'][0]}",
                f"Apply {style_info['interaction']} for interactions"
            ],
            "potential_challenges": [
                "May require careful color balancing",
                "Typography should complement the art style"
            ],
            "best_use_cases": style_info["suitability"]
        }

        return {"analysis": analysis}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to analyze aesthetic style: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze aesthetic style: {str(e)}"
        )
