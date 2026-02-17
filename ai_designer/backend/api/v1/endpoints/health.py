"""
Health Check Endpoints
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0",
        "services": {
            "api": "running",
            "database": "connected",
            "ai_models": "loading..."
        }
    }


@router.get("/detailed")
async def detailed_health_check():
    """
    Detailed health check with service status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0",
        "services": {
            "api": {
                "status": "running",
                "uptime": "unknown"
            },
            "database": {
                "status": "connected",
                "type": "postgresql"
            },
            "redis": {
                "status": "connected",
                "type": "redis"
            },
            "ai_models": {
                "flux": "loading...",
                "gemini": "configured",
                "clip": "ready"
            }
        }
    }
