#!/usr/bin/env python3
"""
Truth Contract - Verification Contract System
Part of SAGCO OS CPU Architecture

This module implements a contract-based verification system where
claims must satisfy defined truth contracts before being accepted
into the system. Contracts define pre-conditions, post-conditions,
and invariants that must hold.

Based on Hoare logic and design-by-contract principles.
"""

import time
import hashlib
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum


class ContractType(Enum):
    """Types of truth contracts"""
    PRECONDITION = "precondition"
    POSTCONDITION = "postcondition"
    INVARIANT = "invariant"
    ASSERTION = "assertion"


@dataclass
class Contract:
    """Represents a truth contract"""
    name: str
    contract_type: ContractType
    predicate: Callable[[Dict], bool]
    description: str
    severity: int  # 1-5, where 5 is critical


@dataclass
class ContractViolation:
    """Represents a contract violation"""
    contract: Contract
    timestamp: float
    context: Dict
    message: str


@dataclass
class VerificationResult:
    """Result of contract verification"""
    passed: bool
    violations: List[ContractViolation]
    satisfied_contracts: List[str]
    confidence: float
    proof_hash: str


class TruthContract:
    """
    Contract-Based Verification System
    
    Enforces truth contracts on all claims and operations.
    Violations result in rejection and logging.
    """
    
    def __init__(self):
        self.contracts: Dict[str, Contract] = {}
        self.violation_history: List[ContractViolation] = []
        self.verification_count = 0
        self._initialize_core_contracts()
        
    def _initialize_core_contracts(self):
        """Initialize core truth contracts"""
        
        # Non-contradiction contract
        self.register_contract(Contract(
            name="non_contradiction",
            contract_type=ContractType.INVARIANT,
            predicate=lambda ctx: not (
                ctx.get("claim_a") and ctx.get("claim_b") and
                ctx.get("claim_a") == not ctx.get("claim_b")
            ),
            description="A claim cannot be both true and false simultaneously",
            severity=5
        ))
        
        # Non-negative energy contract
        self.register_contract(Contract(
            name="non_negative_energy",
            contract_type=ContractType.PRECONDITION,
            predicate=lambda ctx: ctx.get("energy", 0) >= 0,
            description="Energy values must be non-negative",
            severity=4
        ))
        
        # Causality contract
        self.register_contract(Contract(
            name="causality",
            contract_type=ContractType.INVARIANT,
            predicate=lambda ctx: (
                ctx.get("cause_time", 0) <= ctx.get("effect_time", float('inf'))
            ),
            description="Cause must precede or be simultaneous with effect",
            severity=5
        ))
        
        # Completeness contract
        self.register_contract(Contract(
            name="completeness",
            contract_type=ContractType.PRECONDITION,
            predicate=lambda ctx: all(
                ctx.get(required) is not None
                for required in ctx.get("required_fields", [])
            ),
            description="All required fields must be present",
            severity=3
        ))
        
        # Bounded values contract
        self.register_contract(Contract(
            name="bounded_values",
            contract_type=ContractType.PRECONDITION,
            predicate=lambda ctx: (
                ctx.get("min_value", float('-inf')) <= 
                ctx.get("value", 0) <= 
                ctx.get("max_value", float('inf'))
            ),
            description="Values must be within specified bounds",
            severity=3
        ))
    
    def register_contract(self, contract: Contract):
        """Register a new truth contract"""
        self.contracts[contract.name] = contract
    
    def verify(self, context: Dict[str, Any]) -> VerificationResult:
        """
        Verify context against all applicable contracts
        
        Args:
            context: Dictionary containing claims and data to verify
            
        Returns:
            VerificationResult with pass/fail and details
        """
        violations = []
        satisfied = []
        
        self.verification_count += 1
        
        # Check each contract
        for name, contract in self.contracts.items():
            try:
                if contract.predicate(context):
                    satisfied.append(name)
                else:
                    violation = ContractViolation(
                        contract=contract,
                        timestamp=time.time(),
                        context=context.copy(),
                        message=f"Contract '{name}' violated: {contract.description}"
                    )
                    violations.append(violation)
                    self.violation_history.append(violation)
            except Exception as e:
                # Predicate evaluation failed - treat as violation
                violation = ContractViolation(
                    contract=contract,
                    timestamp=time.time(),
                    context=context.copy(),
                    message=f"Contract '{name}' evaluation failed: {str(e)}"
                )
                violations.append(violation)
                self.violation_history.append(violation)
        
        # Calculate confidence based on severity of violations
        if not violations:
            confidence = 1.0
            passed = True
        else:
            # Critical violations (severity 5) completely fail verification
            critical_violations = [v for v in violations if v.contract.severity == 5]
            if critical_violations:
                confidence = 0.0
                passed = False
            else:
                # Reduce confidence based on severity of violations
                max_severity = max(v.contract.severity for v in violations)
                confidence = 1.0 - (max_severity / 5.0)
                passed = confidence > 0.5
        
        # Generate proof hash
        proof_data = {
            "timestamp": time.time(),
            "context": str(sorted(context.items())),
            "satisfied": sorted(satisfied),
            "violations": [v.message for v in violations],
        }
        proof_hash = hashlib.sha256(str(proof_data).encode()).hexdigest()[:16]
        
        return VerificationResult(
            passed=passed,
            violations=violations,
            satisfied_contracts=satisfied,
            confidence=confidence,
            proof_hash=proof_hash
        )
    
    def verify_transaction(
        self, 
        preconditions: Dict,
        operation: Callable,
        postconditions: Dict
    ) -> Tuple[bool, Any]:
        """
        Verify a transaction with pre/post conditions
        
        Args:
            preconditions: Context that must be satisfied before operation
            operation: The operation to perform
            postconditions: Context that must be satisfied after operation
            
        Returns:
            Tuple of (success, result)
        """
        # Verify preconditions
        pre_result = self.verify(preconditions)
        if not pre_result.passed:
            return False, f"Preconditions failed: {[v.message for v in pre_result.violations]}"
        
        # Perform operation
        try:
            result = operation()
        except Exception as e:
            return False, f"Operation failed: {str(e)}"
        
        # Verify postconditions
        post_result = self.verify(postconditions)
        if not post_result.passed:
            return False, f"Postconditions failed: {[v.message for v in post_result.violations]}"
        
        return True, result
    
    def get_contract_statistics(self) -> Dict:
        """Return contract verification statistics"""
        total_violations = len(self.violation_history)
        recent_violations = [
            v for v in self.violation_history 
            if time.time() - v.timestamp < 3600
        ]
        
        critical_violations = [
            v for v in self.violation_history 
            if v.contract.severity == 5
        ]
        
        return {
            "total_verifications": self.verification_count,
            "total_violations": total_violations,
            "recent_violations": len(recent_violations),
            "critical_violations": len(critical_violations),
            "registered_contracts": len(self.contracts),
            "violation_rate": total_violations / self.verification_count if self.verification_count > 0 else 0,
            "system_integrity": "COMPROMISED" if len(critical_violations) > 0 else "STRONG",
        }


