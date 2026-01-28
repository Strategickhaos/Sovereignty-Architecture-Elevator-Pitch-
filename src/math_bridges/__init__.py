"""
Mathematical Bridges for Sovereignty Architecture

This module provides formal mathematical bridges between different encoding domains,
transforming conceptual correlations into testable, provable mathematical relationships.

The bridges connect:
- Discrete ↔ Continuous (Quantization)
- Cube ↔ Sphere (Geometric Projection)
- Position ↔ Trig (Spherical Coordinates)
- Algorithm ↔ Direction (Permutation Eigenvalues)
- Fallacies ↔ Chess (Graph Laplacian)
- MIDI ↔ Geometry (Exponential Pitch)
- DNA ↔ 64-grid (Base-4 to Base-2)
- Hash ↔ Structure (Birthday Bound)
- Trees ↔ Decisions (Cost Functions)
- Cognition ↔ Control (Energy Minimization)
"""

from .quantization import Quantization
from .geometric_projection import GeometricProjection
from .spherical_coordinates import SphericalCoordinates
from .permutation_group import PermutationGroup
from .graph_laplacian import GraphLaplacian
from .sound_physics import SoundPhysics
from .codon_encoding import CodonEncoding
from .hash_geometry import HashGeometry
from .tree_cost import TreeCost
from .energy_minimization import EnergyMinimization

__all__ = [
    'Quantization',
    'GeometricProjection',
    'SphericalCoordinates',
    'PermutationGroup',
    'GraphLaplacian',
    'SoundPhysics',
    'CodonEncoding',
    'HashGeometry',
    'TreeCost',
    'EnergyMinimization',
]

__version__ = '0.1.0'
