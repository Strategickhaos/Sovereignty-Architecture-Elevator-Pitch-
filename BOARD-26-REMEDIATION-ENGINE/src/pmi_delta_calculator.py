#!/usr/bin/env python3
"""
BOARD-26 PMI Delta Calculator — measures organism health improvement.

PMI = Particle Mastery Index (0.0 → 1.0)
  1.0 = perfect organism — every board green, every case closed, every citizen registered
  0.0 = dead organism — nothing works

Components:
  citizen_coverage  (0.25 weight) — citizens / expected_artifacts
  antibody_coverage (0.25 weight) — antibodies firing correctly
  board_health      (0.25 weight) — boards present and populated
  case_closure      (0.25 weight) — closed cases / total cases

Usage:
  pmi_delta_calculator.py --measure
  pmi_delta_calculator.py --compare 0.85 0.92
  pmi_delta_calculator.py --history
  pmi_delta_calculator.py --target 0.99 --plan
"""
import argparse, json, time, yaml
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent.parent
CASES_OPEN  = Path(__file__).resolve().parent.parent / "cases" / "open"
CASES_CLOSE = Path(__file__).resolve().parent.parent / "cases" / "closed"
PMI_LOG     = Path(__file__).resolve().parent.parent / "reports" / "pmi_history.jsonl"
PMI_LOG.parent.mkdir(parents=True, exist_ok=True)

EXPECTED_BOARDS = [
    "BOARD-10-UNIVERSITY", "BOARD-11-ANTIBODIES", "BOARD-13-RECON",
    "BOARD-21-PHYSICS-FLEET", "BOARD-23-REFINERY-WAFER-BRIDGE",
    "BOARD-24-GCP-MASTERY", "BOARD-25-SAGCO-HUB", "BOARD-26-REMEDIATION-ENGINE",
    "08-CITIZENS", "SAGCO-LANG", "sagco-agents",
]

EXPECTED_ANTIBODIES = [
    "RAT_PROCESS_VARIANCE", "RAT_NETWORK_BEACONING", "RAT_CLOUD_PRIVESC",
    "RAT_PI_SSH_ANOMALY", "RAT_BROWSER_OAUTH_DRIFT", "RAT_DOCKER_ESCAPE",
    "RAT_WSL_CROSSBOUNDARY",
]


def _ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _score_citizens() -> tuple[float, dict]:
    registry = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    if not registry.exists():
        return 0.0, {"error": "registry not found"}
    raw = json.loads(registry.read_text())
    citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw
    count = len(citizens)
    # Score: 10 citizens = 0.5, 50 = 0.8, 100+ = 1.0
    score = min(1.0, count / 100.0 + 0.1)
    return round(score, 4), {"count": count}


def _score_antibodies() -> tuple[float, dict]:
    ab_dir = REPO_ROOT / "BOARD-11-ANTIBODIES" / "antibodies"
    if not ab_dir.exists():
        return 0.0, {"error": "antibodies dir not found"}
    found = {p.stem for p in ab_dir.glob("*.yaml")}
    hits  = len(found & set(EXPECTED_ANTIBODIES))
    score = hits / len(EXPECTED_ANTIBODIES)
    return round(score, 4), {"found": len(found), "expected": len(EXPECTED_ANTIBODIES), "hits": hits}


def _score_boards() -> tuple[float, dict]:
    found = [b for b in EXPECTED_BOARDS if (REPO_ROOT / b).exists()]
    score = len(found) / len(EXPECTED_BOARDS)
    missing = [b for b in EXPECTED_BOARDS if b not in found]
    return round(score, 4), {"found": len(found), "missing": missing}


def _score_cases() -> tuple[float, dict]:
    open_count   = len(list(CASES_OPEN.glob("*.yaml")))
    closed_count = len(list(CASES_CLOSE.glob("*.yaml")))
    total = open_count + closed_count
    if total == 0:
        return 1.0, {"note": "no cases — perfect baseline"}
    score = closed_count / total
    return round(score, 4), {"open": open_count, "closed": closed_count, "total": total}


