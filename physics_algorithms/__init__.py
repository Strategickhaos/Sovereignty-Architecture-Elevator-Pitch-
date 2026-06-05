"""
Physics-Based Optimization Algorithms for Cyber Defense
Sovereignty Architecture Enhancement v1.0

This package contains 16 physics-inspired optimization algorithms
adapted for defensive cybersecurity applications.
"""

from .base import PhysicsOptimizer
from .gravitational import GravitationalSearchAlgorithm, GravitationalInteractionOptimizer
from .thermodynamic import SimulatedAnnealing, EquilibriumOptimizer
from .electromagnetic import ElectromagnetismAlgorithm, ChargedSystemSearch, MagneticOptimization
from .mechanical import CentralForceOptimization, CollidingBodiesOptimization, ArtificialPhysicsOptimization
from .cosmological import BlackHoleAlgorithm, BigBangBigCrunch, MultiverseOptimizer
from .optical import OpticsInspiredOptimization, RayOptimization
from .immune import ImmuneGravitationOptimizer

__all__ = [
    'PhysicsOptimizer',
    'GravitationalSearchAlgorithm',
    'SimulatedAnnealing',
    'CentralForceOptimization',
    'ElectromagnetismAlgorithm',
    'ChargedSystemSearch',
    'CollidingBodiesOptimization',
    'BlackHoleAlgorithm',
    'BigBangBigCrunch',
    'MultiverseOptimizer',
    'OpticsInspiredOptimization',
    'RayOptimization',
    'MagneticOptimization',
    'ArtificialPhysicsOptimization',
    'GravitationalInteractionOptimizer',
    'EquilibriumOptimizer',
    'ImmuneGravitationOptimizer',
]

__version__ = '1.0.0'
