"""
ERU Analyzer — Expected / Reality / Variance engine for BOARD-21-PHYSICS-FLEET

Takes any observation dict and produces a structured ERU report.
Integrates with SAGCO citizen registry and antibody board.

Usage:
  python eru_analyzer.py --case PHYSICS-FLEET-001
  python eru_analyzer.py --live                   # analyze live cluster metrics
  python eru_analyzer.py --list
"""
import argparse, json, time
from pathlib import Path

BOARD = Path(__file__).resolve().parent.parent
CASE_STUDIES = BOARD / "reports" / "physics_fleet_case_studies.yaml"
REPORTS = BOARD / "reports"

def load_cases() -> list[dict]:
    try:
        import yaml
        return yaml.safe_load(CASE_STUDIES.read_text()).get("case_studies", [])
    except Exception:
        return []

def eru_report(case: dict) -> dict:
    return {
        "id":           case["id"],
        "title":        case["title"],
        "physics_law":  case.get("physics_law", ""),
        "team":         case.get("team", "purple"),
        "E":            case.get("expected", ""),
        "R":            case.get("actual", ""),
        "U":            case.get("variance", ""),
        "understanding":case.get("understanding", "").strip(),
        "resolution":   case.get("resolution", []),
        "antibody":     case.get("antibody"),
        "severity":     case.get("severity", "MEDIUM"),
        "analyzed_at":  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

def print_eru(report: dict):
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"  ERU CASE: {report['id']}")
    print(f"  {report['title']}")
    print(f"  Physics Law: {report['physics_law']}   Team: {report['team'].upper()}   Severity: {report['severity']}")
    print(sep)
    print(f"\n  E (Expected):\n    {report['E']}")
    print(f"\n  R (Reality):\n    {report['R']}")
    print(f"\n  U (Variance):\n    {report['U']}")
    print(f"\n  Understanding:\n    {report['understanding'][:300]}")
    print(f"\n  Resolution:")
    for step in report["resolution"]:
        print(f"    → {step}")
    if report["antibody"]:
        print(f"\n  Antibody: {report['antibody']}")
    print()

def analyze_live() -> dict:
    """Produce an ERU report from live system state."""
    import platform, os

    # Gather reality
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        reality = {
            "cpu_percent": cpu,
            "mem_used_pct": mem.percent,
            "mem_available_gb": round(mem.available / 1e9, 2),
        }
    except ImportError:
        reality = {"note": "psutil not installed — limited metrics"}

    # Simple variance detection
    variances = []
    if reality.get("cpu_percent", 0) > 80:
        variances.append("HIGH_CPU: cpu_percent > 80 — possible RAT_PROCESS_VARIANCE")
    if reality.get("mem_used_pct", 0) > 90:
        variances.append("HIGH_MEM: memory > 90% — possible energy bleed (PHYSICS-FLEET-001)")

    report = {
        "id": f"LIVE-ERU-{int(time.time())}",
        "title": "Live System ERU Analysis",
        "E": "System operates within baseline CPU < 70%, MEM < 80%",
        "R": str(reality),
        "U": variances or ["No critical variance detected"],
        "analyzed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host": platform.node(),
    }

    out = REPORTS / f"live_eru_{int(time.time())}.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"  Live ERU report → {out}")
    return report

def main():
    parser = argparse.ArgumentParser(description="SAGCO ERU Analyzer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--case", help="Case study ID (e.g. PHYSICS-FLEET-001)")
    group.add_argument("--live", action="store_true", help="Analyze live system state")
    group.add_argument("--list", action="store_true", help="List all case studies")
    args = parser.parse_args()

    cases = load_cases()

    if args.list:
        print(f"\n  PHYSICS FLEET ERU CASES ({len(cases)})\n")
        for c in cases:
            print(f"  [{c.get('severity','?'):8}] {c['id']}  —  {c['title']}")
            print(f"            Physics: {c.get('physics_law','')}")
        return

    if args.live:
        r = analyze_live()
        print_eru(r)
        return

    case = next((c for c in cases if c["id"] == args.case), None)
    if not case:
        print(f"ERROR: case {args.case} not found")
        print(f"Run: python eru_analyzer.py --list")
        return

    print_eru(eru_report(case))

if __name__ == "__main__":
    main()
