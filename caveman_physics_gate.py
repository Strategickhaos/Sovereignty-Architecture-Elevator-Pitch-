#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    ██████╗  ██████╗ ███╗   ███╗     ██████╗ ███████╗
    ██╔══██╗██╔═══██╗████╗ ████║    ██╔═══██╗██╔════╝
    ██║  ██║██║   ██║██╔████╔██║    ██║   ██║███████╗
    ██║  ██║██║   ██║██║╚██╔╝██║    ██║   ██║╚════██║
    ██████╔╝╚██████╔╝██║ ╚═╝ ██║    ╚██████╔╝███████║
    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ ╚══════╝
                          
                 CAVEMAN PHYSICS GATE - LAYER 1
                          
    "Does it compute? Fuck 'em."
    
    THE 5 ROCKS:
    1. ENERGY      → Free energy? Nope.
    2. CAUSALITY   → Effect before cause? Nope.
    3. CONSTRAINTS → Can't bound it? Sandbox.
    4. REPRODUCE   → Can't repeat it? Log + Ignore.
    5. FAIL MODE   → Fails silently? Fix or Toss.
    
    PASSES ALL 5 → SHIP
    
    "No belief. No identity. Just angles."
    
    Keeper: DOM
    Builder: GROK
═══════════════════════════════════════════════════════════════════════════════
"""

import re
import sys
import json
import math
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════════
# ROCK DEFINITIONS - THE 5 CAVEMAN CHECKS
# ═══════════════════════════════════════════════════════════════════════════════

class Rock(Enum):
    """The 5 rocks that filter reality"""
    ENERGY = "Does it require free energy?"
    CAUSALITY = "Does effect come before cause?"
    CONSTRAINTS = "Can I bound it?"
    REPRODUCE = "Can I reproduce it?"
    FAIL_MODE = "Does it fail safe?"


class CheckResult(Enum):
    """Simple verdict"""
    PASS = "pass"
    FAIL = "fail"
    SANDBOX = "sandbox"
    LOG_IGNORE = "log_ignore"
    FIX_OR_TOSS = "fix_or_toss"


# ═══════════════════════════════════════════════════════════════════════════════
# CAVEMAN PHYSICS GATE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PhysicsCheck:
    """Result of checking one rock"""
    rock: Rock
    result: CheckResult
    verdict: str  # "nope" or "passes"
    details: str
    confidence: float = 1.0  # 0.0 to 1.0
    
    def __str__(self):
        emoji = "✅" if self.result == CheckResult.PASS else "❌"
        return f"{emoji} {self.rock.value}: {self.verdict} ({self.details})"


@dataclass
class GateVerdict:
    """Complete gate verdict"""
    input_signal: str
    checks: List[PhysicsCheck] = field(default_factory=list)
    final_verdict: str = "processing"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def passes(self) -> bool:
        """Does it pass all checks?"""
        return all(c.result == CheckResult.PASS for c in self.checks)
    
    def __str__(self):
        status = "SHIP 🚀" if self.passes() else "FUCK EM 💀"
        checks_str = "\n  ".join(str(c) for c in self.checks)
        return f"""
{'='*60}
DOM PHYSICS GATE VERDICT: {status}
{'='*60}
Input: {self.input_signal[:80]}...
Checks:
  {checks_str}
