#!/usr/bin/env python3
"""
SAGCO OS — Main CLI
Usage:
  sagco solve <file>              solve any file (XLSX/CSV/YAML/TXT)
  sagco solve --demo              run on built-in Water Street menu
  sagco flashgame                 open the typing game in browser
  sagco fuzz [--n 100]            run SAGCO language fuzz tester
  sagco run <file.sagco>          execute a .sagco program
  sagco eru <file>                just run ERU pass
  sagco help                      show this

Examples:
  sagco solve data/water_street_menu.yaml
  sagco fuzz --n 500 --verbose
  sagco run examples/hello.sagco
"""
import sys
import os
import argparse

# Ensure the package is importable
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def cmd_solve(args):
    """Run the full solver pipeline on a file."""
    if args.demo or (hasattr(args, 'file') and (not args.file or args.file == '--demo')):
        print("SAGCO OS — Running demo on Water Street menu...")
        from sagco.solver.pipeline import run_demo
        result = run_demo(output_dir=os.path.join(_HERE, "outputs"))
    else:
        path = args.file
        if not os.path.exists(path):
            print(f"ERROR: File not found: {path}")
            sys.exit(1)
        from sagco.solver.pipeline import SolverPipeline
        pipe = SolverPipeline(path, output_dir=os.path.join(_HERE, "outputs"))
        result = pipe.run()

    print(f"\nSAGCO Solve Results:")
    print(f"  Input:          {result['input']}")
    print(f"  Rows extracted: {result['rows']}")
    print(f"  Flashcards:     {result['flashcards']}")
    print(f"  Quiz questions: {result['quiz_questions']}")
    if result.get('eru_summary'):
        s = result['eru_summary']
        print(f"  ERU: {s.get('PASS',0)} PASS / {s.get('PARTIAL',0)} PARTIAL / {s.get('FAIL',0)} FAIL  ({s.get('pass_rate',0)}% pass rate)")
    print("\nPipeline steps:")
    for step in result['steps']:
        print(f"  ✓ {step}")
    print("\nOutputs:")
    for out in result['outputs']:
        print(f"  → {out}")


def cmd_fuzz(args):
    """Run the SAGCO language fuzz tester."""
    n = getattr(args, 'n', 100) or 100
    verbose = getattr(args, 'verbose', False)
    print(f"SAGCO Fuzz Tester — running {n} programs...")
    from sagco.lang.fuzz import SAGCOFuzzer
    fuzzer = SAGCOFuzzer()
    r = fuzzer.fuzz(n=n, verbose=verbose)
    print(f"\n{'='*50}")
    print(f"SAGCO Fuzz Report — {r['total']} programs")
    print(f"{'='*50}")
    print(f"  Valid:        {r['valid']:4d}  ({r['valid']/r['total']*100:.1f}%)")
    print(f"  Lex errors:   {r['lex_error']:4d}")
    print(f"  Parse errors: {r['parse_error']:4d}")
    print(f"  Eval errors:  {r['eval_error']:4d}")
    print(f"  Assert fails: {r['assert_fail']:4d}")
    print(f"  Crashes:      {r['crash']:4d}")
    print(f"  Total time:   {r['elapsed_ms']} ms  ({r['ms_per_prog']} ms/prog)")
    print(f"{'='*50}")


