#!/usr/bin/env python3
"""
SAGCO ERU Agent — Expected/Reality/Variance/Understanding loop runner

Usage:
  agent_eru.py --scan-board BOARD_DIR
  agent_eru.py --new --expected TEXT --reality TEXT --variance TEXT
  agent_eru.py --list
"""
import argparse, json, time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ERU_LOG   = REPO_ROOT / "08-CITIZENS" / "eru_log.jsonl"

def scan_board(board_dir: Path):
    import yaml
    cases = []
    for f in board_dir.rglob("*.yaml"):
        try:
            doc = yaml.safe_load(f.read_text())
            if isinstance(doc, dict) and "case_studies" in doc:
                for cs in doc["case_studies"]:
                    cs["_source"] = str(f.relative_to(REPO_ROOT))
                    cases.append(cs)
        except Exception:
            pass
    print(f"\n  ERU Agent — scanned {board_dir.name}")
    print(f"  Found {len(cases)} case studies\n")
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    cases.sort(key=lambda c: sev_order.get(c.get("severity", "LOW"), 9))
    for cs in cases:
        sev = cs.get("severity", "?")
        marker = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡"
        print(f"  {marker}  [{sev:8s}]  {cs.get('id','?'):20s}  {cs.get('title','')}")
    return cases


def new_case(expected: str, reality: str, variance: str):
    tick = int(time.time() * 1000)
    cid  = f"eru-{tick}-{tick % 3449}"
    entry = {
        "cid": cid,
        "ts":  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "expected": expected,
        "reality":  reality,
        "variance": variance,
        "understanding": "",
        "antibody":      "",
        "status": "open",
    }
    with open(ERU_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"  ERU case logged: {cid}")
    print(f"  Expected: {expected}")
    print(f"  Reality:  {reality}")
    print(f"  Variance: {variance}")
    print(f"  Log: {ERU_LOG.relative_to(REPO_ROOT)}")


def list_cases():
    if not ERU_LOG.exists():
        print("  No ERU cases logged yet."); return
    cases = [json.loads(l) for l in ERU_LOG.read_text().splitlines() if l.strip()]
    print(f"\n  ERU Log — {len(cases)} cases")
    for c in cases[-20:]:
        print(f"  [{c['status']:8s}]  {c['cid']}  V={c['variance'][:40]}")


def main():
    parser = argparse.ArgumentParser(description="SAGCO ERU Agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan-board", metavar="DIR")
    group.add_argument("--new",   action="store_true")
    group.add_argument("--list",  action="store_true")
    parser.add_argument("--expected", default="")
    parser.add_argument("--reality",  default="")
    parser.add_argument("--variance", default="")
    args = parser.parse_args()

    if args.scan_board:
        scan_board(REPO_ROOT / args.scan_board)
    elif args.new:
        new_case(args.expected, args.reality, args.variance)
    elif args.list:
        list_cases()

if __name__ == "__main__":
    main()
