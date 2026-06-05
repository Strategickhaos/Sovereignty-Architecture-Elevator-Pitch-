"""
TRIG6 Pattern Detection Package

This package implements the AI Validation Pivot Pattern detection system.
"""

from .ai_validation_pivot import (
    AIValidationPivotDetector,
    ValidationState,
    ContextProfile,
    PROFESSIONAL_CONTEXTS,
    demonstrate_pattern
)

__all__ = [
    'AIValidationPivotDetector',
    'ValidationState',
    'ContextProfile',
    'PROFESSIONAL_CONTEXTS',
    'demonstrate_pattern'
]

__version__ = '1.0.0'
__author__ = 'TRIG6 Analysis Team'
