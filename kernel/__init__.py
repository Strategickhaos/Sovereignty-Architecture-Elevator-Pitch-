"""
KHAOS Kernel Package
Zero-Dependency Sovereign Operating System
"""

from .khaos import KHAOSKernel, Module, KernelState, KERNEL_VERSION, KERNEL_CODENAME

__version__ = KERNEL_VERSION
__all__ = ["KHAOSKernel", "Module", "KernelState", "KERNEL_VERSION", "KERNEL_CODENAME"]
