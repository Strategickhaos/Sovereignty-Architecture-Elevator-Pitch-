"""
SAGCO Language Lexer.
Handles: strings (single/double quoted), numbers (int/float), cell refs (A1-ZZ999),
identifiers/keywords, all operators, #comments, newlines.
Returns list[Token].
"""
import re
from .tokens import Token, TokenType, KEYWORDS


class LexError(SyntaxError):
    pass


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: list = []

    def error(self, msg: str):
        raise LexError(f"Lex error at line {self.line}, col {self.col}: {msg}")

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return ""

    def advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def match(self, ch: str) -> bool:
        if self.pos < len(self.source) and self.source[self.pos] == ch:
            self.advance()
            return True
        return False

    def tok(self, ttype: TokenType, value: str, line: int, col: int) -> Token:
        return Token(ttype, value, line, col)

    def skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos] in (" ", "\t", "\r"):
            self.advance()

    def read_string(self, quote: str) -> Token:
        line, col = self.line, self.col
        self.advance()  # consume opening quote
        buf = []
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch == quote:
                self.advance()
                break
            if ch == "\\" and self.pos + 1 < len(self.source):
                self.advance()
                esc = self.advance()
                escape_map = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\",
                              "'": "'", '"': '"'}
                buf.append(escape_map.get(esc, esc))
            elif ch == "\n":
                break  # unterminated string — just stop
            else:
                buf.append(self.advance())
        return self.tok(TokenType.STRING, "".join(buf), line, col)

    def read_number(self) -> Token:
        line, col = self.line, self.col
        buf = []
        if self.peek() == "-":
            buf.append(self.advance())
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            buf.append(self.advance())
        if self.pos < len(self.source) and self.source[self.pos] == ".":
            buf.append(self.advance())
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                buf.append(self.advance())
        return self.tok(TokenType.NUMBER, "".join(buf), line, col)

    def read_ident_or_keyword(self) -> Token:
        line, col = self.line, self.col
        buf = []
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == "_"):
            buf.append(self.advance())
        word = "".join(buf)
        upper = word.upper()

        # Check if it's a cell reference: letter(s) followed by digits
        cell_ref_match = re.fullmatch(r"[A-Za-z]{1,2}\d{1,3}", word)
        if cell_ref_match and upper not in KEYWORDS:
            return self.tok(TokenType.CELLREF, upper, line, col)

        if upper in KEYWORDS:
            ttype = KEYWORDS[upper]
            val = upper if ttype == TokenType.BOOL else word
            return self.tok(ttype, val, line, col)

        return self.tok(TokenType.IDENT, word, line, col)

    def read_comment(self) -> Token:
        line, col = self.line, self.col
        buf = []
        while self.pos < len(self.source) and self.source[self.pos] != "\n":
            buf.append(self.advance())
        return self.tok(TokenType.COMMENT, "".join(buf), line, col)

    def tokenize(self) -> list:
        """Tokenize the source. Returns list of Token (excludes COMMENT tokens)."""
        tokens = []
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break
            ch = self.source[self.pos]
            line, col = self.line, self.col

            if ch == "\n":
                self.advance()
                # Emit NEWLINE but collapse multiples
                if not tokens or tokens[-1].type != TokenType.NEWLINE:
                    tokens.append(self.tok(TokenType.NEWLINE, "\n", line, col))
                continue

            if ch == "#":
                self.read_comment()  # discard
                continue

            if ch in ('"', "'"):
                tokens.append(self.read_string(ch))
                continue

            if ch.isdigit() or (ch == "-" and self.peek(1).isdigit() and
                                  (not tokens or tokens[-1].type in (
                                      TokenType.ASSIGN, TokenType.LPAREN,
                                      TokenType.COMMA, TokenType.PLUS,
                                      TokenType.MINUS, TokenType.NEWLINE,
                                      TokenType.EOF))):
                tokens.append(self.read_number())
                continue

            if ch.isalpha() or ch == "_":
                tokens.append(self.read_ident_or_keyword())
                continue

            # Operators
            self.advance()
            if ch == "=":
                if self.match("="):
                    tokens.append(self.tok(TokenType.EQ, "==", line, col))
                else:
                    tokens.append(self.tok(TokenType.ASSIGN, "=", line, col))
            elif ch == "!":
                if self.match("="):
                    tokens.append(self.tok(TokenType.NEQ, "!=", line, col))
                else:
                    self.error(f"Unexpected character '!'")
            elif ch == "<":
                if self.match("="):
                    tokens.append(self.tok(TokenType.LTEQ, "<=", line, col))
                else:
                    tokens.append(self.tok(TokenType.LT, "<", line, col))
            elif ch == ">":
                if self.match("="):
                    tokens.append(self.tok(TokenType.GTEQ, ">=", line, col))
                else:
                    tokens.append(self.tok(TokenType.GT, ">", line, col))
            elif ch == "+":
                tokens.append(self.tok(TokenType.PLUS, "+", line, col))
            elif ch == "-":
                tokens.append(self.tok(TokenType.MINUS, "-", line, col))
            elif ch == "*":
                tokens.append(self.tok(TokenType.STAR, "*", line, col))
            elif ch == "/":
                tokens.append(self.tok(TokenType.SLASH, "/", line, col))
            elif ch == "(":
                tokens.append(self.tok(TokenType.LPAREN, "(", line, col))
            elif ch == ")":
                tokens.append(self.tok(TokenType.RPAREN, ")", line, col))
            elif ch == "[":
                tokens.append(self.tok(TokenType.LBRACKET, "[", line, col))
            elif ch == "]":
                tokens.append(self.tok(TokenType.RBRACKET, "]", line, col))
            elif ch == ",":
                tokens.append(self.tok(TokenType.COMMA, ",", line, col))
            elif ch == ":":
                tokens.append(self.tok(TokenType.COLON, ":", line, col))
            elif ch == "$":
                # treat as start of a price string token
                buf = ["$"]
                while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == "."):
                    buf.append(self.advance())
                tokens.append(self.tok(TokenType.STRING, "".join(buf), line, col))
            else:
                # Unknown char — skip silently
                pass

        tokens.append(self.tok(TokenType.EOF, "", self.line, self.col))
        return tokens
