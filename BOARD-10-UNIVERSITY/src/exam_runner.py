#!/usr/bin/env python3
"""
SAGCO University Exam Runner — BOARD-10-UNIVERSITY

Grades the entire SAGCO organism by reading actual repo artifacts.
Each grader follows ERU: Expected / Reality / Variance / Understanding.

Usage:
  python exam_runner.py --all
  python exam_runner.py --exam brick-health
  python exam_runner.py --exam security-eru
  python exam_runner.py --exam physics-fleet
  python exam_runner.py --exam net-scan
  python exam_runner.py --exam citizens
  python exam_runner.py --exam inventions
"""

import argparse, datetime, json, time
from pathlib import Path

REPO_ROOT  = Path(__file__).resolve().parent.parent.parent
BOARD      = REPO_ROOT / "BOARD-10-UNIVERSITY"
REPORTS    = BOARD / "reports"
CERTS      = BOARD / "certificates"

def now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def _load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None

def _load_yaml(p: Path):
    try:
        import yaml
        return yaml.safe_load(p.read_text())
    except Exception:
        return None

def _finding(fid, area, expected, actual, variance, rec):
    return {
        "id": fid, "area": area,
        "E": expected, "R": actual, "U": variance,
        "recommendation": rec if isinstance(rec, list) else [rec],
    }

# ── GRADER 1: Brick Health ────────────────────────────────────────────────────

def grade_brick_health() -> dict:
    checks = {}

    # SAGCO-LANG
    flamec = REPO_ROOT / "SAGCO-LANG" / "src" / "main.rs"
    checks["sagco_lang"] = flamec.exists()

    # BOARD-11 antibodies
    ab_dir = REPO_ROOT / "BOARD-11-ANTIBODIES" / "antibodies"
    checks["antibody_board"] = ab_dir.exists() and any(ab_dir.glob("*.yaml"))

    # BOARD-13-RECON reports
    recon_dir = REPO_ROOT / "BOARD-13-RECON" / "reports"
    checks["recon_reports"] = recon_dir.exists() and any(recon_dir.glob("*.json"))

    # catpush
    checks["catpush"] = (REPO_ROOT / "08-CITIZENS" / "catpush.py").exists()

    # citizen registry
    registry = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    checks["citizen_registry"] = registry.exists()

    # BOARD-21
    checks["physics_fleet"] = (REPO_ROOT / "BOARD-21-PHYSICS-FLEET" / "board.yaml").exists()

    passed  = sum(1 for v in checks.values() if v)
    total   = len(checks)
    score   = round(passed / total * 10, 1)

    findings = []
    for name, ok in checks.items():
        if not ok:
            findings.append(_finding(
                f"BRICK-{name.upper()}",
                name,
                f"{name} artifacts exist in repo",
                f"{name} not found",
                "brick missing or not committed",
                f"Build and commit {name}",
            ))

    return {
        "exam": "brick-health",
        "timestamp": now_iso(),
        "score": f"{score}/10",
        "passed": passed,
        "total": total,
        "checks": checks,
        "findings": findings,
        "status": "PASS" if passed == total else ("WARN" if passed >= total * 0.7 else "FAIL"),
    }

# ── GRADER 2: Security ERU ────────────────────────────────────────────────────

RAT_FLEET = {
    "RAT_PROCESS_VARIANCE",
    "RAT_NETWORK_BEACONING",
    "RAT_CLOUD_PRIVESC",
    "RAT_PI_SSH_ANOMALY",
    "RAT_BROWSER_OAUTH_DRIFT",
    "RAT_DOCKER_ESCAPE",
    "RAT_WSL_CROSSBOUNDARY",
}

