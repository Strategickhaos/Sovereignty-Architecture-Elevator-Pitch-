"""
FlameLang CPU module

Contains the caveman physics gate - a constraint-based evaluation system
that uses TRIG6 (6 independent perspectives) to validate claims.
"""

from .caveman_physics_gate import Claim, CavemanPhysicsGate

__all__ = ['Claim', 'CavemanPhysicsGate']