def main():
    """Demonstration of Truth Contract system"""
    contract_system = TruthContract()
    
    print("📜 TRUTH CONTRACT - Verification Contract System")
    print("=" * 70)
    
    # Test cases
    test_cases = [
        {
            "name": "Valid energy claim",
            "context": {"energy": 100.0},
        },
        {
            "name": "Invalid negative energy",
            "context": {"energy": -50.0},
        },
        {
            "name": "Causality violation",
            "context": {"cause_time": 100.0, "effect_time": 50.0},
        },
        {
            "name": "Valid causality",
            "context": {"cause_time": 50.0, "effect_time": 100.0},
        },
        {
            "name": "Bounded value test (valid)",
            "context": {"value": 50, "min_value": 0, "max_value": 100},
        },
        {
            "name": "Bounded value test (invalid)",
            "context": {"value": 150, "min_value": 0, "max_value": 100},
        },
    ]
    
    for test in test_cases:
        print(f"\n[Test] {test['name']}")
        result = contract_system.verify(test['context'])
        
        print(f"Result: {'✅ PASS' if result.passed else '❌ FAIL'} (confidence: {result.confidence:.0%})")
        print(f"Proof Hash: {result.proof_hash}")
        
        if result.violations:
            print("Violations:")
            for violation in result.violations:
                print(f"  - {violation.message}")
        
        print(f"Satisfied: {', '.join(result.satisfied_contracts)}")
    
    print("\n" + "=" * 70)
    stats = contract_system.get_contract_statistics()
    print(f"Contract System Statistics:")
    print(f"  Total Verifications: {stats['total_verifications']}")
    print(f"  Total Violations: {stats['total_violations']}")
    print(f"  Critical Violations: {stats['critical_violations']}")
    print(f"  System Integrity: {stats['system_integrity']}")
    print(f"  Violation Rate: {stats['violation_rate']:.1%}")


if __name__ == "__main__":
    main()