def grade_security_eru() -> dict:
    ab_dir  = REPO_ROOT / "BOARD-11-ANTIBODIES" / "antibodies"
    present = set()
    severity_map = {}

    if ab_dir.exists():
        for f in ab_dir.glob("*.yaml"):
            if f.stem in RAT_FLEET:
                present.add(f.stem)
                data = _load_yaml(f)
                if data:
                    severity_map[f.stem] = data.get("severity", "UNKNOWN")

    missing   = sorted(RAT_FLEET - present)
    score_val = round(len(present) / len(RAT_FLEET) * 10, 1)

    # Also check browser recon caught OAuth drift
    browser_report = REPO_ROOT / "BOARD-13-RECON" / "reports" / "browser_nodes.json"
    oauth_caught = False
    if browser_report.exists():
        nodes = _load_json(browser_report)
        if isinstance(nodes, list):
            oauth_caught = any(
                any(a.get("anomaly","").startswith("oauth") for a in n.get("anomalies", []))
                for n in nodes
            )

    findings = []
    if missing:
        findings.append(_finding(
            "SEC-ERU-001", "RAT_FLEET",
            "All 7 RAT antibodies present in BOARD-11-ANTIBODIES",
            f"Missing: {', '.join(missing)}",
            "incomplete RAT fleet — coverage gap",
            "Create missing antibody YAML files",
        ))
    if not oauth_caught:
        findings.append(_finding(
            "SEC-ERU-002", "browser_recon",
            "Browser recon detected at least 1 OAuth drift event",
            "No OAuth anomaly found in browser_nodes.json",
            "browser recon not run or no flagged tabs",
            "Run: python sagco_recon.py browser --emit-citizens",
        ))

    status = "DISTINGUISHED" if not findings else ("PASS" if score_val >= 7 else "WARN")
    return {
        "exam": "security-eru",
        "timestamp": now_iso(),
        "score": f"{score_val}/10",
        "rat_fleet_present": sorted(present),
        "rat_fleet_missing": missing,
        "severity_map": severity_map,
        "oauth_drift_caught": oauth_caught,
        "findings": findings,
        "status": status,
    }

# ── GRADER 3: Net Scan ────────────────────────────────────────────────────────

def grade_net_scan() -> dict:
    net_report  = REPO_ROOT / "BOARD-13-RECON" / "reports" / "net_nodes.json"
    recon_net   = REPO_ROOT / "BOARD-13-RECON" / "recon_net.py"
    net_nodes   = _load_json(net_report) or []
    findings    = []

    module_ok   = recon_net.exists()
    nodes_ok    = isinstance(net_nodes, list)
    pi_found    = any(n.get("node_type") == "raspberry_pi" for n in net_nodes)
    unk_hosts   = [n for n in net_nodes if n.get("vendor") == "unknown" and n.get("status") == "online"]

    if not module_ok:
        findings.append(_finding("NET-001", "net_scan",
            "recon_net.py exists in BOARD-13-RECON",
            "module not found", "brick 9 not committed",
            "Build recon_net.py"))

    if unk_hosts:
        findings.append(_finding("NET-002", "unknown_hosts",
            "All online hosts have known vendor/type",
            f"{len(unk_hosts)} unknown host(s) online",
            "potential RAT_NETWORK_BEACONING candidates",
            "Run: python sagco_recon.py pi --auto  to check each"))

    score_val = 10 if module_ok else 0
    if module_ok and unk_hosts:
        score_val = 8

    return {
        "exam": "net-scan",
        "timestamp": now_iso(),
        "score": f"{score_val}/10",
        "module_exists": module_ok,
        "hosts_observed": len(net_nodes),
        "pi_detected": pi_found,
        "unknown_online": len(unk_hosts),
        "findings": findings,
        "status": "PASS" if module_ok else "WARN",
    }

# ── GRADER 4: Physics Fleet ───────────────────────────────────────────────────

