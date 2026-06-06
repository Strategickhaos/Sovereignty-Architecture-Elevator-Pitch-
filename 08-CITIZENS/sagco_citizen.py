#!/usr/bin/env python3
"""
sagco citizen — CLI for the SAGCO Citizen System
Usage:
  sagco citizen new   <name> --kind <kind> --born-in <district>
  sagco citizen move  <cid> --to <district> --gate <gate>
  sagco citizen show  <cid>
  sagco citizen list  [--kind <kind>] [--district <district>] [--status <status>]
  sagco citizen prove <cid> --source <source> --hash <hash>
"""

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "citizen_registry.json"

DISTRICTS = [
    "genesis", "compiler_city", "c64", "eru", "trinity",
    "frequency_coast", "industrial", "memory_palace", "contradiction_forest"
]

KINDS = [
    "proof", "invention", "artifact", "contradiction",
    "deploy_packet", "midi", "trig6_state"
]

STATUSES = ["embryo", "active", "inspected", "deployed", "archived", "contradiction"]


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text())
    return {"schema_version": "1.0", "genesis_tick": 1674852049000, "citizens": []}


def save_registry(reg: dict):
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, default=str))


def make_cid(kind: str) -> str:
    tick = int(time.time() * 1000)
    # increment derived from genesis: distance mod 3449
    increment = tick % 3449
    return f"sgc-{kind}-{tick}-{increment}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def cmd_new(args):
    reg = load_registry()
    cid = make_cid(args.kind)
    citizen = {
        "cid": cid,
        "name": args.name,
        "kind": args.kind,
        "born_in": args.born_in,
        "born_at": now_iso(),
        "born_from": args.born_from,
        "district": args.born_in,
        "status": "embryo",
        "travel_log": [
            {"district": args.born_in, "entered_at": now_iso(), "gate": None, "result": "passed"}
        ],
        "payload": {"summary": args.summary or "", "data": {}, "checksum": "pending"},
        "proofs": [],
        "tags": args.tags.split(",") if args.tags else [],
        "links": [],
    }
    reg["citizens"].append(citizen)
    save_registry(reg)
    print(f"[SAGCO CITIZEN] Born: {cid}")
    print(f"  name:     {citizen['name']}")
    print(f"  kind:     {citizen['kind']}")
    print(f"  district: {citizen['district']}")
    print(f"  status:   {citizen['status']}")


def cmd_move(args):
    reg = load_registry()
    citizen = next((c for c in reg["citizens"] if c["cid"] == args.cid), None)
    if not citizen:
        print(f"[ERROR] Citizen not found: {args.cid}", file=sys.stderr)
        sys.exit(1)
    entry = {
        "district": args.to,
        "entered_at": now_iso(),
        "gate": args.gate,
        "result": "passed",
    }
    citizen["travel_log"].append(entry)
    citizen["district"] = args.to
    citizen["status"] = "active"
    save_registry(reg)
    print(f"[SAGCO CITIZEN] Moved: {args.cid}")
    print(f"  district: {args.to}  (via gate: {args.gate})")


def cmd_show(args):
    reg = load_registry()
    citizen = next((c for c in reg["citizens"] if c["cid"] == args.cid), None)
    if not citizen:
        print(f"[ERROR] Citizen not found: {args.cid}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(citizen, indent=2, default=str))


def cmd_list(args):
    reg = load_registry()
    results = reg["citizens"]
    if args.kind:
        results = [c for c in results if c["kind"] == args.kind]
    if args.district:
        results = [c for c in results if c["district"] == args.district]
    if args.status:
        results = [c for c in results if c["status"] == args.status]
    if not results:
        print("[SAGCO CITIZEN] No citizens match filter.")
        return
    print(f"{'CID':<45} {'NAME':<35} {'KIND':<18} {'DISTRICT':<22} {'STATUS'}")
    print("-" * 140)
    for c in results:
        print(f"{c['cid']:<45} {c['name']:<35} {c['kind']:<18} {c['district']:<22} {c['status']}")


def cmd_prove(args):
    reg = load_registry()
    citizen = next((c for c in reg["citizens"] if c["cid"] == args.cid), None)
    if not citizen:
        print(f"[ERROR] Citizen not found: {args.cid}", file=sys.stderr)
        sys.exit(1)
    proof = {
        "source": args.source,
        "hash": args.hash,
        "verified_at": now_iso(),
    }
    citizen["proofs"].append(proof)
    if citizen["status"] == "embryo":
        citizen["status"] = "active"
    save_registry(reg)
    print(f"[SAGCO CITIZEN] Proof attached to {args.cid}")
    print(f"  source: {args.source}")
    print(f"  hash:   {args.hash}")


def main():
    parser = argparse.ArgumentParser(
        prog="sagco citizen",
        description="SAGCO Citizen System — make the map move"
    )
    sub = parser.add_subparsers(dest="command")

    p_new = sub.add_parser("new", help="Create a new citizen")
    p_new.add_argument("name")
    p_new.add_argument("--kind", required=True, choices=KINDS)
    p_new.add_argument("--born-in", required=True, choices=DISTRICTS, dest="born_in")
    p_new.add_argument("--born-from", default=None, dest="born_from")
    p_new.add_argument("--summary", default="")
    p_new.add_argument("--tags", default="")

    p_move = sub.add_parser("move", help="Move a citizen to a new district")
    p_move.add_argument("cid")
    p_move.add_argument("--to", required=True, choices=DISTRICTS)
    p_move.add_argument("--gate", default="manual")

    p_show = sub.add_parser("show", help="Show a citizen's full record")
    p_show.add_argument("cid")

    p_list = sub.add_parser("list", help="List citizens")
    p_list.add_argument("--kind", choices=KINDS, default=None)
    p_list.add_argument("--district", choices=DISTRICTS, default=None)
    p_list.add_argument("--status", choices=STATUSES, default=None)

    p_prove = sub.add_parser("prove", help="Attach a proof to a citizen")
    p_prove.add_argument("cid")
    p_prove.add_argument("--source", required=True)
    p_prove.add_argument("--hash", required=True)

    args = parser.parse_args()
    dispatch = {
        "new": cmd_new,
        "move": cmd_move,
        "show": cmd_show,
        "list": cmd_list,
        "prove": cmd_prove,
    }
    if args.command not in dispatch:
        parser.print_help()
        sys.exit(1)
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
