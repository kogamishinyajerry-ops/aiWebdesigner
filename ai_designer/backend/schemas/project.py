"""
Project schemas
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    """项目状态"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ProjectType(str, Enum):
    """项目类型"""
    IMAGE_GENERATION = "image_generation"
    SVG_GENERATION = "svg_generation"
    CODE_GENERATION = "code_generation"
    DESIGN_TO_CODE = "design_to_code"
    MIXED = "mixed"


class ProjectBase(BaseModel):
    """项目基础模型"""

    name: str = Field(..., description="项目名称", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="项目描述", max_length=1000)
    project_type: ProjectType = Field(..., description="项目类型")


class ProjectCreate(ProjectBase):
    """创建项目"""

    initial_prompt: Optional[str] = Field(None, description="初始提示词")


class ProjectUpdate(BaseModel):
    """更新项目"""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[ProjectStatus] = None


class ProjectResponse(BaseModel):
    """项目响应"""

    id: str = Field(..., description="项目ID")
    name: str = Field(..., description="项目名称")
    description: Optional[str] = Field(None, description="项目描述")
    project_type: ProjectType = Field(..., description="项目类型")
    status: ProjectStatus = Field(..., description="项目状态")
    user_id: str = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True
