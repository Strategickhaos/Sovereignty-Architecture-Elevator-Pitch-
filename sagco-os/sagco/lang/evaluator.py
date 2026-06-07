"""
SAGCO language evaluator.
Walks the AST and executes each node.
"""
import sys
from .ast_nodes import (
    Program, CellAssign, VarAssign, AssertStmt, PrintStmt,
    IfStmt, ForStmt, ReturnStmt, FuncCall, BinOp, UnaryOp,
    CellRef, Ident, Literal
)


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class EvalError(Exception):
    pass


class Env:
    """Runtime environment: cell store and variable store."""
    def __init__(self):
        self.cells: dict = {}
        self.vars: dict = {}

    def set_cell(self, ref: str, val):
        self.cells[ref] = val

    def get_cell(self, ref: str):
        return self.cells.get(ref, None)

    def set_var(self, name: str, val):
        self.vars[name] = val

    def get_var(self, name: str):
        return self.vars.get(name, None)

    def __repr__(self):
        return f"Env(cells={self.cells}, vars={self.vars})"


class Evaluator:
    def __init__(self, env: Env, stdlib: dict = None):
        self.env = env
        self.stdlib = stdlib or {}
        self.output = []

    def eval(self, node):
        """Dispatch on node type."""
        if node is None:
            return None
        ntype = type(node).__name__
        method = getattr(self, f"eval_{ntype}", None)
        if method is None:
            raise EvalError(f"Unknown AST node: {ntype}")
        return method(node)

    def eval_Program(self, node: Program):
        result = None
        for stmt in node.statements:
            result = self.eval(stmt)
        return result

    def eval_CellAssign(self, node: CellAssign):
        val = self.eval(node.expr)
        self.env.set_cell(node.ref, val)
        return val

    def eval_VarAssign(self, node: VarAssign):
        val = self.eval(node.expr)
        self.env.set_var(node.name, val)
        return val

    def eval_AssertStmt(self, node: AssertStmt):
        left = self.eval(node.left)
        right = self.eval(node.right)
        result = self._compare(left, node.op, right)
        if not result:
            raise AssertionError(
                f"ASSERT FAILED: {left!r} {node.op} {right!r}"
            )
        return True

    def _compare(self, left, op: str, right) -> bool:
        try:
            l = float(left) if left is not None else 0
            r = float(right) if right is not None else 0
            if op == "==":
                return l == r
            if op == "!=":
                return l != r
            if op == "<":
                return l < r
            if op == ">":
                return l > r
            if op == "<=":
                return l <= r
            if op == ">=":
                return l >= r
        except (ValueError, TypeError):
            pass
        # String comparison
        ls, rs = str(left) if left is not None else "", str(right) if right is not None else ""
        if op == "==":
            return ls == rs
        if op == "!=":
            return ls != rs
        if op == "<":
            return ls < rs
        if op == ">":
            return ls > rs
        if op == "<=":
            return ls <= rs
        if op == ">=":
            return ls >= rs
        return False

    def eval_PrintStmt(self, node: PrintStmt):
        val = self.eval(node.expr)
        out = str(val) if val is not None else "NULL"
        self.output.append(out)
        print(out)
        return val

    def eval_IfStmt(self, node: IfStmt):
        cond = self.eval(node.cond)
        branch = node.then if self._truthy(cond) else node.else_
        result = None
        for stmt in branch:
            result = self.eval(stmt)
        return result

    def eval_ForStmt(self, node: ForStmt):
        iterable = self.eval(node.iterable)
        if not hasattr(iterable, "__iter__"):
            iterable = [iterable]
        result = None
        for item in iterable:
            self.env.set_var(node.var, item)
            for stmt in node.body:
                try:
                    result = self.eval(stmt)
                except ReturnSignal as rs:
                    return rs.value
        return result

    def eval_ReturnStmt(self, node: ReturnStmt):
        val = self.eval(node.expr)
        raise ReturnSignal(val)

    def eval_FuncCall(self, node: FuncCall):
        fn = self.stdlib.get(node.name) or self.stdlib.get(node.name.upper())
        if fn is None:
            raise EvalError(f"Unknown function: {node.name!r}")
        args = [self.eval(a) for a in node.args]
        return fn(*args)

    def eval_BinOp(self, node: BinOp):
        left = self.eval(node.left)
        right = self.eval(node.right)
        op = node.op
        if op in ("==", "!=", "<", ">", "<=", ">="):
            return self._compare(left, op, right)
        # Arithmetic
        try:
            l = float(left) if left is not None else 0
            r = float(right) if right is not None else 0
            if op == "+":
                result = l + r
            elif op == "-":
                result = l - r
            elif op == "*":
                result = l * r
            elif op == "/":
                if r == 0:
                    raise EvalError("Division by zero")
                result = l / r
            else:
                raise EvalError(f"Unknown operator: {op!r}")
            return int(result) if result == int(result) else result
        except (TypeError, ValueError):
            # String concatenation for +
            if op == "+":
                return str(left if left is not None else "") + str(right if right is not None else "")
            raise EvalError(f"Cannot apply operator {op!r} to {type(left).__name__} and {type(right).__name__}")

    def eval_UnaryOp(self, node: UnaryOp):
        val = self.eval(node.operand)
        if node.op == "-":
            try:
                return -float(val)
            except (TypeError, ValueError):
                return val
        return val

    def eval_CellRef(self, node: CellRef):
        return self.env.get_cell(node.ref)

    def eval_Ident(self, node: Ident):
        val = self.env.get_var(node.name)
        return val

    def eval_Literal(self, node: Literal):
        return node.value

    def _truthy(self, val) -> bool:
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            return val.strip().lower() not in ("", "false", "0", "null", "nil")
        return bool(val)
