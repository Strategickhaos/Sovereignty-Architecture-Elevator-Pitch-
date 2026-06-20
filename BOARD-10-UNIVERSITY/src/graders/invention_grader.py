#!/usr/bin/env python3
"""
BOARD-10-UNIVERSITY Invention Grader

Reports on MISSING-LINKS invention seeds and portfolio exports.

Metrics:
  invention_seeds_open
  invention_seeds_closed
  portfolio_artifacts_created
  invention_candidates_created
  active_inventions (open seeds with pmi_delta_estimate > 0)
"""

from __future__ import annotations
import yaml
from pathlib import Path
from typing import Any

REPO_ROOT  = Path(__file__).resolve().parents[3]
ML_ROOT    = REPO_ROOT / "MISSING-LINKS"
SEEDS_DIR  = ML_ROOT / "seeds"
CASES_OPEN = ML_ROOT / "cases" / "open"
CASES_CLOSED = ML_ROOT / "cases" / "closed"
PORTFOLIO  = ML_ROOT / "exports" / "portfolio_artifacts"
INVENTIONS = ML_ROOT / "exports" / "invention_candidates"


def _load_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text()) or {}
    except Exception:
        return {}


def grade() -> dict[str, Any]:
    seeds      = list(SEEDS_DIR.glob("*.yaml")) if SEEDS_DIR.exists() else []
    open_cases = list(CASES_OPEN.glob("*.yaml")) if CASES_OPEN.exists() else []
    closed     = list(CASES_CLOSED.glob("*.yaml")) if CASES_CLOSED.exists() else []
    portfolio  = list(PORTFOLIO.glob("*.yaml")) if PORTFOLIO.exists() else []
    inv_cands  = list(INVENTIONS.glob("*.yaml")) if INVENTIONS.exists() else []

    open_seeds   = [s for s in seeds if _load_yaml(s).get("status") == "OPEN"]
    closed_seeds = [s for s in seeds if _load_yaml(s).get("status") == "CLOSED"]
    active_invs  = [
        _load_yaml(s) for s in open_seeds
        if (_load_yaml(s).get("pmi_delta_estimate") or 0) > 0
    ]

    active_names = [
        f"{inv.get('invention', {}).get('name', inv.get('title', '?'))} "
        f"(pmi_delta≈{inv.get('pmi_delta_estimate', '?')})"
        for inv in active_invs
    ]

    report = {
        "subject":                    "BOARD-29/MISSING-LINKS Invention Pipeline",
        "invention_seeds_open":       len(open_seeds),
        "invention_seeds_closed":     len(closed_seeds),
        "open_cases":                 len(open_cases),
        "closed_cases":               len(closed),
        "portfolio_artifacts_created": len(portfolio),
        "invention_candidates":       len(inv_cands),
        "active_inventions":          len(active_invs),
        "active_invention_names":     active_names,
        "contradiction_inventions":   (
            f"{len(open_seeds)} seed{'s' if len(open_seeds)!=1 else ''}, "
            f"{len(closed_seeds)} closed, "
            f"{len(active_invs)} active"
            + (f" ({active_invs[0].get('invention', {}).get('name', '')})"
               if active_invs else "")
        ),
        "grade": (
            "DISTINGUISHED" if len(closed_seeds) >= 3 else
            "EXCELLENT"     if len(closed_seeds) >= 1 and len(open_seeds) >= 1 else
            "PASS"          if len(open_seeds) >= 1 else
            "INCOMPLETE"
        ),
    }
    return report


def print_report(report: dict):
    print(f"\n  BOARD-10 Invention Grader")
    print(f"  {'─'*55}")
    print(f"  Seeds open               : {report['invention_seeds_open']}")
    print(f"  Seeds closed             : {report['invention_seeds_closed']}")
    print(f"  Active inventions        : {report['active_inventions']}")
    for name in report["active_invention_names"]:
        print(f"    → {name}")
    print(f"  Portfolio artifacts      : {report['portfolio_artifacts_created']}")
    print(f"  Invention candidates     : {report['invention_candidates']}")
    print(f"  {'─'*55}")
    print(f"  contradiction_inventions : {report['contradiction_inventions']}")
    print(f"  Grade                    : {report['grade']}")


if __name__ == "__main__":
    print_report(grade())
