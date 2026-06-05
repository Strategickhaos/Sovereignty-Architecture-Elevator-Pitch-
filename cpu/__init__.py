"""
SAGCO OS CPU Architecture
Part of Sovereignty Architecture Governance and Control Operating System

This package contains the core CPU verification and validation modules
that form the foundation of SAGCO OS's adversarial-aware architecture.
"""

from .dom_immune_system import DOMImmuneSystem, PsychologicalThreat, ThreatLevel
from .caveman_physics_gate import CavemanPhysicsGate, Claim, ValidationResult
from .trig6_flame_mapper import TRIG6FlameMapper, TrigFunction, TRIG6Report
from .truth_contract import TruthContract, Contract, ContractType, VerificationResult
from .load_shedding_scheduler import LoadSheddingScheduler, Task, Priority, ResourceType

__version__ = "1.0.0"
__all__ = [
    "DOMImmuneSystem",
    "PsychologicalThreat",
    "ThreatLevel",
    "CavemanPhysicsGate",
    "Claim",
    "ValidationResult",
    "TRIG6FlameMapper",
    "TrigFunction",
    "TRIG6Report",
    "TruthContract",
    "Contract",
    "ContractType",
    "VerificationResult",
    "LoadSheddingScheduler",
    "Task",
    "Priority",
    "ResourceType",
]
