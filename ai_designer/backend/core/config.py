"""
Configuration settings for AI Designer Backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Designer"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_designer"
    )
    
    # Redis
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )
    
    # AI Models
    FLUX_MODEL_PATH: str = "black-forest-labs/FLUX.1-schnell"
    FLUX_DEVICE: str = "cuda"
    FLUX_DTYPE: str = "float16"
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    
    # OpenAI (GPT-4o for code generation)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o"
    
    # Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    STORAGE_TYPE: str = "local"  # local, s3
    
    # AWS S3 (if using S3 storage)
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_BUCKET: str = os.getenv("AWS_BUCKET", "")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    # Caching
    CACHE_TTL: int = 3600  # 1 hour
    CACHE_ENABLED: bool = True
    
    # Image Generation
    DEFAULT_IMAGE_WIDTH: int = 1920
    DEFAULT_IMAGE_HEIGHT: int = 1080
    MAX_IMAGE_WIDTH: int = 4096
    MAX_IMAGE_HEIGHT: int = 4096
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings()


settings = get_settings()
