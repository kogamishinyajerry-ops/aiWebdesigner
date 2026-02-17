"""
Asset Model
管理生成的图像、SVG等资源
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from core.database import Base


class Asset(Base):
    """资源表"""
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id"), nullable=True)

    # 资源信息
    type = Column(String, nullable=False)  # image, svg, code, other
    name = Column(String, nullable=False)
    file_path = Column(String)  # 本地文件路径
    url = Column(String)  # 公共访问URL

    # 图像相关
    width = Column(Integer)
    height = Column(Integer)
    format = Column(String)  # png, jpg, svg, etc.
    file_size = Column(Integer)  # 文件大小（字节）

    # 元数据
    description = Column(Text)
    tags = Column(String)  # 逗号分隔的标签
    metadata = Column(String)  # JSON字符串

    # 状态
    is_public = Column(Boolean, default=False)  # 是否公开
    is_deleted = Column(Boolean, default=False)  # 软删除标记

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User")
    project = relationship("Project")
    generation = relationship("Generation")

    def __repr__(self):
        return f"<Asset {self.name} ({self.type})>"
