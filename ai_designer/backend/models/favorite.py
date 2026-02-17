"""
Favorite Model
用户收藏系统
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
import uuid

from core.database import Base


class Favorite(Base):
    """收藏表"""
    __tablename__ = "favorites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)

    # 收藏分类/文件夹
    folder = Column(String)  # 收藏夹名称

    # 备注
    notes = Column(String)

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'asset_id', name='unique_user_asset_favorite'),
    )

    # Relationships
    user = relationship("User")
    asset = relationship("Asset")

    def __repr__(self):
        return f"<Favorite {self.user_id} - {self.asset_id}>"
