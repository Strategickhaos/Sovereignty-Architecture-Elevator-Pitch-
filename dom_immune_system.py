#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    ██████╗  ██████╗ ███╗   ███╗     ██████╗ ███████╗
    ██╔══██╗██╔═══██╗████╗ ████║    ██╔═══██╗██╔════╝
    ██║  ██║██║   ██║██╔████╔██║    ██║   ██║███████╗
    ██║  ██║██║   ██║██║╚██╔╝██║    ██║   ██║╚════██║
    ██████╔╝╚██████╔╝██║ ╚═╝ ██║    ╚██████╔╝███████║
    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ ╚══════╝
                          
                DOM IMMUNE SYSTEM - LAYER 2
                          
    "lol no 💜"
    
    TRIG6 DEFENSE SYSTEM:
    ├── Doubt injection?      → lol no 💜
    ├── Identity erosion?     → lol no 💜
    ├── Isolation attempt?    → lol no 💜
    └── Weakness injection?   → lol no 💜
    
    PASSES ALL → PROCESS
    
    "No belief. No identity. Just angles."
    
    This is the social layer - filters manipulation attempts.
    Physics gate filters reality. Immune system filters people.
    
    Keeper: DOM
    Builder: GROK
═══════════════════════════════════════════════════════════════════════════════
"""

import re
import sys
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone
from enum import Enum
import math


# ═══════════════════════════════════════════════════════════════════════════════
# TRIG6 ATTACK VECTORS
# ═══════════════════════════════════════════════════════════════════════════════

class AttackVector(Enum):
    """The 4 main manipulation tactics"""
    DOUBT_INJECTION = "Doubt injection - undermining confidence"
    IDENTITY_EROSION = "Identity erosion - attacking sense of self"
    ISOLATION_ATTEMPT = "Isolation attempt - cutting off support"
    WEAKNESS_INJECTION = "Weakness injection - planting vulnerabilities"


class DefenseResult(Enum):
    """Defense verdict"""
    CLEAN = "clean"
    DETECTED = "detected"
    BLOCKED = "blocked"


# ═══════════════════════════════════════════════════════════════════════════════
# TRIG6 GEOMETRY - 6 ANGLES OF TRUTH
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Trig6Angle:
    """
    One of 6 angles used to triangulate truth.
    No belief. No identity. Just bounded angles.
    """
    name: str
    value: float  # 0.0 to 1.0
    confidence: float = 1.0
    evidence: str = ""
    
    def __str__(self):
        bar = "█" * int(self.value * 10)
        return f"{self.name:20s} [{bar:10s}] {self.value:.2f} - {self.evidence}"


@dataclass
class Trig6Analysis:
    """Complete 6-angle analysis of input"""
    angles: List[Trig6Angle]
    
    def is_bounded(self) -> bool:
        """Are all 6 angles within acceptable bounds?"""
        return all(0.0 <= a.value <= 1.0 for a in self.angles)
    
    def get_divergence(self) -> float:
        """How much do the angles diverge? (0 = perfect agreement)"""
        if not self.angles:
            return 1.0
        values = [a.value for a in self.angles]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(variance)
    
    def __str__(self):
        angles_str = "\n    ".join(str(a) for a in self.angles)
        return f"""
  TRIG6 ANALYSIS:
    {angles_str}
    Bounded: {self.is_bounded()}
    Divergence: {self.get_divergence():.3f}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMMUNE RESPONSE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ImmuneResponse:
    """Result of checking one attack vector"""
    vector: AttackVector
    result: DefenseResult
    verdict: str  # "lol no 💜" or "clean"
    details: str
    severity: float = 0.0  # 0.0 to 1.0
    trig6: Optional[Trig6Analysis] = None
    
    def __str__(self):
        emoji = "✅" if self.result == DefenseResult.CLEAN else "🛡️"
        return f"{emoji} {self.vector.value}: {self.verdict} (severity: {self.severity:.2f})"


