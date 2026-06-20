"""Tests for lang/fuzz.py"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from sagco.lang.fuzz import SAGCOFuzzer


class TestFuzz(unittest.TestCase):
    def test_fuzz_no_crash(self):
        f = SAGCOFuzzer()
        r = f.fuzz(n=50)
        self.assertEqual(r["crash"], 0)
        self.assertEqual(r["total"], 50)
        total_accounted = (r["valid"] + r["lex_error"] + r["parse_error"] +
                           r["eval_error"] + r["assert_fail"] + r["crash"])
        self.assertEqual(total_accounted, 50)

    def test_fuzz_valid_programs_exist(self):
        f = SAGCOFuzzer()
        r = f.fuzz(n=100)
        # At least some programs should be valid
        self.assertGreater(r["valid"], 0)

    def test_fuzz_timing(self):
        f = SAGCOFuzzer()
        r = f.fuzz(n=50)
        # Should complete in reasonable time
        self.assertLess(r["elapsed_ms"], 30000)  # under 30 seconds

    def test_hello_sagco(self):
        from sagco.lang.lexer import Lexer
        from sagco.lang.parser import Parser
        from sagco.lang.evaluator import Evaluator, Env
        from sagco.lang.sagco_stdlib import STDLIB
        prog = '''
CELL A1 = "Eggs Orleans"
CELL B1 = ERU("Eggs Orleans", "Eggs Orleans")
ASSERT B1 == "VARIANCE_0"
PRINT B1
'''
        tokens = Lexer(prog).tokenize()
        ast = Parser(tokens).parse()
        env = Env()
        Evaluator(env, STDLIB).eval(ast)
        self.assertEqual(env.get_cell("B1"), "VARIANCE_0")

    def test_eru_variance_zero(self):
        from sagco.lang.sagco_stdlib import fn_eru
        self.assertEqual(fn_eru("test", "test"), "VARIANCE_0")
        self.assertEqual(fn_eru("42", "42"), "VARIANCE_0")
        self.assertEqual(fn_eru("test", "other"), "OPEN_VARIANCE")

    def test_guard_clean(self):
        from sagco.lang.sagco_stdlib import fn_guard
        self.assertEqual(fn_guard("$22"), "MOBIUS_READY")
        self.assertEqual(fn_guard("Black Pearl Roll"), "MOBIUS_READY")

    def test_guard_dirty(self):
        from sagco.lang.sagco_stdlib import fn_guard
        self.assertEqual(fn_guard("**bold**"), "NOT_READY")
        self.assertEqual(fn_guard("\\frac{1}{2}"), "NOT_READY")
        self.assertEqual(fn_guard("∑x"), "NOT_READY")

    def test_morse(self):
        from sagco.lang.sagco_stdlib import fn_morse
        result = fn_morse("SOS")
        self.assertIn("...", result)
        self.assertIn("---", result)

    def test_sanity(self):
        from sagco.lang.sagco_stdlib import fn_sanity
        self.assertEqual(fn_sanity("Eggs Benedict $16"), "SOVEREIGN")
        self.assertEqual(fn_sanity("**bold** text"), "HALLUCINATION_RISK")
        self.assertEqual(fn_sanity("\\frac{a}{b}"), "HALLUCINATION_RISK")

    def test_hello_sagco_program(self):
        """Test the full hello.sagco program."""
        from sagco.lang.lexer import Lexer
        from sagco.lang.parser import Parser
        from sagco.lang.evaluator import Evaluator, Env
        from sagco.lang.sagco_stdlib import STDLIB
        prog = '''
CELL A1 = "Black Pearl Roll"
CELL A2 = "$22"
CELL B1 = MORSE(A1)
CELL C1 = ERU("menu_item", A1)
CELL D1 = GUARD(A2)
ASSERT D1 == "MOBIUS_READY"
PRINT B1
PRINT C1
'''
        tokens = Lexer(prog).tokenize()
        ast = Parser(tokens).parse()
        env = Env()
        Evaluator(env, STDLIB).eval(ast)
        self.assertEqual(env.get_cell("D1"), "MOBIUS_READY")
        self.assertIsNotNone(env.get_cell("B1"))


if __name__ == "__main__":
    unittest.main()
