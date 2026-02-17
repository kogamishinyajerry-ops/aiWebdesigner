"""
Template Model
模板系统，预设的设计模板
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from core.database import Base


class Template(Base):
    """模板表"""
    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # None表示系统模板

    # 模板信息
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    type = Column(String, nullable=False)  # image, svg, code
    category = Column(String)  # 分类

    # 描述和预览
    description = Column(Text)
    preview_url = Column(String)  # 预览图URL
    thumbnail_url = Column(String)  # 缩略图URL

    # 模板内容
    prompt_template = Column(Text)  # 提示词模板（支持变量）
    parameters = Column(String)  # JSON字符串，默认参数
    code_snippet = Column(Text)  # 代码片段（如果是代码模板）

    # 使用统计
    usage_count = Column(Integer, default=0)  # 使用次数
    rating = Column(Integer, default=0)  # 评分

    # 状态
    is_public = Column(Boolean, default=False)  # 是否公开
    is_official = Column(Boolean, default=False)  # 是否官方模板

    # 排序
    order = Column(Integer, default=0)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<Template {self.name} ({self.type})>"