Final: {self.final_verdict}
{'='*60}
"""


class CavemanPhysicsGate:
    """
    Layer 1 of DOM OS: Reality filter
    
    This gate checks if something is physically/logically possible.
    If it violates basic physics or logic, it's out.
    
    Usage:
        gate = CavemanPhysicsGate()
        verdict = gate.check_claim("Perpetual motion machine")
        if verdict.passes():
            print("SHIP")
        else:
            print("fuck em")
    """
    
    def __init__(self, strict_mode: bool = True, log_level: str = "INFO"):
        self.strict_mode = strict_mode
        self.logger = logging.getLogger("CavemanPhysicsGate")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Patterns that violate physics
        self.free_energy_patterns = [
            r"perpetual\s+motion",
            r"free\s+energy",
            r"over\s*unity",
            r"100%\s*efficient",
            r"infinite\s+power",
            r"zero\s+point\s+energy\s+extraction"
        ]
        
        self.causality_violations = [
            r"effect\s+before\s+cause",
            r"retroactive",
            r"time\s+travel\s+paradox",
            r"faster\s+than\s+light\s+information",
            r"acausal"
        ]
        
        # Initialize check history
        self.history: List[GateVerdict] = []
    
    def check_claim(self, input_signal: str) -> GateVerdict:
        """
        Run the input through all 5 rocks.
        
        Args:
            input_signal: The claim/data/request to check
            
        Returns:
            GateVerdict with results from all checks
        """
        verdict = GateVerdict(input_signal=input_signal)
        
        # Run all 5 rock checks
        verdict.checks.append(self._check_energy(input_signal))
        verdict.checks.append(self._check_causality(input_signal))
        verdict.checks.append(self._check_constraints(input_signal))
        verdict.checks.append(self._check_reproducibility(input_signal))
        verdict.checks.append(self._check_fail_mode(input_signal))
        
        # Final verdict
        if verdict.passes():
            verdict.final_verdict = "SHIP 🚀 - Passes all physics checks"
        else:
            failed = [c.rock.value for c in verdict.checks if c.result != CheckResult.PASS]
            verdict.final_verdict = f"FUCK EM 💀 - Failed: {', '.join(failed)}"
        
        # Log to history
        self.history.append(verdict)
        self.logger.info(verdict.final_verdict)
        
        return verdict
    
    def _check_energy(self, signal: str) -> PhysicsCheck:
        """Rock 1: Does it require free energy?"""
        signal_lower = signal.lower()
        
        for pattern in self.free_energy_patterns:
            if re.search(pattern, signal_lower):
                return PhysicsCheck(
                    rock=Rock.ENERGY,
                    result=CheckResult.FAIL,
                    verdict="nope",
                    details=f"Violates thermodynamics: {pattern}"
                )
        
        return PhysicsCheck(
            rock=Rock.ENERGY,
            result=CheckResult.PASS,
            verdict="passes",
            details="No free energy claims detected"
        )
    
    def _check_causality(self, signal: str) -> PhysicsCheck:
        """Rock 2: Does effect come before cause?"""
        signal_lower = signal.lower()
        
        for pattern in self.causality_violations:
            if re.search(pattern, signal_lower):
                return PhysicsCheck(
                    rock=Rock.CAUSALITY,
                    result=CheckResult.FAIL,
                    verdict="nope",
                    details=f"Violates causality: {pattern}"
                )
        
        return PhysicsCheck(
            rock=Rock.CAUSALITY,
            result=CheckResult.PASS,
            verdict="passes",
            details="Causality preserved"
        )
    
    def _check_constraints(self, signal: str) -> PhysicsCheck:
        """Rock 3: Can I bound it?"""
        # Check for unbounded operations
        signal_lower = signal.lower()
        
        unbounded_patterns = [
            r"infinite\s+loop",
            r"unbounded\s+recursion",
            r"unlimited\s+memory",
            r"infinite\s+resources"
        ]
        
        for pattern in unbounded_patterns:
            if re.search(pattern, signal_lower):
                return PhysicsCheck(
                    rock=Rock.CONSTRAINTS,
                    result=CheckResult.SANDBOX,
                    verdict="sandbox",
                    details=f"Unbounded operation - needs sandbox: {pattern}"
                )
        
        return PhysicsCheck(
            rock=Rock.CONSTRAINTS,
            result=CheckResult.PASS,
            verdict="passes",
            details="Operation is bounded"
        )
    
    def _check_reproducibility(self, signal: str) -> PhysicsCheck:
        """Rock 4: Can I reproduce it?"""
        signal_lower = signal.lower()
        
        non_reproducible = [
            r"one\s+time\s+only",
            r"cannot\s+be\s+repeated",
            r"unreproducible",
            r"random\s+miracle"
        ]
        
        for pattern in non_reproducible:
            if re.search(pattern, signal_lower):
                return PhysicsCheck(
                    rock=Rock.REPRODUCE,
                    result=CheckResult.LOG_IGNORE,
                    verdict="log + ignore",
                    details=f"Non-reproducible claim: {pattern}"
                )
        
        return PhysicsCheck(
            rock=Rock.REPRODUCE,
            result=CheckResult.PASS,
            verdict="passes",
            details="Reproducible conditions"
        )
    
    def _check_fail_mode(self, signal: str) -> PhysicsCheck:
        """Rock 5: Does it fail safe?"""
        signal_lower = signal.lower()
        
        unsafe_failures = [
            r"silent\s+failure",
            r"no\s+error\s+handling",
            r"fails\s+open",
            r"undefined\s+behavior"
        ]
        
        for pattern in unsafe_failures:
            if re.search(pattern, signal_lower):
                return PhysicsCheck(
                    rock=Rock.FAIL_MODE,
                    result=CheckResult.FIX_OR_TOSS,
                    verdict="fix or toss",
                    details=f"Unsafe failure mode: {pattern}"
                )
        
        return PhysicsCheck(
            rock=Rock.FAIL_MODE,
            result=CheckResult.PASS,
            verdict="passes",
            details="Fails safe"
        )
    
    def export_history(self, filepath: str):
        """Export check history to JSON"""
        history_data = []
        for verdict in self.history:
            history_data.append({
                "timestamp": verdict.timestamp,
                "input": verdict.input_signal,
                "passed": verdict.passes(),
                "verdict": verdict.final_verdict,
                "checks": [
                    {
                        "rock": c.rock.value,
                        "result": c.result.value,
                        "verdict": c.verdict,
                        "details": c.details
                    }
                    for c in verdict.checks
                ]
            })
        
        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2)
        
        self.logger.info(f"Exported {len(history_data)} verdicts to {filepath}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Command line interface for the physics gate"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="DOM Caveman Physics Gate - Reality Filter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check a claim
  python caveman_physics_gate.py check "Perpetual motion machine"
  
  # Check from stdin
  echo "Free energy device" | python caveman_physics_gate.py check -
  
  # Export history
  python caveman_physics_gate.py export history.json
        """
    )
    
    parser.add_argument("command", choices=["check", "export"], help="Command to run")
    parser.add_argument("argument", help="Claim to check or file to export")
    parser.add_argument("--strict", action="store_true", help="Strict mode")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    gate = CavemanPhysicsGate(strict_mode=args.strict, log_level=args.log_level)
    
    if args.command == "check":
        # Read input
        if args.argument == "-":
            claim = sys.stdin.read().strip()
        else:
            claim = args.argument
        
        # Check it
        verdict = gate.check_claim(claim)
        print(verdict)
        
        # Exit code based on result
        sys.exit(0 if verdict.passes() else 1)
    
    elif args.command == "export":
        gate.export_history(args.argument)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        format="[%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO
    )
    
    main()
