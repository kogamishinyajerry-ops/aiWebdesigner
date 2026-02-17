"""
Image generation schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


class ImagePreset(str, Enum):
    """图像生成预设"""
    HERO_BANNER = "hero_banner"
    PRODUCT_SHOWCASE = "product_showcase"
    LOGIN_PAGE = "login_page"
    DATA_VISUALIZATION = "data_visualization"
    BACKGROUND = "background"
    ILLUSTRATION = "illustration"


class ImageSize(str, Enum):
    """图像尺寸"""
    HD = "1920x1080"  # 16:9
    FHD = "1280x720"   # 16:9
    SQUARE = "1080x1080"  # 1:1
    SD = "800x600"      # 4:3
    MOBILE = "375x812"   # 移动端


class ImageStyle(str, Enum):
    """图像风格"""
    MODERN_MINIMAL = "modern_minimal"
    TECH_CYBER = "tech_cyber"
    ELEGANT_FANCY = "elegant_fancy"
    PLAYFUL_VIBRANT = "playful_vibrant"
    NATURE_ORGANIC = "nature_organic"
    RETRO_VINTAGE = "retro_vintage"


class ImageGenerationRequest(BaseModel):
    """图像生成请求"""

    prompt: str = Field(
        ...,
        description="图像描述提示词",
        min_length=1,
        max_length=1000
    )

    width: Optional[int] = Field(
        1920,
        description="图像宽度",
        ge=256,
        le=2048
    )

    height: Optional[int] = Field(
        1080,
        description="图像高度",
        ge=256,
        le=2048
    )

    style: Optional[ImageStyle] = Field(
        ImageStyle.MODERN_MINIMAL,
        description="图像风格"
    )

    preset: Optional[ImagePreset] = Field(
        None,
        description="使用预设"
    )

    negative_prompt: Optional[str] = Field(
        None,
        description="负面提示词",
        max_length=500
    )

    num_inference_steps: Optional[int] = Field(
        30,
        description="推理步数",
        ge=10,
        le=100
    )

    guidance_scale: Optional[float] = Field(
        7.5,
        description="引导系数",
        ge=1.0,
        le=20.0
    )

    seed: Optional[int] = Field(
        None,
        description="随机种子",
        ge=-1,
        le=2147483647
    )

    @validator('width', 'height')
    def validate_dimensions(cls, v):
        if v % 64 != 0:
            raise ValueError('Dimensions must be multiples of 64')
        return v

    @validator('prompt')
    def validate_prompt(cls, v):
        if not v or not v.strip():
            raise ValueError('Prompt cannot be empty')
        return v.strip()


class ImageGenerationResponse(BaseModel):
    """图像生成响应"""

    success: bool = Field(..., description="是否成功")
    image_url: Optional[str] = Field(None, description="生成的图像URL")
    image_base64: Optional[str] = Field(None, description="Base64编码的图像")
    generation_id: str = Field(..., description="生成ID")
    generation_time: float = Field(..., description="生成时间(秒)")
    prompt: str = Field(..., description="使用的提示词")
    dimensions: dict = Field(..., description="图像尺寸")
    style: str = Field(..., description="使用的风格")
    seed: Optional[int] = Field(None, description="使用的种子")
    request_id: str = Field(..., description="请求ID")


class ImagePresetsResponse(BaseModel):
    """预设列表响应"""

    presets: List[dict] = Field(..., description="预设列表")
