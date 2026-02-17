"""
Image Generation Endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import Field
from typing import Optional
import uuid
from datetime import datetime
from loguru import logger

from services.image_generator import ImageGenerator
from schemas.image import (
    ImageGenerationRequest,
    ImageGenerationResponse,
    ImagePresetsResponse
)
from core.config import settings

router = APIRouter()

# Initialize image generator
image_generator = ImageGenerator()


class HeroBannerRequest:
    """Hero banner generation request"""
    title: str = Field(..., description="Title text for banner")
    subtitle: Optional[str] = Field(None, description="Subtitle text")
    style: str = Field(default="modern", description="Style preset")
    dimensions: str = Field(default="1920x1080", description="Dimensions (WxH)")


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest, http_request: Request):
    """
    Generate an image using FLUX model
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        logger.info(f"[{request_id}] Generating image: {request.prompt}")

        # Generate image
        images = await image_generator.generate(
            prompt=request.prompt,
            style=request.style,
            width=request.width,
            height=request.height,
            num_images=1,
            seed=request.seed
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        # Save image and get URL
        image_url = None
        if images:
            image_id = str(uuid.uuid4())
            image_url = await image_generator.save_image(images[0], image_id)

        logger.info(f"[{request_id}] Image generated successfully")

        return ImageGenerationResponse(
            success=bool(images),
            image_url=image_url,
            generation_id=str(uuid.uuid4()),
            generation_time=generation_time,
            prompt=request.prompt,
            dimensions={"width": request.width, "height": request.height},
            style=request.style,
            seed=request.seed,
            request_id=request_id
        )

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Image generation failed: {str(e)}")
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
