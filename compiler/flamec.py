#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
 FlameLang Reference Interpreter v0.1.0 (M1)
 Strategickhaos DAO LLC | EIN 39-2900295
 Inventor: Domenic Gabriel Garza (Me10101)
 Classification: NOVEL

 This is the M1 milestone: a tree-walking interpreter that makes FlameLang
 a real, executable programming language.

 Usage:
   python3 flamec.py <file.flm>           # Run a FlameLang program
   python3 flamec.py --ast <file.flm>     # Print AST (debug)
   python3 flamec.py --tokens <file.flm>  # Print tokens (debug)
   echo 'print(2 + 3);' | python3 flamec.py --stdin

 M1 Feature Set:
   - Integer and float literals
   - String literals
   - Arithmetic: + - * / %
   - Comparison: == != < > <= >=
   - Boolean: and or not true false
   - Variables: let x = expr;
   - Assignment: x = expr;
   - Print: print(expr);
   - Blocks: { ... }
   - If/else: if (cond) { ... } else { ... }
   - While: while (cond) { ... }
   - Functions: fn name(params) { ... }
   - Return: return expr;
   - Comments: // single line, /* multi line */
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# TOKENS
# ═══════════════════════════════════════════════════════════════════════════════

class TT(Enum):
    """Token types for FlameLang."""
    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    IDENT = auto()

    # Keywords
    LET = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    PRINT = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQ = auto()
    EQEQ = auto()
    BANGEQ = auto()
    LT = auto()
    GT = auto()
    LTEQ = auto()
    GTEQ = auto()
    BANG = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMI = auto()

    # Special
    EOF = auto()


KEYWORDS = {
    "let": TT.LET, "fn": TT.FN, "return": TT.RETURN,
    "if": TT.IF, "else": TT.ELSE, "while": TT.WHILE,
    "true": TT.TRUE, "false": TT.FALSE,
    "and": TT.AND, "or": TT.OR, "not": TT.NOT,
    "print": TT.PRINT,
}


@dataclass
class Token:
    type: TT
    value: Any
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:{self.col})"


# ═══════════════════════════════════════════════════════════════════════════════
# LEXER
# ═══════════════════════════════════════════════════════════════════════════════

class LexerError(Exception):
    pass


