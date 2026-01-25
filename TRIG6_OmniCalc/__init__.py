"""
TRIG6 OmniCalc - Calculator, VM, and Compiler for TRIG6 Mathematics

This package provides:
- Core TRIG6 mathematical operations (trig6_core)
- Virtual machine for state management (trig6_vm)
- Interactive REPL calculator (trig6_cli)

Example usage:
    from TRIG6_OmniCalc import Trig6VM
    import math
    
    vm = Trig6VM(theta=math.pi/4, alpha=0.0, theta_opt=math.pi/4)
    vm.op_step()
    print(vm.snapshot())
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC / Valoryield Engine"

from .trig6_core import (
    Trig6Projections,
    BlendParams,
    compute_trig6,
    blend_trig_hyper,
    compute_noise,
    compute_drift,
    compute_resonance,
    danger_zones,
)

from .trig6_vm import (
    Trig6State,
    Trig6VM,
)

__all__ = [
    # Core math
    'Trig6Projections',
    'BlendParams',
    'compute_trig6',
    'blend_trig_hyper',
    'compute_noise',
    'compute_drift',
    'compute_resonance',
    'danger_zones',
    # VM
    'Trig6State',
    'Trig6VM',
]
