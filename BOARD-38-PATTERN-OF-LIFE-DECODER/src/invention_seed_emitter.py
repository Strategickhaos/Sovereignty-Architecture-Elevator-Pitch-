"""
BOARD-38 — Pattern-of-Life Decoder
invention_seed_emitter.py — Emits MISSING-LINKS seeds from patterns.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path

from pattern_of_life import PatternOfLife


def emit_seeds(pol: PatternOfLife) -> list[dict]:
    """
    Emit MISSING-LINKS invention seeds from a PatternOfLife.

    Merges the pol.invention_seeds with missing-link metadata.

    Args:
        pol: PatternOfLife built by build_pattern_of_life().
    Returns:
        list of seed dicts ready for serialisation.
    """
    enriched: list[dict] = []
    for seed in pol.invention_seeds:
        enriched.append({
            **seed,
            "pol_id": pol.pol_id,
            "generated": pol.generated,
            "missing_links": pol.missing_links,
        })

    # Also emit one generic seed per missing link that didn't get a motif seed
    covered = {s["motif"] for s in pol.invention_seeds}
    for link in pol.missing_links:
        already_covered = any(link in s.get("missing_links", []) for s in enriched)
        if not already_covered:
            enriched.append({
                "seed_id": f"SEED-{uuid.uuid4().hex[:6].upper()}",
                "motif": "generic_missing_link",
                "missing_link": link,
                "pol_id": pol.pol_id,
                "generated": pol.generated,
                "priority": "LOW",
            })

    return enriched


def write_seeds(seeds: list[dict], output_dir: Path) -> None:
    """
    Write seeds to output_dir/seeds/ as individual JSON files.
    The canonical output is MISSING-LINKS/seeds/.

    Args:
        seeds: list of seed dicts from emit_seeds().
        output_dir: directory that contains (or will contain) a seeds/ subdirectory.
    """
    seeds_dir = output_dir / "seeds"
    seeds_dir.mkdir(parents=True, exist_ok=True)

    for seed in seeds:
        seed_id = seed.get("seed_id", f"SEED-{uuid.uuid4().hex[:6].upper()}")
        dest = seeds_dir / f"{seed_id}.json"
        dest.write_text(json.dumps(seed, indent=2))

    # Also write a master index
    index_path = seeds_dir / "_index.json"
    index_path.write_text(
        json.dumps(
            {
                "generated": datetime.utcnow().isoformat(),
                "count": len(seeds),
                "seeds": [s.get("seed_id", "") for s in seeds],
            },
            indent=2,
        )
    )
    print(f"  [emitter] Wrote {len(seeds)} seeds to {seeds_dir}")
