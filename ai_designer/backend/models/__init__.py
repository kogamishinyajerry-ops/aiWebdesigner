"""
Database Models
"""

from core.database import Base

from .user import User
from .project import Project
from .design import Design
from .generation import Generation, GenerationCache
from .asset import Asset
from .tag import Tag, AssetTag
from .favorite import Favorite
from .template import Template

__all__ = [
    # Core models
    'User',
    'Project',
    'Design',
    # Generation models
    'Generation',
    'GenerationCache',
    # Asset models
    'Asset',
    # Tag models
    'Tag',
    'AssetTag',
    # Favorite models
    'Favorite',
    # Template models
    'Template',
]
