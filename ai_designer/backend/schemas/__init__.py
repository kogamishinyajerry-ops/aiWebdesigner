"""
Pydantic schemas for request/response validation
"""

from .image import (
    ImageGenerationRequest,
    ImageGenerationResponse,
    ImagePreset
)
from .svg import (
    SVGGenerationRequest,
    SVGGenerationResponse,
    SVGStyle
)
from .code import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    CodeFramework
)
from .user import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from .project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)

__all__ = [
    # Image schemas
    'ImageGenerationRequest',
    'ImageGenerationResponse',
    'ImagePreset',
    # SVG schemas
    'SVGGenerationRequest',
    'SVGGenerationResponse',
    'SVGStyle',
    # Code schemas
    'CodeGenerationRequest',
    'CodeGenerationResponse',
    'CodeFramework',
    # User schemas
    'UserCreate',
    'UserUpdate',
    'UserResponse',
    # Project schemas
    'ProjectCreate',
    'ProjectUpdate',
    'ProjectResponse',
]
