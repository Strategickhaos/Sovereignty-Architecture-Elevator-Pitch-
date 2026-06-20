#!/usr/bin/env python3
"""
BOARD-30 Phone Parser — folder → YAML files → token stream → AST → citizens.

Usage:
  python phone_parser.py                          # parses device/inbox/
  python phone_parser.py --inbox PATH             # custom inbox folder
  python phone_parser.py --file MSG-0001.yaml     # single message
  python phone_parser.py --dry-run                # preview, no writes
"""

from __future__ import annotations
import yaml, json, sys, time, hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
BOARD_ROOT = Path(__file__).resolve().parents[2]
INBOX      = BOARD_ROOT / "device" / "inbox"
AST_DIR    = BOARD_ROOT / "ast"
CITIZENS_F = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

GENESIS_INCREMENT = 3449
_tick = 0


def _next_cid(kind: str) -> str:
    global _tick
    ts   = int(time.time() * 1000)
    tick = _tick % GENESIS_INCREMENT
    _tick += 1
    return f"sgc-{kind}-{ts}-{tick}"


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}


def _write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, sort_keys=False))


# ── Lexer ─────────────────────────────────────────────────────────────────────

def lex_message(msg: dict, source: str = "") -> list[dict]:
    return [
        {"type": "FROM",           "value": msg.get("from", "")},
        {"type": "TO",             "value": msg.get("to", "")},
        {"type": "TIMESTAMP",      "value": msg.get("timestamp", "")},
        {"type": "BODY",           "value": msg.get("body", "")},
        {"type": "CLASSIFICATION", "value": msg.get("classification", "unknown")},
        {"type": "SOURCE",         "value": source},
    ]


# ── Parser ────────────────────────────────────────────────────────────────────

def parse_tokens(tokens: list[dict], source_file: str) -> dict:
    data = {t["type"].lower(): t["value"] for t in tokens}
    classification = data.get("classification", "unknown")

    district = "trinity"        if classification in ("otp", "financial") else \
               "frequency_coast" if classification in ("system_boot", "comms", "unknown") else \
               "memory_palace"

    severity = "CRITICAL" if classification == "otp"       else \
               "HIGH"      if classification == "financial" else "LOW"

    return {
        "ast_type":       "conversation_message",
        "source_file":    source_file,
        "from":           data.get("from"),
        "to":             data.get("to"),
        "timestamp":      data.get("timestamp"),
        "body":           data.get("body"),
        "classification": classification,
        "district":       district,
        "severity":       severity,
        "citizen_type":   "phone_message",
    }


# ── Citizen registration ──────────────────────────────────────────────────────

def _fingerprint(node: dict) -> str:
    raw = f"{node.get('from')}|{node.get('classification')}|{node.get('body','')[:80]}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def register_citizen(node: dict, dry_run: bool) -> dict:
    if not CITIZENS_F.exists():
        doc = {"schema_version": "1.0", "genesis_tick": 0, "citizens": []}
        citizens = doc["citizens"]
    else:
        raw = json.loads(CITIZENS_F.read_text())
        if isinstance(raw, dict):
            doc, citizens = raw, raw.get("citizens", [])
        else:
            doc = {"schema_version": "1.0", "genesis_tick": 0, "citizens": raw}
            citizens = doc["citizens"]

    fp = _fingerprint(node)
    if any(c.get("fingerprint") == fp for c in citizens):
        return {}  # already registered

    citizen = {
        "cid":         _next_cid("phone-message"),
        "kind":        node["citizen_type"],
        "district":    node["district"],
        "severity":    node["severity"],
        "name":        f"PhoneMsg from {str(node.get('from','?'))[:40]}",
        "source":      "BOARD-30-FAKE-CELL-BUSINESS-LINE",
        "fingerprint": fp,
        "body_preview": str(node.get("body",""))[:120],
    }
    if not dry_run:
        citizens.append(citizen)
        doc["citizens"] = citizens
        CITIZENS_F.parent.mkdir(parents=True, exist_ok=True)
        CITIZENS_F.write_text(json.dumps(doc, indent=2))
    return citizen


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_inbox(inbox: Path, dry_run: bool = False) -> int:
    AST_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for file in sorted(inbox.glob("*.yaml")):
        if file.name == "sagco-phone-node.yaml":
            continue
        msg    = _load_yaml(file)
        tokens = lex_message(msg, source=str(file))
        node   = parse_tokens(tokens, str(file))

        ast_out = AST_DIR / f"{file.stem}.ast.yaml"
        if not dry_run:
            _write_yaml(ast_out, node)

        citizen = register_citizen(node, dry_run)
        marker  = "🔴" if node["severity"] == "CRITICAL" else \
                  "🟠" if node["severity"] == "HIGH"      else "⚪"
        cid_str = citizen.get("cid", "already registered")
        print(f"  {marker} {file.name:<25} [{node['district']:20s}] {cid_str}")
        count += 1

    return count


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--inbox",   default=str(INBOX))
    ap.add_argument("--file",    help="Single message YAML file")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    print("\n  BOARD-30 Fake Cell Business Line — Phone Parser\n")

    dry = args.dry_run
    if args.file:
        inbox = Path(args.file).parent
    else:
        inbox = Path(args.inbox)

    count = parse_inbox(inbox, dry_run=dry)
    print(f"\n  SAGCO PHONE PARSE COMPLETE: {count} messages")
    if dry:
        print("  DRY RUN — no files written, no citizens registered")


if __name__ == "__main__":
    main()
