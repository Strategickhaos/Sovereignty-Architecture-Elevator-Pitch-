#!/usr/bin/env python3
"""
SAGCO GCP Agent — Google Cloud Platform navigator & ERU mapper

Usage:
  agent_gcp.py --iam-drift   --project PROJECT
  agent_gcp.py --cost-pulse  --project PROJECT
  agent_gcp.py --services    --project PROJECT
  agent_gcp.py --badge-check
"""
import argparse, json, subprocess, sys, time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def _gcloud(cmd: list[str], project: str | None = None) -> list | dict | None:
    full = ["gcloud"] + cmd + ["--format=json"]
    if project:
        full += ["--project", project]
    try:
        raw = subprocess.check_output(full, stderr=subprocess.DEVNULL, timeout=20).decode()
        return json.loads(raw)
    except Exception:
        return None

def iam_drift(project: str):
    """ERU: IAM Entropy check — list service accounts + key ages."""
    print(f"\n  IAM Drift Scan — project={project}\n")
    sas = _gcloud(["iam", "service-accounts", "list"], project)
    if not isinstance(sas, list):
        print("  gcloud not reachable or no service accounts"); return

    for sa in sas:
        email = sa.get("email", "?")
        disabled = sa.get("disabled", False)
        status = "DISABLED" if disabled else "active"
        print(f"  {'✗' if disabled else '·'}  {email:60s}  [{status}]")

        keys = _gcloud(["iam", "service-accounts", "keys", "list",
                        f"--iam-account={email}"], project)
        if isinstance(keys, list):
            user_keys = [k for k in keys if k.get("keyType") == "USER_MANAGED"]
            if user_keys:
                print(f"      ⚠  {len(user_keys)} user-managed key(s) — potential identity anchor drift")
                print(f"         ERU: see GKE-ERU-003 → Workload Identity remedy")

def cost_pulse(project: str):
    """Check for unquota'd namespaces / high-cost signals."""
    print(f"\n  Cost Pulse — project={project}\n")
    clusters = _gcloud(["container", "clusters", "list"], project)
    if not isinstance(clusters, list):
        print("  No GKE clusters found"); return
    for c in clusters:
        name   = c.get("name")
        nodes  = c.get("currentNodeCount", 0)
        zone   = c.get("zone") or c.get("location")
        status = c.get("status")
        flag = "⚠" if nodes > 5 else "·"
        print(f"  {flag}  {name:40s}  nodes={nodes:3d}  zone={zone}  [{status}]")
        if nodes > 5:
            print(f"      ERU: see GKE-ERU-002 → ResourceQuota as energy budget")

def services_list(project: str):
    """List enabled GCP services."""
    print(f"\n  Enabled Services — project={project}\n")
    svcs = _gcloud(["services", "list", "--enabled"], project)
    if not isinstance(svcs, list):
        print("  gcloud not reachable"); return
    for s in svcs:
        name = s.get("config", {}).get("name", s.get("name", "?"))
        print(f"  · {name}")
    print(f"\n  {len(svcs)} services enabled")

def badge_check():
    """Check BOARD-24-GCP-MASTERY study progress."""
    mastery = REPO_ROOT / "BOARD-24-GCP-MASTERY"
    badges = {
        "ACE":  mastery / "university" / "ace_exam.yaml",
        "PCA":  mastery / "university" / "pca_exam.yaml",
        "PCNE": mastery / "university" / "pcne_exam.yaml",
        "PCD":  mastery / "university" / "pcd_exam.yaml",
    }
    eru_files = list((mastery / "eru").glob("*.yaml"))
    notes_files = list(mastery.rglob("notes/*.md"))
    labs_files  = list(mastery.rglob("labs/*.md"))

    print("\n  GCP Mastery Badge Check\n")
    print(f"  ERU case study files:  {len(eru_files)}")
    print(f"  Notes files:           {len(notes_files)}")
    print(f"  Lab files:             {len(labs_files)}")
    print("\n  Exam readiness:")
    for badge, path in badges.items():
        exists = "✓" if path.exists() else "✗"
        print(f"  {exists}  {badge:6s}  {path.relative_to(REPO_ROOT)}")

def main():
    parser = argparse.ArgumentParser(description="SAGCO GCP Agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--iam-drift",   action="store_true")
    group.add_argument("--cost-pulse",  action="store_true")
    group.add_argument("--services",    action="store_true")
    group.add_argument("--badge-check", action="store_true")
    parser.add_argument("--project", default=None)
    args = parser.parse_args()

    if args.badge_check:
        badge_check(); return

    project = args.project
    if not project:
        try:
            project = subprocess.check_output(
                ["gcloud", "config", "get-value", "project"],
                stderr=subprocess.DEVNULL, timeout=10
            ).decode().strip() or None
        except Exception:
            pass
    if not project and not args.badge_check:
        print("  ERROR: --project required (or set gcloud config project)")
        sys.exit(1)

    if args.iam_drift:   iam_drift(project)
    elif args.cost_pulse: cost_pulse(project)
    elif args.services:   services_list(project)

if __name__ == "__main__":
    main()
