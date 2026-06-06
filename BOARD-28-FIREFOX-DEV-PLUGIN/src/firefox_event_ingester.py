#!/usr/bin/env python3
"""
BOARD-28 Firefox Event Ingester — reads exported SAGCO extension JSON
and converts events into BOARD-26 cases + 08-CITIZENS entries.

Usage:
  firefox_event_ingester.py --file sagco-firefox-events-1234567890.json
  firefox_event_ingester.py --file events.json --emit-cases
  firefox_event_ingester.py --file events.json --emit-citizens
  firefox_event_ingester.py --file events.json --emit-cases --emit-citizens --summary
"""
import argparse, json, sys, time, yaml
from pathlib import Path
from collections import Counter

REPO_ROOT   = Path(__file__).resolve().parent.parent.parent
CASES_OPEN  = REPO_ROOT / "BOARD-26-REMEDIATION-ENGINE" / "cases" / "open"
REGISTRY    = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
REPORTS     = Path(__file__).resolve().parent.parent / "reports"
CASES_OPEN.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

GENESIS_INCREMENT = 3449
SEV_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
SEV_MARK  = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "⚪"}


def _ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _cid(kind: str = "artifact") -> str:
    tick = int(time.time() * 1000)
    return f"sgc-{kind}-{tick}-{tick % GENESIS_INCREMENT}"

def _case_id() -> str:
    existing = len(list(CASES_OPEN.glob("*.yaml")))
    n = existing + 1
    return f"FF-{n:04d}"


def load_export(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def summarize(events: list[dict]):
    by_sev  = Counter(e.get("severity", "LOW") for e in events)
    by_ab   = Counter(e.get("antibody", "?")   for e in events)
    by_dist = Counter(e.get("district", "?")   for e in events)

    print(f"\n  BOARD-28 Firefox Event Summary\n")
    print(f"  Total events: {len(events)}\n")

    print("  By severity:")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        n = by_sev.get(sev, 0)
        if n:
            print(f"    {SEV_MARK[sev]}  {sev:10s}  {n}")

    print("\n  By antibody (top 8):")
    for ab, n in by_ab.most_common(8):
        print(f"    {ab:40s}  {n}")

    print("\n  By district:")
    for dist, n in by_dist.most_common():
        print(f"    {dist:25s}  {n}")


def emit_cases(events: list[dict]) -> int:
    opened = 0
    # Only open cases for CRITICAL + HIGH
    high_events = [e for e in events if SEV_ORDER.get(e.get("severity","LOW"), 9) <= 1]
    # Deduplicate by antibody
    seen = set()
    for evt in high_events:
        key = evt.get("antibody", "?")
        if key in seen:
            continue
        seen.add(key)

        case_id = _case_id()
        case = {
            "case_id":     case_id,
            "cid":         _cid("case"),
            "opened_at":   _ts(),
            "status":      "OPEN",
            "source":      "BOARD-28-FIREFOX-DEV-PLUGIN",
            "trigger":     evt.get("antibody", "?"),
            "expected":    "No sensitive data in browser request URLs",
            "actual":      evt.get("type", "?") + (" — " + evt.get("note", "")) if evt.get("note") else evt.get("type", "?"),
            "variance":    f"Firefox extension detected {evt.get('antibody')} [{evt.get('severity')}]",
            "severity":    evt.get("severity", "HIGH"),
            "owner":       "BOARD-13-RECON",
            "district":    evt.get("district", "trinity"),
            "raw":         evt,
        }
        path = CASES_OPEN / f"{case_id}.yaml"
        path.write_text(yaml.dump(case, sort_keys=False, allow_unicode=True))
        print(f"  {SEV_MARK[evt.get('severity','HIGH')]}  Case opened: {case_id}  [{evt.get('antibody')}]")
        opened += 1

    return opened


def emit_citizens(events: list[dict]) -> int:
    if not REGISTRY.exists():
        print("  Citizen registry not found"); return 0
    raw = json.loads(REGISTRY.read_text())
    citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw
    existing = {c["cid"] for c in citizens}

    added = 0
    seen_ab = set()
    for evt in events:
        ab = evt.get("antibody", "?")
        if ab in seen_ab:
            continue
        seen_ab.add(ab)

        cid = _cid("artifact")
        if cid in existing:
            continue

        citizens.append({
            "cid":      cid,
            "name":     f"firefox.event.{ab}",
            "kind":     "artifact",
            "born_in":  "genesis",
            "district": evt.get("district", "memory_palace"),
            "status":   "observed",
            "payload":  {
                "antibody": ab,
                "severity": evt.get("severity"),
                "type":     evt.get("type"),
                "source":   "BOARD-28-FIREFOX-DEV-PLUGIN",
            },
            "tags":     ["firefox", "browser", "board-28", ab.lower()],
            "created_at": _ts(),
        })
        added += 1

    if isinstance(raw, dict):
        raw["citizens"] = citizens
        REGISTRY.write_text(json.dumps(raw, indent=2))
    else:
        REGISTRY.write_text(json.dumps(citizens, indent=2))

    print(f"  Registered {added} Firefox event citizen(s)")
    return added


def main():
    parser = argparse.ArgumentParser(description="BOARD-28 Firefox Event Ingester")
    parser.add_argument("--file",           required=True)
    parser.add_argument("--emit-cases",     action="store_true")
    parser.add_argument("--emit-citizens",  action="store_true")
    parser.add_argument("--summary",        action="store_true", default=True)
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"  ERROR: {path} not found"); sys.exit(1)

    doc    = load_export(path)
    events = doc.get("events", [])

    print(f"\n  BOARD-28 Firefox Event Ingester")
    print(f"  File:    {path.name}")
    print(f"  Exported:{doc.get('exported_at','?')}")
    print(f"  Events:  {len(events)}")

    if args.summary:
        summarize(events)

    if args.emit_cases:
        print(f"\n  Opening BOARD-26 cases for HIGH/CRITICAL events...")
        n = emit_cases(events)
        print(f"  {n} case(s) opened")

    if args.emit_citizens:
        print(f"\n  Registering events as citizens...")
        emit_citizens(events)

    # Write report
    report = REPORTS / f"ingested_{int(time.time())}.yaml"
    report.write_text(yaml.dump({
        "ingested_at": _ts(),
        "source_file": str(path),
        "total_events": len(events),
        "emit_cases": args.emit_cases,
        "emit_citizens": args.emit_citizens,
    }, sort_keys=False, allow_unicode=True))
    print(f"\n  Report: {report.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
