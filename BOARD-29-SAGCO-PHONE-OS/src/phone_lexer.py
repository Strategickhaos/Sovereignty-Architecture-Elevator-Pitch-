#!/usr/bin/env python3
"""
BOARD-29 Phone Lexer — folder → token stream.

A desktop folder IS a phone device.
Each file in the folder IS a signal (message / attachment / call record).
"""

from __future__ import annotations
import re, os
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional


class PhoneToken(Enum):
    SENDER       = auto()   # FROM: or E.164 number
    RECIPIENT    = auto()   # TO: or sagco://agent
    TIMESTAMP    = auto()   # ISO-8601 or Windows file mtime
    BODY         = auto()   # message text body
    ATTACHMENT   = auto()   # file path / binary blob reference
    OTP          = auto()   # 6-digit one-time code
    FINANCIAL    = auto()   # amount / account / routing number
    MARKETING    = auto()   # promotional / bulk sender
    SEPARATOR    = auto()   # blank line / --- between messages
    AGENT_CALL   = auto()   # sagco://agent extension dial


# Patterns
_E164        = re.compile(r'\+?1?\s*[\(\-]?\d{3}[\)\-\s]?\d{3}[\-\s]?\d{4}')
_SAGCO_URI   = re.compile(r'sagco://[\w\-]+')
_ISO_TS      = re.compile(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}')
_OTP         = re.compile(r'\b\d{6}\b')
_AMOUNT      = re.compile(r'\$[\d,]+\.?\d{0,2}')
_MARKETING   = re.compile(r'SALE|PROMO|OFFER|DISCOUNT|CLICK HERE|UNSUBSCRIBE', re.I)
_SEPARATOR   = re.compile(r'^[-=]{3,}$', re.M)

FINANCIAL_SENDERS = {
    "18337384591": "NFCU",
    "18559676655": "Bridgecrest",
    "22891":       "BestBuy",
    "15127739959": "DOMENIC_MASTER",
}


@dataclass
class Token:
    kind:  PhoneToken
    value: str
    meta:  dict = field(default_factory=dict)


def _classify_sender(raw: str) -> PhoneToken:
    normalized = re.sub(r'\D', '', raw)
    if normalized in FINANCIAL_SENDERS:
        return PhoneToken.FINANCIAL
    if _SAGCO_URI.match(raw):
        return PhoneToken.AGENT_CALL
    return PhoneToken.SENDER


def tokenize_text(text: str, source: str = "") -> List[Token]:
    tokens: List[Token] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            tokens.append(Token(PhoneToken.SEPARATOR, ""))
            continue
        if _SEPARATOR.match(stripped):
            tokens.append(Token(PhoneToken.SEPARATOR, stripped))
            continue
        if stripped.upper().startswith("FROM:"):
            raw = stripped[5:].strip()
            kind = _classify_sender(raw)
            tokens.append(Token(kind, raw, {"role": "sender", "source": source}))
            continue
        if stripped.upper().startswith("TO:"):
            raw = stripped[3:].strip()
            kind = PhoneToken.AGENT_CALL if _SAGCO_URI.match(raw) else PhoneToken.RECIPIENT
            tokens.append(Token(kind, raw, {"role": "recipient", "source": source}))
            continue
        if _SAGCO_URI.search(stripped):
            tokens.append(Token(PhoneToken.AGENT_CALL, stripped, {"source": source}))
            continue
        if _ISO_TS.search(stripped):
            tokens.append(Token(PhoneToken.TIMESTAMP, stripped, {"source": source}))
            continue
        if _OTP.search(stripped) and ("code" in stripped.lower() or "otp" in stripped.lower() or len(stripped) < 80):
            tokens.append(Token(PhoneToken.OTP, stripped, {"source": source, "sensitive": True}))
            continue
        if _AMOUNT.search(stripped) or "account" in stripped.lower():
            tokens.append(Token(PhoneToken.FINANCIAL, stripped, {"source": source}))
            continue
        if _MARKETING.search(stripped):
            tokens.append(Token(PhoneToken.MARKETING, stripped, {"source": source}))
            continue
        tokens.append(Token(PhoneToken.BODY, stripped, {"source": source}))
    return tokens


def tokenize_folder(folder: Path) -> List[Token]:
    """Treat every file in a folder as a phone signal."""
    tokens: List[Token] = []
    if not folder.exists():
        return tokens
    for fpath in sorted(folder.iterdir()):
        if fpath.is_dir():
            tokens += tokenize_folder(fpath)
            continue
        suffix = fpath.suffix.lower()
        if suffix in (".txt", ".md", ".log", ".yaml", ".json"):
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
                tokens.append(Token(PhoneToken.TIMESTAMP,
                                    str(fpath.stat().st_mtime),
                                    {"source": str(fpath), "file": fpath.name}))
                tokens += tokenize_text(text, source=str(fpath))
                tokens.append(Token(PhoneToken.SEPARATOR, "---"))
            except Exception:
                pass
        else:
            tokens.append(Token(PhoneToken.ATTACHMENT, str(fpath),
                                {"size": fpath.stat().st_size}))
    return tokens


if __name__ == "__main__":
    import sys
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    toks = tokenize_folder(path) if path.is_dir() else tokenize_text(path.read_text())
    for t in toks:
        val = t.value[:80] if not t.meta.get("sensitive") else "*** REDACTED ***"
        print(f"  {t.kind.name:<16} {val}")
