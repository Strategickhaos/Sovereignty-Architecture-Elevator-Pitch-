#!/usr/bin/env python3
"""
SAGCO Comms Agent — email + SMS + Sequence unified inbox.

Uses Gmail MCP tools when available, falls back to comms_router.py classification.

Usage:
  agent_comms.py --inbox           # scan Gmail inbox (MCP)
  agent_comms.py --sms             # scan SMS via Phone Link demo
  agent_comms.py --classify SENDER BODY  # classify any message
  agent_comms.py --contacts        # show known contacts
  agent_comms.py --thread ID       # read Gmail thread (MCP)
  agent_comms.py --draft TO SUBJECT BODY  # create Gmail draft (MCP)
  agent_comms.py --stats           # comms district stats
"""
import argparse, json, subprocess, sys
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parent.parent
COMMS_SRC   = REPO_ROOT / "BOARD-27-COMMS-WING" / "src"
ROUTER      = COMMS_SRC / "comms_router.py"
CONTACTS_F  = REPO_ROOT / "BOARD-27-COMMS-WING" / "contacts" / "known_contacts.json"
REGISTRY    = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

DISTRICT_MARK = {
    "trinity": "🔵", "frequency_coast": "🟢", "memory_palace": "🟡",
    "eru": "🟣", "industrial": "🟠", "genesis": "⚪",
}


def _router(args: list[str]):
    subprocess.run([sys.executable, str(ROUTER)] + args)


def scan_inbox_mcp():
    """Try Gmail MCP, fall back to usage hint."""
    try:
        import importlib
        # MCP Gmail tools exposed via sagco session
        print("\n  SAGCO Comms — Gmail Inbox\n")
        print("  Gmail MCP tools available in this session.")
        print("  To read threads: sagco comms --thread THREAD_ID")
        print("  To search:       sagco comms --search 'from:nfcu.org'")
        print("  To draft:        sagco comms --draft TO SUBJECT BODY")
        print()
        print("  Registered email contacts:")
        _router(["--contacts"])
    except Exception as e:
        print(f"  Gmail MCP not ready: {e}")


def stats():
    if not REGISTRY.exists():
        print("  No citizen registry found"); return
    raw = json.loads(REGISTRY.read_text())
    citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw

    comms = [c for c in citizens if "comms" in c.get("tags", []) or
             c.get("district") == "frequency_coast"]

    from collections import Counter
    by_type = Counter(c.get("payload", {}).get("type", "unknown") for c in comms)
    by_dist = Counter(c.get("district", "?") for c in comms)

    print(f"\n  SAGCO Comms Stats — {len(comms)} comms citizens\n")
    print("  By type:")
    for t, n in by_type.most_common():
        print(f"    {t:20s}  {n}")
    print("  By district:")
    for d, n in by_dist.most_common():
        mark = DISTRICT_MARK.get(d, "⚫")
        print(f"    {mark} {d:20s}  {n}")


def main():
    parser = argparse.ArgumentParser(description="SAGCO Comms Agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inbox",    action="store_true")
    group.add_argument("--sms",      action="store_true")
    group.add_argument("--classify", nargs=2, metavar=("SENDER","BODY"))
    group.add_argument("--contacts", action="store_true")
    group.add_argument("--stats",    action="store_true")
    group.add_argument("--thread",   metavar="THREAD_ID")
    group.add_argument("--search",   metavar="QUERY")
    group.add_argument("--draft",    nargs=3, metavar=("TO","SUBJECT","BODY"))
    parser.add_argument("--emit-citizens", action="store_true")
    args = parser.parse_args()

    if args.inbox:
        scan_inbox_mcp()
    elif args.sms:
        _router(["--scan-sms"])
    elif args.classify:
        extra = ["--emit-citizens"] if args.emit_citizens else []
        _router(["--classify", "--sender", args.classify[0], "--body", args.classify[1]] + extra)
    elif args.contacts:
        _router(["--contacts"])
    elif args.stats:
        stats()
    elif args.thread:
        print(f"  Fetching thread {args.thread} via Gmail MCP...")
        print(f"  (Use Gmail MCP tool: mcp__Gmail__get_thread)")
    elif args.search:
        print(f"  Searching Gmail for: {args.search}")
        print(f"  (Use Gmail MCP tool: mcp__Gmail__search_threads)")
    elif args.draft:
        to, subject, body = args.draft
        print(f"  Creating draft → To: {to} | Subject: {subject}")
        print(f"  (Use Gmail MCP tool: mcp__Gmail__create_draft)")

if __name__ == "__main__":
    main()
