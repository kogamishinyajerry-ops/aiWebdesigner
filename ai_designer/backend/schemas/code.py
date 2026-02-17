"""
Code generation schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum


class CodeFramework(str, Enum):
    """代码框架"""
    REACT = "react"
    VUE = "vue"
    HTML = "html"
    NEXTJS = "nextjs"
    MINIPROGRAM = "miniprogram"


class CodeLanguage(str, Enum):
    """代码语言"""
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    HTML = "html"
    CSS = "css"


class ComponentType(str, Enum):
    """组件类型"""
    BUTTON = "button"
    CARD = "card"
    FORM = "form"
    MODAL = "modal"
    NAVBAR = "navbar"
    SIDEBAR = "sidebar"
    HERO = "hero"
    FOOTER = "footer"


class CodeGenerationRequest(BaseModel):
    """代码生成请求"""

    description: str = Field(
        ...,
        description="组件/页面描述",
        min_length=1,
        max_length=1000
    )

    component_type: Optional[ComponentType] = Field(
        None,
        description="组件类型"
    )

    framework: Optional[CodeFramework] = Field(
        CodeFramework.REACT,
        description="目标框架"
    )

    language: Optional[CodeLanguage] = Field(
        CodeLanguage.TYPESCRIPT,
        description="代码语言"
    )

    use_tailwind: Optional[bool] = Field(
        True,
        description="是否使用Tailwind CSS"
    )

    responsive: Optional[bool] = Field(
        True,
        description="是否生成响应式代码"
    )

    include_tests: Optional[bool] = Field(
        False,
        description="是否包含测试代码"
    )

    include_styling: Optional[bool] = Field(
        True,
        description="是否包含样式"
    )

    design_preferences: Optional[Dict[str, Any]] = Field(
        None,
        description="设计偏好"
    )

    @validator('description')
    def validate_description(cls, v):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()

    @validator('design_preferences')
    def validate_design_preferences(cls, v):
        if v is None:
            return {}
        return v


class CodeFile(BaseModel):
    """代码文件"""

    filename: str = Field(..., description="文件名")
    language: str = Field(..., description="语言")
    content: str = Field(..., description="代码内容")


class CodeGenerationResponse(BaseModel):
    """代码生成响应"""

    success: bool = Field(..., description="是否成功")
    generation_id: str = Field(..., description="生成ID")
    generation_time: float = Field(..., description="生成时间(秒)")
    description: str = Field(..., description="使用的描述")
    framework: str = Field(..., description="目标框架")
    files: List[CodeFile] = Field(..., description="生成的代码文件")
    preview_url: Optional[str] = Field(None, description="预览URL")
    request_id: str = Field(..., description="请求ID")


class ComponentLibraryResponse(BaseModel):
    """组件库响应"""

    components: List[dict] = Field(..., description="可用组件列表")