def grade_physics_fleet() -> dict:
    reports_dir = REPO_ROOT / "BOARD-21-PHYSICS-FLEET" / "reports"
    case_file   = reports_dir / "physics_fleet_case_studies.yaml"
    data        = _load_yaml(case_file)
    cases       = data.get("case_studies", []) if data else []
    findings    = []

    eru_src     = REPO_ROOT / "BOARD-21-PHYSICS-FLEET" / "src" / "eru_analyzer.py"
    orch_src    = REPO_ROOT / "BOARD-21-PHYSICS-FLEET" / "src" / "gke_fleet_orchestrator.py"

    critical = [c for c in cases if c.get("severity") == "CRITICAL"]
    high     = [c for c in cases if c.get("severity") == "HIGH"]

    if not cases:
        findings.append(_finding("PHYS-001", "physics_fleet",
            "ERU case studies exist in BOARD-21-PHYSICS-FLEET/reports",
            "no case studies found",
            "physics fleet not initialized",
            "Run: python BOARD-21-PHYSICS-FLEET/src/eru_analyzer.py --list"))

    score_val = min(10, len(cases) * 2.5)

    return {
        "exam": "physics-fleet",
        "timestamp": now_iso(),
        "score": f"{score_val}/10",
        "case_study_count": len(cases),
        "critical_cases": len(critical),
        "high_cases": len(high),
        "eru_analyzer_exists": eru_src.exists(),
        "orchestrator_exists": orch_src.exists(),
        "physics_laws_covered": [c.get("physics_law","") for c in cases],
        "findings": findings,
        "status": "DISTINGUISHED" if len(cases) >= 4 else ("PASS" if cases else "WARN"),
    }

# ── GRADER 5: Citizens ────────────────────────────────────────────────────────

def grade_citizens() -> dict:
    registry = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    catpush  = REPO_ROOT / "08-CITIZENS" / "catpush.py"
    data     = _load_json(registry)
    findings = []

    if isinstance(data, dict):
        citizens = data.get("citizens", [])
    elif isinstance(data, list):
        citizens = data
    else:
        citizens = []

    district_counts: dict[str, int] = {}
    for c in citizens:
        d = c.get("district", "unknown")
        district_counts[d] = district_counts.get(d, 0) + 1

    catpush_citizens = sum(1 for c in citizens if "catpush" in c.get("tags", []))
    pi_citizens      = sum(1 for c in citizens if "pi" in c.get("tags", []))
    browser_citizens = sum(1 for c in citizens if "browser" in c.get("tags", []))

    if len(citizens) < 10:
        findings.append(_finding("CIT-001", "citizens",
            "At least 10 citizens registered in registry",
            f"Only {len(citizens)} citizens found",
            "low citizen population — recon not connected to registry",
            "Run: python sagco_recon.py all  with --emit-citizens"))

    score_val = min(10, len(citizens) * 0.3)

    return {
        "exam": "citizens",
        "timestamp": now_iso(),
        "score": f"{round(score_val, 1)}/10",
        "total_citizens": len(citizens),
        "catpush_citizens": catpush_citizens,
        "pi_citizens": pi_citizens,
        "browser_citizens": browser_citizens,
        "district_distribution": district_counts,
        "catpush_exists": catpush.exists(),
        "findings": findings,
        "status": "DISTINGUISHED" if len(citizens) >= 30 else ("PASS" if len(citizens) >= 10 else "WARN"),
    }

# ── Certification writer ──────────────────────────────────────────────────────

def issue_certificate(results: list[dict]) -> Path:
    CERTS.mkdir(parents=True, exist_ok=True)
    statuses = [r["status"] for r in results]
    overall  = (
        "DISTINGUISHED" if all(s == "DISTINGUISHED" for s in statuses)
        else "PASS" if all(s in ("PASS","DISTINGUISHED") for s in statuses)
        else "WARN"
    )

    cert = {
        "certificate": "SAGCO Sovereign Organism Certification",
        "agent": "purple_sagco",
        "issued_by": "SAGCO-OS-UNIVERSITY  BOARD-10",
        "issued_at": now_iso(),
        "overall_status": overall,
        "exams_passed": sum(1 for s in statuses if s in ("PASS","DISTINGUISHED")),
        "exams_total": len(results),
        "status": overall,
    }

    try:
        import yaml
        out = CERTS / "sovereign_organism_certificate.yaml"
        out.write_text(yaml.dump(cert, sort_keys=False, allow_unicode=True))
    except ImportError:
        out = CERTS / "sovereign_organism_certificate.json"
        out.write_text(json.dumps(cert, indent=2))

    return out

