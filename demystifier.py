#!/usr/bin/env python3
"""
DEMYSTIFIER CLI - INV-091
A semantic linter that validates claims against grounding checks.

Usage:
    python demystifier.py "I can manifest abundance"
    python demystifier.py --file claims.txt
    python demystifier.py --interactive

Not hype. Not mythology. Just validation.
"""

import re
import sys
import json
import argparse
from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

IDENTITY_CLAIMS = [
    r"\bi am (a |an |the )?(lightworker|empath|starseed|healer|chosen|awakened)",
    r"\bi('m| am) (spiritually |cosmically )?(connected|aligned|attuned)",
    r"\bmy (soul|spirit|essence|true self)",
    r"\bi have (a |the )?(gift|power|ability to sense)",
]

DESTINY_FRAMES = [
    r"\b(the )?(universe|cosmos|divine|spirit) (wants|needs|tells|guides|chose)",
    r"\b(meant|destined|fated) to (be|happen|occur)",
    r"\beverything happens for a reason",
    r"\bmy (purpose|calling|destiny|path) is",
    r"\bit('s| is| was) (meant|written|ordained)",
]

POWER_CLAIMS = [
    r"\bi can (manifest|channel|transmit|receive|sense|read)",
    r"\bi (have|possess) (the )?(power|ability|gift) (to|of)",
    r"\bmy (energy|vibration|frequency) (is|can|will)",
    r"\bi('m| am) (able to |capable of )?(heal|transform|shift)",
]

UNBOUNDED_NOUNS = [
    r"\b(infinite|unlimited|boundless|eternal|cosmic|universal) \w+",
    r"\ball (things|people|beings|consciousness)",
    r"\beverything (is |and )",
    r"\bthe (universe|multiverse|all|everything)",
]

ABSTRACT_VERBS = [
    r"\b(manifest|channel|transmit|align|attune|vibrate|resonate)",
    r"\b(awaken|ascend|transcend|evolve) (to|into|beyond)",
    r"\b(connect|merge|become one) with",
]

# ═══════════════════════════════════════════════════════════════════════════════
# TRANSLATION TABLE
# ═══════════════════════════════════════════════════════════════════════════════

DEMYSTIFICATION_MAP = {
    # Identity claims
    "i am a lightworker": "I help people (metric: count_helped)",
    "i am an empath": "I notice emotional cues (metric: prediction_accuracy)",
    "i am awakened": "I updated my beliefs (metric: diff(before, after))",
    "i am chosen": "I have a task (metric: deliverable_defined)",
    
    # Destiny frames
    "the universe wants": "I want (owner: self)",
    "meant to be": "It happened (causation: none_claimed)",
    "everything happens for a reason": "Events have causes (type: physical|stochastic)",
    "my purpose is": "My goal is (mutable: true)",
    "my destiny": "My plan (revisable: true)",
    
    # Power claims
    "i can manifest": "I can plan and execute (process: goal→action→outcome)",
    "i channel energy": "I focus attention (metric: hours_focused)",
    "i read auras": "I interpret body language (skill: pattern_recognition)",
    "i have visions": "I generate hypotheses (cognitive: imagination+inference)",
    
    # Unbounded nouns
    "infinite potential": "large but finite capacity (bound: measurable_limit)",
    "universal truth": "widely applicable claim (scope: domain_specific)",
    "everything is connected": "systems have dependencies (model: Graph{nodes,edges})",
    "cosmic consciousness": "shared information (model: network_protocol)",
    
    # Abstract verbs
    "manifest": "plan_and_execute()",
    "channel": "focus_attention()",
    "vibrate": "oscillate_at_frequency(hz: f32)",
    "resonate": "match_frequency(target: f32)",
    "transcend": "exceed_previous_limit(metric: measurable)",
    "align": "coordinate_with(target: defined)",
}

# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

