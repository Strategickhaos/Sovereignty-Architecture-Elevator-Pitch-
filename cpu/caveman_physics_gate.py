#!/usr/bin/env python3
"""
Caveman Physics Gate - Reality Verification Layer
Part of SAGCO OS CPU Architecture

This module implements the fundamental reality checking and claim validation
system. It uses "caveman physics" - basic, undeniable physical principles
that even a caveman would understand - to verify claims and prevent
acceptance of physically impossible or logically contradictory statements.

Philosophy: If you can't explain it with rocks, fire, and gravity, 
it probably doesn't exist.
"""

import math
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class ValidationResult(Enum):
    """Result of reality validation"""
    VALID = "VALID"
    SUSPICIOUS = "SUSPICIOUS"
    IMPOSSIBLE = "IMPOSSIBLE"
    CONTRADICTORY = "CONTRADICTORY"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


@dataclass
class Claim:
    """Represents a claim to be validated"""
    statement: str
    properties: Dict[str, Any]
    timestamp: float
    source: str


@dataclass
class ValidationReport:
    """Result of claim validation"""
    claim: Claim
    result: ValidationResult
    confidence: float
    violations: List[str]
    supporting_evidence: List[str]
    caveman_explanation: str


class CavemanPhysicsGate:
    """
    Reality Verification Layer using fundamental physical principles
    
    Validates claims against basic physics, logic, and causality.
    Rejects claims that violate conservation laws, causality, or
    basic arithmetic.
    """
    
    # Physical constants (caveman-accessible)
    GRAVITY = 9.81  # m/s² - things fall down
    SPEED_OF_LIGHT = 299792458  # m/s - nothing goes faster
    WATER_BOILS = 373.15  # K - water boils at 100°C
    WATER_FREEZES = 273.15  # K - water freezes at 0°C
    
    def __init__(self):
        self.validation_history: List[ValidationReport] = []
        self.rejected_claims = 0
        self.accepted_claims = 0
        
    def validate_claim(self, claim: Claim) -> ValidationReport:
        """
        Validate a claim against caveman physics principles
        
        Args:
            claim: The claim to validate
            
        Returns:
            ValidationReport with results and explanation
        """
        violations = []
        supporting = []
        
        # Check energy conservation
        if "energy_in" in claim.properties and "energy_out" in claim.properties:
            violation = self._check_energy_conservation(
                claim.properties["energy_in"],
                claim.properties["energy_out"]
            )
            if violation:
                violations.append(violation)
        
        # Check causality
        if "cause_time" in claim.properties and "effect_time" in claim.properties:
            violation = self._check_causality(
                claim.properties["cause_time"],
                claim.properties["effect_time"]
            )
            if violation:
                violations.append(violation)
        
        # Check speed limit
        if "velocity" in claim.properties:
            violation = self._check_speed_limit(claim.properties["velocity"])
            if violation:
                violations.append(violation)
        
        # Check arithmetic consistency
        if "value" in claim.properties and "expected" in claim.properties:
            violation = self._check_arithmetic(
                claim.properties["value"],
                claim.properties["expected"]
            )
            if violation:
                violations.append(violation)
        
        # Check temperature sanity
        if "temperature" in claim.properties:
            violation = self._check_temperature(claim.properties["temperature"])
            if violation:
                violations.append(violation)
            else:
                supporting.append("Temperature is within physical bounds")
        
        # Determine result
        if len(violations) > 0:
            if any("impossible" in v.lower() for v in violations):
                result = ValidationResult.IMPOSSIBLE
                confidence = 0.95
            else:
                result = ValidationResult.SUSPICIOUS
                confidence = 0.70
        else:
            result = ValidationResult.VALID
            confidence = 0.85
        
        # Generate caveman explanation
        caveman_explanation = self._generate_caveman_explanation(
            claim, result, violations
        )
        
        # Create report
        report = ValidationReport(
            claim=claim,
            result=result,
            confidence=confidence,
            violations=violations,
            supporting_evidence=supporting,
            caveman_explanation=caveman_explanation
        )
        
        # Update statistics
        if result == ValidationResult.VALID:
            self.accepted_claims += 1
        else:
            self.rejected_claims += 1
        
        self.validation_history.append(report)
        
        return report
    
    def _check_energy_conservation(self, energy_in: float, energy_out: float) -> Optional[str]:
        """Check if energy is conserved (caveman: you can't create fire from nothing)"""
        tolerance = 0.1  # 10% tolerance for measurement error
        
        if energy_out > energy_in * (1 + tolerance):
            return f"Energy conservation violated: output ({energy_out}) > input ({energy_in}). " \
                   f"Caveman says: You can't make more fire than the wood you burn."
        
        return None
    
    def _check_causality(self, cause_time: float, effect_time: float) -> Optional[str]:
        """Check if cause precedes effect (caveman: you throw rock, then rock flies)"""
        if effect_time < cause_time:
            return f"Causality violated: effect ({effect_time}) before cause ({cause_time}). " \
                   f"Caveman says: Rock can't land before you throw it."
        
        return None
    
    def _check_speed_limit(self, velocity: float) -> Optional[str]:
        """Check if velocity exceeds speed of light (caveman: nothing goes faster than light)"""
        if abs(velocity) > self.SPEED_OF_LIGHT:
            return f"Speed limit violated: velocity ({velocity} m/s) > speed of light. " \
                   f"Caveman says: Even fastest spear not faster than lightning."
        
        return None
    
    def _check_arithmetic(self, value: float, expected: float) -> Optional[str]:
        """Check basic arithmetic (caveman: two rocks plus two rocks equals four rocks)"""
        tolerance = 0.01  # 1% tolerance
        
        if abs(value - expected) > abs(expected * tolerance):
            return f"Arithmetic inconsistent: got {value}, expected {expected}. " \
                   f"Caveman says: Count rocks again, numbers not match."
        
        return None
    
    def _check_temperature(self, temperature: float) -> Optional[str]:
        """Check if temperature is physically reasonable (caveman: ice cold, fire hot)"""
        # Absolute zero check
        if temperature < 0:  # Assuming Kelvin
            return f"Temperature impossible: {temperature}K below absolute zero. " \
                   f"Caveman says: Nothing colder than coldest cold."
        
        # Unreasonably high (hotter than core of sun)
        if temperature > 15_000_000:  # 15 million K
            return f"Temperature impossible: {temperature}K hotter than sun. " \
                   f"Caveman says: This hotter than biggest fire in sky."
        
        return None
    
    def _generate_caveman_explanation(
        self, 
        claim: Claim, 
        result: ValidationResult,
        violations: List[str]
    ) -> str:
        """Generate a caveman-style explanation of the validation result"""
        
        if result == ValidationResult.VALID:
            return "✅ Caveman understand claim. Make sense with rocks and fire. Trust this."
        
        elif result == ValidationResult.SUSPICIOUS:
            return f"⚠️ Caveman confused. Claim maybe true, but seem strange. " \
                   f"Like saying: '{violations[0] if violations else 'something odd'}'. " \
                   f"Need more proof before trust."
        
        elif result == ValidationResult.IMPOSSIBLE:
            return f"❌ Caveman know this impossible! " \
                   f"This like saying: '{violations[0] if violations else 'rocks fall up'}'. " \
                   f"Cannot be true. Reject claim."
        
        else:
            return "❓ Caveman need more information. Not enough to know if true or false."
    
    def get_gate_statistics(self) -> Dict:
        """Return gate performance statistics"""
        total = self.accepted_claims + self.rejected_claims
        
        return {
            "total_validations": total,
            "accepted": self.accepted_claims,
            "rejected": self.rejected_claims,
            "rejection_rate": self.rejected_claims / total if total > 0 else 0,
            "gate_integrity": "STRONG" if self.rejected_claims > 0 else "UNTESTED",
            "caveman_wisdom": "Trust but verify. When in doubt, consult the rocks."
        }


