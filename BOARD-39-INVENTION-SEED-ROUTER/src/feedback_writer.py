"""
feedback_writer.py — writes routing feedback to BOARD-38 so the pattern
baseline knows which seeds were acted on (prevents re-routing duplicates).
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import List

import yaml

REPO_ROOT    = Path(__file__).resolve().parent.parent.parent
BOARD38_DIR  = REPO_ROOT / "BOARD-38-PATTERN-OF-LIFE-DECODER"
FEEDBACK_OUT = BOARD38_DIR / "reports" / "routing_feedback.yaml"


def write_feedback(routed_seeds: List[dict], verified_boards: List[dict]):
    """
    Write BOARD-38/reports/routing_feedback.yaml.

    BOARD-38 reads this on its next cycle to skip already-routed seeds.
    """
    FEEDBACK_OUT.parent.mkdir(parents=True, exist_ok=True)

    acted_seed_ids = [r.get("seed_id") for r in routed_seeds if r.get("seed_id")]
    built_boards   = [r.get("board_name") for r in routed_seeds if r.get("board_name")]
    verified_names = [v.get("board_name") for v in verified_boards if v.get("verified")]

    feedback = {
        "routing_feedback": {
            "timestamp":        datetime.datetime.utcnow().isoformat() + "Z",
            "seeds_routed":     len(routed_seeds),
            "boards_built":     len([r for r in routed_seeds if r.get("success")]),
            "boards_verified":  len(verified_names),
            "acted_seed_ids":   acted_seed_ids,
            "built_boards":     built_boards,
            "verified_boards":  verified_names,
            "eru_variance":     0,
            "status":           "FEEDBACK_WRITTEN",
        }
    }

    FEEDBACK_OUT.write_text(yaml.dump(feedback, default_flow_style=False, sort_keys=False))
    print(f"  FEEDBACK → {FEEDBACK_OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    # Smoke test
    write_feedback(
        routed_seeds=[{"seed_id": "TEST-001", "board_name": "BOARD-AUTO-TEST", "success": True}],
        verified_boards=[{"board_name": "BOARD-AUTO-TEST", "verified": True}],
    )