class CheckStatus(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    WARN = "⚠️ WARN"
    UNKNOWN = "❓ UNKNOWN"

@dataclass
class GroundingCheck:
    name: str
    question: str
    status: CheckStatus
    reason: str
    suggestion: Optional[str] = None

@dataclass 
class Detection:
    category: str
    pattern: str
    match: str
    position: Tuple[int, int]

@dataclass
class DemystifyResult:
    input_claim: str
    timestamp: str
    detections: List[Detection]
    translations: List[str]
    grounding_checks: List[GroundingCheck]
    final_status: str
    grounded_version: Optional[str]
    next_steps: List[str]

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def detect_patterns(text: str) -> List[Detection]:
    """Detect mystical patterns in text."""
    detections = []
    text_lower = text.lower()
    
    pattern_sets = [
        ("IDENTITY_CLAIM", IDENTITY_CLAIMS),
        ("DESTINY_FRAME", DESTINY_FRAMES),
        ("POWER_CLAIM", POWER_CLAIMS),
        ("UNBOUNDED_NOUN", UNBOUNDED_NOUNS),
        ("ABSTRACT_VERB", ABSTRACT_VERBS),
    ]
    
    for category, patterns in pattern_sets:
        for pattern in patterns:
            for match in re.finditer(pattern, text_lower):
                detections.append(Detection(
                    category=category,
                    pattern=pattern,
                    match=match.group(),
                    position=(match.start(), match.end())
                ))
    
    return detections

def translate_claim(text: str) -> List[str]:
    """Translate mystical phrases to grounded equivalents."""
    translations = []
    text_lower = text.lower()
    
    for mystical, grounded in DEMYSTIFICATION_MAP.items():
        if mystical in text_lower:
            translations.append(f'"{mystical}" → {grounded}')
    
    return translations

# ═══════════════════════════════════════════════════════════════════════════════
# GROUNDING CHECKS
# ═══════════════════════════════════════════════════════════════════════════════

def check_measurable(text: str, detections: List[Detection]) -> GroundingCheck:
    """Can you assign a number to it?"""
    # Look for quantifiable elements
    has_numbers = bool(re.search(r'\d+', text))
    has_metrics = bool(re.search(r'\b(count|measure|percent|rate|score|level|amount|hours|days)\b', text.lower()))
    has_unbounded = any(d.category == "UNBOUNDED_NOUN" for d in detections)
    
    if has_numbers or has_metrics:
        return GroundingCheck(
            name="MEASURABLE",
            question="Can you assign a number to it?",
            status=CheckStatus.PASS,
            reason="Contains quantifiable elements"
        )
    elif has_unbounded:
        return GroundingCheck(
            name="MEASURABLE",
            question="Can you assign a number to it?",
            status=CheckStatus.FAIL,
            reason="Contains unbounded/infinite claims",
            suggestion="Replace with specific, finite quantities"
        )
    else:
        return GroundingCheck(
            name="MEASURABLE",
            question="Can you assign a number to it?",
            status=CheckStatus.WARN,
            reason="No explicit metrics found",
            suggestion="Add: count, duration, frequency, or other metric"
        )

def check_falsifiable(text: str, detections: List[Detection]) -> GroundingCheck:
    """What would prove it wrong?"""
    # Unfalsifiable patterns
    universal_claims = bool(re.search(r'\b(always|never|all|everything|nothing)\b', text.lower()))
    has_destiny = any(d.category == "DESTINY_FRAME" for d in detections)
    has_conditional = bool(re.search(r'\b(if|when|unless|until|provided)\b', text.lower()))
    
    if has_destiny or universal_claims:
        return GroundingCheck(
            name="FALSIFIABLE",
            question="What would prove it wrong?",
            status=CheckStatus.FAIL,
            reason="Contains unfalsifiable destiny/universal claims",
            suggestion="Specify conditions under which this would be false"
        )
    elif has_conditional:
        return GroundingCheck(
            name="FALSIFIABLE",
            question="What would prove it wrong?",
            status=CheckStatus.PASS,
            reason="Contains conditional/testable structure"
        )
    else:
        return GroundingCheck(
            name="FALSIFIABLE",
            question="What would prove it wrong?",
            status=CheckStatus.WARN,
            reason="No explicit test conditions",
            suggestion="Add: 'This fails if...'"
        )

def check_bounded(text: str, detections: List[Detection]) -> GroundingCheck:
    """Where does it start and end?"""
    has_unbounded = any(d.category == "UNBOUNDED_NOUN" for d in detections)
    has_scope = bool(re.search(r'\b(within|between|from|to|until|during|for \d+)\b', text.lower()))
    has_limits = bool(re.search(r'\b(limit|max|min|cap|ceiling|floor|boundary)\b', text.lower()))
    
    if has_unbounded:
        return GroundingCheck(
            name="BOUNDED",
            question="Where does it start and end?",
            status=CheckStatus.FAIL,
            reason="Contains unbounded/infinite scope",
            suggestion="Define explicit boundaries: start, end, limits"
        )
    elif has_scope or has_limits:
        return GroundingCheck(
            name="BOUNDED",
            question="Where does it start and end?",
            status=CheckStatus.PASS,
            reason="Contains scope/boundary markers"
        )
    else:
        return GroundingCheck(
            name="BOUNDED",
            question="Where does it start and end?",
            status=CheckStatus.WARN,
            reason="No explicit boundaries",
            suggestion="Add: scope, duration, or domain limits"
        )

def check_observable(text: str, detections: List[Detection]) -> GroundingCheck:
    """Can someone else verify it?"""
    has_internal = bool(re.search(r'\bi (feel|sense|know|believe|think)\b', text.lower()))
    has_identity = any(d.category == "IDENTITY_CLAIM" for d in detections)
    has_external = bool(re.search(r'\b(shows|demonstrates|produces|results in|outputs)\b', text.lower()))
    
    if has_external:
        return GroundingCheck(
            name="OBSERVABLE",
            question="Can someone else verify it?",
            status=CheckStatus.PASS,
            reason="References external/observable outcomes"
        )
    elif has_internal or has_identity:
        return GroundingCheck(
            name="OBSERVABLE",
            question="Can someone else verify it?",
            status=CheckStatus.FAIL,
            reason="Based on internal/subjective state only",
            suggestion="Add observable behavior or output"
        )
    else:
        return GroundingCheck(
            name="OBSERVABLE",
            question="Can someone else verify it?",
            status=CheckStatus.WARN,
            reason="Observability unclear",
            suggestion="Specify what external evidence would look like"
        )

def check_actionable(text: str, detections: List[Detection]) -> GroundingCheck:
    """What do you DO with this?"""
    has_abstract_verb = any(d.category == "ABSTRACT_VERB" for d in detections)
    has_action = bool(re.search(r'\b(do|make|create|build|write|run|execute|implement|deploy)\b', text.lower()))
    has_imperative = bool(re.search(r'^(do|make|create|run|build|write)', text.lower().strip()))
    
    if has_action or has_imperative:
        return GroundingCheck(
            name="ACTIONABLE",
            question="What do you DO with this?",
            status=CheckStatus.PASS,
            reason="Contains concrete action verbs"
        )
    elif has_abstract_verb:
        return GroundingCheck(
            name="ACTIONABLE",
            question="What do you DO with this?",
            status=CheckStatus.FAIL,
            reason="Uses abstract/non-operational verbs",
            suggestion="Replace with concrete verbs: do, make, create, build"
        )
    else:
        return GroundingCheck(
            name="ACTIONABLE",
            question="What do you DO with this?",
            status=CheckStatus.WARN,
            reason="Action unclear",
            suggestion="Specify the concrete next step"
        )

def check_ownable(text: str, detections: List[Detection]) -> GroundingCheck:
    """Who is responsible?"""
    has_destiny = any(d.category == "DESTINY_FRAME" for d in detections)
    has_external_agent = bool(re.search(r'\b(universe|cosmos|divine|spirit|fate|destiny) (wants|needs|decided|chose)\b', text.lower()))
    has_owner = bool(re.search(r'\b(i will|i am|i can|my|we will|our|team|assigned to)\b', text.lower()))
    
    if has_external_agent or has_destiny:
        return GroundingCheck(
            name="OWNABLE",
            question="Who is responsible?",
            status=CheckStatus.FAIL,
            reason="Responsibility attributed to external/mystical agent",
            suggestion="Replace with human owner: 'I will' or 'Team X owns'"
        )
    elif has_owner:
        return GroundingCheck(
            name="OWNABLE",
            question="Who is responsible?",
            status=CheckStatus.PASS,
            reason="Has explicit human owner"
        )
    else:
        return GroundingCheck(
            name="OWNABLE",
            question="Who is responsible?",
            status=CheckStatus.WARN,
            reason="Owner not specified",
            suggestion="Add: owner, assignee, or responsible party"
        )

def run_grounding_checks(text: str, detections: List[Detection]) -> List[GroundingCheck]:
    """Run all six grounding checks."""
    return [
        check_measurable(text, detections),
        check_falsifiable(text, detections),
        check_bounded(text, detections),
        check_observable(text, detections),
        check_actionable(text, detections),
        check_ownable(text, detections),
    ]

# ═══════════════════════════════════════════════════════════════════════════════
# DEMYSTIFIER ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def demystify(claim: str) -> DemystifyResult:
    """Run the full demystification pipeline."""
    
    # Step 1: Detect patterns
    detections = detect_patterns(claim)
    
    # Step 2: Translate
    translations = translate_claim(claim)
    
    # Step 3: Run grounding checks
    checks = run_grounding_checks(claim, detections)
    
    # Step 4: Determine final status
    fail_count = sum(1 for c in checks if c.status == CheckStatus.FAIL)
    warn_count = sum(1 for c in checks if c.status == CheckStatus.WARN)
    pass_count = sum(1 for c in checks if c.status == CheckStatus.PASS)
    
    if fail_count > 0:
        final_status = "❌ REJECTED - Failed grounding checks"
    elif warn_count >= 3:
        final_status = "⚠️ NEEDS WORK - Multiple warnings"
    elif pass_count == 6:
        final_status = "✅ GROUNDED - All checks passed"
    else:
        final_status = "⚠️ PARTIAL - Some checks inconclusive"
    
    # Step 5: Generate grounded version
    grounded_version = None
    if translations:
        # Use the first translation as base
        grounded_version = translations[0].split(" → ")[1] if " → " in translations[0] else None
    
    # Step 6: Generate next steps
    next_steps = []
    for check in checks:
        if check.suggestion:
            next_steps.append(f"[{check.name}] {check.suggestion}")
    
    return DemystifyResult(
        input_claim=claim,
        timestamp=datetime.now().isoformat(),
        detections=detections,
        translations=translations,
        grounding_checks=checks,
        final_status=final_status,
        grounded_version=grounded_version,
        next_steps=next_steps
    )

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTERS
# ═══════════════════════════════════════════════════════════════════════════════

def format_result_text(result: DemystifyResult) -> str:
    """Format result as human-readable text."""
    lines = [
        "═" * 70,
        "🔥 DEMYSTIFIER REPORT - INV-091",
        "═" * 70,
        f"INPUT: \"{result.input_claim}\"",
        f"TIME:  {result.timestamp}",
        "",
    ]
    
    # Detections
    if result.detections:
        lines.append("📍 DETECTIONS:")
        for d in result.detections:
            lines.append(f"   [{d.category}] \"{d.match}\"")
        lines.append("")
    
    # Translations
    if result.translations:
        lines.append("🔄 TRANSLATIONS:")
        for t in result.translations:
            lines.append(f"   {t}")
        lines.append("")
    
    # Grounding checks
    lines.append("✓ GROUNDING CHECKS:")
    for check in result.grounding_checks:
        lines.append(f"   {check.status.value} {check.name}")
        lines.append(f"      └─ {check.reason}")
    lines.append("")
    
    # Final status
    lines.append("─" * 70)
    lines.append(f"VERDICT: {result.final_status}")
    lines.append("─" * 70)
    
    # Grounded version
    if result.grounded_version:
        lines.append(f"GROUNDED VERSION: {result.grounded_version}")
        lines.append("")
    
    # Next steps
    if result.next_steps:
        lines.append("📋 NEXT STEPS:")
        for step in result.next_steps:
            lines.append(f"   → {step}")
    
    lines.append("═" * 70)
    return "\n".join(lines)

def format_result_json(result: DemystifyResult) -> str:
    """Format result as JSON."""
    data = {
        "input_claim": result.input_claim,
        "timestamp": result.timestamp,
        "detections": [
            {"category": d.category, "match": d.match, "position": d.position}
            for d in result.detections
        ],
        "translations": result.translations,
        "grounding_checks": [
            {
                "name": c.name,
                "status": c.status.name,
                "reason": c.reason,
                "suggestion": c.suggestion
            }
            for c in result.grounding_checks
        ],
        "final_status": result.final_status,
        "grounded_version": result.grounded_version,
        "next_steps": result.next_steps
    }
    return json.dumps(data, indent=2)

# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="DEMYSTIFIER - Validate claims against grounding checks",
        epilog="Not hype. Not mythology. Just validation."
    )
    parser.add_argument("claim", nargs="?", help="Claim to demystify")
    parser.add_argument("-f", "--file", help="File containing claims (one per line)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only show verdict")
    
    args = parser.parse_args()
    
    claims = []
    
    if args.interactive:
        print("🔥 DEMYSTIFIER INTERACTIVE MODE")
        print("Type claims to analyze. Type 'quit' to exit.\n")
        while True:
            try:
                claim = input("CLAIM> ").strip()
                if claim.lower() in ('quit', 'exit', 'q'):
                    break
                if claim:
                    claims.append(claim)
                    result = demystify(claim)
                    if args.json:
                        print(format_result_json(result))
                    elif args.quiet:
                        print(result.final_status)
                    else:
                        print(format_result_text(result))
                    print()
            except (KeyboardInterrupt, EOFError):
                break
        return
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                claims = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied reading '{args.file}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    elif args.claim:
        claims = [args.claim]
    else:
        # Demo mode
        claims = [
            "I am a lightworker channeling universal energy",
            "I can manifest abundance through high vibration",
            "The universe wants me to succeed",
            "I will build a CLI tool that validates claims within 2 hours",
        ]
        print("🔥 DEMYSTIFIER DEMO MODE\n")
    
    for claim in claims:
        result = demystify(claim)
        if args.json:
            print(format_result_json(result))
        elif args.quiet:
            print(f"{claim[:50]}... → {result.final_status}")
        else:
            print(format_result_text(result))
        print()

if __name__ == "__main__":
    main()
