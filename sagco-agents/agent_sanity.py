#!/usr/bin/env python3
"""
SAGCO Sanity Check — Anti-Hallucination Engine

Pipeline:
  input → lexer → parser → enumerator → compiler → echo-magic →
  anti-hallucination filter → sovereign-unit normalizer → Sovereign Truth Score

Usage:
  sagco sanity "some claim or text"
  sagco sanity --file path/to/file.yaml
  sagco sanity --self                    # sanity-check the repo itself
"""

from __future__ import annotations
import re, sys, json, hashlib, yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

BANNER = """
╔════════════════════════════════════════════════════════════╗
║  SAGCO SANITY CHECK — Anti-Hallucination Engine           ║
║  Trust nothing. Verify everything. Compile the universe.  ║
╚════════════════════════════════════════════════════════════╝
"""

# ── Stage 1: Lexer — tokenize the claim ──────────────────────────────────────

HALLUCINATION_MARKERS = [
    "trust me", "definitely", "always works", "never fails", "100%",
    "impossible", "can't be done", "obviously", "clearly", "just works",
    "no way", "guaranteed", "proven fact",
]
SOVEREIGN_ANCHORS = [
    "eru", "expected", "actual", "variance", "antibody", "citizen",
    "board", "district", "invariant", "pmi", "sagco", "proof",
]

@dataclass
class SanityToken:
    kind:  str
    value: str

def lex(text: str) -> list[SanityToken]:
    tokens = []
    words = re.findall(r'\b\w[\w\-]*\b', text.lower())
    for w in words:
        if any(h in w for h in HALLUCINATION_MARKERS):
            tokens.append(SanityToken("HALLUCINATION_MARKER", w))
        elif any(a in w for a in SOVEREIGN_ANCHORS):
            tokens.append(SanityToken("SOVEREIGN_ANCHOR", w))
        elif re.match(r'^\d+$', w):
            tokens.append(SanityToken("NUMBER", w))
        elif len(w) > 2:
            tokens.append(SanityToken("WORD", w))
    return tokens


# ── Stage 2: Parser — structure the claim ────────────────────────────────────

@dataclass
class SanityClaim:
    raw:          str
    hallucination_count: int = 0
    anchor_count: int = 0
    number_count: int = 0
    word_count:   int = 0
    has_expected: bool = False
    has_actual:   bool = False
    has_variance: bool = False

def parse_claim(text: str, tokens: list[SanityToken]) -> SanityClaim:
    c = SanityClaim(raw=text)
    for tok in tokens:
        if tok.kind == "HALLUCINATION_MARKER": c.hallucination_count += 1
        elif tok.kind == "SOVEREIGN_ANCHOR":   c.anchor_count += 1
        elif tok.kind == "NUMBER":             c.number_count += 1
        elif tok.kind == "WORD":               c.word_count   += 1
    tl = text.lower()
    c.has_expected = "expected" in tl
    c.has_actual   = "actual"   in tl
    c.has_variance = "variance" in tl or "delta" in tl
    return c


# ── Stage 3: Echo-Magic — repeat back and detect contradictions ───────────────

def echo_magic(claim: SanityClaim) -> dict:
    echo = {
        "echo": claim.raw[:200],
        "contradictions_detected": [],
    }
    raw = claim.raw.lower()
    # Check for contradictory pairs
    pairs = [
        ("always", "never"), ("definitely", "maybe"),
        ("100%", "error"), ("impossible", "built"),
        ("never fails", "exception"), ("guaranteed", "variance"),
    ]
    for a, b in pairs:
        if a in raw and b in raw:
            echo["contradictions_detected"].append(f"'{a}' contradicts '{b}'")
    return echo


# ── Stage 4: Compiler — can the claim be formalized? ─────────────────────────

def compile_claim(claim: SanityClaim) -> dict:
    compilable = claim.has_expected and claim.has_actual
    eru_complete = claim.has_expected and claim.has_actual and claim.has_variance
    return {
        "compilable":   compilable,
        "eru_complete": eru_complete,
        "missing":      (
            (["expected"] if not claim.has_expected else []) +
            (["actual"]   if not claim.has_actual   else []) +
            (["variance"] if not claim.has_variance else [])
        ),
    }


# ── Stage 5: Anti-Hallucination Filter ───────────────────────────────────────

def anti_hallucination(claim: SanityClaim, echo: dict) -> dict:
    flags = []
    if claim.hallucination_count > 0:
        flags.append(f"{claim.hallucination_count} hallucination marker(s) detected")
    if echo["contradictions_detected"]:
        flags += [f"contradiction: {c}" for c in echo["contradictions_detected"]]
    if claim.anchor_count == 0 and claim.word_count > 10:
        flags.append("no sovereign anchors found — claim is untethered")
    return {
        "clean":  len(flags) == 0,
        "flags":  flags,
    }


# ── Stage 6: Sovereign Truth Score ───────────────────────────────────────────

