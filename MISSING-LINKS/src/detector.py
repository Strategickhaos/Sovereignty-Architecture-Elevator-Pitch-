#!/usr/bin/env python3
"""
MISSING-LINKS Detector — scans the organism for missing links.

Modes:
  --orphans     citizens with no board, boards with no citizens
  --phantoms    MACs/nodes in recon but not in registry
  --gaps        threat patterns with no antibody
  --drift       nodes that have changed without update
  --all         run everything
"""

from __future__ import annotations
import json, sys, yaml
from pathlib import Path
from typing import List

REPO_ROOT   = Path(__file__).resolve().parents[2]
ML_ROOT     = REPO_ROOT / "MISSING-LINKS"
CITIZENS_F  = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
ANTIBODY_D  = REPO_ROOT / "BOARD-11-ANTIBODIES" / "antibodies"
BOARDS      = [d for d in REPO_ROOT.iterdir()
               if d.is_dir() and d.name.startswith("BOARD-")]


def _load_citizens() -> list:
    if not CITIZENS_F.exists():
        return []
    raw = json.loads(CITIZENS_F.read_text())
    return raw.get("citizens", raw) if isinstance(raw, dict) else raw


def detect_orphans() -> dict:
    citizens   = _load_citizens()
    board_ids  = {b.name for b in BOARDS}
    orphan_cits = [c for c in citizens if not c.get("source")]
    boardless   = [c for c in citizens
                   if c.get("source") and c["source"] not in board_ids
                   and not c["source"].startswith("sgc-")]
    result = {
        "orphan_citizens": orphan_cits,
        "boardless_citizens": boardless,
        "total_citizens": len(citizens),
    }
    out = ML_ROOT / "analysis" / "orphan_nodes.yaml"
    out.write_text(yaml.dump(result, sort_keys=False))
    print(f"  Orphan citizens  : {len(orphan_cits)}")
    print(f"  Boardless        : {len(boardless)}")
    print(f"  Written → {out.relative_to(REPO_ROOT)}")
    return result


def detect_rat_gaps() -> dict:
    antibodies = {a.stem for a in ANTIBODY_D.glob("*.yaml")}
    fire_log   = REPO_ROOT / "BOARD-11-ANTIBODIES" / "fire_log.jsonl"
    fired      = set()
    if fire_log.exists():
        for line in fire_log.read_text().splitlines():
            try:
                fired.add(json.loads(line)["antibody"])
            except Exception:
                pass
    gaps = [{"pattern": ab, "status": "never_fired"} for ab in antibodies - fired]
    result = {"gaps": gaps, "antibodies_total": len(antibodies), "fired_count": len(fired)}
    out = ML_ROOT / "analysis" / "rat_coverage_gaps.yaml"
    out.write_text(yaml.dump(result, sort_keys=False))
    print(f"  Antibodies total : {len(antibodies)}")
    print(f"  Never fired      : {len(gaps)}")
    print(f"  Written → {out.relative_to(REPO_ROOT)}")
    return result


def detect_drift() -> dict:
    citizens  = _load_citizens()
    import time
    now       = time.time()
    stale_days = 30
    stale_secs = stale_days * 86400
    drifts = []
    for c in citizens:
        ts = c.get("timestamp") or c.get("ts")
        if ts:
            try:
                import datetime
                dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                age = now - dt.timestamp()
                if age > stale_secs:
                    drifts.append({"cid": c.get("cid"), "last_seen": ts,
                                   "age_days": round(age / 86400, 1)})
            except Exception:
                pass
    result = {"drifts": drifts}
    out = ML_ROOT / "analysis" / "drift_map.yaml"
    out.write_text(yaml.dump(result, sort_keys=False))
    print(f"  Stale citizens (>{stale_days}d): {len(drifts)}")
    print(f"  Written → {out.relative_to(REPO_ROOT)}")
    return result


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--orphans",  action="store_true")
    ap.add_argument("--gaps",     action="store_true")
    ap.add_argument("--drift",    action="store_true")
    ap.add_argument("--all",      action="store_true")
    args = ap.parse_args()

    print("\n  MISSING-LINKS Detector\n")
    if args.all or args.orphans:
        print("  [orphans]")
        detect_orphans()
    if args.all or args.gaps:
        print("  [rat gaps]")
        detect_rat_gaps()
    if args.all or args.drift:
        print("  [drift]")
        detect_drift()
    if not any(vars(args).values()):
        ap.print_help()


if __name__ == "__main__":
    main()
