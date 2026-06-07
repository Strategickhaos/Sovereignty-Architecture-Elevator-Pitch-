#!/usr/bin/env python3
"""
sheet_music_cli.py — SAGCO Sheet Music CLI (BOARD-37)

Usage:
  python sheet_music_cli.py --xlsx PATH [--out DIR] [--bpm 120] [--title "name"]
  python sheet_music_cli.py --csv PATH [--out DIR]
  python sheet_music_cli.py --demo          # runs built-in demo with sample words
  python sheet_music_cli.py --eru           # prints ERU report

Outputs:
  exports/score.abc     ABC notation
  exports/score.mid     MIDI file
  exports/score.txt     text score
  reports/music_eru.yaml
"""
import argparse
import os
import sys

# Allow running from the src/ directory
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from music_mapper import map_rows_to_notes
from xlsx_parser import load_frequency_data
from abc_exporter import save_abc
from midi_exporter import save_midi
from text_score import render_text_score, print_score
from eru_report import build_eru_report

BOARD_ROOT = os.path.join(HERE, "..")
EXPORTS_DIR = os.path.join(BOARD_ROOT, "exports")
REPORTS_DIR = os.path.join(BOARD_ROOT, "reports")

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║   BOARD-37  ·  SAGCO  SHEET  MUSIC  CLI                      ║
║   district: frequency_coast  ·  role: sheet_music_compiler   ║
║   "Every word becomes a note. Every score is sovereign law." ║
╚══════════════════════════════════════════════════════════════╝
"""

# ── Demo data ─────────────────────────────────────────────────────────────────

DEMO_ROWS = [
    {"rank": 1,  "word": "registry",  "lemma": "registry",  "pos": "Noun",        "pct": 1.20, "occurrence": 45},
    {"rank": 2,  "word": "sagco",     "lemma": "sagco",     "pos": "Noun",        "pct": 1.10, "occurrence": 42},
    {"rank": 3,  "word": "compile",   "lemma": "compile",   "pos": "Verb",        "pct": 1.05, "occurrence": 40},
    {"rank": 4,  "word": "sovereign", "lemma": "sovereign", "pos": "Adjective",   "pct": 0.95, "occurrence": 36},
    {"rank": 5,  "word": "cell",      "lemma": "cell",      "pos": "Noun",        "pct": 0.90, "occurrence": 34},
    {"rank": 6,  "word": "formula",   "lemma": "formula",   "pos": "Noun",        "pct": 0.85, "occurrence": 32},
    {"rank": 7,  "word": "lexer",     "lemma": "lexer",     "pos": "Noun",        "pct": 0.80, "occurrence": 30},
    {"rank": 8,  "word": "parse",     "lemma": "parse",     "pos": "Verb",        "pct": 0.75, "occurrence": 28},
    {"rank": 9,  "word": "abstract",  "lemma": "abstract",  "pos": "Adjective",   "pct": 0.70, "occurrence": 26},
    {"rank": 10, "word": "quickly",   "lemma": "quickly",   "pos": "Adverb",      "pct": 0.65, "occurrence": 24},
    {"rank": 11, "word": "compiler",  "lemma": "compiler",  "pos": "Noun",        "pct": 0.60, "occurrence": 23},
    {"rank": 12, "word": "guard",     "lemma": "guard",     "pos": "Verb",        "pct": 0.55, "occurrence": 21},
    {"rank": 13, "word": "mobius",    "lemma": "mobius",    "pos": "Noun",        "pct": 0.50, "occurrence": 19},
    {"rank": 14, "word": "and",       "lemma": "and",       "pos": "Conjunction", "pct": 0.45, "occurrence": 17},
    {"rank": 15, "word": "eru",       "lemma": "eru",       "pos": "Noun",        "pct": 0.40, "occurrence": 15},
    {"rank": 16, "word": "sheet",     "lemma": "sheet",     "pos": "Noun",        "pct": 0.35, "occurrence": 13},
    {"rank": 17, "word": "morse",     "lemma": "morse",     "pos": "Noun",        "pct": 0.30, "occurrence": 11},
    {"rank": 18, "word": "value",     "lemma": "value",     "pos": "Noun",        "pct": 0.25, "occurrence": 9},
    {"rank": 19, "word": "passes",    "lemma": "pass",      "pos": "Verb",        "pct": 0.20, "occurrence": 7},
    {"rank": 20, "word": "tokens",    "lemma": "token",     "pos": "Noun",        "pct": 0.15, "occurrence": 5},
]


# ── Core pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(rows: list, out_dir: str, bpm: int, title: str, source: str = "demo"):
    """Run the full mapping + export pipeline."""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    print(f"[sheet_music] Mapping {len(rows)} words to notes...")
    notes = map_rows_to_notes(rows)

    abc_path  = os.path.join(out_dir, "score.abc")
    midi_path = os.path.join(out_dir, "score.mid")
    txt_path  = os.path.join(out_dir, "score.txt")

    print(f"[sheet_music] Exporting ABC  → {abc_path}")
    save_abc(notes, abc_path, title=title)

    print(f"[sheet_music] Exporting MIDI → {midi_path}")
    save_midi(notes, midi_path, bpm=bpm)

    print(f"[sheet_music] Exporting text → {txt_path}")
    score_text = render_text_score(notes)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(score_text)

    print(f"[sheet_music] Building ERU report...")
    eru = build_eru_report(notes, source, [abc_path, midi_path, txt_path])

    print_score(notes)
    print(f"[sheet_music] ERU status: {eru['proof']['status']} — {eru['proof']['message']}")
    print(f"[sheet_music] Done. Outputs in {out_dir}/")
    return notes, eru


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="SAGCO Sheet Music CLI — converts word frequency data to music",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--xlsx",  metavar="PATH", help="Input XLSX file")
    parser.add_argument("--csv",   metavar="PATH", help="Input CSV file")
    parser.add_argument("--out",   metavar="DIR",  default=EXPORTS_DIR, help="Output directory")
    parser.add_argument("--bpm",   type=int, default=120, help="Tempo in BPM (default 120)")
    parser.add_argument("--title", default="SAGCO Score", help="Score title")
    parser.add_argument("--demo",  action="store_true", help="Run with built-in demo data")
    parser.add_argument("--eru",   action="store_true", help="Print ERU report")

    args = parser.parse_args()

    if args.eru:
        eru_path = os.path.join(REPORTS_DIR, "music_eru.yaml")
        if os.path.exists(eru_path):
            with open(eru_path) as f:
                print(f.read())
        else:
            print("[eru] No report found. Run a conversion first.")
        return

    if args.demo:
        run_pipeline(DEMO_ROWS, args.out, args.bpm, args.title, source="demo")
        return

    if args.xlsx:
        rows = load_frequency_data(args.xlsx)
        run_pipeline(rows, args.out, args.bpm, args.title, source=args.xlsx)
        return

    if args.csv:
        rows = load_frequency_data(args.csv)
        run_pipeline(rows, args.out, args.bpm, args.title, source=args.csv)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
