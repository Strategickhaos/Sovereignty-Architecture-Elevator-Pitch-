"""
BOARD-40-SAGCO-SOLVER — solver_pipeline.py
Orchestrates all passes: fingerprint → extract → classify → tokenize →
frequency → flashcards → quiz → ERU → motifs → seeds → summary.
"""

import json
import re
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from fingerprint import fingerprint as _fingerprint
from extractor import extract as _extract
from classifier import classify, multi_classify
from tokenizer import tokenize, word_frequency
from flashcard_generator import generate_flashcards, save_flashcards_csv, save_quiz_csv
from eru_solver import build_eru


# ── Motif detector (board38-style) ──────────────────────────────────────────

def _detect_motifs(tokens: dict, top_n: int = 20) -> list:
    """Find repeating word patterns (n-grams or top co-occurrences)."""
    freq = word_frequency(tokens, top_n=top_n)
    motifs = []
    for entry in freq[:10]:
        motifs.append({
            "motif":  entry["word"],
            "score":  entry["count"],
            "type":   "high_frequency_token",
        })
    return motifs


# ── Invention seed generator (board39-style) ─────────────────────────────────

def _generate_seeds(extracted: dict, category: str, motifs: list) -> list:
    """Generate invention seeds from dominant motifs + category."""
    seeds = []
    top_motifs = [m["motif"] for m in motifs[:5]]
    seeds.append({
        "seed_id":   "SEED-001",
        "idea":      f"Build a {category}-aware classifier that detects {', '.join(top_motifs[:3])}",
        "origin":    "frequency_analysis",
        "category":  category,
    })
    seeds.append({
        "seed_id":   "SEED-002",
        "idea":      f"Create an ERU dashboard for {category} data showing variance trends",
        "origin":    "eru_insight",
        "category":  category,
    })
    char_count = extracted.get("metadata", {}).get("char_count", 0)
    seeds.append({
        "seed_id":   "SEED-003",
        "idea":      f"Compress {char_count} chars of {category} into a category vector for SAGCO-HUB",
        "origin":    "compression_pass",
        "category":  category,
    })
    return seeds


# ── Main pipeline ─────────────────────────────────────────────────────────────

