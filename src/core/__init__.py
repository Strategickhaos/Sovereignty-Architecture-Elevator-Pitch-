# SAGCO Core Package
from .sagco import (
    SAGCOKernel,
    ProcessingNode,
    Task,
    AcademicContext,
    DopamineEngine,
    LayerType,
    DopamineLevel,
    create_sagco_kernel
)

__version__ = "0.1.0"
__all__ = [
    "SAGCOKernel",
    "ProcessingNode",
    "Task",
    "AcademicContext",
    "DopamineEngine",
    "LayerType",
    "DopamineLevel",
    "create_sagco_kernel"
]
