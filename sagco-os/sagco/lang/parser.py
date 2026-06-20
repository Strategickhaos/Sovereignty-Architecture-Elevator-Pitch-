"""
SAGCO language recursive descent parser.
Parses SAGCO token stream into a Program AST.
"""
from .tokens import Token, TokenType
from .ast_nodes import (
    Program, CellAssign, VarAssign, AssertStmt, PrintStmt,
    IfStmt, ForStmt, ReturnStmt, FuncCall, BinOp, UnaryOp,
    CellRef, Ident, Literal
)


class ParseError(SyntaxError):
    pass


class Parser:
    def __init__(self, tokens: list):
        # Filter out NEWLINE tokens for simpler parsing (we handle them as statement separators)
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE or True]
        self.pos = 0

    def peek(self) -> Token:
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.NEWLINE:
            self.pos += 1
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, "", 0, 0)

    def peek_raw(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, "", 0, 0)

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def skip_newlines(self):
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.NEWLINE:
            self.pos += 1

    def expect(self, ttype: TokenType) -> Token:
        self.skip_newlines()
        tok = self.tokens[self.pos] if self.pos < len(self.tokens) else Token(TokenType.EOF, "", 0, 0)
        if tok.type != ttype:
            raise ParseError(
                f"Expected {ttype.name} but got {tok.type.name} ({tok.value!r}) at line {tok.line}"
            )
        self.pos += 1
        return tok

    def check(self, *ttypes: TokenType) -> bool:
        self.skip_newlines()
        if self.pos >= len(self.tokens):
            return False
        return self.tokens[self.pos].type in ttypes

    def match(self, *ttypes: TokenType) -> Token | None:
        self.skip_newlines()
        if self.pos < len(self.tokens) and self.tokens[self.pos].type in ttypes:
            return self.advance()
        return None

    def parse(self) -> Program:
        stmts = []
        while not self.check(TokenType.EOF):
            self.skip_newlines()
            if self.check(TokenType.EOF):
                break
            stmt = self.parse_statement()
            if stmt is not None:
                stmts.append(stmt)
        return Program(stmts)

    def parse_statement(self):
        tok = self.peek()
        if tok.type == TokenType.CELL:
            return self.parse_cell_assign()
        elif tok.type == TokenType.ASSERT:
            return self.parse_assert()
        elif tok.type == TokenType.PRINT:
            return self.parse_print()
        elif tok.type == TokenType.IF:
            return self.parse_if()
        elif tok.type == TokenType.FOR:
            return self.parse_for()
        elif tok.type == TokenType.RETURN:
            return self.parse_return()
        elif tok.type == TokenType.IDENT:
            # Could be variable assignment: IDENT = expr
            return self.parse_ident_stmt()
        elif tok.type == TokenType.NEWLINE:
            self.advance()
            return None
        elif tok.type == TokenType.EOF:
            return None
        else:
            # Unknown token — skip the line
            self._skip_line()
            return None

    def _skip_line(self):
        """Skip tokens until NEWLINE or EOF."""
        while self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            if t.type in (TokenType.NEWLINE, TokenType.EOF):
                break
            self.pos += 1

    def parse_cell_assign(self) -> CellAssign:
        self.expect(TokenType.CELL)
        ref_tok = self.expect(TokenType.CELLREF)
        self.expect(TokenType.ASSIGN)
        expr = self.parse_expr()
        return CellAssign(ref_tok.value, expr)

    def parse_assert(self) -> AssertStmt:
        self.expect(TokenType.ASSERT)
        # Parse the left side without consuming comparison operators
        left = self.parse_additive()
        op_tok = self.match(TokenType.EQ, TokenType.NEQ, TokenType.LT,
                            TokenType.GT, TokenType.LTEQ, TokenType.GTEQ)
        if op_tok is None:
            # Check if left is already a BinOp comparison (parse_expr consumed it)
            # Wrap as assert True
            return AssertStmt(left, "==", Literal(True))
        right = self.parse_additive()
        return AssertStmt(left, op_tok.value, right)

    def parse_print(self) -> PrintStmt:
        self.expect(TokenType.PRINT)
        expr = self.parse_expr()
        return PrintStmt(expr)

    def parse_if(self) -> IfStmt:
        self.expect(TokenType.IF)
        cond = self.parse_expr()
        self.match(TokenType.THEN)  # optional THEN keyword
        self.skip_newlines()
        then_stmts = []
        else_stmts = []
        while not self.check(TokenType.ELSE, TokenType.END, TokenType.EOF):
            self.skip_newlines()
            if self.check(TokenType.ELSE, TokenType.END, TokenType.EOF):
                break
            stmt = self.parse_statement()
            if stmt is not None:
                then_stmts.append(stmt)
        if self.match(TokenType.ELSE):
            self.skip_newlines()
            while not self.check(TokenType.END, TokenType.EOF):
                self.skip_newlines()
                if self.check(TokenType.END, TokenType.EOF):
                    break
                stmt = self.parse_statement()
                if stmt is not None:
                    else_stmts.append(stmt)
        self.match(TokenType.END)
        return IfStmt(cond, then_stmts, else_stmts)

    def parse_for(self) -> ForStmt:
        self.expect(TokenType.FOR)
        var_tok = self.expect(TokenType.IDENT)
        self.expect(TokenType.IN)
        iterable = self.parse_expr()
        self.skip_newlines()
        body = []
        while not self.check(TokenType.END, TokenType.EOF):
            self.skip_newlines()
            if self.check(TokenType.END, TokenType.EOF):
                break
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        self.match(TokenType.END)
        return ForStmt(var_tok.value, iterable, body)

    def parse_return(self) -> ReturnStmt:
        self.expect(TokenType.RETURN)
        expr = self.parse_expr()
        return ReturnStmt(expr)

    def parse_ident_stmt(self):
        """Handle IDENT = expr (variable assignment) or standalone expression."""
        self.skip_newlines()
        ident_tok = self.tokens[self.pos]
        # Peek ahead to see if next non-nl is ASSIGN
        saved = self.pos
        self.pos += 1
        self.skip_newlines()
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.ASSIGN:
            self.pos += 1  # consume =
            expr = self.parse_expr()
            return VarAssign(ident_tok.value, expr)
        else:
            self.pos = saved
            # Just evaluate and discard (expression statement)
            expr = self.parse_expr()
            return PrintStmt(expr)  # treat as print

    # ---- Expression parsing (precedence climbing) ----

    def parse_expr(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_additive()
        while True:
            op = self.match(TokenType.EQ, TokenType.NEQ, TokenType.LT,
                            TokenType.GT, TokenType.LTEQ, TokenType.GTEQ)
            if op is None:
                break
            right = self.parse_additive()
            left = BinOp(left, op.value, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while True:
            op = self.match(TokenType.PLUS, TokenType.MINUS)
            if op is None:
                break
            right = self.parse_multiplicative()
            left = BinOp(left, op.value, right)
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while True:
            op = self.match(TokenType.STAR, TokenType.SLASH)
            if op is None:
                break
            right = self.parse_unary()
            left = BinOp(left, op.value, right)
        return left

    def parse_unary(self):
        self.skip_newlines()
        op = self.match(TokenType.MINUS)
        if op:
            operand = self.parse_primary()
            return UnaryOp("-", operand)
        return self.parse_primary()

    def parse_primary(self):
        self.skip_newlines()
        if self.pos >= len(self.tokens):
            return Literal(None)
        tok = self.tokens[self.pos]

        if tok.type == TokenType.NUMBER:
            self.pos += 1
            try:
                val = float(tok.value)
                if val == int(val) and "." not in tok.value:
                    val = int(val)
            except ValueError:
                val = 0
            return Literal(val)

        if tok.type == TokenType.STRING:
            self.pos += 1
            return Literal(tok.value)

        if tok.type == TokenType.BOOL:
            self.pos += 1
            return Literal(tok.value.upper() == "TRUE")

        if tok.type == TokenType.NULL:
            self.pos += 1
            return Literal(None)

        if tok.type == TokenType.CELLREF:
            self.pos += 1
            return CellRef(tok.value)

        if tok.type == TokenType.IDENT:
            self.pos += 1
            # Check if function call
            self.skip_newlines()
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.LPAREN:
                return self.parse_func_call(tok.value)
            return Ident(tok.value)

        if tok.type == TokenType.LPAREN:
            self.pos += 1
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return expr

        # Unknown — skip and return None literal
        self.pos += 1
        return Literal(None)

    def parse_func_call(self, name: str) -> FuncCall:
        self.expect(TokenType.LPAREN)
        args = []
        if not self.check(TokenType.RPAREN):
            args.append(self.parse_expr())
            while self.match(TokenType.COMMA):
                if self.check(TokenType.RPAREN):
                    break
                args.append(self.parse_expr())
        self.expect(TokenType.RPAREN)
        return FuncCall(name, args)
