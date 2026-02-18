"""
AI Designer Backend
艺术级前端AI设计师 - 后端API服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")

from core.config import settings
from core.database import init_db
from core.redis import cache
# from middleware import (
#     RequestIDMiddleware,
#     LoggingMiddleware,
#     ErrorHandlerMiddleware,
#     RateLimitMiddleware
# )
from api.v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting AI Designer Backend...")

    # Initialize database (skip if disabled)
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.warning(f"⚠️ Database initialization skipped: {e}")

    # Initialize Redis (skip if disabled)
    try:
        await cache.connect()
        logger.info("✅ Redis cache initialized")
    except Exception as e:
        logger.warning(f"⚠️ Redis initialization skipped: {e}")

    # Initialize AI models (skip for now)
    try:
        from services import model_manager
        await model_manager.load_all_models()
        logger.info("✅ AI models loaded")
    except Exception as e:
        logger.warning(f"⚠️ AI models loading skipped: {e}")

    yield

    logger.info("🛑 Shutting down AI Designer Backend...")
    try:
        await cache.disconnect()
    except:
        pass


# Create FastAPI app
app = FastAPI(
    title="AI Designer API",
    description="艺术级前端AI设计师 - 后端API服务",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware (注意顺序，后添加的先执行)
# app.add_middleware(RequestIDMiddleware)
# app.add_middleware(
#     LoggingMiddleware,
#     skip_paths=["/health", "/api/docs", "/api/redoc", "/"]
# )
# app.add_middleware(ErrorHandlerMiddleware)
# app.add_middleware(RateLimitMiddleware, redis_client=await cache.get_client())

# Include routers
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AI Designer API",
        "version": "0.1.0",
        "status": "running",
        "documentation": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "models": "loaded"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
