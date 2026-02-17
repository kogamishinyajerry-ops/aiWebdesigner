"""
SVG generation schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from enum import Enum


class SVGStyle(str, Enum):
    """SVG风格"""
    MINIMALIST = "minimalist"
    OUTLINE = "outline"
    FILLED = "filled"
    GRADIENT = "gradient"
    FLAT = "flat"
    ISOMETRIC = "isometric"
    HAND_DRAWN = "hand_drawn"


class SVGElement(str, Enum):
    """SVG元素类型"""
    ICON = "icon"
    ILLUSTRATION = "illustration"
    PATTERN = "pattern"
    LOGO = "logo"
    DIAGRAM = "diagram"


class SVGGenerationRequest(BaseModel):
    """SVG生成请求"""

    prompt: str = Field(
        ...,
        description="SVG描述提示词",
        min_length=1,
        max_length=500
    )

    element_type: Optional[SVGElement] = Field(
        SVGElement.ICON,
        description="SVG元素类型"
    )

    style: Optional[SVGStyle] = Field(
        SVGStyle.MINIMALIST,
        description="SVG风格"
    )

    width: Optional[int] = Field(
        512,
        description="宽度",
        ge=64,
        le=1024
    )

    height: Optional[int] = Field(
        512,
        description="高度",
        ge=64,
        le=1024
    )

    stroke_width: Optional[int] = Field(
        2,
        description="描边宽度",
        ge=1,
        le=10
    )

    primary_color: Optional[str] = Field(
        None,
        description="主色 (hex格式)",
        regex=r'^#[0-9A-Fa-f]{6}$'
    )

    secondary_color: Optional[str] = Field(
        None,
        description="副色 (hex格式)",
        regex=r'^#[0-9A-Fa-f]{6}$'
    )

    background_color: Optional[str] = Field(
        None,
        description="背景色 (hex格式)",
        regex=r'^#[0-9A-Fa-f]{6}$'
    )

    animate: Optional[bool] = Field(
        False,
        description="是否添加动画"
    )

    @validator('primary_color', 'secondary_color', 'background_color')
    def validate_color(cls, v, values):
        if v and not v.startswith('#'):
            raise ValueError('Color must start with #')
        return v

    @validator('width', 'height')
    def validate_dimensions(cls, v):
        if v < 64 or v > 1024:
            raise ValueError('Dimensions must be between 64 and 1024')
        return v


class SVGGenerationResponse(BaseModel):
    """SVG生成响应"""

    success: bool = Field(..., description="是否成功")
    svg_code: Optional[str] = Field(None, description="SVG代码")
    svg_url: Optional[str] = Field(None, description="SVG URL")
    generation_id: str = Field(..., description="生成ID")
    generation_time: float = Field(..., description="生成时间(秒)")
    prompt: str = Field(..., description="使用的提示词")
    element_type: str = Field(..., description="元素类型")
    style: str = Field(..., description="使用的风格")
    dimensions: dict = Field(..., description="尺寸")
    request_id: str = Field(..., description="请求ID")


class SVGTemplateResponse(BaseModel):
    """SVG模板响应"""

    templates: List[dict] = Field(..., description="模板列表")
