"""
Image Generation Endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List
import io
import uuid
from datetime import datetime

from services.image_generator import ImageGenerator
from core.config import settings

router = APIRouter()

# Initialize image generator
image_generator = ImageGenerator()


class ImageGenerationRequest(BaseModel):
    """Image generation request"""
    prompt: str = Field(..., description="Description of the image to generate")
    style: str = Field(default="modern", description="Style preset (modern, minimal, glassmorphism, etc.)")
    width: int = Field(default=settings.DEFAULT_IMAGE_WIDTH, ge=64, le=settings.MAX_IMAGE_WIDTH)
    height: int = Field(default=settings.DEFAULT_IMAGE_HEIGHT, ge=64, le=settings.MAX_IMAGE_HEIGHT)
    num_images: int = Field(default=1, ge=1, le=4)
    seed: Optional[int] = None


class HeroBannerRequest(BaseModel):
    """Hero banner generation request"""
    title: str = Field(..., description="Title text for the banner")
    subtitle: Optional[str] = Field(None, description="Subtitle text")
    style: str = Field(default="modern", description="Style preset")
    dimensions: str = Field(default="1920x1080", description="Dimensions (WxH)")


class ImageGenerationResponse(BaseModel):
    """Image generation response"""
    id: str
    prompt: str
    style: str
    image_urls: List[str]
    generation_time: float
    created_at: datetime


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """
    Generate an image using FLUX model
    """
    try:
        start_time = datetime.now()
        
        # Generate image
        images = await image_generator.generate(
            prompt=request.prompt,
            style=request.style,
            width=request.width,
            height=request.height,
            num_images=request.num_images,
            seed=request.seed
        )
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        # Save images and get URLs
        image_urls = []
        for image in images:
            image_id = str(uuid.uuid4())
            url = await image_generator.save_image(image, image_id)
            image_urls.append(url)
        
        return ImageGenerationResponse(
            id=str(uuid.uuid4()),
            prompt=request.prompt,
            style=request.style,
            image_urls=image_urls,
            generation_time=generation_time,
            created_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hero-banner", response_model=ImageGenerationResponse)
async def generate_hero_banner(request: HeroBannerRequest):
    """
    Generate a hero banner specifically designed for web pages
    """
    try:
        # Parse dimensions
        width, height = map(int, request.dimensions.split('x'))
        
        # Build prompt for hero banner
        prompt = f"hero banner for website, {request.title}"
        if request.subtitle:
            prompt += f", {request.subtitle}"
        
        # Generate banner
        images = await image_generator.generate_hero_banner(
            prompt=prompt,
            style=request.style,
            width=width,
            height=height,
            title=request.title
        )
        
        # Save and return
        image_urls = []
        for image in images:
            image_id = str(uuid.uuid4())
            url = await image_generator.save_image(image, image_id)
            image_urls.append(url)
        
        return ImageGenerationResponse(
            id=str(uuid.uuid4()),
            prompt=prompt,
            style=request.style,
            image_urls=image_urls,
            generation_time=0,
            created_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/styles")
async def get_available_styles():
    """
    Get list of available image styles
    """
    styles = {
        "modern": {
            "name": "Modern",
            "description": "Clean design with flat colors and modern typography",
            "colors": ["#6366f1", "#8b5cf6", "#f59e0b"],
            "example": "clean design, flat colors, modern typography, sans-serif"
        },
        "minimal": {
            "name": "Minimal",
            "description": "Minimalist with plenty of whitespace and simple geometry",
            "colors": ["#1f2937", "#4b5563", "#3b82f6"],
            "example": "minimalist, plenty of whitespace, simple geometry"
        },
        "glassmorphism": {
            "name": "Glassmorphism",
            "description": "Glass effect with blur and translucent elements",
            "colors": ["rgba(255,255,255,0.1)", "rgba(255,255,255,0.2)"],
            "example": "glass effect, blur, translucent, gradient background"
        },
        "neumorphism": {
            "name": "Neumorphism",
            "description": "Soft shadows with extruded shapes",
            "colors": ["#e0e5ec", "#ffffff", "#a3b1c6"],
            "example": "soft shadows, extruded shapes, monochromatic"
        },
        "brutalism": {
            "name": "Brutalism",
            "description": "Bold colors with raw aesthetic and large typography",
            "colors": ["#ff6b6b", "#4ecdc4", "#ffe66d"],
            "example": "bold colors, raw aesthetic, large typography"
        }
    }
    
    return styles
