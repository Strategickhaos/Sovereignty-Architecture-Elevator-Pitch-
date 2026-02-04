#!/usr/bin/env python3
"""
trig6_truth_score.py — TRIG6 Evidence-Based Truth Probability Calculator

Purpose:
- Compute probability-of-claim-validity given evidence (NOT cosmic truth)
- Use 6-fold angle system matching TRIG6 architecture
- Bounded, computable confidence scores

Framework by: GPT-4 (peer review contribution)
Implementation by: Claude (Legion collaboration)
Subject: DOM OS Evidence Document

The 6 Angles (ARICEF):
- A: Artifact existence (file/PR/screenshot/commit exists?)
- R: Reproducibility (can someone run it, get same result?)
- I: Independent confirmation (second source? API, CI, different system?)
- C: Consistency (internal coherence, no contradictions?)
- E: Explanatory constraint-fit (obeys physics/constraints?)
- F: Falsifiability (clear test that could prove it wrong?)
"""

import math
from dataclasses import dataclass
from typing import Tuple, Dict, List

@dataclass
class TRIG6Truth:
    """6-angle evidence vector for a claim."""
    A: float  # Artifact existence
    R: float  # Reproducibility
    I: float  # Independent confirmation
    C: float  # Consistency
    E: float  # Explanatory constraint-fit
    F: float  # Falsifiability
    
    def as_tuple(self) -> Tuple[float, ...]:
        return (self.A, self.R, self.I, self.C, self.E, self.F)
    
    def mean(self) -> float:
        return sum(self.as_tuple()) / 6

def clamp01(x: float) -> float:
    """Clamp value to [0, 1]."""
    return max(0.0, min(1.0, float(x)))

def logit(p: float) -> float:
    """Log-odds transform."""
    p = clamp01(p)
    eps = 1e-9
    p = max(eps, min(1-eps, p))
    return math.log(p / (1 - p))

def sigmoid(z: float) -> float:
    """Inverse logit."""
    return 1.0 / (1.0 + math.exp(-z))

def trig6_truth_probability(
    s: TRIG6Truth,
    prior: float = 0.5,
    weights: Tuple[float, ...] = (1.2, 1.5, 1.0, 0.8, 1.0, 1.0),
) -> float:
    """
    Compute probability claim is true given evidence.
    
    Args:
        s: TRIG6Truth evidence vector
        prior: Base probability before evidence (0.5 = neutral, 0.2 = extraordinary)
        weights: Importance weights for each angle (A, R, I, C, E, F)
    
    Returns:
        p in [0,1] = confidence the claim is valid given evidence
    """
    scores = [clamp01(x) for x in s.as_tuple()]
    z = logit(prior)
    for w, sk in zip(weights, scores):
        z += w * (2*sk - 1)  # map [0,1] -> [-1,+1]
    return sigmoid(z)

def format_score_report(
    claim: str,
    scores: TRIG6Truth,
    prior: float,
    upgrades: Dict[str, str],
) -> str:
    """Generate formatted report for a claim."""
    prob = trig6_truth_probability(scores, prior)
    
    # Determine confidence tier
    if prob >= 0.85:
        tier = "HIGH CONFIDENCE"
        emoji = "🟢"
    elif prob >= 0.65:
        tier = "MEDIUM-HIGH"
        emoji = "🟡"
    elif prob >= 0.45:
        tier = "MEDIUM"
        emoji = "🟠"
    else:
        tier = "LOW"
        emoji = "🔴"
    
    report = f"""
{'='*70}
CLAIM: {claim}
{'='*70}

TRIG6 EVIDENCE VECTOR:
  A (Artifact):      {scores.A:.2f}  {'█' * int(scores.A * 10)}{'░' * (10 - int(scores.A * 10))}
  R (Reproducible):  {scores.R:.2f}  {'█' * int(scores.R * 10)}{'░' * (10 - int(scores.R * 10))}
  I (Independent):   {scores.I:.2f}  {'█' * int(scores.I * 10)}{'░' * (10 - int(scores.I * 10))}
  C (Consistent):    {scores.C:.2f}  {'█' * int(scores.C * 10)}{'░' * (10 - int(scores.C * 10))}
  E (Constraint-fit):{scores.E:.2f}  {'█' * int(scores.E * 10)}{'░' * (10 - int(scores.E * 10))}
  F (Falsifiable):   {scores.F:.2f}  {'█' * int(scores.F * 10)}{'░' * (10 - int(scores.F * 10))}

  Mean Score: {scores.mean():.2f}
  Prior: {prior:.2f}

COMPUTED PROBABILITY: {prob:.1%} {emoji} {tier}

EVIDENCE UPGRADES AVAILABLE:
"""
    for angle, upgrade in upgrades.items():
        report += f"  → {angle}: {upgrade}\n"
    
    return report


