"""
API v1 Router
"""

from fastapi import APIRouter
from api.v1.endpoints import (
    image,
    svg,
    code,
    health,
)

router = APIRouter()

# Include endpoints
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(image.router, prefix="/image", tags=["Image Generation"])
router.include_router(svg.router, prefix="/svg", tags=["SVG Generation"])
router.include_router(code.router, prefix="/code", tags=["Code Generation"])
