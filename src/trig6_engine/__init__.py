"""
TRIG6 Engine - Cognitive Efficiency Verification System

Provides formal verification tools for cognitive efficiency claims.
Implements proof system with convergence analysis and fitness scoring.

Core functionality:
- TRIG6 formula calculations
- Convergence detection
- Fitness scoring
- Proof certificate generation
"""

from .verifier import (
    TRIG6Verifier,
    ProofCertificate,
    verify_efficiency_claim,
    verify_120x_claim
)

from .calculator import (
    TRIG6Calculator,
    calculate_efficiency,
    batch_calculate
)

from .convergence import (
    ConvergenceAnalyzer,
    check_convergence,
    calculate_fitness
)

__version__ = '6.0.0'
__module__ = 'TRIG6 Math Engine'
__status__ = 'DEPLOYED'

__all__ = [
    'TRIG6Verifier',
    'ProofCertificate',
    'verify_efficiency_claim',
    'verify_120x_claim',
    'TRIG6Calculator',
    'calculate_efficiency',
    'batch_calculate',
    'ConvergenceAnalyzer',
    'check_convergence',
    'calculate_fitness'
]