class Lexer:
    """Tokenizes FlameLang source code."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: list[Token] = []

    def _peek(self) -> str:
        if self.pos >= len(self.source):
            return '\0'
        return self.source[self.pos]

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self.pos >= len(self.source) or self.source[self.pos] != expected:
            return False
        self._advance()
        return True

    def _add(self, tt: TT, value: Any = None):
        self.tokens.append(Token(tt, value, self.line, self.col))

    def tokenize(self) -> list[Token]:
        while self.pos < len(self.source):
            ch = self._peek()

            # Whitespace
            if ch in ' \t\r\n':
                self._advance()
                continue

            # Comments
            if ch == '/' and self.pos + 1 < len(self.source):
                next_ch = self.source[self.pos + 1]
                if next_ch == '/':
                    while self.pos < len(self.source) and self._peek() != '\n':
                        self._advance()
                    continue
                if next_ch == '*':
                    self._advance()  # /
                    self._advance()  # *
                    while self.pos < len(self.source) - 1:
                        if self._peek() == '*' and self.source[self.pos + 1] == '/':
                            self._advance()  # *
                            self._advance()  # /
                            break
                        self._advance()
                    continue

            # Numbers
            if ch.isdigit():
                self._read_number()
                continue

            # Strings
            if ch == '"':
                self._read_string()
                continue

            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                self._read_ident()
                continue

            # Two-char operators
            start_col = self.col
            self._advance()
            if ch == '=' and self._match('='):
                self._add(TT.EQEQ, "==")
            elif ch == '!' and self._match('='):
                self._add(TT.BANGEQ, "!=")
            elif ch == '<' and self._match('='):
                self._add(TT.LTEQ, "<=")
            elif ch == '>' and self._match('='):
                self._add(TT.GTEQ, ">=")
            # Single-char
            elif ch == '=':
                self._add(TT.EQ, "=")
            elif ch == '!':
                self._add(TT.BANG, "!")
            elif ch == '<':
                self._add(TT.LT, "<")
            elif ch == '>':
                self._add(TT.GT, ">")
            elif ch == '+':
                self._add(TT.PLUS, "+")
            elif ch == '-':
                self._add(TT.MINUS, "-")
            elif ch == '*':
                self._add(TT.STAR, "*")
            elif ch == '/':
                self._add(TT.SLASH, "/")
            elif ch == '%':
                self._add(TT.PERCENT, "%")
            elif ch == '(':
                self._add(TT.LPAREN, "(")
            elif ch == ')':
                self._add(TT.RPAREN, ")")
            elif ch == '{':
                self._add(TT.LBRACE, "{")
            elif ch == '}':
                self._add(TT.RBRACE, "}")
            elif ch == ',':
                self._add(TT.COMMA, ",")
            elif ch == ';':
                self._add(TT.SEMI, ";")
            else:
                raise LexerError(f"Unexpected character '{ch}' at L{self.line}:{start_col}")

        self._add(TT.EOF)
        return self.tokens

    def _read_number(self):
        start = self.pos
        is_float = False
        while self.pos < len(self.source) and (self._peek().isdigit() or self._peek() == '.'):
            if self._peek() == '.':
                if is_float:
                    break
                is_float = True
            self._advance()
        text = self.source[start:self.pos]
        if is_float:
            self._add(TT.FLOAT, float(text))
        else:
            self._add(TT.INT, int(text))

    def _read_string(self):
        self._advance()  # opening "
        start = self.pos
        while self.pos < len(self.source) and self._peek() != '"':
            if self._peek() == '\n':
                raise LexerError(f"Unterminated string at L{self.line}")
            self._advance()
        if self.pos >= len(self.source):
            raise LexerError(f"Unterminated string at L{self.line}")
        text = self.source[start:self.pos]
        self._advance()  # closing "
        self._add(TT.STRING, text)

    def _read_ident(self):
        start = self.pos
        while self.pos < len(self.source) and (self._peek().isalnum() or self._peek() == '_'):
            self._advance()
        text = self.source[start:self.pos]
        tt = KEYWORDS.get(text, TT.IDENT)
        self._add(tt, text)


# ═══════════════════════════════════════════════════════════════════════════════
# AST NODES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Program:
    statements: list

@dataclass
class IntLit:
    value: int

@dataclass
class FloatLit:
    value: float

@dataclass
class StringLit:
    value: str

@dataclass
class BoolLit:
    value: bool

@dataclass
class Ident:
    name: str

@dataclass
class BinOp:
    op: str
    left: Any
    right: Any

@dataclass
class UnaryOp:
    op: str
    operand: Any

@dataclass
class LetStmt:
    name: str
    init: Any

@dataclass
class AssignStmt:
    name: str
    value: Any

@dataclass
class PrintStmt:
    expr: Any

@dataclass
class Block:
    statements: list

@dataclass
class IfStmt:
    condition: Any
    then_block: Any
    else_block: Any = None

@dataclass
class WhileStmt:
    condition: Any
    body: Any

@dataclass
class FnDecl:
    name: str
    params: list
    body: Any

@dataclass
class CallExpr:
    callee: str
    args: list

@dataclass
class ReturnStmt:
    value: Any = None


# ═══════════════════════════════════════════════════════════════════════════════
# PARSER (Recursive Descent)
# ═══════════════════════════════════════════════════════════════════════════════

class ParseError(Exception):
    pass


class Parser:
    """Recursive descent parser for FlameLang."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _check(self, tt: TT) -> bool:
        return self._peek().type == tt

    def _match(self, *types: TT) -> Optional[Token]:
        for tt in types:
            if self._check(tt):
                return self._advance()
        return None

    def _expect(self, tt: TT, msg: str = "") -> Token:
        tok = self._match(tt)
        if tok is None:
            p = self._peek()
            raise ParseError(f"Expected {tt.name} but got {p.type.name} ({p.value!r}) at L{p.line}:{p.col}. {msg}")
        return tok

    # ── Top Level ──

    def parse(self) -> Program:
        stmts = []
        while not self._check(TT.EOF):
            stmts.append(self._declaration())
        return Program(stmts)

    def _declaration(self):
        if self._check(TT.FN):
            return self._fn_decl()
        if self._check(TT.LET):
            return self._let_stmt()
        return self._statement()

    def _fn_decl(self):
        self._advance()  # fn
        name = self._expect(TT.IDENT, "Expected function name").value
        self._expect(TT.LPAREN)
        params = []
        if not self._check(TT.RPAREN):
            params.append(self._expect(TT.IDENT).value)
            while self._match(TT.COMMA):
                params.append(self._expect(TT.IDENT).value)
        self._expect(TT.RPAREN)
        body = self._block()
        return FnDecl(name, params, body)

    def _let_stmt(self):
        self._advance()  # let
        name = self._expect(TT.IDENT, "Expected variable name").value
        self._expect(TT.EQ, "Expected '=' after variable name")
        init = self._expression()
        self._expect(TT.SEMI, "Expected ';' after let statement")
        return LetStmt(name, init)

    # ── Statements ──

    def _statement(self):
        if self._check(TT.PRINT):
            return self._print_stmt()
        if self._check(TT.IF):
            return self._if_stmt()
        if self._check(TT.WHILE):
            return self._while_stmt()
        if self._check(TT.RETURN):
            return self._return_stmt()
        if self._check(TT.LBRACE):
            return self._block()
        # Assignment or expression statement
        if self._check(TT.IDENT) and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TT.EQ:
            name = self._advance().value
            self._advance()  # =
            value = self._expression()
            self._expect(TT.SEMI)
            return AssignStmt(name, value)
        # Expression statement
        expr = self._expression()
        self._expect(TT.SEMI, "Expected ';' after expression")
        return expr

    def _print_stmt(self):
        self._advance()  # print
        self._expect(TT.LPAREN)
        expr = self._expression()
        self._expect(TT.RPAREN)
        self._expect(TT.SEMI, "Expected ';' after print")
        return PrintStmt(expr)

    def _if_stmt(self):
        self._advance()  # if
        self._expect(TT.LPAREN)
        cond = self._expression()
        self._expect(TT.RPAREN)
        then = self._block()
        else_block = None
        if self._match(TT.ELSE):
            if self._check(TT.IF):
                else_block = self._if_stmt()
            else:
                else_block = self._block()
        return IfStmt(cond, then, else_block)

    def _while_stmt(self):
        self._advance()  # while
        self._expect(TT.LPAREN)
        cond = self._expression()
        self._expect(TT.RPAREN)
        body = self._block()
        return WhileStmt(cond, body)

    def _return_stmt(self):
        self._advance()  # return
        value = None
        if not self._check(TT.SEMI):
            value = self._expression()
        self._expect(TT.SEMI)
        return ReturnStmt(value)

    def _block(self):
        self._expect(TT.LBRACE)
        stmts = []
        while not self._check(TT.RBRACE) and not self._check(TT.EOF):
            stmts.append(self._declaration())
        self._expect(TT.RBRACE, "Expected '}'")
        return Block(stmts)

    # ── Expressions (Pratt-style precedence) ──

    def _expression(self):
        return self._or_expr()

    def _or_expr(self):
        left = self._and_expr()
        while self._match(TT.OR):
            right = self._and_expr()
            left = BinOp("or", left, right)
        return left

    def _and_expr(self):
        left = self._equality()
        while self._match(TT.AND):
            right = self._equality()
            left = BinOp("and", left, right)
        return left

    def _equality(self):
        left = self._comparison()
        while True:
            tok = self._match(TT.EQEQ, TT.BANGEQ)
            if not tok:
                break
            right = self._comparison()
            left = BinOp(tok.value, left, right)
        return left

    def _comparison(self):
        left = self._addition()
        while True:
            tok = self._match(TT.LT, TT.GT, TT.LTEQ, TT.GTEQ)
            if not tok:
                break
            right = self._addition()
            left = BinOp(tok.value, left, right)
        return left

    def _addition(self):
        left = self._multiplication()
        while True:
            tok = self._match(TT.PLUS, TT.MINUS)
            if not tok:
                break
            right = self._multiplication()
            left = BinOp(tok.value, left, right)
        return left

    def _multiplication(self):
        left = self._unary()
        while True:
            tok = self._match(TT.STAR, TT.SLASH, TT.PERCENT)
            if not tok:
                break
            right = self._unary()
            left = BinOp(tok.value, left, right)
        return left

    def _unary(self):
        tok = self._match(TT.MINUS, TT.NOT, TT.BANG)
        if tok:
            operand = self._unary()
            return UnaryOp(tok.value, operand)
        return self._call()

    def _call(self):
        expr = self._primary()
        if isinstance(expr, Ident) and self._match(TT.LPAREN):
            args = []
            if not self._check(TT.RPAREN):
                args.append(self._expression())
                while self._match(TT.COMMA):
                    args.append(self._expression())
            self._expect(TT.RPAREN)
            return CallExpr(expr.name, args)
        return expr

    def _primary(self):
        tok = self._match(TT.INT)
        if tok:
            return IntLit(tok.value)

        tok = self._match(TT.FLOAT)
        if tok:
            return FloatLit(tok.value)

        tok = self._match(TT.STRING)
        if tok:
            return StringLit(tok.value)

        tok = self._match(TT.TRUE)
        if tok:
            return BoolLit(True)

        tok = self._match(TT.FALSE)
        if tok:
            return BoolLit(False)

        tok = self._match(TT.IDENT)
        if tok:
            return Ident(tok.value)

        if self._match(TT.LPAREN):
            expr = self._expression()
            self._expect(TT.RPAREN, "Expected ')' after expression")
            return expr

        p = self._peek()
        raise ParseError(f"Unexpected token {p.type.name} ({p.value!r}) at L{p.line}:{p.col}")


