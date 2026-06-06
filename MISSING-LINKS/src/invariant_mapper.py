#!/usr/bin/env python3
"""
MISSING-LINKS Invariant Mapper — finds which invariant rule was violated.

Usage:
  python invariant_mapper.py --all        scan all invariants
  python invariant_mapper.py --inv INV-003
  python invariant_mapper.py --report     write invariants_health.yaml
"""

from __future__ import annotations
import json, yaml, re, sys
from pathlib import Path

REPO_ROOT    = Path(__file__).resolve().parents[2]
ML_ROOT      = REPO_ROOT / "MISSING-LINKS"
INV_DIR      = ML_ROOT / "invariants"
CITIZENS_F   = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
ANTIBODY_D   = REPO_ROOT / "BOARD-11-ANTIBODIES" / "antibodies"
FIRE_LOG     = REPO_ROOT / "BOARD-11-ANTIBODIES" / "fire_log.jsonl"

VALID_DISTRICTS = {
    "genesis", "eru", "trinity", "industrial",
    "compiler_city", "frequency_coast", "memory_palace", "contradiction_forest"
}
CID_RE = re.compile(r'^sgc-[\w-]+-\d{13}-\d{1,4}$')


def _citizens() -> list:
    if not CITIZENS_F.exists():
        return []
    raw = json.loads(CITIZENS_F.read_text())
    return raw.get("citizens", raw) if isinstance(raw, dict) else raw


def check_inv001() -> list[dict]:
    citizens = _citizens()
    seen_cids, violations = {}, []
    for c in citizens:
        cid = c.get("cid", "")
        if not CID_RE.match(cid):
            violations.append({"rule": "R003", "cid": cid, "issue": "malformed CID"})
        if cid in seen_cids:
            violations.append({"rule": "R001", "cid": cid, "issue": "duplicate CID"})
        seen_cids[cid] = True
        if c.get("sensitive") and c.get("body_preview", "").lower() not in ("*** redacted ***", ""):
            if any(p in c.get("body_preview", "").lower()
                   for p in ("access_token", "id_token", "otp", "phone_number")):
                violations.append({"rule": "R004", "cid": cid, "issue": "sensitive data in body_preview"})
    return violations


def check_inv002() -> list[dict]:
    citizens   = _citizens()
    violations = []
    for c in citizens:
        d = c.get("district")
        if not d:
            violations.append({"cid": c.get("cid"), "issue": "no district"})
        elif d not in VALID_DISTRICTS:
            violations.append({"cid": c.get("cid"), "district": d, "issue": "invalid district"})
    return violations


def check_inv003() -> list[dict]:
    violations = []
    if FIRE_LOG.exists():
        for line in FIRE_LOG.read_text().splitlines():
            try:
                e = json.loads(line)
                if e.get("severity") == "CRITICAL":
                    pass  # would cross-check BOARD-26 open cases here
            except Exception:
                pass
    citizens = _citizens()
    for c in citizens:
        if c.get("sensitive") and c.get("district") != "trinity":
            violations.append({
                "cid": c.get("cid"),
                "issue": "sensitive citizen not in trinity",
                "district": c.get("district"),
            })
    return violations


def check_all() -> dict:
    health = {
        "INV-001": {"name": "Identity Invariance",     "violations": check_inv001()},
        "INV-002": {"name": "District Invariance",     "violations": check_inv002()},
        "INV-003": {"name": "Token Invariance",        "violations": check_inv003()},
    }
    for inv_id, data in health.items():
        n = len(data["violations"])
        data["status"] = "PASS" if n == 0 else ("CRITICAL" if n > 5 else "WARN")
        print(f"  {inv_id} {data['name']:30s} {data['status']} ({n} violations)")
    return health


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--all",    action="store_true")
    ap.add_argument("--inv",    help="INV-001 etc")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    print("\n  MISSING-LINKS Invariant Mapper\n")
    health = {}

    if args.all or args.report:
        health = check_all()
    elif args.inv:
        fn = {"INV-001": check_inv001, "INV-002": check_inv002, "INV-003": check_inv003}.get(args.inv)
        if fn:
            vs = fn()
            print(yaml.dump(vs, sort_keys=False))
        else:
            print(f"  Unknown invariant: {args.inv}")
        return

    if args.report and health:
        out = ML_ROOT / "reports" / "invariants_health.yaml"
        out.write_text(yaml.dump(health, sort_keys=False))
        print(f"\n  Written → {out.relative_to(REPO_ROOT)}")

    if not any(vars(args).values()):
        ap.print_help()


if __name__ == "__main__":
    main()
