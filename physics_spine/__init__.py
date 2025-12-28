"""
Physics Spine: Multi-Regime BB Spectrum in Unified LQC-String Model

This module implements the unified model combining Loop Quantum Cosmology (LQC) 
bounce effects with string theory cosmic defects, constrained by a discrete 
selection operator inspired by FlameLang's Hebrew-root and DNA layers.
"""

from .core import (
    ModelParameters,
    UnifiedModel,
    SelectionOperator,
    BBSpectrumCalculator,
)

from .likelihood import (
    BayesianPipeline,
    PlanckData,
    compute_chi_squared,
    compute_bayes_factor,
    compute_likelihood,
)

__version__ = "1.0.0"
__all__ = [
    "ModelParameters",
    "UnifiedModel",
    "SelectionOperator",
    "BBSpectrumCalculator",
    "BayesianPipeline",
    "PlanckData",
    "compute_chi_squared",
    "compute_bayes_factor",
    "compute_likelihood",
]