# ═══════════════════════════════════════════════════════════════════════════════
# INTERPRETER (Tree-Walking)
# ═══════════════════════════════════════════════════════════════════════════════

class ReturnSignal(Exception):
    """Used to unwind the call stack on return."""
    def __init__(self, value):
        self.value = value


class RuntimeError_(Exception):
    pass


class Environment:
    """Variable scope with lexical chaining."""

    def __init__(self, parent=None):
        self.values: dict[str, Any] = {}
        self.parent: Optional[Environment] = parent

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError_(f"Undefined variable '{name}'")

    def set(self, name: str, value: Any):
        self.values[name] = value

    def assign(self, name: str, value: Any):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise RuntimeError_(f"Undefined variable '{name}'")


@dataclass
class FlameFunction:
    """Runtime representation of a user-defined function."""
    name: str
    params: list
    body: Block
    closure: Environment


class Interpreter:
    """Tree-walking interpreter for FlameLang AST."""

    def __init__(self):
        self.global_env = Environment()
        self.output: list[str] = []  # Captured output for testing

        # Built-in functions
        self.builtins = {
            "len": lambda args: self._builtin_len(args),
            "str": lambda args: str(args[0]),
            "int": lambda args: int(args[0]),
            "float": lambda args: float(args[0]),
            "abs": lambda args: abs(args[0]),
            "min": lambda args: min(args),
            "max": lambda args: max(args),
        }

    def interpret(self, program: Program):
        """Execute a program."""
        for stmt in program.statements:
            self._execute(stmt, self.global_env)

    def _execute(self, node, env: Environment):
        """Execute a statement node."""
        if isinstance(node, LetStmt):
            value = self._evaluate(node.init, env)
            env.set(node.name, value)

        elif isinstance(node, AssignStmt):
            value = self._evaluate(node.value, env)
            env.assign(node.name, value)

        elif isinstance(node, PrintStmt):
            value = self._evaluate(node.expr, env)
            text = self._stringify(value)
            print(text)
            self.output.append(text)

        elif isinstance(node, Block):
            child_env = Environment(parent=env)
            for stmt in node.statements:
                self._execute(stmt, child_env)

        elif isinstance(node, IfStmt):
            cond = self._evaluate(node.condition, env)
            if self._truthy(cond):
                self._execute(node.then_block, env)
            elif node.else_block:
                self._execute(node.else_block, env)

        elif isinstance(node, WhileStmt):
            while self._truthy(self._evaluate(node.condition, env)):
                self._execute(node.body, env)

        elif isinstance(node, FnDecl):
            fn = FlameFunction(node.name, node.params, node.body, env)
            env.set(node.name, fn)

        elif isinstance(node, ReturnStmt):
            value = None
            if node.value is not None:
                value = self._evaluate(node.value, env)
            raise ReturnSignal(value)

        else:
            # Expression statement
            self._evaluate(node, env)

    def _evaluate(self, node, env: Environment) -> Any:
        """Evaluate an expression node and return its value."""

        if isinstance(node, IntLit):
            return node.value

        if isinstance(node, FloatLit):
            return node.value

        if isinstance(node, StringLit):
            return node.value

        if isinstance(node, BoolLit):
            return node.value

        if isinstance(node, Ident):
            return env.get(node.name)

        if isinstance(node, UnaryOp):
            val = self._evaluate(node.operand, env)
            if node.op == '-':
                return -val
            if node.op in ('not', '!'):
                return not self._truthy(val)
            raise RuntimeError_(f"Unknown unary operator '{node.op}'")

        if isinstance(node, BinOp):
            left = self._evaluate(node.left, env)

            # Short-circuit for logical ops
            if node.op == 'and':
                if not self._truthy(left):
                    return left
                return self._evaluate(node.right, env)
            if node.op == 'or':
                if self._truthy(left):
                    return left
                return self._evaluate(node.right, env)

            right = self._evaluate(node.right, env)

            if node.op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return self._stringify(left) + self._stringify(right)
                return left + right
            if node.op == '-':
                return left - right
            if node.op == '*':
                return left * right
            if node.op == '/':
                if right == 0:
                    raise RuntimeError_("Division by zero")
                if isinstance(left, int) and isinstance(right, int):
                    return left // right
                return left / right
            if node.op == '%':
                if right == 0:
                    raise RuntimeError_("Modulo by zero")
                return left % right
            if node.op == '==':
                return left == right
            if node.op == '!=':
                return left != right
            if node.op == '<':
                return left < right
            if node.op == '>':
                return left > right
            if node.op == '<=':
                return left <= right
            if node.op == '>=':
                return left >= right

            raise RuntimeError_(f"Unknown binary operator '{node.op}'")

        if isinstance(node, CallExpr):
            # Check builtins first
            if node.callee in self.builtins:
                args = [self._evaluate(a, env) for a in node.args]
                return self.builtins[node.callee](args)

            fn = env.get(node.callee)
            if not isinstance(fn, FlameFunction):
                raise RuntimeError_(f"'{node.callee}' is not a function")

            if len(node.args) != len(fn.params):
                raise RuntimeError_(
                    f"Function '{fn.name}' expects {len(fn.params)} args, got {len(node.args)}")

            args = [self._evaluate(a, env) for a in node.args]
            call_env = Environment(parent=fn.closure)
            for param, arg in zip(fn.params, args):
                call_env.set(param, arg)

            try:
                self._execute(fn.body, call_env)
            except ReturnSignal as r:
                return r.value
            return None

        raise RuntimeError_(f"Cannot evaluate {type(node).__name__}")

    def _truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True

    def _stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        return str(value)

    def _builtin_len(self, args):
        if len(args) != 1:
            raise RuntimeError_("len() takes exactly 1 argument")
        if isinstance(args[0], str):
            return len(args[0])
        raise RuntimeError_("len() argument must be a string")