def main():
    """Demonstration of the Caveman Physics Gate"""
    gate = CavemanPhysicsGate()
    
    # Test claims
    test_claims = [
        Claim(
            statement="Solar panel converts sunlight to electricity",
            properties={"energy_in": 100.0, "energy_out": 20.0},
            timestamp=time.time(),
            source="test"
        ),
        Claim(
            statement="Perpetual motion machine generates infinite energy",
            properties={"energy_in": 10.0, "energy_out": 100.0},
            timestamp=time.time(),
            source="test"
        ),
        Claim(
            statement="Time traveler causes effect before cause",
            properties={"cause_time": 100.0, "effect_time": 50.0},
            timestamp=time.time(),
            source="test"
        ),
        Claim(
            statement="Spacecraft traveling at reasonable speed",
            properties={"velocity": 50000.0},  # 50 km/s
            timestamp=time.time(),
            source="test"
        ),
    ]
    
    print("🪨 CAVEMAN PHYSICS GATE - Reality Verification Layer")
    print("=" * 70)
    
    for i, claim in enumerate(test_claims, 1):
        print(f"\n[Claim {i}] {claim.statement}")
        report = gate.validate_claim(claim)
        
        print(f"Result: {report.result.value} (confidence: {report.confidence:.0%})")
        
        if report.violations:
            print("Violations:")
            for violation in report.violations:
                print(f"  - {violation}")
        
        print(f"\n{report.caveman_explanation}")
    
    print("\n" + "=" * 70)
    stats = gate.get_gate_statistics()
    print(f"Gate Statistics:")
    print(f"  Total Validations: {stats['total_validations']}")
    print(f"  Accepted: {stats['accepted']}")
    print(f"  Rejected: {stats['rejected']}")
    print(f"  Gate Integrity: {stats['gate_integrity']}")
    print(f"\n💎 {stats['caveman_wisdom']}")


if __name__ == "__main__":
    main()
