#!/usr/bin/env python3
"""
BOARD-59 — SAGCO ERU Burnrate Comparator
Expected → Reality → Variance vs Industry Baseline

Usage:
  python3 eru_compare.py                  # full comparison report
  python3 eru_compare.py --json           # JSON output
  python3 eru_compare.py --board BOARD-44 # single board ERU
  python3 eru_compare.py --live           # live ticker (refreshes every 60s)

ERU Loop:
  E  Expected    — what was planned
  R  Reality     — what actually happened
  U  Understanding — what we learned from the variance
  V  Variance    — E minus R (negative = ahead, positive = behind)
"""
import os, sys, json, time, math
from datetime import date, datetime, timedelta
from typing import Dict, List

# ── Industry baselines (source: published engineering benchmarks) ──────────────
# DORA metrics / McKinsey dev productivity / GitHub Octoverse 2025
INDUSTRY = {
    "commits_per_day":        2.1,   # avg developer
    "boards_per_sprint":      1.0,   # features per 2-week sprint
    "concepts_per_day":       3.5,   # knowledge worker concepts/day
    "bugs_per_feature":       0.8,   # industry avg defect rate
    "lead_time_days":        14.0,   # idea → deployed (DORA median)
    "pr_merge_time_hours":   47.0,   # industry median PR open→merge
    "test_coverage_pct":     62.0,   # industry avg test coverage
    "deploy_frequency_days":  7.0,   # weekly deploys (DORA medium performer)
    "eru_resolution_days":    5.0,   # avg days to close a variance
}


# ── SAGCO actuals (pulled from repo + board index) ────────────────────────────

def _count_boards(repo_root: str) -> Dict:
    """Count ACTIVE vs PENDING boards from BOARD-INDEX.md."""
    idx = os.path.join(repo_root, "BOARD-INDEX.md")
    active = pending = total = 0
    if os.path.exists(idx):
        for line in open(idx):
            if "| BOARD-" in line:
                total += 1
                if "ACTIVE" in line:
                    active += 1
                elif "PENDING" in line:
                    pending += 1
    return {"active": active, "pending": pending, "total": total}


def _git_commits(repo_root: str, days: int = 30) -> int:
    """Count commits in last N days via git log."""
    import subprocess
    since = (date.today() - timedelta(days=days)).isoformat()
    try:
        r = subprocess.run(
            ["git", "log", "--oneline", f"--since={since}"],
            cwd=repo_root, capture_output=True, text=True, timeout=10
        )
        return len([l for l in r.stdout.splitlines() if l.strip()])
    except Exception:
        return 0


def _count_antibodies(repo_root: str) -> int:
    """Count antibody YAML files across all boards."""
    count = 0
    for root, _, files in os.walk(repo_root):
        for f in files:
            if f.startswith("AB_") and f.endswith(".yaml"):
                count += 1
    return count


def _count_open_variances(repo_root: str) -> int:
    """Count OPEN_VARIANCE entries in board files."""
    import re
    count = 0
    for root, _, files in os.walk(repo_root):
        for f in files:
            if f.endswith((".md", ".yaml", ".txt")):
                try:
                    content = open(os.path.join(root, f),
                                   encoding="utf-8", errors="ignore").read(8192)
                    count += len(re.findall(r"OPEN_VARIANCE", content))
                except Exception:
                    pass
    return count


def _mat225_burnrate(repo_root: str) -> Dict:
    """Pull MAT-225 burnrate from habebian pathway."""
    try:
        sys.path.insert(0, os.path.join(repo_root, "BOARD-44-HABEBIAN-NEURAL"))
        from modules.mat225_calc1 import build_mat225_pathway
        from src.harvest import compute_burnrate
        pathway = build_mat225_pathway()
        return compute_burnrate(pathway)
    except Exception as e:
        return {"concepts_per_day": 0, "concepts_learned": 0,
                "total_concepts": 0, "days_active": 0, "error": str(e)}


def _pr_stats(repo_root: str) -> Dict:
    """Count PRs merged via git log analysis (no API needed)."""
    import subprocess, re
    try:
        r = subprocess.run(
            ["git", "log", "--oneline", "--since=30 days ago"],
            cwd=repo_root, capture_output=True, text=True, timeout=10
        )
        lines = r.stdout.splitlines()
        merges = sum(1 for l in lines if "merge" in l.lower() or "feat" in l.lower())
        fixes  = sum(1 for l in lines if "fix" in l.lower())
        return {"commits_30d": len(lines), "features": merges, "fixes": fixes}
    except Exception:
        return {"commits_30d": 0, "features": 0, "fixes": 0}


# ── ERU Table ─────────────────────────────────────────────────────────────────

def _variance_label(pct: float) -> str:
    if pct <= -20:  return "AHEAD ⚡"
    if pct <= 0:    return "ON_TRACK ✓"
    if pct <= 20:   return "MINOR_LAG"
    if pct <= 50:   return "VARIANCE ⚠"
    return "CRITICAL_VAR ✗"


def _eff_score(sagco_val: float, baseline: float, higher_is_better: bool = True) -> float:
    """Efficiency ratio: >1.0 means SAGCO beats industry."""
    if baseline == 0:
        return 0.0
    ratio = sagco_val / baseline
    return ratio if higher_is_better else (baseline / sagco_val if sagco_val else 0)


