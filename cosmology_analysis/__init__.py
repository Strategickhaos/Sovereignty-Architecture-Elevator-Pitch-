"""
Loop Quantum Cosmology (LQC) B-Mode Predictions and Planck 2018 Data Analysis

This module provides tools for analyzing CMB data from Planck 2018 and comparing
predictions from Loop Quantum Cosmology (LQC) with the standard ΛCDM model.
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC"

from .lqc_model import LQCModel
from .planck_data import PlanckData
from .visualization import plot_comparison, generate_analysis_report

__all__ = [
    'LQCModel',
    'PlanckData',
    'plot_comparison',
    'generate_analysis_report'
]
