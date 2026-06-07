"""Token types and Token dataclass for the SAGCO language."""
from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Keywords
    CELL = auto()
    ASSERT = auto()
    PRINT = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    END = auto()
    FOR = auto()
    IN = auto()
    RETURN = auto()
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()
    NULL = auto()
    # Identifiers / references
    IDENT = auto()
    CELLREF = auto()   # A1, B2, ZZ99, etc.
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQ = auto()         # ==
    NEQ = auto()        # !=
    LT = auto()         # <
    GT = auto()         # >
    LTEQ = auto()       # <=
    GTEQ = auto()       # >=
    ASSIGN = auto()     # =
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    # Special
    COMMENT = auto()
    NEWLINE = auto()
    EOF = auto()


KEYWORDS = {
    "CELL": TokenType.CELL,
    "ASSERT": TokenType.ASSERT,
    "PRINT": TokenType.PRINT,
    "IF": TokenType.IF,
    "THEN": TokenType.THEN,
    "ELSE": TokenType.ELSE,
    "END": TokenType.END,
    "FOR": TokenType.FOR,
    "IN": TokenType.IN,
    "RETURN": TokenType.RETURN,
    "TRUE": TokenType.BOOL,
    "FALSE": TokenType.BOOL,
    "NULL": TokenType.NULL,
    "NIL": TokenType.NULL,
}


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.col})"
