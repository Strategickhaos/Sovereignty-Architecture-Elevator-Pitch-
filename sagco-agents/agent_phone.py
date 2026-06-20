#!/usr/bin/env python3
"""
SAGCO Phone Agent — BOARD-29
sagco phone call AGENT
sagco phone sms AGENT MESSAGE
sagco phone inbox [--path PATH]
sagco phone directory
sagco phone enumerate PATH [--dry-run]
"""

from __future__ import annotations
import sys, yaml
from pathlib import Path

REPO_ROOT    = Path(__file__).resolve().parent.parent
PHONE_BOARD  = REPO_ROOT / "BOARD-29-SAGCO-PHONE-OS"
DIRECTORY    = PHONE_BOARD / "manifests" / "agent_phone_directory.yaml"
VOICEMAIL    = PHONE_BOARD / "voicemail"

BANNER = """
╔════════════════════════════════════════════════════════════╗
║  SAGCO Phone OS — BOARD-29                                 ║
║  Every agent has a line. sagco:// is the protocol.        ║
╚════════════════════════════════════════════════════════════╝
"""


def _load_directory() -> list[dict]:
    if not DIRECTORY.exists():
        return []
    raw = yaml.safe_load(DIRECTORY.read_text())
    return raw.get("directory", [])


def cmd_directory(args: list[str]):
    entries = _load_directory()
    print(BANNER)
    print(f"  {'AGENT':<30} {'EXTENSION':<22} {'DISTRICT':<22} ROLE")
    print("  " + "-" * 100)
    for e in entries:
        agent    = e.get("agent", "")
        ext      = e.get("extension", "")
        district = e.get("district", "")
        role     = e.get("role", "")
        print(f"  {agent:<30} {ext:<22} {district:<22} {role}")
    print(f"\n  {len(entries)} lines registered")


def cmd_call(args: list[str]):
    if not args:
        print("  Usage: sagco phone call AGENT_NAME"); return
    target  = args[0].upper()
    entries = _load_directory()
    for e in entries:
        if e.get("agent", "").upper() == target or target in e.get("name", "").upper():
            print(f"\n  📞 Calling {e['name']} ...")
            print(f"     Extension : {e.get('extension','?')}")
            print(f"     Internal  : {e.get('internal','?')}")
            print(f"     District  : {e.get('district','?')}")
            print(f"     Role      : {e.get('role','?')}")
            if e.get("voiceprint"):
                print(f"     Voiceprint: \"{e['voiceprint']}\"")
            print(f"\n  RING RING — sagco:// protocol active")
            return
    print(f"  ERROR: agent '{target}' not found in directory")
    print(f"  Run: sagco phone directory")


def cmd_sms(args: list[str]):
    if len(args) < 2:
        print("  Usage: sagco phone sms AGENT MESSAGE"); return
    target  = args[0].upper()
    message = " ".join(args[1:])
    entries = _load_directory()
    dest    = next((e for e in entries
                    if e.get("agent","").upper() == target), None)
    if not dest:
        print(f"  ERROR: agent '{target}' not found"); return

    import json, time, datetime
    VOICEMAIL.mkdir(parents=True, exist_ok=True)
    ts  = datetime.datetime.utcnow().isoformat() + "Z"
    sms = {
        "ts":        ts,
        "from":      "DOMENIC_MASTER",
        "to":        dest["agent"],
        "extension": dest.get("extension"),
        "internal":  dest.get("internal"),
        "body":      message,
    }
    log = VOICEMAIL / "sms_log.jsonl"
    with open(log, "a") as f:
        f.write(json.dumps(sms) + "\n")
    print(f"\n  📨 SMS → {dest['name']}")
    print(f"     To      : {dest.get('extension')}")
    print(f"     Message : {message}")
    print(f"     Logged  : {log.relative_to(REPO_ROOT)}")


def cmd_inbox(args: list[str]):
    path_arg = None
    for i, a in enumerate(args):
        if a == "--path" and i + 1 < len(args):
            path_arg = Path(args[i + 1])

    if path_arg:
        _enumerate_path(path_arg, dry_run=False)
        return

    sms_log = VOICEMAIL / "sms_log.jsonl"
    if not sms_log.exists():
        print("  Inbox empty — no SMS log found"); return

    import json
    lines = sms_log.read_text().strip().splitlines()
    print(f"\n  📬 Inbox ({len(lines)} messages)\n")
    for line in lines[-20:]:
        try:
            m = json.loads(line)
            print(f"  [{m.get('ts','')}] {m.get('from','?'):20s} → {m.get('to','?'):25s}  {m.get('body','')[:60]}")
        except Exception:
            pass


def _enumerate_path(path: Path, dry_run: bool):
    import subprocess
    enumerator = PHONE_BOARD / "src" / "phone_enumerator.py"
    cmd = [sys.executable, str(enumerator), str(path)]
    if dry_run:
        cmd.append("--dry-run")
    subprocess.run(cmd)


def cmd_enumerate(args: list[str]):
    dry_run = "--dry-run" in args
    paths   = [a for a in args if not a.startswith("--")]
    path    = Path(paths[0]) if paths else Path(".")
    _enumerate_path(path, dry_run)


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(BANNER)
        print(__doc__)
        return

    sub  = args[0].lower()
    rest = args[1:]

    dispatch = {
        "call":      cmd_call,
        "sms":       cmd_sms,
        "inbox":     cmd_inbox,
        "directory": cmd_directory,
        "dir":       cmd_directory,
        "enumerate": cmd_enumerate,
        "enum":      cmd_enumerate,
    }

    if sub not in dispatch:
        print(f"  Unknown phone command: {sub}")
        print(f"  Available: {', '.join(dispatch)}")
        return

    dispatch[sub](rest)


if __name__ == "__main__":
    main()
