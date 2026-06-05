"""
CPU Boot System - Recovery Protocol
====================================

Mount persistent artifacts before letting volatile interpretation run.
"""

from .boot_digest import BootDigest, main

__version__ = "1.0.0"
__all__ = ["BootDigest", "main"]
