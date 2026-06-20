#!/usr/bin/env python3
"""
BOARD-29 Phone Parser — token stream → PhoneAST.

Message → Conversation → PhoneAST
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from .phone_lexer import Token, PhoneToken


@dataclass
class Message:
    sender:    str = ""
    recipient: str = ""
    timestamp: str = ""
    body:      List[str] = field(default_factory=list)
    otp:       Optional[str] = None
    financial: List[str] = field(default_factory=list)
    marketing: bool = False
    attachments: List[str] = field(default_factory=list)
    agent_calls: List[str] = field(default_factory=list)
    sensitive:   bool = False
    source:      str = ""

    @property
    def district(self) -> str:
        if self.otp or self.sensitive:
            return "trinity"
        if self.financial:
            return "trinity"
        if self.marketing:
            return "memory_palace"
        if self.agent_calls:
            return "frequency_coast"
        return "frequency_coast"

    @property
    def severity(self) -> str:
        if self.otp:
            return "CRITICAL"
        if self.financial:
            return "HIGH"
        if self.marketing:
            return "LOW"
        return "LOW"


@dataclass
class Conversation:
    messages: List[Message] = field(default_factory=list)
    source:   str = ""

    def participants(self) -> List[str]:
        seen = set()
        out  = []
        for m in self.messages:
            for p in (m.sender, m.recipient):
                if p and p not in seen:
                    seen.add(p)
                    out.append(p)
        return out


@dataclass
class PhoneAST:
    conversations: List[Conversation] = field(default_factory=list)

    def all_messages(self) -> List[Message]:
        return [m for c in self.conversations for m in c.messages]

    def critical_messages(self) -> List[Message]:
        return [m for m in self.all_messages() if m.severity == "CRITICAL"]


def parse(tokens: List[Token]) -> PhoneAST:
    ast  = PhoneAST()
    conv = Conversation()
    msg  = Message()

    def _flush_msg():
        nonlocal msg
        if msg.sender or msg.body or msg.otp or msg.financial:
            conv.messages.append(msg)
        msg = Message()

    def _flush_conv():
        nonlocal conv
        _flush_msg()
        if conv.messages:
            ast.conversations.append(conv)
        conv = Conversation()

    for tok in tokens:
        src = tok.meta.get("source", "")

        if tok.kind == PhoneToken.SEPARATOR:
            _flush_msg()

        elif tok.kind in (PhoneToken.SENDER, PhoneToken.FINANCIAL) and tok.meta.get("role") == "sender":
            if msg.sender:
                _flush_msg()
            msg.sender  = tok.value
            msg.source  = src
            if tok.kind == PhoneToken.FINANCIAL:
                msg.financial.append(tok.value)

        elif tok.kind == PhoneToken.RECIPIENT:
            msg.recipient = tok.value
            msg.source    = src

        elif tok.kind == PhoneToken.TIMESTAMP:
            if msg.timestamp and (msg.body or msg.otp):
                _flush_msg()
            msg.timestamp = tok.value
            if not msg.source:
                msg.source = src

        elif tok.kind == PhoneToken.BODY:
            msg.body.append(tok.value)

        elif tok.kind == PhoneToken.OTP:
            msg.otp       = tok.value
            msg.sensitive = True

        elif tok.kind == PhoneToken.FINANCIAL:
            msg.financial.append(tok.value)

        elif tok.kind == PhoneToken.MARKETING:
            msg.marketing = True
            msg.body.append(tok.value)

        elif tok.kind == PhoneToken.ATTACHMENT:
            msg.attachments.append(tok.value)

        elif tok.kind == PhoneToken.AGENT_CALL:
            msg.agent_calls.append(tok.value)

    _flush_conv()
    return ast


if __name__ == "__main__":
    import sys
    from pathlib import Path
    from .phone_lexer import tokenize_folder, tokenize_text

    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    toks = tokenize_folder(path) if path.is_dir() else tokenize_text(path.read_text())
    ast  = parse(toks)
    print(f"Conversations: {len(ast.conversations)}")
    print(f"Messages:      {len(ast.all_messages())}")
    print(f"Critical:      {len(ast.critical_messages())}")
    for m in ast.all_messages()[:10]:
        print(f"  [{m.district:20s}] {m.severity:8s} FROM={m.sender[:30]} body={str(m.body)[:60]}")