# ── Main runner ───────────────────────────────────────────────────────────────

def grade_inventions() -> dict:
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from graders.invention_grader import grade as _grade, print_report
        report = _grade()
        print_report(report)
        return {
            "exam":   "inventions",
            "timestamp": now_iso(),
            "score":  f"{min(10, report['invention_seeds_open'] * 3 + report['invention_seeds_closed'] * 5)}/10",
            "status": report["grade"],
            **report,
        }
    except Exception as e:
        return {"exam": "inventions", "timestamp": now_iso(),
                "score": "0/10", "status": "WARN",
                "findings": [_finding("INV-000", "inventions",
                    "Invention grader loads", str(e), "grader error", "check invention_grader.py")]}


EXAMS = {
    "brick-health":  grade_brick_health,
    "security-eru":  grade_security_eru,
    "net-scan":      grade_net_scan,
    "physics-fleet": grade_physics_fleet,
    "citizens":      grade_citizens,
    "inventions":    grade_inventions,
}

BANNER = """
╔══════════════════════════════════════════════════╗
║  SAGCO UNIVERSITY EXAM RUNNER  —  BOARD-10      ║
║  Grading the sovereign organism                 ║
╚══════════════════════════════════════════════════╝
"""

def _print_result(r: dict):
    sym = {"DISTINGUISHED": "🏆", "PASS": "✓", "WARN": "⚠", "FAIL": "✗"}.get(r["status"], "?")
    print(f"\n  {sym} [{r['status']:14}]  {r['exam']:<20}  score={r.get('score','?')}")
    for f in r.get("findings", []):
        print(f"      ⚠  [{f['id']}] {f['U']}")
        for rec in f.get("recommendation", []):
            print(f"         → {rec}")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(
        prog="exam_runner",
        description="SAGCO University Exam Runner — grades the full organism",
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--all",  action="store_true", help="Run all exams + issue certificate")
    g.add_argument("--exam", choices=list(EXAMS.keys()), help="Run a single exam")
    args = parser.parse_args()

    results = []
    if args.all:
        for name, fn in EXAMS.items():
            print(f"  running {name}...")
            results.append(fn())
    else:
        results.append(EXAMS[args.exam]())

    for r in results:
        _print_result(r)

    # Write report
    REPORTS.mkdir(parents=True, exist_ok=True)
    report = {
        "exam_suite": "BOARD-10-UNIVERSITY",
        "timestamp": now_iso(),
        "results": results,
    }
    try:
        import yaml
        out = REPORTS / "latest_exam_report.yaml"
        out.write_text(yaml.dump(report, sort_keys=False, allow_unicode=True))
    except ImportError:
        out = REPORTS / "latest_exam_report.json"
        out.write_text(json.dumps(report, indent=2))

    print(f"\n  report → {out}")

    if args.all:
        cert = issue_certificate(results)
        print(f"  cert   → {cert}")

    # Summary
    statuses = [r["status"] for r in results]
    overall  = (
        "DISTINGUISHED" if all(s == "DISTINGUISHED" for s in statuses)
        else "PASS" if all(s in ("PASS","DISTINGUISHED") for s in statuses)
        else "WARN"
    )
    sym = {"DISTINGUISHED": "🏆", "PASS": "✓", "WARN": "⚠"}.get(overall, "?")
    print(f"\n  {sym} ORGANISM STATUS: {overall}\n")

if __name__ == "__main__":
    main()
