"""
BOARD-38 — Pattern-of-Life Decoder
pattern_of_life.py — Main pattern-of-life model.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

from cadence_lexer import CadenceToken, lex_text, lex_word_frequency, lex_music_tokens
from rhythm_parser import RhythmPattern, parse_cadence
from tic_signature import TicSignature, build_signature
from motif_detector import detect_motifs, score_motif_strength


@dataclass
class PatternOfLife:
    pol_id: str
    generated: str
    motifs: list[str]
    signature: TicSignature
    missing_links: list[str]
    invention_seeds: list[dict]

    def to_dict(self) -> dict:
        return {
            "pol_id": self.pol_id,
            "generated": self.generated,
            "motifs": self.motifs,
            "signature": {
                "sig_id": self.signature.sig_id,
                "signals": self.signature.signals,
                "cadence_mode": self.signature.cadence_mode,
                "dominant_pos": self.signature.dominant_pos,
                "dominant_board": self.signature.dominant_board,
                "loop_ratio": self.signature.loop_ratio,
                "invention_probability": self.signature.invention_probability,
            },
            "missing_links": self.missing_links,
            "invention_seeds": self.invention_seeds,
        }


# ── Missing-link heuristics ───────────────────────────────────────────────────

_MOTIF_MISSING_LINKS: dict[str, list[str]] = {
    "rapid_associative_engineering": [
        "reusable compiler core",
        "scaffold-to-board bridge",
    ],
    "contradiction_to_board": [
        "automated contradiction resolver",
        "ERU variance annotator",
    ],
    "screenshot_to_command": [
        "OCR-to-command pipeline",
        "visual antibody generator",
    ],
    "mobius_problem_to_proof": [
        "mobius proof verifier",
        "formula step-tracer",
    ],
    "baby_lookii": [
        "invention seed router",
        "pattern-to-music bridge",
    ],
}


def _derive_missing_links(motifs: list[str]) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for m in motifs:
        for link in _MOTIF_MISSING_LINKS.get(m, []):
            if link not in seen:
                links.append(link)
                seen.add(link)
    return links


def _build_seeds(motifs: list[str], signature: TicSignature) -> list[dict]:
    seeds: list[dict] = []
    for motif in motifs:
        strength = score_motif_strength(motif, signature)
        seeds.append({
            "seed_id": f"SEED-{uuid.uuid4().hex[:6].upper()}",
            "motif": motif,
            "strength": strength,
            "cadence_mode": signature.cadence_mode,
            "dominant_signal": signature.signals[0] if signature.signals else "",
            "priority": "HIGH" if strength > 0.5 else "MEDIUM",
        })
    return seeds


# ── Public API ────────────────────────────────────────────────────────────────

def build_pattern_of_life(sources: list[str]) -> PatternOfLife:
    """
    Build a PatternOfLife from a list of text sources.

    Each source is lexed, parsed into rhythm patterns, then combined into
    a single TicSignature and motif scan.

    Args:
        sources: list of raw text strings (word-freq JSON strings or plain text).
    Returns:
        PatternOfLife dataclass.
    """
    all_tokens: list[CadenceToken] = []

    for src in sources:
        src = src.strip()
        if not src:
            continue
        # Try to parse as JSON word-freq list
        if src.startswith("["):
            try:
                data = json.loads(src)
                all_tokens.extend(lex_word_frequency(data))
                continue
            except (json.JSONDecodeError, TypeError):
                pass
        # Fall back to plain text
        all_tokens.extend(lex_text(src))

    patterns: list[RhythmPattern] = parse_cadence(all_tokens)
    signature: TicSignature = build_signature(patterns)
    motifs: list[str] = detect_motifs(signature)
    missing_links = _derive_missing_links(motifs)
    seeds = _build_seeds(motifs, signature)

    return PatternOfLife(
        pol_id=f"POL-{uuid.uuid4().hex[:8].upper()}",
        generated=datetime.utcnow().isoformat(),
        motifs=motifs,
        signature=signature,
        missing_links=missing_links,
        invention_seeds=seeds,
    )
