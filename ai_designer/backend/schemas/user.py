"""
User schemas
"""

from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""

    email: EmailStr = Field(..., description="邮箱")
    username: str = Field(..., description="用户名", min_length=3, max_length=50)


class UserCreate(UserBase):
    """创建用户"""

    password: str = Field(..., description="密码", min_length=8, max_length=100)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """更新用户"""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    """用户响应"""

    id: str = Field(..., description="用户ID")
    email: str = Field(..., description="邮箱")
    username: str = Field(..., description="用户名")
    bio: Optional[str] = Field(None, description="个人简介")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True
