"""
BOARD-38 — Pattern-of-Life Decoder
rhythm_parser.py — Parses cadence tokens into rhythm patterns.
"""

from __future__ import annotations

import uuid
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Tuple

from cadence_lexer import CadenceToken


@dataclass
class RhythmPattern:
    pattern_id: str
    tokens: list[CadenceToken]
    cadence_mode: str   # "rapid_associative", "deep_focus", "exploratory", "inventive"
    dominant_symbol: str
    loop_count: int

    def __repr__(self) -> str:
        return (
            f"RhythmPattern(id={self.pattern_id}, mode={self.cadence_mode}, "
            f"dominant={self.dominant_symbol!r}, loops={self.loop_count}, "
            f"tokens={len(self.tokens)})"
        )


# ── Private helpers ───────────────────────────────────────────────────────────

def _dominant_symbol(tokens: list[CadenceToken]) -> str:
    if not tokens:
        return ""
    freq_map: Counter[str] = Counter()
    for t in tokens:
        freq_map[t.value] += t.frequency
    return freq_map.most_common(1)[0][0]


def _infer_cadence_mode(tokens: list[CadenceToken], loop_count: int) -> str:
    """
    Heuristic cadence-mode classifier based on token mix.

    rapid_associative  — many TRANSITIONs + TICs; short bursts
    deep_focus         — high LOOP + PHRASE ratio; sustained repeats
    exploratory        — many SYMBOLs; wide vocabulary
    inventive          — SPIKEs + PHRASEs; novel high-energy patterns
    """
    if not tokens:
        return "exploratory"

    type_counts: Counter[str] = Counter(t.token_type for t in tokens)
    total = len(tokens)

    spike_ratio      = type_counts.get("SPIKE", 0) / total
    loop_ratio       = type_counts.get("LOOP", 0) / total
    transition_ratio = type_counts.get("TRANSITION", 0) / total
    tic_ratio        = type_counts.get("TIC", 0) / total
    phrase_ratio     = type_counts.get("PHRASE", 0) / total
    symbol_ratio     = type_counts.get("SYMBOL", 0) / total

    if spike_ratio + phrase_ratio > 0.30:
        return "inventive"
    if transition_ratio + tic_ratio > 0.25:
        return "rapid_associative"
    if loop_ratio > 0.20 or loop_count > 5:
        return "deep_focus"
    return "exploratory"


# ── Public API ────────────────────────────────────────────────────────────────

def detect_loops(tokens: list[CadenceToken]) -> list[tuple]:
    """
    Find tokens that repeat more than 3 times in the stream.

    Returns:
        list of (token_value, count) tuples sorted descending by count.
    """
    freq: Counter[str] = Counter()
    for t in tokens:
        freq[t.value] += 1

    return sorted(
        [(val, cnt) for val, cnt in freq.items() if cnt > 3],
        key=lambda x: x[1],
        reverse=True,
    )


def detect_transitions(tokens: list[CadenceToken]) -> list[tuple]:
    """
    Find phase-change points — places where the dominant value shifts
    after a sustained run (≥3 identical tokens).

    Returns:
        list of (position, from_value, to_value) tuples.
    """
    if len(tokens) < 2:
        return []

    transitions: list[tuple] = []
    run_val = tokens[0].value
    run_len = 1

    for i in range(1, len(tokens)):
        if tokens[i].value == run_val:
            run_len += 1
        else:
            if run_len >= 3:
                transitions.append((i, run_val, tokens[i].value))
            run_val = tokens[i].value
            run_len = 1

    return transitions


def parse_cadence(tokens: list[CadenceToken]) -> list[RhythmPattern]:
    """
    Parse a flat list of CadenceTokens into a list of RhythmPatterns.

    Strategy: split on TRANSITION tokens, treating each segment as one
    candidate pattern.  If no transitions exist, the whole stream is one
    pattern.  Each segment must have at least 2 tokens.

    Args:
        tokens: output of any cadence_lexer.lex_* function.
    Returns:
        list of RhythmPattern objects (may be empty if tokens is empty).
    """
    if not tokens:
        return []

    # Split stream on TRANSITION markers
    segments: list[list[CadenceToken]] = []
    current: list[CadenceToken] = []

    for tok in tokens:
        if tok.token_type == "TRANSITION":
            if len(current) >= 2:
                segments.append(current)
            current = []
        else:
            current.append(tok)

    if len(current) >= 2:
        segments.append(current)

    # If nothing was split, treat whole stream as one segment
    if not segments:
        segments = [tokens]

    patterns: list[RhythmPattern] = []
    for seg in segments:
        loops = detect_loops(seg)
        loop_count = len(loops)
        dominant = _dominant_symbol(seg)
        mode = _infer_cadence_mode(seg, loop_count)

        patterns.append(RhythmPattern(
            pattern_id=f"RP-{uuid.uuid4().hex[:8].upper()}",
            tokens=seg,
            cadence_mode=mode,
            dominant_symbol=dominant,
            loop_count=loop_count,
        ))

    return patterns
