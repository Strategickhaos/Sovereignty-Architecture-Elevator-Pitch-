#!/usr/bin/env python3
"""
BOARD-29 Phone Intake Bloodwork — defensive intake report generator.

Scans a folder (Downloads, inbox, etc.) and produces
phone_intake_bloodwork.yaml — safe to share (sensitive fields redacted).

Usage:
  python bloodwork.py --path "$USERPROFILE/Downloads"
  python bloodwork.py --path BOARD-29-SAGCO-PHONE-OS/voicemail
  python bloodwork.py --dry-run
"""

from __future__ import annotations
import sys, yaml, json, datetime
from pathlib import Path

REPO_ROOT  = Path(__file__).resolve().parents[3]
BOARD_ROOT = Path(__file__).resolve().parents[2]
REPORT_OUT = BOARD_ROOT / "reports" / "phone_intake_bloodwork.yaml"

sys.path.insert(0, str(BOARD_ROOT / "src"))
from phone_lexer  import tokenize_folder, PhoneToken
from phone_parser import parse


SENSITIVE_PATTERNS = ("access_token", "id_token", "bearer", "phone_number", "otp")


def _is_sensitive(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in SENSITIVE_PATTERNS)


def _redact(text: str) -> str:
    if _is_sensitive(text):
        return "*** REDACTED ***"
    return text[:120]


def run_bloodwork(folder: Path, dry_run: bool = False) -> dict:
    print(f"\n  BOARD-29 Phone Intake Bloodwork")
    print(f"  Scanning: {folder}")
    print(f"  {'─'*55}")

    tokens = tokenize_folder(folder)
    ast    = parse(tokens)

    # Count heap snapshots
    heap_files = list(folder.glob("*.heapsnapshot")) if folder.exists() else []

    # Tally by token kind
    kind_counts: dict[str, int] = {}
    unparseable = 0
    for tok in tokens:
        kind_counts[tok.kind.name] = kind_counts.get(tok.kind.name, 0) + 1

    messages   = ast.all_messages()
    otp_msgs   = [m for m in messages if m.otp]
    fin_msgs   = [m for m in messages if m.financial and not m.otp]
    mkt_msgs   = [m for m in messages if m.marketing]
    agent_msgs = [m for m in messages if m.agent_calls]
    crit_msgs  = [m for m in messages if m.severity == "CRITICAL"]
    high_msgs  = [m for m in messages if m.severity == "HIGH"]

    # Load citizen registry to count new vs dup
    registry    = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    citizen_pre = 0
    if registry.exists():
        raw = json.loads(registry.read_text())
        citizen_pre = len(raw.get("citizens", raw) if isinstance(raw, dict) else raw)

    report = {
        "name":      "Phone Intake Bloodwork",
        "board":     "BOARD-29-SAGCO-PHONE-OS",
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "scan_path": str(folder),
        "description": "Defensive intake report — sensitive fields redacted",

        "scan_summary": {
            "messages_scanned":  len(messages),
            "otp_signals":       len(otp_msgs),
            "financial_signals": len(fin_msgs),
            "marketing_noise":   len(mkt_msgs),
            "agent_calls":       sum(len(m.agent_calls) for m in messages),
            "attachments":       kind_counts.get("ATTACHMENT", 0),
            "unparseable":       unparseable,
        },

        "heap_snapshots": {
            "found": len(heap_files),
            "files": [f.name for f in heap_files],
            "note":  "Run: python sagco-agents/sagco.py heap <file> --summary" if heap_files else "",
        },

        "cases": {
            "opened":   len(crit_msgs) + len(high_msgs),
            "critical": len(crit_msgs),
            "high":     len(high_msgs),
        },

        "sensitive": {
            "note": "OTP codes, tokens, and phone numbers are REDACTED in this report",
            "redacted_fields": list(SENSITIVE_PATTERNS),
            "otp_count": len(otp_msgs),
        },
    }

    print(f"  Messages scanned   : {len(messages)}")
    print(f"  OTP signals        : {len(otp_msgs)}  {'⚠ CRITICAL — not logged' if otp_msgs else ''}")
    print(f"  Financial signals  : {len(fin_msgs)}")
    print(f"  Marketing noise    : {len(mkt_msgs)}")
    print(f"  Agent calls        : {report['scan_summary']['agent_calls']}")
    print(f"  Heap snapshots     : {len(heap_files)}")
    if heap_files:
        for hf in heap_files:
            print(f"    → {hf.name}")
    print(f"  Cases to open      : {report['cases']['opened']} "
          f"(CRITICAL={report['cases']['critical']}, HIGH={report['cases']['high']})")

    if not dry_run:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(yaml.dump(report, sort_keys=False))
        print(f"\n  Report → {REPORT_OUT.relative_to(REPO_ROOT)}")

    return report


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--path",    default=str(Path.home() / "Downloads"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    folder = Path(args.path)
    if not folder.exists():
        print(f"  Folder not found: {folder}")
        print(f"  Using repo voicemail as fallback")
        folder = BOARD_ROOT / "voicemail"

    run_bloodwork(folder, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