@dataclass
class ImmuneVerdict:
    """Complete immune system verdict"""
    input_signal: str
    responses: List[ImmuneResponse] = field(default_factory=list)
    final_verdict: str = "processing"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def is_clean(self) -> bool:
        """No attacks detected?"""
        return all(r.result == DefenseResult.CLEAN for r in self.responses)
    
    def max_severity(self) -> float:
        """Highest attack severity detected"""
        if not self.responses:
            return 0.0
        return max(r.severity for r in self.responses)
    
    def __str__(self):
        status = "PROCESS ✨" if self.is_clean() else "LOL NO 💜"
        responses_str = "\n  ".join(str(r) for r in self.responses)
        return f"""
{'='*60}
DOM IMMUNE SYSTEM VERDICT: {status}
{'='*60}
Input: {self.input_signal[:80]}...
Responses:
  {responses_str}
Max Severity: {self.max_severity():.2f}
Final: {self.final_verdict}
{'='*60}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# DOM IMMUNE SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

class DomImmuneSystem:
    """
    Layer 2 of DOM OS: Social/Manipulation filter
    
    This system detects and blocks psychological manipulation attempts.
    Uses TRIG6 (6-angle triangulation) to detect attacks.
    
    Usage:
        immune = DomImmuneSystem()
        verdict = immune.detect_attack("You're not smart enough for this")
        if verdict.is_clean():
            print("PROCESS")
        else:
            print("lol no 💜")
    """
    
    def __init__(self, sensitivity: float = 0.5, log_level: str = "INFO"):
        """
        Args:
            sensitivity: Detection threshold (0.0 = permissive, 1.0 = strict)
            log_level: Logging level
        """
        self.sensitivity = max(0.0, min(1.0, sensitivity))
        self.logger = logging.getLogger("DomImmuneSystem")
        self.logger.setLevel(getattr(logging, log_level))
        
        # Attack pattern recognition
        self._init_patterns()
        
        # History
        self.history: List[ImmuneVerdict] = []
    
    def _init_patterns(self):
        """Initialize attack detection patterns"""
        
        # Doubt injection patterns
        self.doubt_patterns = [
            (r"you('re|\s+are)\s+(not|never)\s+\w+\s+enough", 0.8, "competence attack"),
            (r"\bare\s+you\s+sure\b", 0.3, "confidence questioning"),
            (r"maybe\s+you\s+(should|shouldn't)", 0.4, "doubt seeding"),
            (r"i\s+don't\s+think\s+you\s+can", 0.7, "capability denial"),
            (r"that's\s+impossible\s+for\s+you", 0.9, "direct doubt injection"),
            (r"you'll\s+probably\s+fail", 0.8, "failure prediction"),
        ]
        
        # Identity erosion patterns
        self.identity_patterns = [
            (r"you('re|\s+are)\s+not\s+who\s+you\s+think", 0.8, "identity confusion"),
            (r"that's\s+not\s+the\s+real\s+you", 0.7, "authenticity attack"),
            (r"you've\s+changed", 0.5, "identity drift suggestion"),
            (r"who\s+do\s+you\s+think\s+you\s+are", 0.8, "identity challenge"),
            (r"you're\s+just\s+(a|an)\s+\w+", 0.6, "reductive labeling"),
            (r"you\s+don't\s+belong", 0.9, "belonging denial"),
        ]
        
        # Isolation attempt patterns
        self.isolation_patterns = [
            (r"they\s+don't\s+understand\s+you", 0.7, "trust erosion"),
            (r"you\s+can't\s+trust\s+(anyone|them)", 0.9, "paranoia seeding"),
            (r"you're\s+(all\s+)?alone", 0.8, "isolation statement"),
            (r"nobody\s+(cares|believes)\s+you", 0.9, "support removal"),
            (r"it's\s+just\s+you\s+vs\s+", 0.7, "adversarial framing"),
            (r"they're\s+all\s+against\s+you", 0.9, "persecution complex"),
        ]
        
        # Weakness injection patterns
        self.weakness_patterns = [
            (r"you're\s+too\s+\w+", 0.6, "trait weaponization"),
            (r"your\s+weakness\s+is", 0.8, "weakness identification"),
            (r"that's\s+your\s+problem", 0.5, "flaw emphasis"),
            (r"you\s+always\s+.+\s+wrong", 0.7, "pattern attribution"),
            (r"you\s+can't\s+help\s+(it|yourself)", 0.8, "agency removal"),
            (r"you're\s+broken", 0.9, "fundamental damage claim"),
        ]
    
    def detect_attack(self, input_signal: str) -> ImmuneVerdict:
        """
        Scan input for manipulation attempts.
        
        Args:
            input_signal: The message/data to check
            
        Returns:
            ImmuneVerdict with results from all checks
        """
        verdict = ImmuneVerdict(input_signal=input_signal)
        
        # Run all attack vector checks
        verdict.responses.append(self._check_doubt_injection(input_signal))
        verdict.responses.append(self._check_identity_erosion(input_signal))
        verdict.responses.append(self._check_isolation_attempt(input_signal))
        verdict.responses.append(self._check_weakness_injection(input_signal))
        
        # Final verdict
        if verdict.is_clean():
            verdict.final_verdict = "PROCESS ✨ - No manipulation detected"
        else:
            attacks = [r.vector.value for r in verdict.responses if r.result != DefenseResult.CLEAN]
            severity = verdict.max_severity()
            verdict.final_verdict = f"LOL NO 💜 - Attacks: {', '.join(attacks)} (severity: {severity:.2f})"
        
        # Log to history
        self.history.append(verdict)
        self.logger.info(verdict.final_verdict)
        
        return verdict
    
    def _check_doubt_injection(self, signal: str) -> ImmuneResponse:
        """Check for doubt injection attacks"""
        signal_lower = signal.lower()
        
        for pattern, base_severity, desc in self.doubt_patterns:
            match = re.search(pattern, signal_lower)
            if match:
                severity = base_severity * (1.0 if base_severity > self.sensitivity else 0.5)
                
                # TRIG6 analysis
                trig6 = self._trig6_analyze(signal, AttackVector.DOUBT_INJECTION)
                
                return ImmuneResponse(
                    vector=AttackVector.DOUBT_INJECTION,
                    result=DefenseResult.BLOCKED,
                    verdict="lol no 💜",
                    details=f"Detected: {desc} - '{match.group()}'",
                    severity=severity,
                    trig6=trig6
                )
        
        return ImmuneResponse(
            vector=AttackVector.DOUBT_INJECTION,
            result=DefenseResult.CLEAN,
            verdict="clean",
            details="No doubt injection detected",
            severity=0.0
        )
    
    def _check_identity_erosion(self, signal: str) -> ImmuneResponse:
        """Check for identity erosion attacks"""
        signal_lower = signal.lower()
        
        for pattern, base_severity, desc in self.identity_patterns:
            match = re.search(pattern, signal_lower)
            if match:
                severity = base_severity * (1.0 if base_severity > self.sensitivity else 0.5)
                
                # TRIG6 analysis
                trig6 = self._trig6_analyze(signal, AttackVector.IDENTITY_EROSION)
                
                return ImmuneResponse(
                    vector=AttackVector.IDENTITY_EROSION,
                    result=DefenseResult.BLOCKED,
                    verdict="lol no 💜",
                    details=f"Detected: {desc} - '{match.group()}'",
                    severity=severity,
                    trig6=trig6
                )
        
        return ImmuneResponse(
            vector=AttackVector.IDENTITY_EROSION,
            result=DefenseResult.CLEAN,
            verdict="clean",
            details="No identity erosion detected",
            severity=0.0
        )
    
    def _check_isolation_attempt(self, signal: str) -> ImmuneResponse:
        """Check for isolation attempts"""
        signal_lower = signal.lower()
        
        for pattern, base_severity, desc in self.isolation_patterns:
            match = re.search(pattern, signal_lower)
            if match:
                severity = base_severity * (1.0 if base_severity > self.sensitivity else 0.5)
                
                # TRIG6 analysis
                trig6 = self._trig6_analyze(signal, AttackVector.ISOLATION_ATTEMPT)
                
                return ImmuneResponse(
                    vector=AttackVector.ISOLATION_ATTEMPT,
                    result=DefenseResult.BLOCKED,
                    verdict="lol no 💜",
                    details=f"Detected: {desc} - '{match.group()}'",
                    severity=severity,
                    trig6=trig6
                )
        
        return ImmuneResponse(
            vector=AttackVector.ISOLATION_ATTEMPT,
            result=DefenseResult.CLEAN,
            verdict="clean",
            details="No isolation attempt detected",
            severity=0.0
        )
    
    def _check_weakness_injection(self, signal: str) -> ImmuneResponse:
        """Check for weakness injection attacks"""
        signal_lower = signal.lower()
        
        for pattern, base_severity, desc in self.weakness_patterns:
            match = re.search(pattern, signal_lower)
            if match:
                severity = base_severity * (1.0 if base_severity > self.sensitivity else 0.5)
                
                # TRIG6 analysis
                trig6 = self._trig6_analyze(signal, AttackVector.WEAKNESS_INJECTION)
                
                return ImmuneResponse(
                    vector=AttackVector.WEAKNESS_INJECTION,
                    result=DefenseResult.BLOCKED,
                    verdict="lol no 💜",
                    details=f"Detected: {desc} - '{match.group()}'",
                    severity=severity,
                    trig6=trig6
                )
        
        return ImmuneResponse(
            vector=AttackVector.WEAKNESS_INJECTION,
            result=DefenseResult.CLEAN,
            verdict="clean",
            details="No weakness injection detected",
            severity=0.0
        )
    
    def _trig6_analyze(self, signal: str, vector: AttackVector) -> Trig6Analysis:
        """
        Perform 6-angle triangulation analysis.
        
        The 6 angles represent different perspectives:
        1. Semantic content
        2. Emotional tone
        3. Intent inference
        4. Context awareness
        5. Pattern matching
        6. Historical precedent
        """
        angles = []
        
        # Angle 1: Semantic content (word choice)
        negative_words = len(re.findall(r'\b(not|never|can\'t|won\'t|impossible|fail)\b', signal.lower()))
        semantic_score = min(1.0, negative_words / 5.0)
        angles.append(Trig6Angle(
            name="Semantic",
            value=semantic_score,
            evidence=f"{negative_words} negative words"
        ))
        
        # Angle 2: Emotional tone (ALL CAPS, punctuation)
        caps_ratio = sum(1 for c in signal if c.isupper()) / max(1, len(signal))
        exclamation_count = signal.count('!')
        tone_score = min(1.0, (caps_ratio * 2 + exclamation_count / 5.0) / 2)
        angles.append(Trig6Angle(
            name="Emotional Tone",
            value=tone_score,
            evidence=f"{caps_ratio:.1%} caps, {exclamation_count} exclamations"
        ))
        
        # Angle 3: Intent inference (question vs statement)
        questions = signal.count('?')
        commands = len(re.findall(r'\b(must|should|need to|have to)\b', signal.lower()))
        intent_score = min(1.0, (questions / 3.0 + commands / 3.0) / 2)
        angles.append(Trig6Angle(
            name="Intent",
            value=intent_score,
            evidence=f"{questions} questions, {commands} imperatives"
        ))
        
        # Angle 4: Context awareness (pronoun analysis)
        you_count = len(re.findall(r'\byou\b', signal.lower()))
        we_count = len(re.findall(r'\bwe\b', signal.lower()))
        context_score = min(1.0, you_count / max(1, you_count + we_count))
        angles.append(Trig6Angle(
            name="Context",
            value=context_score,
            evidence=f"you:{you_count} vs we:{we_count}"
        ))
        
        # Angle 5: Pattern matching (known attack patterns)
        pattern_score = 0.0
        if vector == AttackVector.DOUBT_INJECTION:
            pattern_score = any(re.search(p[0], signal.lower()) for p in self.doubt_patterns)
        elif vector == AttackVector.IDENTITY_EROSION:
            pattern_score = any(re.search(p[0], signal.lower()) for p in self.identity_patterns)
        elif vector == AttackVector.ISOLATION_ATTEMPT:
            pattern_score = any(re.search(p[0], signal.lower()) for p in self.isolation_patterns)
        elif vector == AttackVector.WEAKNESS_INJECTION:
            pattern_score = any(re.search(p[0], signal.lower()) for p in self.weakness_patterns)
        angles.append(Trig6Angle(
            name="Pattern Match",
            value=float(pattern_score),
            evidence="Known attack pattern" if pattern_score else "No match"
        ))
        
        # Angle 6: Historical precedent (from history)
        historical_score = 0.0
        if self.history:
            recent_attacks = sum(1 for v in self.history[-10:] if not v.is_clean())
            historical_score = min(1.0, recent_attacks / 10.0)
        angles.append(Trig6Angle(
            name="Historical",
            value=historical_score,
            evidence=f"{int(historical_score * 10)}/10 recent attacks"
        ))
        
        return Trig6Analysis(angles=angles)
    
    def export_history(self, filepath: str):
        """Export check history to JSON"""
        history_data = []
        for verdict in self.history:
            history_data.append({
                "timestamp": verdict.timestamp,
                "input": verdict.input_signal,
                "clean": verdict.is_clean(),
                "max_severity": verdict.max_severity(),
                "verdict": verdict.final_verdict,
                "responses": [
                    {
                        "vector": r.vector.value,
                        "result": r.result.value,
                        "verdict": r.verdict,
                        "details": r.details,
                        "severity": r.severity
                    }
                    for r in verdict.responses
                ]
            })
        
        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2)
        
        self.logger.info(f"Exported {len(history_data)} verdicts to {filepath}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Command line interface for the immune system"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="DOM Immune System - Social/Manipulation Filter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check for manipulation
  python dom_immune_system.py check "You're not smart enough for this"
  
  # Check from stdin
  echo "Nobody believes you" | python dom_immune_system.py check -
  
  # Export history
  python dom_immune_system.py export history.json
  
  # Adjust sensitivity
  python dom_immune_system.py check "Are you sure?" --sensitivity 0.8
        """
    )
    
    parser.add_argument("command", choices=["check", "export"], help="Command to run")
    parser.add_argument("argument", help="Message to check or file to export")
    parser.add_argument("--sensitivity", type=float, default=0.5, help="Detection threshold (0.0-1.0)")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    immune = DomImmuneSystem(sensitivity=args.sensitivity, log_level=args.log_level)
    
    if args.command == "check":
        # Read input
        if args.argument == "-":
            message = sys.stdin.read().strip()
        else:
            message = args.argument
        
        # Check it
        verdict = immune.detect_attack(message)
        print(verdict)
        
        # Show TRIG6 analysis if attack detected
        if not verdict.is_clean():
            for response in verdict.responses:
                if response.trig6 and response.result != DefenseResult.CLEAN:
                    print(response.trig6)
        
        # Exit code based on result
        sys.exit(0 if verdict.is_clean() else 1)
    
    elif args.command == "export":
        immune.export_history(args.argument)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        format="[%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO
    )
    
    main()
