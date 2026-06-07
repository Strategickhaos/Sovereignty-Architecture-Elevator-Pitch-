"""
BOARD-38 — Pattern-of-Life Decoder
decoder_cli.py — CLI entry point.

Usage:
  python decoder_cli.py --word-freq PATH [--music PATH] [--eru]
  python decoder_cli.py --demo
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure src/ is on the path when invoked directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cadence_lexer import lex_word_frequency, lex_music_tokens, lex_text
from pattern_of_life import build_pattern_of_life
from invention_seed_emitter import emit_seeds, write_seeds
from eru_decoder import build_eru


# ── Demo payload ──────────────────────────────────────────────────────────────

DEMO_TEXT = """
Baby lookii — I found the pattern again.
Screenshot then command then antibody.
Contradiction to board to proof.
The contradiction is clear: the system expected one output, the board received another.
We need to compile this into a reusable core.
Deploy the pipeline, iterate fast.
The eureka moment: the mobius problem is actually a proof of the pattern.
Baby lookii — the bridge is here.
Rapid engineering, rapid associative thinking.
Pipeline deploy pipeline iterate compile build.
The antibody fires. The board resolves. The proof stands.
""".strip()

DEMO_WORD_FREQ = [
    {"word": "pipeline", "count": 8},
    {"word": "contradiction", "count": 6},
    {"word": "board", "count": 10},
    {"word": "proof", "count": 7},
    {"word": "baby lookii", "count": 3},
    {"word": "compile", "count": 5},
    {"word": "deploy", "count": 6},
    {"word": "antibody", "count": 4},
    {"word": "screenshot", "count": 3},
    {"word": "eureka", "count": 2},
    {"word": "mobius", "count": 3},
    {"word": "pattern", "count": 5},
    {"word": "engineer", "count": 4},
    {"word": "bridge", "count": 3},
    {"word": "iterate", "count": 4},
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║  BOARD-38 — Pattern-of-Life Decoder                     ║
║  district: contradiction_forest                          ║
╚══════════════════════════════════════════════════════════╝
""")


def _print_pol(pol, eru=None):
    print(f"\n  POL ID     : {pol.pol_id}")
    print(f"  Generated  : {pol.generated}")
    print(f"  Cadence    : {pol.signature.cadence_mode}")
    print(f"  Loop ratio : {pol.signature.loop_ratio}")
    print(f"  Inv. prob  : {pol.signature.invention_probability}")
    print(f"\n  Motifs ({len(pol.motifs)}):")
    for m in pol.motifs:
        print(f"    • {m}")
    print(f"\n  Missing Links ({len(pol.missing_links)}):")
    for ml in pol.missing_links:
        print(f"    → {ml}")
    print(f"\n  Invention Seeds ({len(pol.invention_seeds)}):")
    for s in pol.invention_seeds:
        print(f"    [{s['priority']:6s}] {s['seed_id']}  {s['motif']}")
    if eru:
        print(f"\n  ERU Status : {eru['status']}  (variance={eru['variance']})")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="decoder_cli",
        description="BOARD-38 Pattern-of-Life Decoder",
    )
    parser.add_argument("--word-freq", metavar="PATH",
                        help="Path to word-frequency JSON file (list of {word, count})")
    parser.add_argument("--music", metavar="PATH",
                        help="Path to music token JSON file (list of note strings or dicts)")
    parser.add_argument("--text", metavar="TEXT",
                        help="Raw text string to lex directly")
    parser.add_argument("--eru", action="store_true",
                        help="Print ERU proof report")
    parser.add_argument("--emit", metavar="OUTPUT_DIR",
                        help="Emit seeds to OUTPUT_DIR/seeds/")
    parser.add_argument("--demo", action="store_true",
                        help="Run built-in demo")

    args = parser.parse_args()

    _banner()

    if args.demo:
        print("  [demo] Running with built-in SAGCO data stream...\n")
        sources = [
            json.dumps(DEMO_WORD_FREQ),
            DEMO_TEXT,
        ]
        pol = build_pattern_of_life(sources)
        eru = build_eru(pol)
        _print_pol(pol, eru)

        # Write seeds to local MISSING-LINKS/seeds/
        seeds_dir = Path(__file__).resolve().parent.parent / "MISSING-LINKS"
        seeds = emit_seeds(pol)
        write_seeds(seeds, seeds_dir)
        print(f"\n  [demo] Done. {len(seeds)} seeds written.\n")
        return

    sources: list[str] = []

    if args.word_freq:
        p = Path(args.word_freq)
        if not p.exists():
            print(f"  ERROR: file not found: {p}", file=sys.stderr)
            sys.exit(1)
        sources.append(p.read_text())

    if args.music:
        p = Path(args.music)
        if not p.exists():
            print(f"  ERROR: file not found: {p}", file=sys.stderr)
            sys.exit(1)
        raw = json.loads(p.read_text())
        from cadence_lexer import lex_music_tokens
        # Inline music lex into a fake word-freq format then treat as source text
        tokens = lex_music_tokens(raw)
        for t in tokens:
            sources.append(t.value)

    if args.text:
        sources.append(args.text)

    if not sources:
        print("  No input provided. Use --word-freq, --text, or --demo.")
        parser.print_help()
        sys.exit(1)

    pol = build_pattern_of_life(sources)
    eru = build_eru(pol) if args.eru else None
    _print_pol(pol, eru)

    if args.emit:
        out = Path(args.emit)
        seeds = emit_seeds(pol)
        write_seeds(seeds, out)


if __name__ == "__main__":
    main()
