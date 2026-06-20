"""
priority_queue.py — ranks invention seeds for board generation.

Priority score formula:
    priority_score = invention_prob * 0.6 + bond_order_gap * 0.4
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class SeedPriority:
    seed_id: str
    title: str
    source: str          # "missing_links" | "lattice_gap" | "open_case" | "pattern"
    invention_prob: float
    bond_order_gap: float
    priority_score: float = field(init=False)
    recommended_board: str = field(init=False)

    def __post_init__(self):
        # Clamp inputs to [0, 1]
        self.invention_prob = max(0.0, min(1.0, float(self.invention_prob)))
        self.bond_order_gap = max(0.0, min(1.0, float(self.bond_order_gap)))
        self.priority_score = round(
            self.invention_prob * 0.6 + self.bond_order_gap * 0.4, 4
        )
        self.recommended_board = auto_name_board(self.title)

    def to_dict(self) -> dict:
        return {
            "seed_id": self.seed_id,
            "title": self.title,
            "source": self.source,
            "invention_prob": self.invention_prob,
            "bond_order_gap": self.bond_order_gap,
            "priority_score": self.priority_score,
            "recommended_board": self.recommended_board,
        }


# ── Board naming ──────────────────────────────────────────────────────────────

def auto_name_board(seed_title: str) -> str:
    """
    Convert a seed title to a board name slug.
    e.g. "reusable compiler core" -> "BOARD-AUTO-REUSABLE-COMPILER-CORE"
    """
    slug = re.sub(r"[^a-z0-9]+", "-", seed_title.lower()).strip("-")
    slug = slug[:50]  # cap length
    return f"BOARD-AUTO-{slug.upper()}"


# ── Scoring & ranking ─────────────────────────────────────────────────────────

def score_seed(seed: dict) -> SeedPriority:
    """Convert a raw seed dict to a scored SeedPriority."""
    return SeedPriority(
        seed_id=seed.get("seed_id", "UNKNOWN"),
        title=seed.get("title", "untitled"),
        source=seed.get("source", "unknown"),
        invention_prob=float(seed.get("invention_prob", 0.5)),
        bond_order_gap=float(seed.get("bond_order_gap", 0.5)),
    )


def rank_seeds(seeds: list[dict]) -> List[SeedPriority]:
    """Score and sort seeds descending by priority_score."""
    scored = [score_seed(s) for s in seeds]
    return sorted(scored, key=lambda s: s.priority_score, reverse=True)


def top_n(seeds: list[dict], n: int = 5) -> List[SeedPriority]:
    """Return the top-n highest-priority seeds."""
    return rank_seeds(seeds)[:n]


if __name__ == "__main__":
    demo_seeds = [
        {"seed_id": "S1", "title": "reusable compiler core", "source": "missing_links",
         "invention_prob": 0.8, "bond_order_gap": 0.9},
        {"seed_id": "S2", "title": "eru variance annotator", "source": "lattice_gap",
         "invention_prob": 0.6, "bond_order_gap": 0.5},
        {"seed_id": "S3", "title": "scaffold bridge", "source": "open_case",
         "invention_prob": 0.4, "bond_order_gap": 0.3},
    ]
    for sp in rank_seeds(demo_seeds):
        print(f"  [{sp.priority_score:.4f}] {sp.recommended_board}")
