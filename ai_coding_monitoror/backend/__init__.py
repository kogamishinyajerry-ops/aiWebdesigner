"""
AI Coding Monitoror - Backend package
"""

__version__ = "0.1.0"

from .main import app
from .context_manager import ContextManager
from .code_detector import CodeChangeDetector
from .validation_engine import ValidationEngine
from .alert_system import AlertSystem, Alert
from .memory_store import MemoryStore

__all__ = [
    "app",
    "ContextManager",
    "CodeChangeDetector",
    "ValidationEngine",
    "AlertSystem",
    "Alert",
    "MemoryStore"
]
