"""Tests for lang/lexer.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from sagco.lang.lexer import Lexer
from sagco.lang.tokens import TokenType


class TestLexer(unittest.TestCase):
    def tokenize(self, src):
        return Lexer(src).tokenize()

    def test_keywords(self):
        tokens = self.tokenize("CELL ASSERT PRINT IF THEN ELSE END FOR IN RETURN")
        types = [t.type for t in tokens if t.type != TokenType.EOF]
        self.assertIn(TokenType.CELL, types)
        self.assertIn(TokenType.ASSERT, types)
        self.assertIn(TokenType.PRINT, types)
        self.assertIn(TokenType.IF, types)

    def test_cell_ref(self):
        tokens = self.tokenize("A1 B2 ZZ99")
        types = [t.type for t in tokens if t.type not in (TokenType.EOF, TokenType.NEWLINE)]
        self.assertTrue(all(t == TokenType.CELLREF for t in types))

    def test_string_double_quote(self):
        tokens = self.tokenize('"Hello World"')
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "Hello World")

    def test_string_single_quote(self):
        tokens = self.tokenize("'sagco'")
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "sagco")

    def test_numbers(self):
        tokens = self.tokenize("42 3.14 100")
        nums = [t for t in tokens if t.type == TokenType.NUMBER]
        self.assertEqual(len(nums), 3)
        self.assertEqual(nums[0].value, "42")
        self.assertEqual(nums[1].value, "3.14")

    def test_operators(self):
        tokens = self.tokenize("== != < > <= >= = + - * /")
        types = [t.type for t in tokens if t.type not in (TokenType.EOF, TokenType.NEWLINE)]
        self.assertIn(TokenType.EQ, types)
        self.assertIn(TokenType.NEQ, types)
        self.assertIn(TokenType.LT, types)
        self.assertIn(TokenType.GT, types)
        self.assertIn(TokenType.LTEQ, types)
        self.assertIn(TokenType.GTEQ, types)
        self.assertIn(TokenType.ASSIGN, types)

    def test_comment_ignored(self):
        tokens = self.tokenize("# this is a comment\nCELL A1 = 42")
        types = [t.type for t in tokens]
        self.assertNotIn(TokenType.COMMENT, types)
        self.assertIn(TokenType.CELL, types)

    def test_cell_assign_tokens(self):
        tokens = self.tokenize('CELL A1 = "Eggs Benedict"')
        types = [t.type for t in tokens if t.type not in (TokenType.EOF, TokenType.NEWLINE)]
        self.assertEqual(types[0], TokenType.CELL)
        self.assertEqual(types[1], TokenType.CELLREF)
        self.assertEqual(types[2], TokenType.ASSIGN)
        self.assertEqual(types[3], TokenType.STRING)

    def test_function_call_tokens(self):
        tokens = self.tokenize('ERU("expected", "actual")')
        types = [t.type for t in tokens if t.type not in (TokenType.EOF, TokenType.NEWLINE)]
        self.assertEqual(types[0], TokenType.IDENT)
        self.assertEqual(types[1], TokenType.LPAREN)
        self.assertEqual(types[2], TokenType.STRING)
        self.assertEqual(types[3], TokenType.COMMA)


if __name__ == "__main__":
    unittest.main()
