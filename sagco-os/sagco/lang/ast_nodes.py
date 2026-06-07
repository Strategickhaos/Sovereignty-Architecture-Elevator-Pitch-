"""AST node classes for the SAGCO language."""
from dataclasses import dataclass, field
from typing import List, Any, Optional


@dataclass
class Program:
    statements: List[Any] = field(default_factory=list)


@dataclass
class CellAssign:
    ref: str
    expr: Any  # Expr


@dataclass
class VarAssign:
    name: str
    expr: Any  # Expr


@dataclass
class AssertStmt:
    left: Any   # Expr
    op: str
    right: Any  # Expr


@dataclass
class PrintStmt:
    expr: Any  # Expr


@dataclass
class IfStmt:
    cond: Any       # Expr
    then: List[Any]
    else_: List[Any] = field(default_factory=list)


@dataclass
class ForStmt:
    var: str
    iterable: Any  # Expr
    body: List[Any]


@dataclass
class ReturnStmt:
    expr: Any  # Expr


@dataclass
class FuncCall:
    name: str
    args: List[Any] = field(default_factory=list)


@dataclass
class BinOp:
    left: Any
    op: str
    right: Any


@dataclass
class UnaryOp:
    op: str
    operand: Any


@dataclass
class CellRef:
    ref: str


@dataclass
class Ident:
    name: str


@dataclass
class Literal:
    value: Any  # str, float, int, bool, None