def sovereign_truth_score(claim: SanityClaim, compiled: dict,
                           anti_hal: dict, echo: dict) -> dict:
    score = 10.0
    # Deductions
    score -= claim.hallucination_count * 2.0
    score -= len(echo["contradictions_detected"]) * 1.5
    score -= len(anti_hal["flags"]) * 0.5
    # Bonuses
    if compiled["eru_complete"]:   score += 2.0
    elif compiled["compilable"]:   score += 1.0
    score += min(3.0, claim.anchor_count * 0.5)
    score  = max(0.0, min(10.0, score))

    grade = (
        "SOVEREIGN"       if score >= 9.0 else
        "DISTINGUISHED"   if score >= 7.0 else
        "PASS"            if score >= 5.0 else
        "SUSPECT"         if score >= 3.0 else
        "HALLUCINATED"
    )
    return {"score": round(score, 1), "grade": grade, "out_of": 10.0}


# ── Self-check — verify the repo itself ──────────────────────────────────────

def self_check() -> dict:
    results = {}
    boards = sorted([d for d in REPO_ROOT.iterdir()
                     if d.is_dir() and d.name.startswith("BOARD-")])
    for board in boards:
        board_yaml = board / "board.yaml"
        results[board.name] = {
            "board_yaml": board_yaml.exists(),
            "src_exists": (board / "src").exists(),
            "status":     "OK" if board_yaml.exists() else "MISSING board.yaml",
        }

    # Citizen registry sanity
    reg = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    reg_ok = False
    cit_count = 0
    if reg.exists():
        try:
            raw = json.loads(reg.read_text())
            citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw
            cit_count = len(citizens)
            cid_re = re.compile(r'^sgc-[\w-]+-\d{13}-\d{1,4}$')
            malformed = sum(1 for c in citizens if not cid_re.match(c.get("cid", "")))
            reg_ok = malformed == 0
        except Exception as e:
            results["citizen_registry"] = {"error": str(e)}

    # Antibody count
    ab_dir = REPO_ROOT / "BOARD-11-ANTIBODIES" / "antibodies"
    ab_count = len(list(ab_dir.glob("*.yaml"))) if ab_dir.exists() else 0

    # Missing-links seeds
    seeds_dir = REPO_ROOT / "MISSING-LINKS" / "seeds"
    seed_count = len(list(seeds_dir.glob("*.yaml"))) if seeds_dir.exists() else 0

    return {
        "boards_checked": len(boards),
        "boards_healthy": sum(1 for v in results.values()
                              if isinstance(v, dict) and v.get("board_yaml")),
        "citizen_count":  cit_count,
        "citizen_registry_ok": reg_ok,
        "antibody_count": ab_count,
        "invention_seeds": seed_count,
        "board_detail":   results,
    }


# ── Runner ────────────────────────────────────────────────────────────────────

def run_pipeline(text: str) -> dict:
    tokens   = lex(text)
    claim    = parse_claim(text, tokens)
    echo     = echo_magic(claim)
    compiled = compile_claim(claim)
    anti_hal = anti_hallucination(claim, echo)
    score    = sovereign_truth_score(claim, compiled, anti_hal, echo)

    return {
        "input":              text[:200],
        "tokens":             len(tokens),
        "hallucination_markers": claim.hallucination_count,
        "sovereign_anchors":  claim.anchor_count,
        "eru_complete":       compiled["eru_complete"],
        "missing_eru_fields": compiled["missing"],
        "contradictions":     echo["contradictions_detected"],
        "flags":              anti_hal["flags"],
        "clean":              anti_hal["clean"],
        "sovereign_truth_score": score["score"],
        "grade":              score["grade"],
    }


def print_result(r: dict):
    grade_color = {
        "SOVEREIGN": "🟢", "DISTINGUISHED": "🟣", "PASS": "⚪",
        "SUSPECT": "🟡", "HALLUCINATED": "🔴",
    }.get(r["grade"], "?")
    print(f"\n  {grade_color} Sovereign Truth Score: {r['sovereign_truth_score']}/10  [{r['grade']}]")
    print(f"  Tokens          : {r['tokens']}")
    print(f"  Anchors         : {r['sovereign_anchors']}")
    print(f"  Halluc. markers : {r['hallucination_markers']}")
    print(f"  ERU complete    : {r['eru_complete']}")
    if r['missing_eru_fields']:
        print(f"  Missing ERU     : {', '.join(r['missing_eru_fields'])}")
    if r['flags']:
        print(f"  Flags:")
        for f in r['flags']:
            print(f"    ⚠  {f}")
    if r['contradictions']:
        print(f"  Contradictions:")
        for c in r['contradictions']:
            print(f"    ✗  {c}")
    print()


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]

    print(BANNER)

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    if "--self" in args:
        result = self_check()
        print(f"  SAGCO Self-Check\n")
        print(f"  Boards checked    : {result['boards_checked']}")
        print(f"  Boards healthy    : {result['boards_healthy']}")
        print(f"  Citizens          : {result['citizen_count']}")
        print(f"  Registry OK       : {result['citizen_registry_ok']}")
        print(f"  Antibodies        : {result['antibody_count']}")
        print(f"  Invention seeds   : {result['invention_seeds']}")
        for board, data in result["board_detail"].items():
            sym = "✓" if data.get("board_yaml") else "✗"
            print(f"  {sym} {board}")
        return

    if "--file" in args:
        idx = args.index("--file")
        path = Path(args[idx + 1])
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        text = " ".join(args)

    result = run_pipeline(text)
    print_result(result)


if __name__ == "__main__":
    main()