def build_eru_report(repo_root: str) -> Dict:
    today = date.today()

    # Collect actuals
    boards    = _count_boards(repo_root)
    pr_stats  = _pr_stats(repo_root)
    antibodies= _count_antibodies(repo_root)
    open_vars = _count_open_variances(repo_root)
    br        = _mat225_burnrate(repo_root)

    # Days since project start (BOARD-44 MAT-225 start: 2026-06-01 approx)
    project_start = date(2026, 5, 1)
    days_elapsed  = max(1, (today - project_start).days)

    commits_30d   = pr_stats["commits_30d"]
    commits_day   = round(commits_30d / 30, 2)
    boards_active = boards["active"]
    boards_total  = boards["total"]
    cpd           = br.get("concepts_per_day", 0)

    # ERU rows: (metric, expected, reality, variance_pct, understanding)
    rows = []

    def eru_row(name, expected, reality, unit, higher_better, understanding):
        if expected == 0:
            vpct = 0.0
        else:
            vpct = round((reality - expected) / expected * 100, 1)
            if not higher_better:
                vpct = -vpct   # flip: lower is better, so being lower = negative variance = good
        eff  = round(_eff_score(reality, expected, higher_better), 2)
        rows.append({
            "metric":       name,
            "expected":     expected,
            "reality":      reality,
            "unit":         unit,
            "variance_pct": vpct,
            "efficiency":   eff,
            "status":       _variance_label(vpct),
            "understanding": understanding,
        })

    eru_row("Commits/day",
            INDUSTRY["commits_per_day"], commits_day, "commits/day", True,
            "SAGCO commits are dense — each touches multiple boards")

    eru_row("Active boards",
            INDUSTRY["boards_per_sprint"] * (days_elapsed / 14),
            boards_active, "boards", True,
            f"{boards_active} active nodes vs {round(INDUSTRY['boards_per_sprint']*(days_elapsed/14),1)} industry sprints")

    eru_row("Concepts/day (MAT-225)",
            INDUSTRY["concepts_per_day"], cpd, "concepts/day", True,
            "Habebian neural pathway tracks calculus concept velocity")

    eru_row("Antibodies deployed",
            days_elapsed * 0.1, antibodies, "antibodies", True,
            "Each antibody = encoded institutional knowledge / pattern")

    eru_row("Open variances",
            0, open_vars, "variances", False,
            "OPEN_VARIANCE items = organism self-awareness of gaps")

    eru_row("Board completion rate",
            80.0, round(boards_active / max(boards_total, 1) * 100, 1), "%", True,
            f"{boards_active}/{boards_total} boards ACTIVE")

    # Organism efficiency score (weighted)
    weights = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
    effs    = [r["efficiency"] for r in rows]
    org_score = round(sum(e * w for e, w in zip(effs, weights)), 3)

    return {
        "date":         today.isoformat(),
        "days_elapsed": days_elapsed,
        "organism_efficiency": org_score,
        "eru_rows":     rows,
        "raw": {
            "commits_30d":  commits_30d,
            "commits_day":  commits_day,
            "boards":       boards,
            "antibodies":   antibodies,
            "open_variances": open_vars,
            "burnrate":     br,
        }
    }


# ── Renderer ─────────────────────────────────────────────────────────────────

def render_report(report: Dict) -> str:
    W = 78
    lines = [
        "═" * W,
        "  SAGCO ERU BURNRATE COMPARATOR — Strategickhaos DAO LLC",
        f"  Date: {report['date']}   Days elapsed: {report['days_elapsed']}",
        "═" * W,
        "",
        f"  {'METRIC':<30} {'EXPECTED':>9} {'REALITY':>9} {'VAR%':>7}  {'EFF':>5}  STATUS",
        "  " + "─" * (W - 2),
    ]

    for r in report["eru_rows"]:
        eff_str   = f"{r['efficiency']:.2f}x"
        var_str   = f"{r['variance_pct']:+.1f}%"
        exp_str   = str(r['expected'])
        real_str  = str(r['reality'])
        lines.append(
            f"  {r['metric']:<30} {exp_str:>9} {real_str:>9} {var_str:>7}  {eff_str:>5}  {r['status']}"
        )

    lines += [
        "  " + "─" * (W - 2),
        "",
        f"  ORGANISM EFFICIENCY SCORE : {report['organism_efficiency']:.3f}x  vs  1.000x (industry baseline)",
    ]

    # Verdict
    oe = report["organism_efficiency"]
    if oe >= 1.5:
        verdict = "SOVEREIGN — organism running at 1.5x+ industry efficiency"
    elif oe >= 1.2:
        verdict = "DOMINANT — 20%+ above industry baseline"
    elif oe >= 1.0:
        verdict = "COMPETITIVE — at or above industry baseline"
    elif oe >= 0.8:
        verdict = "ADAPTIVE — closing gap, ERU loop active"
    else:
        verdict = "CALIBRATING — variance corrected via antibodies"

    lines += [
        f"  VERDICT                   : {verdict}",
        "",
        "  UNDERSTANDING (ERU Loop):",
    ]

    for r in report["eru_rows"]:
        lines.append(f"    [{r['status'][:8]:<8}] {r['metric']}: {r['understanding']}")

    lines += [
        "",
        f"  RAW: commits_30d={report['raw']['commits_30d']}  "
        f"antibodies={report['raw']['antibodies']}  "
        f"open_vars={report['raw']['open_variances']}  "
        f"boards={report['raw']['boards']['active']}/{report['raw']['boards']['total']}",
        "═" * W,
    ]
    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    args   = sys.argv[1:]
    live   = "--live"   in args
    as_json= "--json"   in args
    repo   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def run_once():
        report = build_eru_report(repo)
        if as_json:
            print(json.dumps(report, indent=2))
        else:
            print(render_report(report))
        return report

    if live:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            r = run_once()
            print(f"\n  [live] refreshing in 60s — Ctrl+C to stop")
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                print("\n[eru] live mode stopped")
                break
    else:
        run_once()


if __name__ == "__main__":
    main()
