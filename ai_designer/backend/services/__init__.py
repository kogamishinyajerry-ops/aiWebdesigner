"""
AI Services Package
所有AI服务的统一导出
"""

from .ai_models import (
    ModelManager,
    model_manager,
    get_image_generator,
    get_gemini_client,
    get_gemini_model,
    get_clip_model,
    get_clip_preprocess
)

from .image_generation import (
    ImageGenerationService,
    image_service
)

from .svgn_generation import (
    SVGGenerationService,
    svg_service
)

from .code_generation import (
    CodeGenerationService,
    code_service
)

from .aesthetic_engine import (
    AestheticEngine,
    aesthetic_engine
)

__all__ = [
    # AI Models
    "ModelManager",
    "model_manager",
    "get_image_generator",
    "get_gemini_client",
    "get_gemini_model",
    "get_clip_model",
    "get_clip_preprocess",
    
    # Services
    "ImageGenerationService",
    "image_service",
    "SVGGenerationService",
    "svg_service",
    "CodeGenerationService",
    "code_service",
    "AestheticEngine",
    "aesthetic_engine"
]
