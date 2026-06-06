#!/usr/bin/env python3
"""
BOARD-26 Remediation Runner — fires autonomous remediation actions for open cases.

Usage:
  remediation_runner.py --run-all
  remediation_runner.py --run-case ML-0001
  remediation_runner.py --target BOARD-11-ANTIBODIES --auto
  remediation_runner.py --dry-run
"""
import argparse, json, subprocess, sys, time, yaml
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent.parent
CASES_OPEN  = Path(__file__).resolve().parent.parent / "cases" / "open"
CASES_CLOSE = Path(__file__).resolve().parent.parent / "cases" / "closed"
RULES_FILE  = Path(__file__).resolve().parent.parent / "manifests" / "remediation_rules.yaml"

OWNER_ACTIONS = {
    "BOARD-13-RECON": [
        [sys.executable, str(REPO_ROOT / "BOARD-13-RECON" / "sagco_recon.py"), "net"],
        [sys.executable, str(REPO_ROOT / "BOARD-13-RECON" / "sagco_recon.py"), "browser"],
    ],
    "BOARD-11-ANTIBODIES": [
        [sys.executable, str(REPO_ROOT / "sagco-agents" / "agent_eru.py"),
         "--scan-board", "BOARD-11-ANTIBODIES"],
    ],
    "BOARD-24-GCP-MASTERY": [
        [sys.executable, str(REPO_ROOT / "sagco-agents" / "agent_gcp.py"), "--badge-check"],
    ],
    "BOARD-21-PHYSICS-FLEET": [
        [sys.executable, str(REPO_ROOT / "BOARD-21-PHYSICS-FLEET" / "src" / "eru_analyzer.py"), "--list"],
    ],
    "BOARD-25-SAGCO-HUB": [
        ["kubectl", "apply", "-f",
         str(REPO_ROOT / "BOARD-25-SAGCO-HUB" / "k8s" / "06-network-policies.yaml")],
        ["kubectl", "apply", "-f",
         str(REPO_ROOT / "BOARD-25-SAGCO-HUB" / "k8s" / "07-resource-quotas.yaml")],
    ],
    "BOARD-26-REMEDIATION-ENGINE": [
        [sys.executable, str(REPO_ROOT / "BOARD-10-UNIVERSITY" / "src" / "exam_runner.py"), "--all"],
    ],
    "08-CITIZENS": [
        [sys.executable, str(REPO_ROOT / "08-CITIZENS" / "catpush.py"), "--help"],
    ],
}


def _ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _run_action(cmd: list[str], dry_run: bool = False) -> tuple[bool, str]:
    display = " ".join(str(c) for c in cmd)
    print(f"    → {display}")
    if dry_run:
        return True, "[DRY RUN]"
    try:
        out = subprocess.check_output(
            [str(c) for c in cmd], stderr=subprocess.STDOUT, timeout=60
        ).decode()
        return True, out[:500]
    except subprocess.CalledProcessError as e:
        return False, e.output.decode()[:500] if e.output else str(e)
    except Exception as e:
        return False, str(e)


def remediate_case(case_path: Path, dry_run: bool = False) -> dict:
    case = yaml.safe_load(case_path.read_text())
    case_id = case["case_id"]
    owner   = case.get("owner", "BOARD-26-REMEDIATION-ENGINE")

    print(f"\n  ▶ Remediating {case_id} — owner={owner}")
    print(f"    Variance: {case.get('variance','?')}")
    print(f"    Severity: {case.get('severity','?')}")

    actions = OWNER_ACTIONS.get(owner, [])
    if not actions:
        print(f"    No automated actions for owner={owner} — flagging for manual review")
        case["resolution"] = "manual_review_required"
        case_path.write_text(yaml.dump(case, sort_keys=False, allow_unicode=True))
        return case

    results = []
    all_ok  = True
    for cmd in actions:
        ok, output = _run_action(cmd, dry_run=dry_run)
        results.append({"cmd": " ".join(str(c) for c in cmd), "ok": ok, "output": output})
        if not ok:
            all_ok = False
            print(f"    ✗ Action failed: {output[:100]}")
        else:
            print(f"    ✓ OK")

    case["resolution"]   = "auto_remediated" if all_ok else "partial_remediation"
    case["remediated_at"] = _ts()
    case["action_log"]   = results

    case_path.write_text(yaml.dump(case, sort_keys=False, allow_unicode=True))
    print(f"    Status: {case['resolution']}")
    return case


def run_all(dry_run: bool = False) -> list[dict]:
    open_cases = sorted(CASES_OPEN.glob("*.yaml"))
    if not open_cases:
        print("  No open cases to remediate."); return []

    print(f"\n  BOARD-26 Remediation Runner — {len(open_cases)} open case(s)\n")
    results = []
    for path in open_cases:
        case = remediate_case(path, dry_run=dry_run)
        results.append(case)

    print(f"\n  Remediation complete: {len(results)} case(s) processed")
    return results


def main():
    parser = argparse.ArgumentParser(description="BOARD-26 Remediation Runner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run-all",   action="store_true")
    group.add_argument("--run-case",  metavar="CASE_ID")
    group.add_argument("--target",    metavar="BOARD")
    parser.add_argument("--auto",     action="store_true")
    parser.add_argument("--dry-run",  action="store_true")
    args = parser.parse_args()

    if args.run_all:
        run_all(dry_run=args.dry_run)
    elif args.run_case:
        path = CASES_OPEN / f"{args.run_case}.yaml"
        if not path.exists():
            print(f"  Case {args.run_case} not found"); sys.exit(1)
        remediate_case(path, dry_run=args.dry_run)
    elif args.target:
        cases = [p for p in CASES_OPEN.glob("*.yaml")
                 if args.target in p.read_text()]
        if not cases:
            print(f"  No open cases for target {args.target}"); return
        for p in cases:
            remediate_case(p, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