def measure() -> dict:
    citizen_score,  citizen_info  = _score_citizens()
    antibody_score, antibody_info = _score_antibodies()
    board_score,    board_info    = _score_boards()
    case_score,     case_info     = _score_cases()

    pmi = round(
        citizen_score  * 0.25 +
        antibody_score * 0.25 +
        board_score    * 0.25 +
        case_score     * 0.25,
        4
    )

    grade = (
        "DISTINGUISHED" if pmi >= 0.95 else
        "EXCELLENT"     if pmi >= 0.85 else
        "PASS"          if pmi >= 0.70 else
        "NEEDS_WORK"    if pmi >= 0.50 else
        "CRITICAL"
    )

    result = {
        "timestamp":      _ts(),
        "pmi":            pmi,
        "grade":          grade,
        "components": {
            "citizens":  {"score": citizen_score,  **citizen_info},
            "antibodies":{"score": antibody_score, **antibody_info},
            "boards":    {"score": board_score,    **board_info},
            "cases":     {"score": case_score,     **case_info},
        }
    }

    # Log it
    with open(PMI_LOG, "a") as f:
        f.write(json.dumps(result) + "\n")

    # Print
    bar_len = int(pmi * 40)
    bar = "█" * bar_len + "░" * (40 - bar_len)
    print(f"\n  ╔══════════════════════════════════════════════════╗")
    print(f"  ║  SAGCO-OS PMI  [{bar}]  {pmi:.4f}  {grade:14s} ║")
    print(f"  ╚══════════════════════════════════════════════════╝\n")
    print(f"  Citizens  {citizen_score:.4f}  [{citizen_info.get('count','?')} registered]")
    print(f"  Antibodies {antibody_score:.4f}  [{antibody_info.get('hits','?')}/{antibody_info.get('expected','?')} RAT fleet]")
    print(f"  Boards    {board_score:.4f}  [{board_info.get('found','?')}/{len(EXPECTED_BOARDS)} present]")
    print(f"  Cases     {case_score:.4f}  [{case_info.get('closed','?')} closed / {case_info.get('total','0')} total]")

    if board_info.get("missing"):
        print(f"\n  Missing boards: {board_info['missing']}")

    return result


def compare(before: float, after: float):
    delta = after - before
    mark  = "📈" if delta > 0 else "📉" if delta < 0 else "➡"
    print(f"\n  PMI Delta: {before:.4f} → {after:.4f}  {mark} Δ{delta:+.4f}")
    if delta > 0.05:
        print(f"  Significant improvement — {int(delta*100)}% gain")
    elif delta > 0:
        print(f"  Marginal improvement — system moving forward")
    elif delta == 0:
        print(f"  No change — remediation had no measurable effect")
    else:
        print(f"  ⚠ REGRESSION — PMI dropped. Bloodhound needed.")


def history():
    if not PMI_LOG.exists():
        print("  No PMI history yet — run --measure first"); return
    entries = [json.loads(l) for l in PMI_LOG.read_text().splitlines() if l.strip()]
    print(f"\n  PMI History — {len(entries)} measurement(s)\n")
    for e in entries[-20:]:
        pmi   = e.get("pmi", 0)
        grade = e.get("grade", "?")
        ts    = e.get("timestamp", "?")
        bar   = "█" * int(pmi * 20) + "░" * (20 - int(pmi * 20))
        print(f"  {ts}  [{bar}]  {pmi:.4f}  {grade}")

    if len(entries) >= 2:
        first = entries[0]["pmi"]
        last  = entries[-1]["pmi"]
        print(f"\n  Trajectory: {first:.4f} → {last:.4f}  Δ{last-first:+.4f}")


def plan(target: float):
    current = measure()
    pmi_now = current["pmi"]
    gap = target - pmi_now
    print(f"\n  Target PMI: {target:.4f}  |  Current: {pmi_now:.4f}  |  Gap: {gap:+.4f}\n")
    print(f"  Remediation Plan to reach {target:.4f}:\n")

    comps = current["components"]
    actions = []
    for comp_name, data in comps.items():
        score = data["score"]
        if score < 1.0:
            potential = (1.0 - score) * 0.25
            actions.append((potential, comp_name, data))

    actions.sort(reverse=True)
    for potential, comp_name, data in actions:
        print(f"  +{potential:.4f}  {comp_name:15s}  current={data['score']:.4f}")
        if comp_name == "antibodies":
            hits = data.get("hits", 0)
            exp  = data.get("expected", 7)
            print(f"             Add {exp - hits} more RAT antibodies")
        elif comp_name == "citizens":
            print(f"             Register more artifacts via catpush")
        elif comp_name == "boards":
            print(f"             Missing: {data.get('missing', [])}")
        elif comp_name == "cases":
            print(f"             Close {data.get('open', 0)} open cases via remediation_runner")


def main():
    parser = argparse.ArgumentParser(description="BOARD-26 PMI Delta Calculator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--measure",  action="store_true")
    group.add_argument("--compare",  nargs=2, type=float, metavar=("BEFORE","AFTER"))
    group.add_argument("--history",  action="store_true")
    group.add_argument("--plan",     action="store_true")
    parser.add_argument("--target",  type=float, default=0.99)
    args = parser.parse_args()

    if args.measure:    measure()
    elif args.compare:  compare(args.compare[0], args.compare[1])
    elif args.history:  history()
    elif args.plan:     plan(args.target)

if __name__ == "__main__":
    main()