# ═══════════════════════════════════════════════════════════════════════════════
# AST PRINTER (Debug)
# ═══════════════════════════════════════════════════════════════════════════════

def print_ast(node, indent=0):
    """Pretty-print AST for debugging."""
    pad = "  " * indent
    name = type(node).__name__

    if isinstance(node, Program):
        print(f"{pad}Program")
        for s in node.statements:
            print_ast(s, indent + 1)
    elif isinstance(node, IntLit):
        print(f"{pad}Int({node.value})")
    elif isinstance(node, FloatLit):
        print(f"{pad}Float({node.value})")
    elif isinstance(node, StringLit):
        print(f"{pad}String({node.value!r})")
    elif isinstance(node, BoolLit):
        print(f"{pad}Bool({node.value})")
    elif isinstance(node, Ident):
        print(f"{pad}Ident({node.name})")
    elif isinstance(node, BinOp):
        print(f"{pad}BinOp({node.op})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, UnaryOp):
        print(f"{pad}Unary({node.op})")
        print_ast(node.operand, indent + 1)
    elif isinstance(node, LetStmt):
        print(f"{pad}Let({node.name})")
        print_ast(node.init, indent + 1)
    elif isinstance(node, AssignStmt):
        print(f"{pad}Assign({node.name})")
        print_ast(node.value, indent + 1)
    elif isinstance(node, PrintStmt):
        print(f"{pad}Print")
        print_ast(node.expr, indent + 1)
    elif isinstance(node, Block):
        print(f"{pad}Block")
        for s in node.statements:
            print_ast(s, indent + 1)
    elif isinstance(node, IfStmt):
        print(f"{pad}If")
        print_ast(node.condition, indent + 1)
        print_ast(node.then_block, indent + 1)
        if node.else_block:
            print(f"{pad}Else")
            print_ast(node.else_block, indent + 1)
    elif isinstance(node, WhileStmt):
        print(f"{pad}While")
        print_ast(node.condition, indent + 1)
        print_ast(node.body, indent + 1)
    elif isinstance(node, FnDecl):
        print(f"{pad}Fn({node.name})[{', '.join(node.params)}]")
        print_ast(node.body, indent + 1)
    elif isinstance(node, CallExpr):
        print(f"{pad}Call({node.callee})")
        for a in node.args:
            print_ast(a, indent + 1)
    elif isinstance(node, ReturnStmt):
        print(f"{pad}Return")
        if node.value:
            print_ast(node.value, indent + 1)
    else:
        print(f"{pad}{name}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def run(source: str, debug_tokens=False, debug_ast=False):
    """Lex, parse, and interpret FlameLang source code."""
    # Lex
    lexer = Lexer(source)
    tokens = lexer.tokenize()

    if debug_tokens:
        print("═══ TOKENS ═══")
        for tok in tokens:
            print(f"  {tok}")
        print()

    # Parse
    parser = Parser(tokens)
    program = parser.parse()

    if debug_ast:
        print("═══ AST ═══")
        print_ast(program)
        print()

    # Interpret
    interpreter = Interpreter()
    interpreter.interpret(program)
    return interpreter


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="FlameLang Interpreter v0.1.0 — Strategickhaos DAO LLC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 flamec.py hello.flm
  python3 flamec.py --ast test.flm
  python3 flamec.py --tokens test.flm
  echo 'print(2 + 3);' | python3 flamec.py --stdin
        """
    )
    parser.add_argument("file", nargs="?", help="FlameLang source file (.flm)")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--tokens", action="store_true", help="Print tokens")
    parser.add_argument("--ast", action="store_true", help="Print AST")
    parser.add_argument("--version", action="version",
                        version="FlameLang 0.1.0 (M1 Reference Interpreter)")

    args = parser.parse_args()

    if args.stdin:
        source = sys.stdin.read()
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        with open(args.file, 'r') as f:
            source = f.read()
    else:
        parser.print_help()
        sys.exit(0)

    try:
        run(source, debug_tokens=args.tokens, debug_ast=args.ast)
    except (LexerError, ParseError, RuntimeError_) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
