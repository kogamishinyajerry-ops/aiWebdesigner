"""
SVG Generation Endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid
from loguru import logger

from services import svg_service

router = APIRouter()


class SVGGenerationRequest(BaseModel):
    """SVG generation request"""
    description: str = Field(..., description="Text description of the SVG to generate")
    style: str = Field(default="modern", description="Style preset")
    width: int = Field(default=512, ge=64, le=2048)
    height: int = Field(default=512, ge=64, le=2048)
    optimize: bool = Field(default=True, description="Optimize SVG code")


class SVGGenerationResponse(BaseModel):
    """SVG generation response"""
    success: bool
    svg_code: str
    width: int
    height: int
    style: str
    metadata: Optional[dict] = None
    request_id: Optional[str] = None


class IconSetRequest(BaseModel):
    """Icon set generation request"""
    concept: str = Field(..., description="Icon concept (navigation, social, e-commerce, etc.)")
    count: int = Field(default=10, ge=1, le=20, description="Number of icons to generate")
    style: str = Field(default="outline", description="Icon style")
    size: int = Field(default=512, ge=64, le=1024, description="Icon size")


@router.post("/generate", response_model=SVGGenerationResponse)
async def generate_svg(request: SVGGenerationRequest, http_request: Request):
    """
    Generate SVG from text description
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        logger.info(f"[{request_id}] Generating SVG: {request.description}")

        # Generate SVG
        result = await svg_service.text_to_svg(
            description=request.description,
            style=request.style,
            width=request.width,
            height=request.height,
            optimize=request.optimize
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        logger.info(f"[{request_id}] SVG generated in {generation_time:.2f}s")

        return SVGGenerationResponse(
            success=True,
            svg_code=result["svg_code"],
            width=result["width"],
            height=result["height"],
            style=result["style"],
            metadata=result["metadata"],
            request_id=request_id
        )

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] SVG generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/icon-set")
async def generate_icon_set(
    request: IconSetRequest,
    http_request: Request = None
):
    """
    Generate a set of icons
    """
    try:
        request_id = getattr(http_request.state, "request_id", "unknown")
        start_time = datetime.now()

        logger.info(f"[{request_id}] Generating {request.count} icons for: {request.concept}")

        # Generate icon set
        icons = await svg_service.generate_icon_set(
            concept=request.concept,
            count=request.count,
            style=request.style,
            size=request.size
        )

        generation_time = (datetime.now() - start_time).total_seconds()

        # Prepare response
        icon_list = []
        for icon in icons:
            icon_list.append({
                "name": icon["name"],
                "index": icon["index"],
                "svg_code": icon["svg_code"],
                "width": icon["width"],
                "height": icon["height"]
            })

        logger.info(f"[{request_id}] Generated {len(icons)} icons in {generation_time:.2f}s")

        return {
            "success": True,
            "concept": request.concept,
            "icons": icon_list,
            "generation_time": generation_time,
            "request_id": request_id
        }

    except Exception as e:
        request_id = getattr(http_request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Icon set generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/styles")
async def get_svg_styles():
    """
    Get available SVG styles
    """
    return {
        "styles": [
            {
                "id": "modern",
                "name": "Modern",
                "description": "Clean lines, modern aesthetic"
            },
            {
                "id": "outline",
                "name": "Outline",
                "description": "Outline style icons"
            },
            {
                "id": "filled",
                "name": "Filled",
                "description": "Filled style icons"
            },
            {
                "id": "minimal",
                "name": "Minimal",
                "description": "Minimalist design"
            },
            {
                "id": "glassmorphism",
                "name": "Glassmorphism",
                "description": "Glass effect with blur"
            }
        ]
    }
