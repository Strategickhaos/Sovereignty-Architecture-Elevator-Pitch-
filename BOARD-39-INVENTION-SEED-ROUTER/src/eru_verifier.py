"""
eru_verifier.py — verifies auto-generated boards using ERU criteria.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import yaml

REPO_ROOT   = Path(__file__).resolve().parent.parent.parent
AUTO_BOARDS = REPO_ROOT / "SAGCO-UNIVERSITY" / "output" / "auto_boards"


# ── Board verifier ────────────────────────────────────────────────────────────

def verify_board(board_path: Path) -> dict:
    """
    Verify a single auto-generated board.

    Checks:
      - board.yaml exists
      - atoms/ directory is non-empty
      - bonds/ directory is non-empty
      - eru_report.yaml exists (or is synthesised from atoms/bonds)

    Returns:
        {verified, atom_count, bond_count, stability, warnings}
    """
    board_path = Path(board_path)
    warnings: list[str] = []
    result = {
        "board_path": str(board_path),
        "board_name": board_path.name,
        "verified":   False,
        "atom_count": 0,
        "bond_count": 0,
        "stability":  0.0,
        "warnings":   warnings,
    }

    if not board_path.exists():
        warnings.append("board directory does not exist")
        return result

    # Check board.yaml
    board_yaml = board_path / "board.yaml"
    if not board_yaml.exists():
        warnings.append("board.yaml missing")

    # Count atoms
    atoms_dir = board_path / "atoms"
    atoms: list[Path] = []
    if atoms_dir.exists():
        atoms = [f for f in atoms_dir.iterdir() if f.suffix in (".yaml", ".json")]
        result["atom_count"] = len(atoms)
    else:
        warnings.append("atoms/ directory missing")

    # Count bonds
    bonds_dir = board_path / "bonds"
    bonds: list[Path] = []
    if bonds_dir.exists():
        bonds = [f for f in bonds_dir.iterdir() if f.suffix in (".yaml", ".json")]
        result["bond_count"] = len(bonds)
    else:
        warnings.append("bonds/ directory missing")

    # Check eru_report
    eru_report = board_path / "eru_report.yaml"
    if not eru_report.exists():
        warnings.append("eru_report.yaml missing (will be synthesised)")

    # Compute stability
    if result["atom_count"] > 0:
        result["stability"] = round(
            min(1.0, result["bond_count"] / result["atom_count"]), 4
        )

    # Verified if we have atoms and bonds (even without eru_report)
    result["verified"] = (
        result["atom_count"] > 0
        and result["bond_count"] > 0
        and "board.yaml missing" not in warnings
    )

    return result


def verify_all_auto_boards() -> List[dict]:
    """Verify every board inside SAGCO-UNIVERSITY/output/auto_boards/."""
    results = []

    if not AUTO_BOARDS.exists():
        print(f"  No auto_boards directory found at {AUTO_BOARDS}")
        return results

    board_dirs = [d for d in AUTO_BOARDS.iterdir() if d.is_dir()]
    if not board_dirs:
        print("  No auto-generated boards found.")
        return results

    print(f"\n  Verifying {len(board_dirs)} auto-generated boards …")
    for d in sorted(board_dirs):
        r = verify_board(d)
        status = "PASS" if r["verified"] else "FAIL"
        print(f"  [{status}] {r['board_name']} — "
              f"{r['atom_count']} atoms, {r['bond_count']} bonds, "
              f"stability={r['stability']}")
        if r["warnings"]:
            for w in r["warnings"]:
                print(f"         WARN: {w}")
        results.append(r)

    return results


if __name__ == "__main__":
    verify_all_auto_boards()
