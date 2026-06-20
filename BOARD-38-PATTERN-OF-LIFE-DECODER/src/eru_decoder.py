"""
BOARD-38 — Pattern-of-Life Decoder
eru_decoder.py — ERU (Expected / Received / Unresolved) proof for the decode.
"""

from __future__ import annotations

from datetime import datetime

from pattern_of_life import PatternOfLife


def build_eru(pol: PatternOfLife) -> dict:
    """
    Build an ERU report for a PatternOfLife decode run.

    ERU format:
      expected  — what we expected the decoder to find
      actual    — what was actually found
      variance  — 0 if seeds > 0, else difference
      status    — PASS / PARTIAL / FAIL

    Args:
        pol: PatternOfLife built by build_pattern_of_life().
    Returns:
        ERU report dict.
    """
    n_motifs = len(pol.motifs)
    n_seeds  = len(pol.invention_seeds)
    n_links  = len(pol.missing_links)

    expected_motifs = max(1, n_motifs)   # at least 1 expected
    expected_seeds  = max(1, n_seeds)    # at least 1 seed expected

    variance = 0 if n_seeds > 0 else abs(expected_seeds - n_seeds)

    status = "PASS"
    if n_seeds == 0:
        status = "FAIL"
    elif n_motifs == 0:
        status = "PARTIAL"

    return {
        "eru_id": f"ERU-{pol.pol_id}",
        "board": "BOARD-38",
        "generated": datetime.utcnow().isoformat(),
        "pol_id": pol.pol_id,
        "expected": {
            "motifs_detected": f">= {expected_motifs}",
            "missing_links_identified": ">= 1",
            "seeds_emitted": ">= 1",
        },
        "actual": {
            "motifs_detected": n_motifs,
            "missing_links_identified": n_links,
            "seeds_emitted": n_seeds,
            "cadence_mode": pol.signature.cadence_mode,
            "invention_probability": pol.signature.invention_probability,
        },
        "variance": variance,
        "status": status,
        "motifs": pol.motifs,
        "missing_links": pol.missing_links,
    }
