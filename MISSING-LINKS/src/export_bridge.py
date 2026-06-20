#!/usr/bin/env python3
"""
MISSING-LINKS Export Bridge — sends closed contradictions to inventions.

Closed case → portfolio artifact OR invention candidate based on pmi_delta.

Usage:
  python export_bridge.py --all          export all closed cases
  python export_bridge.py --case ML-xxx  export specific case
  python export_bridge.py --portfolio    list portfolio artifacts
"""

from __future__ import annotations
import yaml, json, sys, shutil
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parents[2]
ML_ROOT     = REPO_ROOT / "MISSING-LINKS"
CLOSED_DIR  = ML_ROOT / "cases" / "closed"
PORTFOLIO   = ML_ROOT / "exports" / "portfolio_artifacts"
INVENTIONS  = ML_ROOT / "exports" / "invention_candidates"


def export_case(case_path: Path) -> dict:
    case = yaml.safe_load(case_path.read_text())
    pmi_delta = case.get("pmi_delta", 0) or 0
    invention = case.get("invention")

    if pmi_delta > 0.05 or invention:
        dest = INVENTIONS / case_path.name
        category = "invention_candidate"
    else:
        dest = PORTFOLIO / case_path.name
        category = "portfolio_artifact"

    shutil.copy2(case_path, dest)
    print(f"  {case_path.name} → {category}  (pmi_delta={pmi_delta})")
    return {"case": case_path.name, "category": category, "pmi_delta": pmi_delta}


def export_all() -> list[dict]:
    results = []
    for case_path in sorted(CLOSED_DIR.glob("*.yaml")):
        results.append(export_case(case_path))
    print(f"\n  Exported {len(results)} closed cases")
    return results


def list_portfolio():
    for category, d in [("Inventions", INVENTIONS), ("Portfolio", PORTFOLIO)]:
        items = list(d.glob("*.yaml"))
        print(f"\n  {category} ({len(items)}):")
        for item in sorted(items):
            c = yaml.safe_load(item.read_text())
            print(f"    {item.name}  pmi_delta={c.get('pmi_delta','?')}  "
                  f"invention={c.get('invention','—')}")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--all",       action="store_true")
    ap.add_argument("--case",      help="Case filename")
    ap.add_argument("--portfolio", action="store_true")
    args = ap.parse_args()

    PORTFOLIO.mkdir(parents=True, exist_ok=True)
    INVENTIONS.mkdir(parents=True, exist_ok=True)
    print("\n  MISSING-LINKS Export Bridge\n")

    if args.all:
        export_all()
    elif args.case:
        p = CLOSED_DIR / args.case
        if not p.exists():
            p = Path(args.case)
        if p.exists():
            export_case(p)
        else:
            print(f"  Case not found: {args.case}")
    elif args.portfolio:
        list_portfolio()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
