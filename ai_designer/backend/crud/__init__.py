"""
CRUD Operations
"""

from .base import CRUDBase
from .user import CRUDUser
from .project import CRUDProject
from .asset import CRUDAsset
from .generation import CRUDGeneration

__all__ = [
    'CRUDBase',
    'CRUDUser',
    'CRUDProject',
    'CRUDAsset',
    'CRUDGeneration',
]
