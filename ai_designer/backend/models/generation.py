"""
Generation Model
记录每次AI生成操作的详细信息
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Float, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from core.database import Base


class Generation(Base):
    """生成记录表"""
    __tablename__ = "generations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)

    # 生成类型
    type = Column(String, nullable=False)  # image, svg, code
    model = Column(String, nullable=False)  # 使用的模型名称

    # 请求参数
    prompt = Column(Text, nullable=False)
    parameters = Column(JSON)  # 生成参数

    # 结果
    status = Column(String, default="pending")  # pending, processing, completed, failed
    result_url = Column(String)  # 生成的资源URL
    result_content = Column(Text)  # 生成的文本内容（SVG代码等）
    generation_time = Column(Float)  # 生成时间（秒）
    tokens_used = Column(Integer, default=0)  # 使用的token数

    # 错误信息
    error_message = Column(Text)
    error_code = Column(String)

    # 元数据
    metadata = Column(JSON)  # 额外的元数据

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Indexes
    __table_args__ = (
        {'schema': None}
    )

    # Relationships
    user = relationship("User")
    project = relationship("Project")

    def __repr__(self):
        return f"<Generation {self.type} - {self.status}>"


class GenerationCache(Base):
    """生成结果缓存表"""
    __tablename__ = "generation_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cache_key = Column(String, unique=True, nullable=False, index=True)

    # 请求信息
    type = Column(String, nullable=False)
    prompt_hash = Column(String, nullable=False)  # prompt的hash
    parameters_hash = Column(String, nullable=False)  # 参数的hash

    # 缓存的结果
    result_url = Column(String)
    result_content = Column(Text)
    metadata = Column(JSON)

    # 统计
    hit_count = Column(Integer, default=0)  # 命中次数

    # 过期时间
    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<GenerationCache {self.cache_key}>"
