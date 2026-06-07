"""
BOARD-38 — Pattern-of-Life Decoder
tic_signature.py — Builds a unique "tic signature" for the organism.
"""

from __future__ import annotations

import uuid
from collections import Counter
from dataclasses import dataclass, field
from typing import List

from rhythm_parser import RhythmPattern


@dataclass
class TicSignature:
    sig_id: str
    signals: list[str]          # repeated phrases, transitions, cadences
    cadence_mode: str
    dominant_pos: str            # most common token type (POS proxy)
    dominant_board: str          # cadence_mode-derived board label
    loop_ratio: float            # loops / total tokens
    invention_probability: float # 0.0–1.0


# ── Private helpers ───────────────────────────────────────────────────────────

_MODE_TO_BOARD = {
    "rapid_associative": "BOARD-38",
    "deep_focus":        "BOARD-36",
    "exploratory":       "BOARD-37",
    "inventive":         "BOARD-38",
}


def _extract_signals(patterns: list[RhythmPattern]) -> list[str]:
    """Pull the top repeated phrases/values across all patterns."""
    freq: Counter[str] = Counter()
    for p in patterns:
        for tok in p.tokens:
            if tok.token_type in ("PHRASE", "LOOP", "SPIKE"):
                freq[tok.value] += tok.frequency
    # Return top-10 signals
    return [val for val, _ in freq.most_common(10)]


def _dominant_pos(patterns: list[RhythmPattern]) -> str:
    """Return the most frequently occurring token_type across all patterns."""
    type_counts: Counter[str] = Counter()
    for p in patterns:
        for tok in p.tokens:
            type_counts[tok.token_type] += 1
    if not type_counts:
        return "SYMBOL"
    return type_counts.most_common(1)[0][0]


def _loop_ratio(patterns: list[RhythmPattern]) -> float:
    total_tokens = sum(len(p.tokens) for p in patterns)
    if total_tokens == 0:
        return 0.0
    loop_tokens = sum(
        sum(1 for t in p.tokens if t.token_type in ("LOOP", "TIC"))
        for p in patterns
    )
    return round(loop_tokens / total_tokens, 4)


def _invention_probability(
    patterns: list[RhythmPattern],
    loop_ratio: float,
    cadence_mode: str,
) -> float:
    """
    Heuristic invention probability:
      - inventive mode gives base 0.75
      - rapid_associative: 0.60
      - deep_focus: 0.50
      - exploratory: 0.40
      - boosted by loop_ratio (high loops = established patterns to invert)
      - boosted by number of patterns found
    """
    base = {
        "inventive":          0.75,
        "rapid_associative":  0.60,
        "deep_focus":         0.50,
        "exploratory":        0.40,
    }.get(cadence_mode, 0.40)

    loop_boost    = loop_ratio * 0.15
    pattern_boost = min(len(patterns) * 0.02, 0.10)
    prob = base + loop_boost + pattern_boost
    return round(min(prob, 1.0), 4)


def _dominant_cadence_mode(patterns: list[RhythmPattern]) -> str:
    if not patterns:
        return "exploratory"
    mode_counter: Counter[str] = Counter(p.cadence_mode for p in patterns)
    return mode_counter.most_common(1)[0][0]


# ── Public API ────────────────────────────────────────────────────────────────

def build_signature(patterns: list[RhythmPattern]) -> TicSignature:
    """
    Build a TicSignature from a list of RhythmPatterns.

    Args:
        patterns: output of rhythm_parser.parse_cadence().
    Returns:
        A fully populated TicSignature.
    """
    cadence_mode = _dominant_cadence_mode(patterns)
    signals      = _extract_signals(patterns)
    dominant_pos = _dominant_pos(patterns)
    lr           = _loop_ratio(patterns)
    inv_prob     = _invention_probability(patterns, lr, cadence_mode)
    board        = _MODE_TO_BOARD.get(cadence_mode, "BOARD-38")

    return TicSignature(
        sig_id=f"SIG-{uuid.uuid4().hex[:8].upper()}",
        signals=signals,
        cadence_mode=cadence_mode,
        dominant_pos=dominant_pos,
        dominant_board=board,
        loop_ratio=lr,
        invention_probability=inv_prob,
    )
