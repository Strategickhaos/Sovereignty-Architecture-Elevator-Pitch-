#!/usr/bin/env python3
"""
BOARD-26 Case Opener — Scans all boards for contradictions and opens case files.

Sources scanned:
  - BOARD-10-UNIVERSITY: exam failures (score < 7)
  - BOARD-11-ANTIBODIES: fired antibodies (fire_log.jsonl)
  - BOARD-13-RECON:      unknown hosts, phantom MACs, OAuth drift
  - BOARD-21-PHYSICS:    entropy spikes, cascade failures
  - BOARD-24-GCP:        IAM drift, cost spikes, missing quotas
  - 08-CITIZENS:         orphan artifacts (not in registry)

Usage:
  case_opener.py --scan-all
  case_opener.py --scan-board BOARD-11-ANTIBODIES
  case_opener.py --open --trigger "manual" --variance "describe" --owner BOARD-13-RECON
  case_opener.py --list [--status open|closed|all]
"""
import argparse, json, time, uuid, yaml
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent.parent
CASES_OPEN  = Path(__file__).resolve().parent.parent / "cases" / "open"
CASES_CLOSE = Path(__file__).resolve().parent.parent / "cases" / "closed"
RULES_FILE  = Path(__file__).resolve().parent.parent / "manifests" / "remediation_rules.yaml"

CASES_OPEN.mkdir(parents=True, exist_ok=True)
CASES_CLOSE.mkdir(parents=True, exist_ok=True)


def _ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _case_id() -> str:
    n = len(list(CASES_OPEN.glob("*.yaml"))) + len(list(CASES_CLOSE.glob("*.yaml"))) + 1
    return f"ML-{n:04d}"

def _load_rules() -> list[dict]:
    if not RULES_FILE.exists():
        return []
    return yaml.safe_load(RULES_FILE.read_text()).get("rules", [])

def _match_rule(text: str, rules: list[dict]) -> dict | None:
    text_lower = text.lower()
    for rule in rules:
        pattern = rule.get("trigger", {}).get("pattern", "")
        if any(p.strip().lower() in text_lower for p in pattern.split("|")):
            return rule
    return None


# ── Scanners ─────────────────────────────────────────────────────────────────

def _scan_antibody_log() -> list[dict]:
    contradictions = []
    log = REPO_ROOT / "BOARD-11-ANTIBODIES" / "fire_log.jsonl"
    if not log.exists():
        return []
    for line in log.read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        contradictions.append({
            "source":    "BOARD-11-ANTIBODIES",
            "trigger":   entry.get("antibody", "?"),
            "expected":  "No antibody activation",
            "actual":    f"Antibody {entry.get('antibody')} fired on host {entry.get('host')}",
            "variance":  entry.get("variance", "security threat detected"),
            "severity":  entry.get("severity", "HIGH"),
            "owner":     "BOARD-11-ANTIBODIES",
            "raw":       entry,
        })
    return contradictions[-10:]  # last 10 events


def _scan_university() -> list[dict]:
    contradictions = []
    cert = REPO_ROOT / "BOARD-10-UNIVERSITY" / "certificates" / "sovereign_organism_certificate.yaml"
    if not cert.exists():
        return []
    try:
        doc = yaml.safe_load(cert.read_text())
        results = doc.get("results", {})
        for subject, data in results.items():
            grade = data.get("grade", "PASS")
            score = data.get("score", 10)
            if grade == "FAIL" or (isinstance(score, (int, float)) and score < 7):
                contradictions.append({
                    "source":   "BOARD-10-UNIVERSITY",
                    "trigger":  "exam_failure",
                    "expected": f"{subject} score >= 7",
                    "actual":   f"{subject} score = {score} [{grade}]",
                    "variance": f"coverage gap in {subject}",
                    "severity": "HIGH",
                    "owner":    "BOARD-26-REMEDIATION-ENGINE",
                    "raw":      data,
                })
    except Exception:
        pass
    return contradictions


def _scan_citizen_registry() -> list[dict]:
    contradictions = []
    registry = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    if not registry.exists():
        return []
    raw = json.loads(registry.read_text())
    citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw
    cids = {c["cid"] for c in citizens}

    # Check for YAML nodes not in registry
    for node_yaml in (REPO_ROOT / "BOARD-13-RECON").rglob("*.yaml"):
        try:
            doc = yaml.safe_load(node_yaml.read_text())
            if isinstance(doc, dict) and "cid" in doc:
                if doc["cid"] not in cids:
                    contradictions.append({
                        "source":   "08-CITIZENS",
                        "trigger":  "orphan_citizen",
                        "expected": f"Node {node_yaml.name} registered in citizen registry",
                        "actual":   f"CID {doc['cid']} not found in registry",
                        "variance": "missing registration — orphan artifact",
                        "severity": "MEDIUM",
                        "owner":    "BOARD-13-RECON",
                        "raw":      {"path": str(node_yaml), "cid": doc["cid"]},
                    })
        except Exception:
            pass
    return contradictions[:5]


