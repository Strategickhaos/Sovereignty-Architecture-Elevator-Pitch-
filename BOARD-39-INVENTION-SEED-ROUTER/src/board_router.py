"""
board_router.py — routes top-priority seeds to sagco-boardgen for auto-generation.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List

from priority_queue import SeedPriority, top_n
from seed_harvester import harvest_all

REPO_ROOT   = Path(__file__).resolve().parent.parent.parent
BOARDGEN    = REPO_ROOT / "SAGCO-UNIVERSITY" / "src" / "sagco_boardgen.py"
AUTO_BOARDS = REPO_ROOT / "SAGCO-UNIVERSITY" / "output" / "auto_boards"


# ── Helpers ───────────────────────────────────────────────────────────────────

def auto_name_board(seed_title: str) -> str:
    """Delegate to priority_queue for consistent naming."""
    from priority_queue import auto_name_board as _anb
    return _anb(seed_title)


# ── Core router ───────────────────────────────────────────────────────────────

def route_seed_to_board(seed: SeedPriority, dry_run: bool = False) -> dict:
    """
    Generate a board for a single seed.

    Calls:
        python SAGCO-UNIVERSITY/src/sagco_boardgen.py generate
              --module <slug> --text <seed_content>

    Returns a result dict with board_path, atom_count, bond_count, stability.
    """
    board_name = seed.recommended_board
    slug       = board_name.lower().replace("board-auto-", "").replace("-", "_")
    text_content = (
        f"Title: {seed.title}\n"
        f"Source: {seed.source}\n"
        f"Invention Probability: {seed.invention_prob}\n"
        f"Bond Order Gap: {seed.bond_order_gap}\n"
        f"Priority Score: {seed.priority_score}\n"
        f"Seed ID: {seed.seed_id}\n"
        f"Definition: Auto-generated board for invention seed '{seed.title}'.\n"
        f"Formula: priority = invention_prob * 0.6 + bond_order_gap * 0.4\n"
    )

    result = {
        "seed_id":    seed.seed_id,
        "board_name": board_name,
        "slug":       slug,
        "dry_run":    dry_run,
        "board_path": None,
        "atom_count": 0,
        "bond_count": 0,
        "stability":  0.0,
        "success":    False,
        "error":      None,
    }

    if dry_run:
        result["board_path"] = str(AUTO_BOARDS / slug)
        result["success"]    = True
        print(f"  [DRY-RUN] Would build: {board_name}")
        return result

    if not BOARDGEN.exists():
        result["error"] = f"sagco_boardgen.py not found at {BOARDGEN}"
        print(f"  ERROR: {result['error']}")
        return result

    try:
        cmd = [
            sys.executable, str(BOARDGEN),
            "generate",
            "--module", slug,
            "--text", text_content,
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = proc.stdout + proc.stderr
        board_dir = AUTO_BOARDS / slug
        result["board_path"] = str(board_dir)

        if proc.returncode == 0 and board_dir.exists():
            atoms = list((board_dir / "atoms").glob("*.yaml")) if (board_dir / "atoms").exists() else []
            bonds = list((board_dir / "bonds").glob("*.yaml")) if (board_dir / "bonds").exists() else []
            result["atom_count"] = len(atoms)
            result["bond_count"]  = len(bonds)
            result["stability"]   = min(1.0, len(bonds) / max(len(atoms), 1))
            result["success"]     = True
            print(f"  BUILT: {board_name} → {len(atoms)} atoms, {len(bonds)} bonds")
        else:
            result["error"] = output[:500]
            print(f"  WARN: boardgen returned code {proc.returncode} for {board_name}")
            # Still record the path if directory was at least partially created
            if board_dir.exists():
                result["success"] = True

    except subprocess.TimeoutExpired:
        result["error"] = "boardgen timed out"
        print(f"  ERROR: boardgen timed out for {board_name}")
    except Exception as exc:
        result["error"] = str(exc)
        print(f"  ERROR: {exc}")

    return result


def route_top_seeds(n: int = 3, dry_run: bool = False) -> List[dict]:
    """Harvest all seeds, pick top-n, route each to boardgen."""
    seeds = harvest_all()
    if not seeds:
        print("  No seeds found.")
        return []

    ranked = top_n(seeds, n)
    print(f"\n  Routing top {len(ranked)} seeds (dry_run={dry_run}) …")
    results = []
    for sp in ranked:
        res = route_seed_to_board(sp, dry_run=dry_run)
        results.append(res)
    return results


if __name__ == "__main__":
    route_top_seeds(n=3, dry_run=True)
