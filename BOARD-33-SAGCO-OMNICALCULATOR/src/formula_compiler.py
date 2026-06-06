#!/usr/bin/env python3
"""
BOARD-33 Formula Compiler
  Excel formula → SAGCO AST → bytecode
  Mobius .mobius → AST → Python callable

Usage:
  python formula_compiler.py ast "SUM(A1:A10) + IF(B1>0, B1, 0)"
  python formula_compiler.py compile "=IF(A1>100, A1*0.9, A1)"
  python formula_compiler.py mobius equations.mobius
  python formula_compiler.py explain "SUM(A1:A10)/COUNT(A1:A10)"
"""

from __future__ import annotations
import re, sys, ast as pyast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ── Excel Formula Lexer ───────────────────────────────────────────────────────

EXCEL_FUNCTIONS = {
    "SUM", "AVERAGE", "COUNT", "COUNTA", "MAX", "MIN", "IF", "IFS",
    "VLOOKUP", "HLOOKUP", "INDEX", "MATCH", "SUMIF", "COUNTIF", "AVERAGEIF",
    "LEFT", "RIGHT", "MID", "LEN", "TRIM", "UPPER", "LOWER", "CONCATENATE",
    "TEXT", "VALUE", "DATE", "TODAY", "NOW", "YEAR", "MONTH", "DAY",
    "ROUND", "FLOOR", "CEILING", "ABS", "SQRT", "LN", "LOG", "EXP",
    "AND", "OR", "NOT", "IFERROR", "ISBLANK", "ISNUMBER", "ISTEXT",
    "NPV", "IRR", "PMT", "PV", "FV", "RATE",
}

@dataclass
class FormulaToken:
    kind:  str   # FUNC, REF, RANGE, NUMBER, STRING, OP, LPAREN, RPAREN, COMMA
    value: str

_RANGE_P  = re.compile(r'([A-Z]+\d+):([A-Z]+\d+)')
_REF_P    = re.compile(r'\$?([A-Z]+)\$?(\d+)')
_FUNC_P   = re.compile(r'([A-Z][A-Z0-9_]*)\s*\(')
_NUM_P    = re.compile(r'-?\d+\.?\d*([eE][+-]?\d+)?')
_STR_P    = re.compile(r'"[^"]*"')


def lex_formula(formula: str) -> list[FormulaToken]:
    if formula.startswith("="):
        formula = formula[1:]
    tokens = []
    i = 0
    while i < len(formula):
        if formula[i].isspace():
            i += 1; continue
        # Range
        m = _RANGE_P.match(formula, i)
        if m:
            tokens.append(FormulaToken("RANGE", m.group()))
            i = m.end(); continue
        # Function call
        m = _FUNC_P.match(formula, i)
        if m:
            name = m.group(1)
            kind = "FUNC" if name in EXCEL_FUNCTIONS else "IDENT"
            tokens.append(FormulaToken(kind, name))
            tokens.append(FormulaToken("LPAREN", "("))
            i = m.end(); continue
        # Cell ref
        m = _REF_P.match(formula, i)
        if m:
            tokens.append(FormulaToken("REF", m.group()))
            i = m.end(); continue
        # Number
        m = _NUM_P.match(formula, i)
        if m:
            tokens.append(FormulaToken("NUMBER", m.group()))
            i = m.end(); continue
        # String
        m = _STR_P.match(formula, i)
        if m:
            tokens.append(FormulaToken("STRING", m.group()))
            i = m.end(); continue
        # Operators and punctuation
        ch = formula[i]
        if ch in "()":
            tokens.append(FormulaToken("LPAREN" if ch == "(" else "RPAREN", ch))
        elif ch == ",":
            tokens.append(FormulaToken("COMMA", ch))
        elif ch in "+-*/^&<>=!%":
            tokens.append(FormulaToken("OP", ch))
        i += 1
    return tokens


# ── AST Node ──────────────────────────────────────────────────────────────────