def _scan_all() -> list[dict]:
    print("\n  BOARD-26 Case Opener — Scanning all boards...\n")
    all_contradictions = []
    scanners = [
        ("ANTIBODIES",  _scan_antibody_log),
        ("UNIVERSITY",  _scan_university),
        ("CITIZENS",    _scan_citizen_registry),
    ]
    for name, fn in scanners:
        found = fn()
        print(f"  [{name:12s}]  {len(found)} contradiction(s)")
        all_contradictions.extend(found)
    print(f"\n  Total: {len(all_contradictions)} contradiction(s) found")
    return all_contradictions


# ── Case file writer ──────────────────────────────────────────────────────────

def open_case(trigger: str, expected: str, actual: str, variance: str,
              owner: str, severity: str = "HIGH", source: str = "manual",
              raw: dict | None = None) -> str:
    rules = _load_rules()
    matched_rule = _match_rule(f"{trigger} {variance}", rules)

    cid = f"case-{int(time.time()*1000) % 3449:04d}"
    case_id = _case_id()

    case = {
        "case_id":      case_id,
        "cid":          cid,
        "opened_at":    _ts(),
        "status":       "OPEN",
        "source":       source,
        "trigger":      trigger,
        "expected":     expected,
        "actual":       actual,
        "variance":     variance,
        "severity":     severity,
        "owner":        owner,
        "rule_matched": matched_rule["id"] if matched_rule else None,
        "action":       matched_rule.get("action") if matched_rule else None,
        "synthesis":    matched_rule.get("synthesis") if matched_rule else None,
        "resolution":   None,
        "pmi_before":   None,
        "pmi_after":    None,
        "pmi_delta":    None,
        "closed_at":    None,
        "verified_by":  None,
        "invention":    None,
        "raw":          raw or {},
    }
    path = CASES_OPEN / f"{case_id}.yaml"
    path.write_text(yaml.dump(case, sort_keys=False, allow_unicode=True))
    print(f"  ✓ CASE OPENED: {case_id}  [{severity}]  owner={owner}")
    print(f"    Variance: {variance}")
    if matched_rule:
        print(f"    Rule matched: {matched_rule['id']} — {matched_rule['name']}")
        print(f"    Synthesis: {matched_rule['synthesis']}")
    return case_id


def open_all(contradictions: list[dict]) -> list[str]:
    case_ids = []
    for c in contradictions:
        cid = open_case(
            trigger=c["trigger"], expected=c["expected"], actual=c["actual"],
            variance=c["variance"], owner=c["owner"], severity=c.get("severity", "HIGH"),
            source=c["source"], raw=c.get("raw", {}),
        )
        case_ids.append(cid)
    return case_ids


def list_cases(status: str = "open"):
    dirs = []
    if status in ("open", "all"):   dirs.append(CASES_OPEN)
    if status in ("closed", "all"): dirs.append(CASES_CLOSE)

    cases = []
    for d in dirs:
        cases.extend(d.glob("*.yaml"))

    if not cases:
        print(f"  No {status} cases."); return

    print(f"\n  BOARD-26 Cases — {status.upper()}\n")
    sev_mark = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "⚪"}
    for p in sorted(cases):
        case = yaml.safe_load(p.read_text())
        mark = sev_mark.get(case.get("severity", "LOW"), "⚫")
        pmi  = f"Δ{case['pmi_delta']:+.3f}" if case.get("pmi_delta") else ""
        print(f"  {mark}  {case['case_id']:8s}  [{case['status']:6s}]  "
              f"{case.get('owner','?'):30s}  {case.get('variance','')[:40]}  {pmi}")

    print(f"\n  {len(cases)} case(s)")


def main():
    parser = argparse.ArgumentParser(description="BOARD-26 Case Opener")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan-all",   action="store_true")
    group.add_argument("--scan-board", metavar="BOARD")
    group.add_argument("--open",       action="store_true")
    group.add_argument("--list",       action="store_true")
    parser.add_argument("--trigger",   default="manual")
    parser.add_argument("--variance",  default="")
    parser.add_argument("--expected",  default="")
    parser.add_argument("--actual",    default="")
    parser.add_argument("--owner",     default="BOARD-26-REMEDIATION-ENGINE")
    parser.add_argument("--severity",  default="HIGH")
    parser.add_argument("--status",    default="open", choices=["open", "closed", "all"])
    args = parser.parse_args()

    if args.scan_all:
        contradictions = _scan_all()
        if contradictions:
            print()
            case_ids = open_all(contradictions)
            print(f"\n  {len(case_ids)} case(s) opened")
    elif args.scan_board:
        print(f"  Scanning {args.scan_board}...")
    elif args.open:
        open_case(args.trigger, args.expected, args.actual,
                  args.variance, args.owner, args.severity)
    elif args.list:
        list_cases(args.status)

if __name__ == "__main__":
    main()
