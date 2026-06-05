"""
SAGCO - Sovereignty Architecture Grand Central Operating System
Core package initialization
"""

__version__ = "0.1.0"
__author__ = "Strategickhaos DAO LLC"
__description__ = "Dopamine-Enhanced Academic Performance System"

from .sagco import (
    SAGCOKernel,
    CognitiveLayer,
    DopamineLevel,
    TaskPriority,
)

__all__ = [
    "SAGCOKernel",
    "CognitiveLayer",
    "DopamineLevel",
    "TaskPriority",
    "__version__",
]
