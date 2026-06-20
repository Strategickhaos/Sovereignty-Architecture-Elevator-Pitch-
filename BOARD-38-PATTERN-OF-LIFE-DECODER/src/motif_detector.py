"""
BOARD-38 — Pattern-of-Life Decoder
motif_detector.py — Detects recurring motifs across all input streams.
"""

from __future__ import annotations

from typing import List

from tic_signature import TicSignature


# ── Motif keyword registry ────────────────────────────────────────────────────

KNOWN_MOTIFS: dict[str, list[str]] = {
    "rapid_associative_engineering": [
        "compile", "build", "deploy", "iterate", "scaffold",
        "rapid", "quick", "fast", "automate", "pipeline",
        "engineer", "engineering", "architecture", "system", "module",
    ],
    "contradiction_to_board": [
        "contradiction", "board", "proof", "variance", "mismatch",
        "expected", "actual", "delta", "eru", "antibody",
        "dispute", "resolve", "claim", "verify",
    ],
    "screenshot_to_command": [
        "screenshot", "command", "antibody", "ocr", "capture",
        "parse", "extract", "image", "pixel", "click",
        "automate", "macro", "trigger",
    ],
    "mobius_problem_to_proof": [
        "mobius", "proof", "problem", "solve", "answer",
        "grade", "autograde", "homework", "formula", "derivative",
        "integral", "calculus", "verify", "check",
    ],
    "baby_lookii": [
        "baby lookii", "eureka", "breakthrough", "discovery",
        "lookii", "found it", "i see", "aha", "pattern",
        "connection", "link", "bridge", "novel",
    ],
}


# ── Public API ────────────────────────────────────────────────────────────────

def detect_motifs(signature: TicSignature) -> list[str]:
    """
    Detect which known motifs are present in the TicSignature's signals.

    Strategy: lower-case signal values are matched against each motif's
    keyword list.  A motif fires if ≥2 keywords match OR if one keyword
    matches with strength ≥ 0.5.

    Args:
        signature: TicSignature built by tic_signature.build_signature().
    Returns:
        list of motif names that fired.
    """
    signal_text = " ".join(signature.signals).lower()
    fired: list[str] = []

    for motif_name, keywords in KNOWN_MOTIFS.items():
        hits = sum(1 for kw in keywords if kw.lower() in signal_text)
        # Also check cadence_mode alignment
        if motif_name == "rapid_associative_engineering" and signature.cadence_mode == "rapid_associative":
            hits += 2
        if motif_name == "mobius_problem_to_proof" and "deep_focus" in signature.cadence_mode:
            hits += 1
        if motif_name == "baby_lookii" and signature.invention_probability > 0.70:
            hits += 2

        if hits >= 2:
            fired.append(motif_name)

    return fired


def score_motif_strength(motif_name: str, signature: TicSignature) -> float:
    """
    Return a strength score 0.0–1.0 for a given motif against a signature.

    Scoring:
      - keyword hit ratio against signal text
      - bonus for cadence_mode alignment
      - bonus for high invention_probability for inventive motifs
    """
    keywords = KNOWN_MOTIFS.get(motif_name, [])
    if not keywords:
        return 0.0

    signal_text = " ".join(signature.signals).lower()
    hit_count = sum(1 for kw in keywords if kw.lower() in signal_text)
    keyword_score = hit_count / len(keywords)

    # Mode bonus
    mode_bonus = 0.0
    if motif_name == "rapid_associative_engineering" and signature.cadence_mode == "rapid_associative":
        mode_bonus = 0.20
    elif motif_name == "baby_lookii" and signature.invention_probability > 0.70:
        mode_bonus = 0.25
    elif motif_name == "contradiction_to_board" and signature.dominant_board == "BOARD-38":
        mode_bonus = 0.10

    score = keyword_score + mode_bonus
    return round(min(score, 1.0), 4)
