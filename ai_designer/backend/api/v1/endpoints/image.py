"""
Image Generation Endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import Field
from typing import Optional
import uuid
import base64
from datetime import datetime
from loguru import logger

from services import image_service
from schemas.image import (
    ImageGenerationRequest,
    ImageGenerationResponse,
    ImagePresetsResponse
)
from core.config import settings

router = APIRouter()


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest, http_request: Request):
    """
    Generate an image using AI model
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        logger.info(f"[{request_id}] Generating image: {request.prompt}")

        # Generate image using service
        result = image_service.generate_hero_banner(
            prompt=request.prompt,
            style=request.style,
            size=request.size,
            negative_prompt=request.negative_prompt,
            guidance_scale=request.guidance_scale,
            num_inference_steps=request.num_steps,
            seed=request.seed
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        # Convert image to base64 for response
        image_base64 = base64.b64encode(result["image_data"]).decode("utf-8")

        logger.info(f"[{request_id}] Image generated successfully in {generation_time:.2f}s")

        return ImageGenerationResponse(
            success=True,
            image_url=f"data:image/png;base64,{image_base64}",
            generation_id=str(uuid.uuid4()),
            generation_time=generation_time,
            prompt=request.prompt,
            dimensions={"width": result["width"], "height": result["height"]},
            style=request.style,
            seed=request.seed,
            request_id=request_id
        )

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Image generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/icons")
async def generate_icons(
    concept: str = Field(..., description="Icon concept (e.g., navigation, social)"),
    style: str = Field(default="outline", description="Icon style"),
    count: int = Field(default=4, ge=1, le=10, description="Number of icons"),
    size: str = Field(default="icon", description="Icon size preset"),
    http_request: Request = None
):
    """
    Generate icon set
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        logger.info(f"[{request_id}] Generating {count} icons for: {concept}")

        # Generate icons
        icons = image_service.generate_icon(
            concept=concept,
            style=style,
            count=count,
            size=size
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        # Convert to base64
        icon_data = []
        for icon in icons:
            icon_base64 = base64.b64encode(icon["image_data"]).decode("utf-8")
            icon_data.append({
                "concept": icon["concept"],
                "style": icon["style"],
                "variant": icon["variant"],
                "data_url": f"data:image/png;base64,{icon_base64}",
                "width": icon["width"],
                "height": icon["height"]
            })

        logger.info(f"[{request_id}] Generated {len(icons)} icons in {generation_time:.2f}s")

        return {
            "success": True,
            "icons": icon_data,
            "generation_time": generation_time,
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Icon generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/background")
async def generate_background(
    style: str = Field(default="gradient", description="Background style"),
    colors: Optional[str] = Field(None, description="Comma-separated colors"),
    complexity: str = Field(default="medium", description="Complexity level"),
    size: str = Field(default="hero_medium", description="Size preset"),
    http_request: Request = None
):
    """
    Generate background texture
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        color_list = colors.split(",") if colors else None

        logger.info(f"[{request_id}] Generating {style} background")

        # Generate background
        result = image_service.generate_background(
            style=style,
            colors=color_list,
            complexity=complexity,
            size=size
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        # Convert to base64
        image_base64 = base64.b64encode(result["image_data"]).decode("utf-8")

        logger.info(f"[{request_id}] Background generated in {generation_time:.2f}s")

        return {
            "success": True,
            "image_url": f"data:image/png;base64,{image_base64}",
            "style": style,
            "complexity": complexity,
            "width": result["width"],
            "height": result["height"],
            "generation_time": generation_time,
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Background generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/styles", response_model=ImagePresetsResponse)
async def get_available_styles():
    """
    Get list of available image styles and presets
    """
    presets = [
        {
            "id": "modern",
            "name": "Modern",
            "description": "Clean design with flat colors and modern typography",
            "colors": ["#6366f1", "#8b5cf6", "#f59e0b"],
            "example": "clean design, flat colors, modern typography, sans-serif"
        },
        {
            "id": "minimal",
            "name": "Minimal",
            "description": "Minimalist with plenty of whitespace and simple geometry",
            "colors": ["#1f2937", "#4b5563", "#3b82f6"],
            "example": "minimalist, plenty of whitespace, simple geometry"
        },
        {
            "id": "glassmorphism",
            "name": "Glassmorphism",
            "description": "Glass effect with blur and translucent elements",
            "colors": ["rgba(255,255,255,0.1)", "rgba(255,255,255,0.2)"],
            "example": "glass effect, blur, translucent, gradient background"
        },
        {
            "id": "neumorphism",
            "name": "Neumorphism",
            "description": "Soft shadows with extruded shapes",
            "colors": ["#e0e5ec", "#ffffff", "#a3b1c6"],
            "example": "soft shadows, extruded shapes, monochromatic"
        },
        {
            "id": "brutalism",
            "name": "Brutalism",
            "description": "Bold colors with raw aesthetic and large typography",
            "colors": ["#ff6b6b", "#4ecdc4", "#ffe66d"],
            "example": "bold colors, raw aesthetic, large typography"
        }
    ]

    return ImagePresetsResponse(presets=presets)
