"""
Tag Model
标签系统，用于组织和搜索资源
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from core.database import Base


class Tag(Base):
    """标签表"""
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # 标签信息
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    color = Column(String)  # 标签颜色（hex）
    description = Column(String)

    # 统计
    usage_count = Column(Integer, default=0)  # 使用次数

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<Tag {self.name}>"


class AssetTag(Base):
    """资源标签关联表（多对多）"""
    __tablename__ = "asset_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    asset = relationship("Asset")
    tag = relationship("Tag")

    def __repr__(self):
        return f"<AssetTag {self.asset_id} - {self.tag_id}>"
