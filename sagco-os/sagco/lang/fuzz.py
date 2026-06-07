"""
SAGCO Fuzz Tester.
Generates random SAGCO programs and runs them through the full pipeline.
Catches crashes, assertion errors, parse errors.
Reports: valid programs generated, crashed, errored, time per program.
"""
import random
import time
from .lexer import Lexer, LexError
from .parser import Parser, ParseError
from .evaluator import Evaluator, Env, EvalError
from .sagco_stdlib import STDLIB


class SAGCOFuzzer:
    """
    Generates random SAGCO programs and runs them through lexer→parser→evaluator.
    Tracks outcomes: valid, lex_error, parse_error, eval_error, assert_fail, crash.
    """

    CELL_REFS = [f"{c}{n}" for c in "ABCDEFGH" for n in range(1, 6)]
    WORDS = ["sagco", "eru", "mobius", "guard", "oyster", "sushi",
             "registry", "compiler", "sovereign", "water", "street", "bar"]

    def gen_string(self) -> str:
        word = random.choice(self.WORDS)
        return f'"{word}"'

    def gen_number(self) -> str:
        return str(round(random.uniform(-100, 100), 2))

    def gen_pos_number(self) -> str:
        return str(round(random.uniform(0, 100), 2))

    def gen_cellref(self) -> str:
        return random.choice(self.CELL_REFS)

    def gen_expr(self, depth: int = 0) -> str:
        if depth > 3:
            return self.gen_string() if random.random() > 0.5 else self.gen_pos_number()
        choices = [
            lambda: self.gen_string(),
            lambda: self.gen_pos_number(),
            lambda: self.gen_cellref(),
            lambda: f'ERU({self.gen_expr(depth+1)}, {self.gen_expr(depth+1)})',
            lambda: f'MORSE({self.gen_expr(depth+1)})',
            lambda: f'GUARD({self.gen_expr(depth+1)})',
            lambda: f'LEN({self.gen_expr(depth+1)})',
            lambda: f'UPPER({self.gen_expr(depth+1)})',
            lambda: f'SANITY({self.gen_expr(depth+1)})',
            lambda: f'({self.gen_expr(depth+1)} + {self.gen_expr(depth+1)})',
        ]
        return random.choice(choices)()

    def gen_statement(self) -> str:
        ref = self.gen_cellref()
        choices = [
            lambda: f'CELL {ref} = {self.gen_expr()}',
            lambda: f'PRINT {self.gen_expr()}',
            lambda: f'ASSERT {self.gen_cellref()} == {self.gen_string()}',
            lambda: f'CELL {ref} = ERU({self.gen_string()}, {self.gen_string()})',
            lambda: f'CELL {ref} = MORSE({self.gen_string()})',
            lambda: f'CELL {ref} = GUARD({self.gen_string()})',
        ]
        return random.choice(choices)()

    def gen_program(self, num_stmts: int = 5) -> str:
        stmts = [self.gen_statement() for _ in range(num_stmts)]
        return "\n".join(stmts)

    def fuzz(self, n: int = 100, verbose: bool = False) -> dict:
        """
        Run n random programs through the full pipeline.
        Returns a results dict with counts.
        """
        results = {
            "total": n,
            "valid": 0,
            "lex_error": 0,
            "parse_error": 0,
            "eval_error": 0,
            "assert_fail": 0,
            "crash": 0,
            "programs": [],
            "elapsed_ms": 0,
        }
        start = time.time()
        for i in range(n):
            prog = self.gen_program()
            if verbose and i < 5:
                print(f"\n--- Program {i} ---\n{prog}\n")
            try:
                tokens = Lexer(prog).tokenize()
                ast = Parser(tokens).parse()
                env = Env()
                import io as _io, sys as _sys
                # Suppress stdout during fuzz
                old_stdout = _sys.stdout
                _sys.stdout = _io.StringIO()
                try:
                    Evaluator(env, STDLIB).eval(ast)
                finally:
                    _sys.stdout = old_stdout
                results["valid"] += 1
                if verbose:
                    print(f"[OK] prog {i}")
            except ParseError:
                results["parse_error"] += 1
            except LexError:
                results["lex_error"] += 1
            except SyntaxError:
                results["lex_error"] += 1
            except AssertionError:
                results["assert_fail"] += 1
            except (EvalError, TypeError, ValueError, ZeroDivisionError, AttributeError) as e:
                results["eval_error"] += 1
                if verbose:
                    print(f"[EVAL_ERR] prog {i}: {type(e).__name__}: {e}")
            except Exception as e:
                # Unexpected crash
                results["crash"] += 1
                if verbose:
                    print(f"[CRASH] prog {i}: {type(e).__name__}: {e}")

        elapsed = (time.time() - start) * 1000
        results["elapsed_ms"] = round(elapsed, 1)
        results["ms_per_prog"] = round(elapsed / n, 3) if n > 0 else 0
        return results

    def fuzz_report(self, n: int = 100) -> str:
        """Return a formatted fuzz report string."""
        r = self.fuzz(n)
        lines = [
            f"SAGCO Fuzz Report — {r['total']} programs",
            f"  Valid:       {r['valid']:4d}  ({r['valid']/r['total']*100:.1f}%)",
            f"  Lex errors:  {r['lex_error']:4d}",
            f"  Parse errors:{r['parse_error']:4d}",
            f"  Eval errors: {r['eval_error']:4d}",
            f"  Assert fails:{r['assert_fail']:4d}",
            f"  Crashes:     {r['crash']:4d}",
            f"  Total time:  {r['elapsed_ms']} ms  ({r['ms_per_prog']} ms/prog)",
        ]
        return "\n".join(lines)
