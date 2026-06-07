"""Tests for lang/parser.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from sagco.lang.lexer import Lexer
from sagco.lang.parser import Parser
from sagco.lang.ast_nodes import (
    Program, CellAssign, AssertStmt, PrintStmt, FuncCall, BinOp, Literal, CellRef
)


def parse(src: str):
    tokens = Lexer(src).tokenize()
    return Parser(tokens).parse()


class TestParser(unittest.TestCase):
    def test_cell_assign_literal(self):
        ast = parse('CELL A1 = "Eggs Benedict"')
        self.assertIsInstance(ast, Program)
        self.assertEqual(len(ast.statements), 1)
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, CellAssign)
        self.assertEqual(stmt.ref, "A1")
        self.assertIsInstance(stmt.expr, Literal)
        self.assertEqual(stmt.expr.value, "Eggs Benedict")

    def test_cell_assign_number(self):
        ast = parse("CELL B2 = 42")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, CellAssign)
        self.assertEqual(stmt.ref, "B2")

    def test_print_stmt(self):
        ast = parse('PRINT "hello"')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, PrintStmt)

    def test_assert_stmt(self):
        ast = parse('ASSERT A1 == "VARIANCE_0"')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, AssertStmt)
        self.assertIsInstance(stmt.left, CellRef)
        self.assertEqual(stmt.op, "==")
        self.assertIsInstance(stmt.right, Literal)

    def test_func_call(self):
        ast = parse('CELL B1 = ERU("expected", "actual")')
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, CellAssign)
        self.assertIsInstance(stmt.expr, FuncCall)
        self.assertEqual(stmt.expr.name, "ERU")
        self.assertEqual(len(stmt.expr.args), 2)

    def test_binop(self):
        ast = parse("CELL C1 = 10 + 5")
        stmt = ast.statements[0]
        self.assertIsInstance(stmt.expr, BinOp)
        self.assertEqual(stmt.expr.op, "+")

    def test_multiline(self):
        src = '''
CELL A1 = "Eggs Orleans"
CELL A2 = "$20"
CELL B1 = ERU("brunch item", A1)
ASSERT B1 == "VARIANCE_0"
PRINT B1
'''
        ast = parse(src)
        self.assertEqual(len(ast.statements), 5)

    def test_if_stmt(self):
        src = '''
IF A1 == "test"
PRINT "yes"
ELSE
PRINT "no"
END
'''
        ast = parse(src)
        self.assertEqual(len(ast.statements), 1)
        from sagco.lang.ast_nodes import IfStmt
        self.assertIsInstance(ast.statements[0], IfStmt)


if __name__ == "__main__":
    unittest.main()
