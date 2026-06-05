"""
BB Simulator for Unified LQC-String Model.

Minimal production-ready Python simulator based on Physics Spine Spec equations.
Generates mock Planck-like B-mode data from the unified model.
"""

from .bb_simulator import (
    bb_model,
    lcdm_model,
    lqc_only,
    string_only,
    chi2,
    generate_mock_data,
    fit_models,
    run_simulation,
    print_results
)

__version__ = "1.0.0"
__all__ = [
    'bb_model',
    'lcdm_model',
    'lqc_only',
    'string_only',
    'chi2',
    'generate_mock_data',
    'fit_models',
    'run_simulation',
    'print_results'
]