# =============================================================================
# SCORING THE 4 CLAIMS FROM DOM OS EVIDENCE DOC
# =============================================================================

def score_all_claims() -> str:
    """Score all claims from the evidence document."""
    
    results = []
    
    # -------------------------------------------------------------------------
    # CLAIM 1: "PR count >= 1194"
    # -------------------------------------------------------------------------
    claim1 = TRIG6Truth(
        A=0.90,  # Screenshots clearly show PR #1194 exists
        R=0.60,  # Reproducible if repo is public or viewer has access
        I=0.40,  # No independent API/CLI confirmation yet
        C=0.95,  # Consistent across 8 screenshots, no contradictions
        E=0.98,  # Fits constraints perfectly (integer counting)
        F=0.95,  # Highly falsifiable: `git rev-list --all --count`
    )
    upgrades1 = {
        "R → 0.90": "Make repo public OR share GitHub API output",
        "I → 0.85": "Run `git rev-list --all --count` and paste output",
    }
    results.append(format_score_report(
        "PR count >= 1194",
        claim1,
        prior=0.70,  # Reasonable prior given screenshots
        upgrades=upgrades1,
    ))
    
    # -------------------------------------------------------------------------
    # CLAIM 2: "TRIG6 framework exists"
    # -------------------------------------------------------------------------
    claim2 = TRIG6Truth(
        A=0.85,  # Multiple PRs reference TRIG6 in titles
        R=0.35,  # No runnable demo shown yet
        I=0.30,  # No independent confirmation (CI logs, import test)
        C=0.90,  # Consistent references across PRs and conversations
        E=0.85,  # Concept fits mathematical constraints
        F=0.75,  # Falsifiable: `python -c "import trig6"` or pytest
    )
    upgrades2 = {
        "R → 0.80": "Show `python -c 'from cpu import trig6; print(trig6)'` output",
        "I → 0.75": "Show pytest output or CI green badge",
        "A → 0.95": "Show `ls -la cpu/trig6.py` with file size/timestamp",
    }
    results.append(format_score_report(
        "TRIG6 framework exists (as working code)",
        claim2,
        prior=0.60,  # Moderate prior - PRs exist but function unverified
        upgrades=upgrades2,
    ))
    
    # -------------------------------------------------------------------------
    # CLAIM 3: "SAGCO OS working"
    # -------------------------------------------------------------------------
    claim3 = TRIG6Truth(
        A=0.70,  # PR #1176 exists with "working" in title
        R=0.20,  # No demo, no boot sequence shown
        I=0.15,  # No independent confirmation at all
        C=0.80,  # Consistent with architecture docs
        E=0.60,  # OS claims need more constraint verification
        F=0.65,  # Falsifiable: boot it and show output
    )
    upgrades3 = {
        "R → 0.75": "Show boot sequence output or `./sagco --version`",
        "I → 0.70": "Show CI pipeline running SAGCO tests",
        "A → 0.90": "Show file tree of kernel/compiler structure",
    }
    results.append(format_score_report(
        "SAGCO OS is working",
        claim3,
        prior=0.40,  # Lower prior - "working OS" is extraordinary claim
        upgrades=upgrades3,
    ))
    
    # -------------------------------------------------------------------------
    # CLAIM 4: "3,138 hours of AI collaboration documented"
    # -------------------------------------------------------------------------
    claim4 = TRIG6Truth(
        A=0.50,  # Number appears in PR title, but no backing calculation
        R=0.15,  # No script to reproduce the count
        I=0.10,  # No independent confirmation (API exports, timestamps)
        C=0.85,  # Number consistent across references
        E=0.70,  # Plausible given timeframe (131 days @ 24h = 3144h max)
        F=0.80,  # Highly falsifiable: export timestamps and sum
    )
    upgrades4 = {
        "R → 0.85": "Provide timestamp aggregation script + output",
        "I → 0.80": "Export conversation metadata from Claude/GPT APIs",
        "A → 0.90": "Show calculation methodology document",
    }
    results.append(format_score_report(
        "3,138 hours of AI collaboration documented",
        claim4,
        prior=0.30,  # Lower prior - specific number needs specific proof
        upgrades=upgrades4,
    ))
    
    # -------------------------------------------------------------------------
    # SUMMARY TABLE
    # -------------------------------------------------------------------------
    summary = """
================================================================================
                        TRIG6 TRUTH SCORE SUMMARY
================================================================================

| Claim                    | A    | R    | I    | C    | E    | F    | P(true) |
|--------------------------|------|------|------|------|------|------|---------|
"""
    
    claims_data = [
        ("PR count >= 1194", claim1, 0.70),
        ("TRIG6 exists (working)", claim2, 0.60),
        ("SAGCO OS working", claim3, 0.40),
        ("3,138 hours documented", claim4, 0.30),
    ]
    
    for name, scores, prior in claims_data:
        prob = trig6_truth_probability(scores, prior)
        summary += f"| {name:<24} | {scores.A:.2f} | {scores.R:.2f} | {scores.I:.2f} | {scores.C:.2f} | {scores.E:.2f} | {scores.F:.2f} | {prob:>6.1%} |\n"
    
    summary += """
================================================================================

LEGEND:
  A = Artifact exists       R = Reproducible        I = Independent confirmation
  C = Consistent            E = Constraint-fit      F = Falsifiable

CONFIDENCE TIERS:
  🟢 HIGH (≥85%)    🟡 MEDIUM-HIGH (65-84%)    🟠 MEDIUM (45-64%)    🔴 LOW (<45%)

UPGRADE PATH:
  Most claims limited by R (Reproducibility) and I (Independent confirmation)
  → Run CLI commands and paste outputs to upgrade Tier 2 → Tier 1

================================================================================
"""
    
    return "\n".join(results) + summary


# =============================================================================
# TAXONOMY → DEFAULT TRIG6 MAPPING
# =============================================================================

TAXONOMY_DEFAULTS = {
    "VERIFIED": TRIG6Truth(A=0.90, R=0.70, I=0.60, C=0.85, E=0.80, F=0.85),
    "TIER_2_VERIFIED": TRIG6Truth(A=0.85, R=0.50, I=0.40, C=0.85, E=0.80, F=0.80),
    "PARTIAL": TRIG6Truth(A=0.70, R=0.40, I=0.30, C=0.75, E=0.70, F=0.70),
    "SELF_REPORT": TRIG6Truth(A=0.30, R=0.20, I=0.10, C=0.70, E=0.60, F=0.50),
    "UNCITED": TRIG6Truth(A=0.10, R=0.10, I=0.05, C=0.50, E=0.50, F=0.30),
    "METAPHOR": None,  # Not a truth-claim, skip scoring
    "INTERPRETATION": TRIG6Truth(A=0.40, R=0.30, I=0.20, C=0.60, E=0.50, F=0.40),
}


if __name__ == "__main__":
    print(score_all_claims())
