"""
seed_harvester.py — harvests invention seeds from multiple sources.

Sources:
  1. BOARD-38 MISSING-LINKS/seeds/*.json  (missing_links field)
  2. SAGCO-UNIVERSITY eru_reports          (missing_prereqs field)
  3. BOARD-26 / MISSING-LINKS/cases/open  (open remediation cases)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ── Helpers ───────────────────────────────────────────────────────────────────

def _slug_title(title: str) -> str:
    """Normalise title for deduplication."""
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")


def _deduplicate(seeds: list[dict]) -> list[dict]:
    """Remove near-duplicate seeds by normalised title."""
    seen: set[str] = set()
    unique: list[dict] = []
    for s in seeds:
        key = _slug_title(s.get("title", s.get("seed_id", "")))
        if key not in seen:
            seen.add(key)
            unique.append(s)
    return unique


# ── Source 1: BOARD-38 missing-links seeds ───────────────────────────────────

def harvest_missing_links_seeds(board38_dir: Path | None = None) -> list[dict]:
    """Read MISSING-LINKS/seeds/*.json and BOARD-38 PatternOfLife outputs."""
    if board38_dir is None:
        board38_dir = REPO_ROOT / "BOARD-38-PATTERN-OF-LIFE-DECODER"

    seeds: list[dict] = []

    seeds_dir = board38_dir / "MISSING-LINKS" / "seeds"
    if seeds_dir.exists():
        for path in sorted(seeds_dir.glob("*.json")):
            try:
                data: Any = json.loads(path.read_text())
                if isinstance(data, dict):
                    # Expand each missing_link string into its own seed entry
                    missing = data.get("missing_links", [])
                    for link in missing:
                        seeds.append({
                            "seed_id": f"{data.get('seed_id','UNK')}-{_slug_title(link)[:8].upper()}",
                            "title": link,
                            "source": "missing_links",
                            "invention_prob": float(data.get("strength", 0.5)),
                            "bond_order_gap": 0.5,
                            "raw": data,
                        })
                    if not missing:
                        seeds.append({
                            "seed_id": data.get("seed_id", path.stem),
                            "title": data.get("dominant_signal", path.stem),
                            "source": "missing_links",
                            "invention_prob": float(data.get("strength", 0.5)),
                            "bond_order_gap": 0.5,
                            "raw": data,
                        })
            except Exception as exc:
                print(f"  WARN seed_harvester: could not read {path}: {exc}")

    # Also check signatures/ directory for PatternOfLife outputs
    sig_dir = board38_dir / "signatures"
    if sig_dir.exists():
        for path in sorted(sig_dir.glob("*.yaml")) + sorted(sig_dir.glob("*.json")):
            try:
                raw_text = path.read_text()
                data = yaml.safe_load(raw_text) if path.suffix == ".yaml" else json.loads(raw_text)
                if isinstance(data, dict) and "missing_links" in data:
                    for link in data["missing_links"]:
                        seeds.append({
                            "seed_id": f"SIG-{path.stem[:8].upper()}-{_slug_title(link)[:8].upper()}",
                            "title": link,
                            "source": "pattern",
                            "invention_prob": 0.6,
                            "bond_order_gap": 0.4,
                            "raw": data,
                        })
            except Exception as exc:
                print(f"  WARN seed_harvester: could not read {path}: {exc}")

    return seeds


# ── Source 2: SAGCO-UNIVERSITY lattice gaps ───────────────────────────────────

def harvest_lattice_gaps(university_dir: Path | None = None) -> list[dict]:
    """Read SAGCO-UNIVERSITY eru_reports for 'missing_prereqs' fields."""
    if university_dir is None:
        university_dir = REPO_ROOT / "SAGCO-UNIVERSITY"

    seeds: list[dict] = []

    # Check output/ for eru reports
    for report_path in sorted(university_dir.rglob("eru_report*.yaml")):
        try:
            data = yaml.safe_load(report_path.read_text())
            if not isinstance(data, dict):
                continue
            missing = data.get("missing_prereqs", [])
            if isinstance(missing, list):
                for item in missing:
                    title = item if isinstance(item, str) else str(item)
                    seeds.append({
                        "seed_id": f"LATTICE-{_slug_title(title)[:12].upper()}",
                        "title": title,
                        "source": "lattice_gap",
                        "invention_prob": 0.7,
                        "bond_order_gap": float(data.get("variance", 0.5)),
                        "raw": data,
                    })
            # Also harvest unbonded atoms
            unbonded = data.get("unbonded_atoms", [])
            for atom in unbonded:
                title = atom if isinstance(atom, str) else atom.get("name", str(atom))
                seeds.append({
                    "seed_id": f"ATOM-{_slug_title(title)[:12].upper()}",
                    "title": title,
                    "source": "lattice_gap",
                    "invention_prob": 0.55,
                    "bond_order_gap": 0.6,
                    "raw": data,
                })
        except Exception as exc:
            print(f"  WARN seed_harvester: could not read {report_path}: {exc}")

    return seeds


# ── Source 3: Open cases ──────────────────────────────────────────────────────

def harvest_open_cases(cases_dir: Path | None = None) -> list[dict]:
    """Read BOARD-26 or MISSING-LINKS/cases/open/*.yaml."""
    if cases_dir is None:
        cases_dir = REPO_ROOT / "MISSING-LINKS" / "cases" / "open"

    seeds: list[dict] = []

    if not cases_dir.exists():
        # Fallback: BOARD-26
        cases_dir = REPO_ROOT / "BOARD-26-REMEDIATION-ENGINE"

    if cases_dir.exists():
        for path in sorted(cases_dir.rglob("*.yaml")):
            try:
                data = yaml.safe_load(path.read_text())
                if not isinstance(data, dict):
                    continue
                title = (data.get("title") or data.get("name") or
                         data.get("case_id") or path.stem)
                seeds.append({
                    "seed_id": f"CASE-{path.stem[:12].upper()}",
                    "title": str(title),
                    "source": "open_case",
                    "invention_prob": 0.5,
                    "bond_order_gap": 0.45,
                    "raw": data,
                })
            except Exception as exc:
                print(f"  WARN seed_harvester: could not read {path}: {exc}")

    return seeds


# ── Combined ──────────────────────────────────────────────────────────────────

def harvest_all() -> list[dict]:
    """Combine all seed sources and deduplicate by title similarity."""
    seeds: list[dict] = []
    seeds.extend(harvest_missing_links_seeds())
    seeds.extend(harvest_lattice_gaps())
    seeds.extend(harvest_open_cases())
    return _deduplicate(seeds)


if __name__ == "__main__":
    all_seeds = harvest_all()
    print(f"Harvested {len(all_seeds)} seeds")
    for s in all_seeds[:5]:
        print(f"  [{s['source']}] {s['title']}")
