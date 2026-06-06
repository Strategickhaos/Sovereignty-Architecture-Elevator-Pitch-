#!/usr/bin/env python3
"""
BOARD-29 Phone Enumerator — PhoneAST → SAGCO citizens.

Each unique message (by district+severity+sender) becomes a citizen.
OTP / financial messages open BOARD-26 cases.
"""

from __future__ import annotations
import json, sys, time, hashlib
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[3]

from .phone_lexer  import tokenize_folder, tokenize_text
from .phone_parser import parse, Message, PhoneAST

GENESIS_INCREMENT = 3449
_tick_counter     = 0


def _next_cid(kind: str) -> str:
    global _tick_counter
    ts   = int(time.time() * 1000)
    tick = _tick_counter % GENESIS_INCREMENT
    _tick_counter += 1
    return f"sgc-{kind}-{ts}-{tick}"


def _load_registry() -> tuple[dict, list]:
    reg_path = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    if reg_path.exists():
        raw = json.loads(reg_path.read_text())
        if isinstance(raw, dict):
            return raw, raw.get("citizens", [])
        return {"schema_version": "1.0", "genesis_tick": 0, "citizens": raw}, raw
    doc = {"schema_version": "1.0", "genesis_tick": 0, "citizens": []}
    return doc, doc["citizens"]


def _save_registry(doc: dict, citizens: list):
    doc["citizens"] = citizens
    reg_path = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    reg_path.write_text(json.dumps(doc, indent=2))


def _msg_fingerprint(msg: Message) -> str:
    raw = f"{msg.sender}|{msg.district}|{msg.severity}|{str(msg.body)[:120]}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def enumerate_ast(ast: PhoneAST, dry_run: bool = False) -> List[dict]:
    doc, citizens = _load_registry()
    existing_fps  = {c.get("fingerprint") for c in citizens}
    new_citizens: List[dict] = []
    cases_to_open: List[Message] = []

    for msg in ast.all_messages():
        fp = _msg_fingerprint(msg)
        if fp in existing_fps:
            continue

        kind = "phone-otp"      if msg.otp      else \
               "phone-financial" if msg.financial else \
               "phone-marketing" if msg.marketing else \
               "phone-comms"

        citizen = {
            "cid":         _next_cid(kind),
            "kind":        kind,
            "district":    msg.district,
            "severity":    msg.severity,
            "name":        f"PhoneMsg from {msg.sender[:40] or 'unknown'}",
            "sender":      msg.sender,
            "recipient":   msg.recipient,
            "timestamp":   msg.timestamp,
            "source":      msg.source,
            "fingerprint": fp,
            "sensitive":   msg.sensitive,
            "body_preview": "*** REDACTED ***" if msg.sensitive else str(msg.body)[:120],
            "agent_calls": msg.agent_calls,
        }
        new_citizens.append(citizen)
        existing_fps.add(fp)

        if msg.severity in ("CRITICAL", "HIGH") and not dry_run:
            cases_to_open.append(msg)

    if not dry_run:
        citizens.extend(new_citizens)
        _save_registry(doc, citizens)
        _open_cases(cases_to_open)

    return new_citizens


def _open_cases(messages: List[Message]):
    case_opener = REPO_ROOT / "BOARD-26-REMEDIATION-ENGINE" / "src" / "case_opener.py"
    if not case_opener.exists():
        return
    import subprocess
    for msg in messages:
        label = "OTP intercepted" if msg.otp else "financial signal"
        cmd = [
            sys.executable, str(case_opener), "--open",
            "--trigger",  "BOARD-29-PHONE-OS",
            "--actual",   label,
            "--variance", f"Phone signal from {msg.sender[:60]}",
            "--severity", msg.severity,
            "--owner",    "BOARD-29",
        ]
        subprocess.run(cmd, capture_output=True)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("path",      nargs="?", default=".",
                    help="Folder (phone device) or text file to enumerate")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()

    path = Path(args.path)
    if path.is_dir():
        toks = tokenize_folder(path)
    else:
        toks = tokenize_text(path.read_text(encoding="utf-8", errors="replace"))

    ast      = parse(toks)
    citizens = enumerate_ast(ast, dry_run=args.dry_run)

    if args.summary or True:
        print(f"\n  Phone OS enumeration — {path}")
        print(f"  Conversations : {len(ast.conversations)}")
        print(f"  Messages      : {len(ast.all_messages())}")
        print(f"  New citizens  : {len(citizens)}")
        for c in citizens:
            marker = "🔴" if c["severity"] == "CRITICAL" else \
                     "🟠" if c["severity"] == "HIGH"     else "⚪"
            print(f"  {marker} [{c['district']:20s}] {c['cid']}  {c['name'][:50]}")
        if args.dry_run:
            print("\n  DRY RUN — no citizens written, no cases opened")


if __name__ == "__main__":
    main()
