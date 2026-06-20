"""
SAGCO Mobius DSL Parser
Board: BOARD-31-CELLPHONE-MOBIUS-LAB

Builds a MobiusAST from the token stream produced by lexer.py.

Grammar (simplified):
    mobius_file  ::= equation*
    equation     ::= KEYWORD  body NEWLINE?

    LIMIT body   ::= ':' lim_call '=' NUMBER
    DERIV body   ::= ':' deriv_call '=' NUMBER
    PIECE body   ::= ':' piece_call
    ASSERT body  ::= ':' assert_body
    INTEGRAL body ::= ':' integral_call '=' expr

    lim_call     ::= 'lim' '(' IDENT ',' IDENT ',' IDENT ')'
    deriv_call   ::= 'd/dt' '(' IDENT ',' IDENT ')'
    piece_call   ::= 'piece' '(' expr ',' IDENT ',' IDENT ')'
    assert_body  ::= 'if' '(' expr ')' 'when' '(' expr ')' 'then' '(' expr ')'
    integral_call ::= 'integral' '(' IDENT ',' expr ',' expr ')'

We parse line-by-line: the first KEYWORD on a (logical) line determines the
equation type; remaining tokens until the next KEYWORD are the body.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from lexer import Token, tokenize, tokenize_file, KEYWORD, IDENT, NUMBER, OP, LPAREN, RPAREN, COMMA, EQUALS, STRING


# ---------------------------------------------------------------------------
# AST nodes
# ---------------------------------------------------------------------------

@dataclass
class MobiusEquation:
    kind: str                      # LIMIT | DERIV | PIECE | ASSERT | INTEGRAL
    name: str                      # derived name (e.g. "cpu_load_steady_state")
    args: List[str]                # positional arguments extracted from call
    body: Dict[str, Any]           # structured body dict; content depends on kind
    raw_tokens: List[Token] = field(default_factory=list, repr=False)

    def __repr__(self) -> str:
        return f"MobiusEquation(kind={self.kind!r}, name={self.name!r}, args={self.args})"


@dataclass
class MobiusAST:
    equations: List[MobiusEquation] = field(default_factory=list)
    source_file: Optional[str] = None

    def __len__(self) -> int:
        return len(self.equations)

    def by_kind(self, kind: str) -> List[MobiusEquation]:
        return [eq for eq in self.equations if eq.kind == kind]


# ---------------------------------------------------------------------------
# Token stream helper
# ---------------------------------------------------------------------------

class TokenStream:
    def __init__(self, tokens: List[Token]):
        self._tokens = tokens
        self._pos = 0

    def peek(self) -> Optional[Token]:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def consume(self) -> Token:
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def expect(self, kind: str) -> Token:
        tok = self.peek()
        if tok is None or tok.kind != kind:
            raise SyntaxError(
                f"Expected token kind {kind!r} but got {tok!r} at pos {self._pos}"
            )
        return self.consume()

    def matches(self, kind: str, value: str = None) -> bool:
        tok = self.peek()
        if tok is None:
            return False
        if tok.kind != kind:
            return False
        if value is not None and tok.value.lower() != value.lower():
            return False
        return True

    def skip_while(self, *kinds: str):
        while self.peek() and self.peek().kind in kinds:
            self.consume()

    def collect_until_keyword(self) -> List[Token]:
        result = []
        while self.peek() and self.peek().kind != KEYWORD:
            result.append(self.consume())
        return result

    def remaining(self) -> int:
        return len(self._tokens) - self._pos


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------

def _collect_paren_args(stream: TokenStream) -> List[str]:
    """Consume '(' arg, arg, ... ')' and return args as strings."""
    stream.expect(LPAREN)
    args = []
    current = []
    depth = 1
    while stream.peek():
        tok = stream.consume()
        if tok.kind == LPAREN:
            depth += 1
            current.append(tok.value)
        elif tok.kind == RPAREN:
            depth -= 1
            if depth == 0:
                if current:
                    args.append(" ".join(current))
                break
            else:
                current.append(tok.value)
        elif tok.kind == COMMA and depth == 1:
            args.append(" ".join(current).strip())
            current = []
        else:
            current.append(tok.value)
    return args


def _join_tokens(tokens: List[Token]) -> str:
    return " ".join(t.value for t in tokens).strip()


def _derive_name(args: List[str], kind: str) -> str:
    """Make a snake_case name from first arg."""
    if not args:
        return kind.lower()
    base = re.sub(r"[^a-zA-Z0-9]", "_", args[0]).strip("_").lower()
    return base or kind.lower()


# ---------------------------------------------------------------------------
# Per-kind body parsers
# ---------------------------------------------------------------------------

def _parse_limit(stream: TokenStream, body_tokens: List[Token]) -> tuple[List[str], Dict]:
    """lim(cpu_load, t, steady_state) = 0.45"""
    bs = TokenStream(body_tokens)
    # skip optional colon and 'lim' ident
    bs.skip_while(OP, IDENT)  # skip ':' or 'lim' prefix

    # find lim call
    args: List[str] = []
    result_val: str = ""
    while bs.peek():
        tok = bs.peek()
        if tok.kind == LPAREN:
            # We're at the paren of lim(...)
            args = _collect_paren_args(bs)
        elif tok.kind == EQUALS:
            bs.consume()
            # rest is result
            rest = []
            while bs.peek():
                rest.append(bs.consume().value)
            result_val = " ".join(rest).strip()
        else:
            bs.consume()

    body = {
        "function": args[0] if len(args) > 0 else "",
        "variable": args[1] if len(args) > 1 else "",
        "approach": args[2] if len(args) > 2 else "",
        "result": result_val,
    }
    return args, body


def _parse_deriv(stream: TokenStream, body_tokens: List[Token]) -> tuple[List[str], Dict]:
    """d/dt(citizen_count, t) = 3449"""
    bs = TokenStream(body_tokens)
    args: List[str] = []
    result_val: str = ""
    while bs.peek():
        tok = bs.peek()
        if tok.kind == LPAREN:
            args = _collect_paren_args(bs)
        elif tok.kind == EQUALS:
            bs.consume()
            rest = []
            while bs.peek():
                rest.append(bs.consume().value)
            result_val = " ".join(rest).strip()
        else:
            bs.consume()
    body = {
        "function": args[0] if len(args) > 0 else "",
        "variable": args[1] if len(args) > 1 else "",
        "rate": result_val,
    }
    return args, body


def _parse_piece(stream: TokenStream, body_tokens: List[Token]) -> tuple[List[str], Dict]:
    """piece(severity == CRITICAL, open_case, log_only)"""
    bs = TokenStream(body_tokens)
    args: List[str] = []
    while bs.peek():
        tok = bs.peek()
        if tok.kind == LPAREN:
            args = _collect_paren_args(bs)
            break
        else:
            bs.consume()
    body = {
        "condition": args[0] if len(args) > 0 else "",
        "value_if_true": args[1] if len(args) > 1 else "",
        "value_if_false": args[2] if len(args) > 2 else "",
    }
    return args, body


def _parse_assert(stream: TokenStream, body_tokens: List[Token]) -> tuple[List[str], Dict]:
    """if(token_in_url) when(browser_nav) then(fire_antibody BROWSER_TOKEN_IN_REFERRER)"""
    bs = TokenStream(body_tokens)
    sections: Dict[str, str] = {}
    current_key: Optional[str] = None

    while bs.peek():
        tok = bs.peek()
        if tok.kind == IDENT and tok.value.lower() in ("if", "when", "then"):
            current_key = tok.value.lower()
            bs.consume()
            if bs.matches(LPAREN):
                args = _collect_paren_args(bs)
                sections[current_key] = " ".join(args).strip()
        else:
            bs.consume()

    args_list = [sections.get("if", ""), sections.get("when", ""), sections.get("then", "")]
    body = {
        "if_expr": sections.get("if", ""),
        "when_cond": sections.get("when", ""),
        "then_action": sections.get("then", ""),
    }
    return args_list, body


def _parse_integral(stream: TokenStream, body_tokens: List[Token]) -> tuple[List[str], Dict]:
    """integral(f, a, b) = cumulative"""
    bs = TokenStream(body_tokens)
    args: List[str] = []
    result_val: str = ""
    while bs.peek():
        tok = bs.peek()
        if tok.kind == LPAREN:
            args = _collect_paren_args(bs)
        elif tok.kind == EQUALS:
            bs.consume()
            rest = []
            while bs.peek():
                rest.append(bs.consume().value)
            result_val = " ".join(rest).strip()
        else:
            bs.consume()
    body = {
        "function": args[0] if len(args) > 0 else "",
        "lower_bound": args[1] if len(args) > 1 else "",
        "upper_bound": args[2] if len(args) > 2 else "",
        "result": result_val,
    }
    return args, body


_KIND_PARSERS = {
    "LIMIT":    _parse_limit,
    "DERIV":    _parse_deriv,
    "PIECE":    _parse_piece,
    "ASSERT":   _parse_assert,
    "INTEGRAL": _parse_integral,
}


# ---------------------------------------------------------------------------
# Main parse function
# ---------------------------------------------------------------------------

def parse(tokens, source_file: str = None) -> MobiusAST:
    """
    Build a MobiusAST from a list of tokens OR a raw DSL source string.

    Parameters
    ----------
    tokens : List[Token] or str
        Either the output of lexer.tokenize() or a raw .mobius source string.
        Passing a string is a convenience shortcut (comments are stripped).
    source_file : str, optional
        Path hint stored in the AST for reporting.

    Returns
    -------
    MobiusAST
    """
    if isinstance(tokens, str):
        tokens = tokenize(tokens, skip_comments=True)

    ast = MobiusAST(source_file=source_file)
    stream = TokenStream(tokens)

    while stream.peek():
        tok = stream.peek()

        if tok.kind != KEYWORD:
            # Skip any loose tokens between equations
            stream.consume()
            continue

        keyword_tok = stream.consume()
        kind = keyword_tok.value  # Already uppercased by lexer

        # Collect all tokens until the next KEYWORD (= one equation body)
        body_tokens = stream.collect_until_keyword()

        parser_fn = _KIND_PARSERS.get(kind)
        if parser_fn is None:
            # Unknown keyword — store as raw
            eq = MobiusEquation(
                kind=kind,
                name=kind.lower(),
                args=[],
                body={"raw": _join_tokens(body_tokens)},
                raw_tokens=body_tokens,
            )
        else:
            args, body = parser_fn(stream, body_tokens)
            name = _derive_name(args, kind)
            eq = MobiusEquation(
                kind=kind,
                name=name,
                args=args,
                body=body,
                raw_tokens=body_tokens,
            )

        ast.equations.append(eq)

    return ast


def parse_source(source: str) -> "MobiusAST":
    """Parse raw DSL source text (not a token list)."""
    tokens = tokenize(source, skip_comments=True)
    return parse(tokens)


def parse_file(path: str) -> MobiusAST:
    """
    Convenience: lex and parse a .mobius file in one call.
    """
    tokens = tokenize_file(path, skip_comments=True)
    return parse(tokens, source_file=path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python parser.py <file.mobius>")
        sys.exit(1)

    ast = parse_file(sys.argv[1])
    print(f"Parsed {len(ast)} equations from {sys.argv[1]}")
    for eq in ast.equations:
        print(f"  {eq}")
        print(f"    body: {eq.body}")