@dataclass
class ASTNode:
    kind:     str
    value:    str = ""
    children: list["ASTNode"] = field(default_factory=list)

    def pretty(self, indent: int = 0) -> str:
        prefix = "  " * indent
        lines  = [f"{prefix}{self.kind}({self.value!r})"]
        for child in self.children:
            lines.append(child.pretty(indent + 1))
        return "\n".join(lines)

    def to_python(self) -> str:
        if self.kind == "NUMBER":  return self.value
        if self.kind == "STRING":  return self.value
        if self.kind == "REF":     return f'cells.get("{self.value}", 0)'
        if self.kind == "RANGE":   return f'range_sum("{self.value}")'
        if self.kind == "OP":
            return f"({self.children[0].to_python()} {self.value} {self.children[1].to_python()})"
        if self.kind == "FUNC":
            args = ", ".join(c.to_python() for c in self.children)
            fn_map = {
                "SUM": "sum([{args}])", "AVERAGE": "(sum([{args}])/len([{args}]))",
                "MAX": "max([{args}])", "MIN": "min([{args}])",
                "IF": "({args0} if {args1} else {args2})",
                "ABS": "abs({args})", "SQRT": "math.sqrt({args})",
                "LN": "math.log({args})", "ROUND": "round({args})",
            }
            if self.value in fn_map:
                return fn_map[self.value].format(args=args, args0=args,
                    args1=self.children[1].to_python() if len(self.children) > 1 else "",
                    args2=self.children[2].to_python() if len(self.children) > 2 else "")
            return f"{self.value.lower()}({args})"
        return self.value


# ── Formula Parser (recursive descent) ───────────────────────────────────────

class FormulaParser:
    def __init__(self, tokens: list[FormulaToken]):
        self.tokens = tokens
        self.pos    = 0

    def peek(self) -> FormulaToken | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self) -> FormulaToken:
        t = self.tokens[self.pos]; self.pos += 1; return t

    def parse(self) -> ASTNode:
        return self.expr()

    def expr(self) -> ASTNode:
        left = self.term()
        while self.peek() and self.peek().kind == "OP" and self.peek().value in "+-&":
            op   = self.consume()
            right= self.term()
            node = ASTNode("OP", op.value)
            node.children = [left, right]
            left = node
        return left

    def term(self) -> ASTNode:
        left = self.factor()
        while self.peek() and self.peek().kind == "OP" and self.peek().value in "*/^":
            op    = self.consume()
            right = self.factor()
            node  = ASTNode("OP", op.value)
            node.children = [left, right]
            left  = node
        return left

    def factor(self) -> ASTNode:
        tok = self.peek()
        if not tok:
            return ASTNode("NULL")
        if tok.kind in ("NUMBER", "STRING"):
            self.consume()
            return ASTNode(tok.kind, tok.value)
        if tok.kind == "RANGE":
            self.consume()
            return ASTNode("RANGE", tok.value)
        if tok.kind == "REF":
            self.consume()
            return ASTNode("REF", tok.value)
        if tok.kind in ("FUNC", "IDENT"):
            name = self.consume().value
            node = ASTNode("FUNC", name)
            if self.peek() and self.peek().kind == "LPAREN":
                self.consume()  # (
                while self.peek() and self.peek().kind != "RPAREN":
                    if self.peek().kind == "COMMA":
                        self.consume(); continue
                    node.children.append(self.expr())
                if self.peek():
                    self.consume()  # )
            return node
        if tok.kind == "LPAREN":
            self.consume()
            inner = self.expr()
            if self.peek() and self.peek().kind == "RPAREN":
                self.consume()
            return inner
        if tok.kind == "OP" and tok.value in "<>=!":
            op = self.consume()
            right = self.factor()
            node = ASTNode("OP", op.value)
            node.children.append(right)
            return node
        self.consume()
        return ASTNode("UNKNOWN", tok.value)


def parse_formula(formula: str) -> ASTNode:
    tokens = lex_formula(formula)
    return FormulaParser(tokens).parse()


