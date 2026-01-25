"""
Neuromorphic Computing Integration Module
Loihi-TRIG6 Beta Thalassemia Gene Editing Simulation
Strategickhaos DAO LLC - SAGCO-OS Compiler Integration
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC"

from .loihi_trig6_beta_thal import (
    loihi_spike_encode,
    trig6_states,
    treo_evolve,
    run_beta_thal_simulation
)

__all__ = [
    'loihi_spike_encode',
    'trig6_states', 
    'treo_evolve',
    'run_beta_thal_simulation'
]
