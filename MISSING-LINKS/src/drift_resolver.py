#!/usr/bin/env python3
"""
MISSING-LINKS Drift Resolver — attempts auto-repair of known drift types.

Rules:
  - CITIZEN_NO_DISTRICT → assign memory_palace
  - DISTRICT_ORPHAN     → re-route based on kind
  - stale citizens      → flag for manual review

Usage:
  python drift_resolver.py --auto     run all auto-resolvable drifts
  python drift_resolver.py --report   print what would be resolved
"""

from __future__ import annotations
import json, sys
from pathlib import Path

REPO_ROOT  = Path(__file__).resolve().parents[2]
CITIZENS_F = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

KIND_DISTRICT_MAP = {
    "phone-otp":       "trinity",
    "phone-financial": "trinity",
    "phone-comms":     "frequency_coast",
    "phone-marketing": "memory_palace",
    "browser-event":   "frequency_coast",
    "network-node":    "industrial",
    "gke-node":        "eru",
    "physics":         "eru",
    "recon":           "industrial",
    "comms":           "frequency_coast",
}

VALID_DISTRICTS = {
    "genesis", "eru", "trinity", "industrial",
    "compiler_city", "frequency_coast", "memory_palace", "contradiction_forest"
}


def _load() -> tuple[dict, list]:
    if not CITIZENS_F.exists():
        return {"schema_version": "1.0", "genesis_tick": 0, "citizens": []}, []
    raw = json.loads(CITIZENS_F.read_text())
    if isinstance(raw, dict):
        return raw, raw.get("citizens", [])
    return {"schema_version": "1.0", "genesis_tick": 0, "citizens": raw}, raw


def _save(doc: dict, citizens: list):
    doc["citizens"] = citizens
    CITIZENS_F.write_text(json.dumps(doc, indent=2))


def resolve_missing_districts(dry_run: bool = True) -> int:
    doc, citizens = _load()
    count = 0
    for c in citizens:
        if not c.get("district") or c["district"] not in VALID_DISTRICTS:
            kind     = c.get("kind", "")
            district = KIND_DISTRICT_MAP.get(kind, "memory_palace")
            print(f"  {'[DRY]' if dry_run else '[FIX]'} {c.get('cid','')} "
                  f"district='{c.get('district','none')}' → '{district}' (kind={kind})")
            if not dry_run:
                c["district"] = district
            count += 1
    if not dry_run and count:
        _save(doc, citizens)
    return count


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--auto",   action="store_true", help="Apply auto-resolvable fixes")
    ap.add_argument("--report", action="store_true", help="Dry-run report only")
    args = ap.parse_args()

    print("\n  MISSING-LINKS Drift Resolver\n")

    if args.auto:
        n = resolve_missing_districts(dry_run=False)
        print(f"\n  Fixed {n} district assignments")
    elif args.report:
        n = resolve_missing_districts(dry_run=True)
        print(f"\n  Would fix {n} district assignments (dry run)")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
