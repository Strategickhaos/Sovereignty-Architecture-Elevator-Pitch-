"""
SAGCO Mobius DSL Lexer
Board: BOARD-31-CELLPHONE-MOBIUS-LAB

Tokenizes .mobius files into a flat token stream.
Supports: LIMIT, DERIV, PIECE, ASSERT, INTEGRAL keywords plus
          IDENT, NUMBER, STRING, OP, LPAREN, RPAREN, COMMA, EQUALS, COMMENT.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional


# ---------------------------------------------------------------------------
# Token types
# ---------------------------------------------------------------------------

KEYWORD = "KEYWORD"
IDENT   = "IDENT"
NUMBER  = "NUMBER"
STRING  = "STRING"
OP      = "OP"
LPAREN  = "LPAREN"
RPAREN  = "RPAREN"
COMMA   = "COMMA"
EQUALS  = "EQUALS"
COMMENT = "COMMENT"
NEWLINE = "NEWLINE"


KEYWORDS = {"LIMIT", "DERIV", "PIECE", "ASSERT", "INTEGRAL"}


@dataclass
class Token:
    kind: str       # one of the constants above
    value: str      # raw matched text
    line: int       # 1-based line number
    col: int        # 1-based column number

    def __repr__(self) -> str:
        return f"Token({self.kind}, {self.value!r}, line={self.line}, col={self.col})"


# ---------------------------------------------------------------------------
# Token patterns — order matters (longest match first for ambiguous rules)
# ---------------------------------------------------------------------------

_TOKEN_PATTERNS: List[tuple[str, str]] = [
    (COMMENT, r"#[^\n]*"),                        # # ... end of line
    (NUMBER,  r"-?\d+(?:\.\d+)?"),                # integer or float
    (STRING,  r'"[^"]*"'),                        # "double quoted"
    (EQUALS,  r"="),                              # =
    (LPAREN,  r"\("),                             # (
    (RPAREN,  r"\)"),                             # )
    (COMMA,   r","),                              # ,
    (OP,      r"[+\-*/:<>!&|]+"),                 # operators (multi-char ok)
    (IDENT,   r"[A-Za-z_][A-Za-z0-9_/]*"),       # identifiers (allow d/dt)
    (NEWLINE, r"\n"),                             # newline (tracked, not emitted)
]

_MASTER_RE = re.compile(
    "|".join(f"(?P<{kind}_{i}>{pat})" for i, (kind, pat) in enumerate(_TOKEN_PATTERNS))
)

# Map group name prefix back to token kind
_GROUP_KIND: dict[str, str] = {
    f"{kind}_{i}": kind for i, (kind, _) in enumerate(_TOKEN_PATTERNS)
}


# ---------------------------------------------------------------------------
# Lexer entry point
# ---------------------------------------------------------------------------

def tokenize(source: str, skip_comments: bool = True) -> List[Token]:
    """
    Tokenize a Mobius DSL source string.

    Parameters
    ----------
    source : str
        Raw text of the .mobius file.
    skip_comments : bool
        When True (default) COMMENT tokens are dropped from the output.

    Returns
    -------
    List[Token]
        Ordered list of tokens; NEWLINE tokens are always suppressed.
    """
    tokens: List[Token] = []
    line = 1
    line_start = 0

    for m in _MASTER_RE.finditer(source):
        # Identify which group matched
        group_name = m.lastgroup
        kind = _GROUP_KIND[group_name]
        value = m.group()
        col = m.start() - line_start + 1

        if kind == NEWLINE:
            line += 1
            line_start = m.end()
            continue

        if kind == COMMENT and skip_comments:
            continue

        # Promote matching identifiers to KEYWORD tokens.
        # Only promote if the token is ALL-CAPS (line-start equation keyword),
        # not the lowercase DSL function name used inside the body (e.g. piece(...)).
        if kind == IDENT and value in KEYWORDS:
            tokens.append(Token(KEYWORD, value, line, col))
        else:
            tokens.append(Token(kind, value, line, col))

    return tokens


def tokenize_file(path: str, skip_comments: bool = True) -> List[Token]:
    """
    Convenience wrapper: read a .mobius file and tokenize it.
    """
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    return tokenize(source, skip_comments=skip_comments)


# ---------------------------------------------------------------------------
# CLI helper
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python lexer.py <file.mobius>")
        sys.exit(1)

    toks = tokenize_file(sys.argv[1])
    for tok in toks:
        print(tok)