# ── Explain mode — ERU on every formula ──────────────────────────────────────

FUNC_EXPLANATIONS = {
    "SUM":     "Adds all values in range. Expected: numeric sum. Variance if empty cells exist.",
    "AVERAGE": "Mean of range. Expected: central value. Variance: sensitive to outliers.",
    "IF":      "Conditional branch. Expected: boolean gate. Variance: unhandled edge cases.",
    "VLOOKUP": "Vertical lookup. Expected: match found. Variance: #N/A if key missing.",
    "COUNT":   "Counts numeric cells. Expected: cell count. Variance: text cells excluded.",
    "SUMIF":   "Conditional sum. Expected: filtered total. Variance: criteria type mismatch.",
}


def explain_formula(formula: str) -> str:
    tokens = lex_formula(formula)
    funcs  = [t.value for t in tokens if t.kind == "FUNC"]
    refs   = [t.value for t in tokens if t.kind == "REF"]
    ranges = [t.value for t in tokens if t.kind == "RANGE"]

    lines = [f"\n  Formula: {formula}",
             f"  Functions used: {', '.join(funcs) or 'none'}",
             f"  Cell refs: {', '.join(refs) or 'none'}",
             f"  Ranges: {', '.join(ranges) or 'none'}",
             ""]
    for fn in funcs:
        if fn in FUNC_EXPLANATIONS:
            lines.append(f"  [{fn}] {FUNC_EXPLANATIONS[fn]}")
    lines.append("")
    lines.append(f"  ERU:")
    lines.append(f"  Expected: formula produces correct result for all valid inputs")
    lines.append(f"  Actual:   depends on cell values at runtime")
    lines.append(f"  Variance: check for empty ranges, type mismatches, circular refs")
    return "\n".join(lines)


# ── Mobius compiler ───────────────────────────────────────────────────────────

def compile_mobius(path: Path) -> str:
    from .math_engine import _sym  # noqa
    lines = path.read_text().splitlines()
    compiled = ["# Compiled from Mobius DSL by SAGCO BOARD-33",
                "# DO NOT EDIT — regenerate with: sagco omni mobius <file>", ""]
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            compiled.append(line)
            continue
        if stripped.startswith("ASSERT:") or stripped.startswith("ASSERT "):
            rest = re.sub(r'^ASSERT\s*:?\s*', '', stripped)
            compiled.append(f"# ASSERT: {rest}")
            # parse if/when/then
            m = re.match(r'if\s*\((.+?)\)\s*when\s*\((.+?)\)\s*then\s*\((.+?)\)', rest)
            if m:
                cond, context, action = m.groups()
                compiled.append(f"def assert_{abs(hash(rest))%10000:04d}(event):")
                compiled.append(f'    """SAGCO ASSERT: if({cond}) when({context}) then({action})"""')
                compiled.append(f"    if event.get('context') == '{context.strip()}':")
                compiled.append(f"        return bool(event.get('data', {{}}).get('{cond.strip()}'))")
                compiled.append(f"    return None  # not applicable")
                compiled.append("")
        else:
            compiled.append(f"# {stripped}")
    return "\n".join(compiled)


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        print(__doc__); return

    op   = args[0].lower()
    rest = args[1:]

    if op == "ast" and rest:
        node = parse_formula(rest[0])
        print(f"\n  AST for: {rest[0]}")
        print(node.pretty())

    elif op == "compile" and rest:
        node   = parse_formula(rest[0])
        python = node.to_python()
        print(f"\n  Compiled: {rest[0]}")
        print(f"  Python  : {python}")

    elif op == "explain" and rest:
        print(explain_formula(rest[0]))

    elif op == "mobius" and rest:
        path   = Path(rest[0])
        result = compile_mobius(path)
        out    = path.with_suffix(".py")
        out.write_text(result)
        print(f"\n  Compiled {path.name} → {out.name}")
        print(result[:500])

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
