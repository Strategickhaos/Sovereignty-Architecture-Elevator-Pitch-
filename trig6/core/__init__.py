"""
TRIG6 Core Module
Zero external dependencies, deterministic physics
"""

from .units import Force, Angle, Length, validate_positive, validate_range
from .citations import Citation, get_citation, list_citations, search_citations
from .model_registry import PhysicsModel, get_model, list_models
from .doctor import run_doctor, format_doctor_output

__all__ = [
    'Force', 'Angle', 'Length', 'validate_positive', 'validate_range',
    'Citation', 'get_citation', 'list_citations', 'search_citations',
    'PhysicsModel', 'get_model', 'list_models',
    'run_doctor', 'format_doctor_output'
]