def solve(path: str, output_dir: str = None, passes: list = None) -> dict:
    """
    Run all solver passes on the given file.
    Returns full report dict and writes output files to output_dir.
    """
    p = Path(path)
    slug = re.sub(r"[^a-zA-Z0-9_-]", "_", p.stem)

    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "outputs" / slug
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    active_passes = set(passes) if passes else None
    def _active(name):
        return active_passes is None or name in active_passes

    report = {
        "file":       str(p),
        "slug":       slug,
        "output_dir": str(output_dir),
        "timestamp":  time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    # ── PASS 1: fingerprint ──────────────────────────────────────────────────
    if _active("fingerprint"):
        print(f"  [1/11] fingerprint...")
        fp = _fingerprint(path)
        report["fingerprint"] = fp

    # ── PASS 2: extract ──────────────────────────────────────────────────────
    if _active("extract"):
        print(f"  [2/11] extract...")
        extracted = _extract(path)
        report["extracted_metadata"] = extracted["metadata"]
    else:
        extracted = _extract(path)

    # ── PASS 3: classify ─────────────────────────────────────────────────────
    if _active("classify"):
        print(f"  [3/11] classify...")
        category = classify(extracted)
        multi    = multi_classify(extracted)
        report["category"]       = category
        report["multi_category"] = multi

    # ── PASS 4: tokenize ─────────────────────────────────────────────────────
    if _active("tokenize"):
        print(f"  [4/11] tokenize...")
        tokens = tokenize(extracted["text"])
        report["token_summary"] = {
            "unique_words":   len(tokens["words"]),
            "total_numbers":  len(tokens["numbers"]),
            "formulas_found": len(tokens["formulas"]),
            "formulas":       tokens["formulas"][:10],
        }

    # ── PASS 5: frequency ────────────────────────────────────────────────────
    if _active("frequency"):
        print(f"  [5/11] frequency...")
        freq = word_frequency(tokens, top_n=100)
        freq_path = output_dir / "frequency_report.txt"
        with open(freq_path, "w") as f:
            f.write(f"# Frequency Report — {p.name}\n")
            f.write(f"{'Rank':>4}  {'Word':<25} {'Count':>6}  {'Pct':>7}\n")
            f.write("-" * 50 + "\n")
            for row in freq:
                f.write(f"{row['rank']:>4}  {row['word']:<25} {row['count']:>6}  {row['pct']:>6.3f}%\n")
        report["frequency_top10"] = freq[:10]
        report["frequency_report"] = str(freq_path)

    # ── PASS 6: compression (vectors) ────────────────────────────────────────
    if _active("compression"):
        print(f"  [6/11] compression vectors...")
        # category vector: category → normalized score
        from classifier import _score
        scores = _score(extracted["text"] + " " + str(extracted.get("rows", "")))
        total_score = sum(scores.values()) or 1
        cat_vector = {k: round(v / total_score, 4) for k, v in scores.items()}

        # price vector from numbers
        numbers = tokens["numbers"]
        price_like = [n for n in numbers if 1 <= n <= 500]
        price_vector = {
            "min":    min(price_like) if price_like else 0,
            "max":    max(price_like) if price_like else 0,
            "mean":   round(sum(price_like) / len(price_like), 2) if price_like else 0,
            "count":  len(price_like),
        }
        report["category_vector"] = cat_vector
        report["price_vector"]    = price_vector

    # ── PASS 7: flashcards ───────────────────────────────────────────────────
    if _active("flashcards"):
        print(f"  [7/11] flashcards...")
        cards = generate_flashcards(extracted, category)
        fc_path = output_dir / "flashcards.csv"
        save_flashcards_csv(cards, str(fc_path))
        report["flashcard_count"] = len(cards)
        report["flashcards_path"] = str(fc_path)
    else:
        cards = generate_flashcards(extracted, category)

    # ── PASS 8: quiz ─────────────────────────────────────────────────────────
    if _active("quiz"):
        print(f"  [8/11] quiz...")
        qz_path = output_dir / "quiz.csv"
        save_quiz_csv(cards, str(qz_path))
        report["quiz_path"] = str(qz_path)

    # ── PASS 9: ERU ──────────────────────────────────────────────────────────
    seeds = []  # will be populated in pass 11

    if _active("eru"):
        print(f"  [9/11] ERU...")
        eru = build_eru(extracted, category, cards, seeds)
        eru_path = output_dir / "eru_report.yaml"
        import yaml as _yaml
        with open(eru_path, "w") as f:
            _yaml.dump(eru, f, default_flow_style=False)
        report["eru"] = eru
        report["eru_path"] = str(eru_path)

    # ── PASS 10: motifs (board38) ─────────────────────────────────────────────
    if _active("board38"):
        print(f"  [10/11] motifs (board38)...")
        motifs = _detect_motifs(tokens)
        motifs_path = output_dir / "motifs.yaml"
        import yaml as _yaml
        with open(motifs_path, "w") as f:
            _yaml.dump({"motifs": motifs}, f, default_flow_style=False)
        report["motifs"]      = motifs
        report["motifs_path"] = str(motifs_path)
    else:
        motifs = _detect_motifs(tokens)

    # ── PASS 11: seeds (board39) ──────────────────────────────────────────────
    if _active("board39"):
        print(f"  [11/11] seeds (board39)...")
        seeds = _generate_seeds(extracted, category, motifs)
        seeds_path = output_dir / "seeds.yaml"
        import yaml as _yaml
        with open(seeds_path, "w") as f:
            _yaml.dump({"seeds": seeds}, f, default_flow_style=False)
        report["seeds"]      = seeds
        report["seeds_path"] = str(seeds_path)

    # ── Write summary.md ──────────────────────────────────────────────────────
    summary_path = output_dir / "summary.md"
    _write_summary(summary_path, report, extracted, cards)
    report["summary_path"] = str(summary_path)

    return report


def _write_summary(path: Path, report: dict, extracted: dict, cards: list):
    lines = [
        f"# SAGCO Solver — {report.get('slug', '?')}",
        f"",
        f"**File:** `{report.get('file', '?')}`",
        f"**Category:** {report.get('category', '?')}",
        f"**Multi-category:** {', '.join(report.get('multi_category', []))}",
        f"**Timestamp:** {report.get('timestamp', '?')}",
        f"",
        f"## Extraction",
        f"- Characters: {extracted['metadata'].get('char_count', 0)}",
        f"- Rows: {extracted['metadata'].get('row_count', 0)}",
        f"- Symbols: {', '.join(extracted.get('symbols', [])) or 'none'}",
        f"",
        f"## Tokens",
    ]
    ts = report.get("token_summary", {})
    lines += [
        f"- Unique words: {ts.get('unique_words', 0)}",
        f"- Numbers found: {ts.get('total_numbers', 0)}",
        f"- Formulas found: {ts.get('formulas_found', 0)}",
        f"",
        f"## Flashcards",
        f"- Generated: {report.get('flashcard_count', len(cards))}",
        f"",
        f"## ERU Status",
    ]
    eru = report.get("eru", {}).get("eru", {})
    lines += [
        f"- Status: **{eru.get('status', 'N/A')}**",
        f"- Variance: {eru.get('actual', {}).get('variance', 'N/A')}",
        f"",
        f"## Seeds",
    ]
    for seed in report.get("seeds", []):
        lines.append(f"- [{seed['seed_id']}] {seed['idea']}")

    path.write_text("\n".join(lines) + "\n")


def print_report(report: dict):
    print("\n" + "=" * 60)
    print("  SAGCO SOLVER REPORT")
    print("=" * 60)
    print(f"  File:       {report.get('file', '?')}")
    print(f"  Category:   {report.get('category', '?')}")
    print(f"  Multi:      {', '.join(report.get('multi_category', []))}")
    print(f"  Output dir: {report.get('output_dir', '?')}")

    fp = report.get("fingerprint", {})
    if fp:
        print(f"\n  SHA256: {fp.get('sha256', '?')[:16]}...")
        print(f"  Size:   {fp.get('size_bytes', 0)} bytes")

    ts = report.get("token_summary", {})
    if ts:
        print(f"\n  Tokens:  {ts.get('unique_words', 0)} unique words, "
              f"{ts.get('total_numbers', 0)} numbers, "
              f"{ts.get('formulas_found', 0)} formulas")

    freq = report.get("frequency_top10", [])
    if freq:
        print(f"\n  Top 5 words:")
        for r in freq[:5]:
            print(f"    #{r['rank']:>3} {r['word']:<20} {r['count']:>5} ({r['pct']:.2f}%)")

    print(f"\n  Flashcards: {report.get('flashcard_count', '?')}")

    eru = report.get("eru", {}).get("eru", {})
    if eru:
        print(f"  ERU:        {eru.get('status', '?')} — variance={eru.get('actual', {}).get('variance', '?')}")

    seeds = report.get("seeds", [])
    if seeds:
        print(f"\n  Seeds ({len(seeds)}):")
        for s in seeds:
            print(f"    [{s['seed_id']}] {s['idea'][:70]}")

    print(f"\n  Outputs written to: {report.get('output_dir', '?')}")
    print("=" * 60)