def cmd_run(args):
    """Execute a .sagco program."""
    path = args.file
    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    print(f"SAGCO OS — Running {path}")
    print("─" * 40)

    from sagco.lang.lexer import Lexer
    from sagco.lang.parser import Parser
    from sagco.lang.evaluator import Evaluator, Env
    from sagco.lang.sagco_stdlib import STDLIB

    try:
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        env = Env()
        Evaluator(env, STDLIB).eval(ast)
        print("─" * 40)
        print(f"Program completed successfully.")
        print(f"Cells set: {list(env.cells.keys())}")
    except AssertionError as e:
        print(f"ASSERT FAILED: {e}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"SYNTAX ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        sys.exit(1)


def cmd_eru(args):
    """Run ERU analysis on a file."""
    path = args.file
    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        sys.exit(1)
    from sagco.core.extractor import extract
    from sagco.core.eru import run_eru_on_rows, eru_summary

    rows = extract(path)
    print(f"Loaded {len(rows)} rows from {path}")

    results = run_eru_on_rows(rows)
    summary = eru_summary(results)

    print(f"\nERU Analysis:")
    print(f"  Total:    {summary['total']}")
    print(f"  PASS:     {summary['PASS']}  ({summary['pass_rate']}%)")
    print(f"  PARTIAL:  {summary['PARTIAL']}")
    print(f"  FAIL:     {summary['FAIL']}")
    print(f"  Mean variance: {summary['mean_variance']}")

    fails = [r for r in results if r.label != "PASS"]
    if fails:
        print(f"\nVariances found ({len(fails)}):")
        for r in fails[:10]:
            print(f"  ID {r.item_id}: expected={r.expected}, actual={r.actual}, var={r.variance}")


def cmd_flashgame(args):
    """Open the SAGCO flashcard typing game in browser."""
    print("SAGCO Flashcard Game")
    print("Launching interactive flashcard quiz in terminal...\n")

    flashcard_path = os.path.join(_HERE, "data", "oyster_flashcards.csv")
    if not os.path.exists(flashcard_path):
        print(f"ERROR: Flashcards not found at {flashcard_path}")
        print("Run: sagco solve --demo  first to generate flashcard data")
        sys.exit(1)

    from sagco.solver.flashcards import load_flashcards_csv
    import random

    cards = load_flashcards_csv(flashcard_path)
    random.shuffle(cards)
    cards = cards[:10]  # limit to 10 for terminal game

    print(f"SAGCO Memory Engine — {len(cards)} questions")
    print("Type the answer and press Enter. Type 'quit' to exit.\n")

    score = 0
    for i, card in enumerate(cards, 1):
        print(f"[{i}/{len(cards)}] {card['front']}")
        print(f"  Category: {card['category']}  |  Hint: {card['mnemonic'][:40]}...")
        try:
            answer = input("  Your answer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGame ended.")
            break
        if answer.lower() == "quit":
            break
        correct = card['back']
        if answer.lower() in correct.lower() or correct.lower() in answer.lower():
            print(f"  ✓ CORRECT! {correct}\n")
            score += 1
        else:
            print(f"  ✗ Answer: {correct}\n")

    print(f"\nFinal score: {score}/{len(cards)}")


def cmd_help(args=None):
    """Show help."""
    print(__doc__)


def main():
    parser = argparse.ArgumentParser(
        prog="sagco",
        description="SAGCO OS — Sovereignty Architecture General Compiler OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command")

    # solve
    p_solve = subparsers.add_parser("solve", help="Solve a file or run demo")
    p_solve.add_argument("file", nargs="?", help="Input file (XLSX/CSV/YAML/TXT)")
    p_solve.add_argument("--demo", action="store_true", help="Run on built-in Water Street menu")
    p_solve.set_defaults(func=cmd_solve)

    # fuzz
    p_fuzz = subparsers.add_parser("fuzz", help="Run SAGCO language fuzz tester")
    p_fuzz.add_argument("--n", type=int, default=100, help="Number of programs to fuzz (default: 100)")
    p_fuzz.add_argument("--verbose", action="store_true", help="Verbose output")
    p_fuzz.set_defaults(func=cmd_fuzz)

    # run
    p_run = subparsers.add_parser("run", help="Execute a .sagco program")
    p_run.add_argument("file", help="Path to .sagco file")
    p_run.set_defaults(func=cmd_run)

    # eru
    p_eru = subparsers.add_parser("eru", help="Run ERU analysis on a file")
    p_eru.add_argument("file", help="Input file")
    p_eru.set_defaults(func=cmd_eru)

    # flashgame
    p_flash = subparsers.add_parser("flashgame", help="Interactive flashcard game")
    p_flash.set_defaults(func=cmd_flashgame)

    # help
    p_help = subparsers.add_parser("help", help="Show help")
    p_help.set_defaults(func=cmd_help)

    args = parser.parse_args()

    if not hasattr(args, "func") or args.func is None:
        cmd_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
