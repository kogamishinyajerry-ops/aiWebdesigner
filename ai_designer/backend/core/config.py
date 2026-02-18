"""
Configuration Management
使用Pydantic Settings管理配置
"""

from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "AI Designer"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # CORS
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ]

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://ai_designer:ai_designer@localhost:5432/ai_designer"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # AI Models
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    GEMINI_ENABLED: bool = True

    IMAGE_MODEL_ID: str = "stabilityai/stable-diffusion-xl-base-1.0"
    IMAGE_GENERATION_ENABLED: bool = True
    DEFAULT_IMAGE_SIZE: str = "hero_medium"
    DEFAULT_IMAGE_STYLE: str = "modern"

    CLIP_MODEL_ID: str = "ViT-B/32"
    CLIP_ENABLED: bool = True

    # Vector Database
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_ENABLED: bool = False

    # Storage
    STORAGE_PATH: str = "./data"
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_FORMATS: List[str] = ["png", "jpg", "jpeg", "webp"]

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None

    # API
    API_V1_PREFIX: str = "/api/v1"
    MAX_REQUEST_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Pagination
    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100


# 全局配置实例
settings = Settings()
