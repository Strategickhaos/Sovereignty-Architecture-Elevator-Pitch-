"""
BOARD-38 — Pattern-of-Life Decoder
tests/test_decoder.py — Unit tests.
"""

import sys
from pathlib import Path

# Allow imports from src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cadence_lexer import lex_text, lex_word_frequency, CadenceToken
from rhythm_parser import detect_loops, parse_cadence
from tic_signature import build_signature
from motif_detector import detect_motifs, KNOWN_MOTIFS


# ── lex_text ──────────────────────────────────────────────────────────────────

def test_lex_text_basic():
    tokens = lex_text("the cat sat on the mat the cat")
    assert len(tokens) > 0
    values = [t.value for t in tokens]
    assert "the" in values or "cat" in values


def test_lex_text_empty():
    tokens = lex_text("")
    assert tokens == []


def test_lex_text_tic_detected():
    # "the" repeated many times should produce a TIC
    text = "the the the the the fox ran over the hill the bridge the road"
    tokens = lex_text(text)
    tic_tokens = [t for t in tokens if t.token_type == "TIC"]
    assert len(tic_tokens) > 0, "Expected at least one TIC token for frequent short word"


def test_lex_text_returns_cadence_tokens():
    tokens = lex_text("baby lookii found the pattern")
    for t in tokens:
        assert isinstance(t, CadenceToken)
        assert t.token_type in ("SYMBOL", "PHRASE", "LOOP", "TRANSITION", "TIC", "SPIKE")


def test_lex_word_frequency():
    data = [
        {"word": "pipeline", "count": 20},
        {"word": "board", "count": 15},
        {"word": "rare", "count": 1},
    ]
    tokens = lex_word_frequency(data)
    assert len(tokens) == 3
    # sorted highest first
    assert tokens[0].value == "pipeline"
    assert tokens[0].frequency == 20


# ── detect_loops ──────────────────────────────────────────────────────────────

def test_detect_loops_finds_repeats():
    tokens = [
        CadenceToken("PHRASE", "baby lookii", 5, ""),
        CadenceToken("PHRASE", "baby lookii", 5, ""),
        CadenceToken("PHRASE", "baby lookii", 5, ""),
        CadenceToken("PHRASE", "baby lookii", 5, ""),
        CadenceToken("SYMBOL", "unique", 1, ""),
    ]
    loops = detect_loops(tokens)
    assert len(loops) == 1
    assert loops[0][0] == "baby lookii"
    assert loops[0][1] == 4


def test_detect_loops_threshold():
    # 3 repeats should NOT appear (threshold is >3)
    tokens = [
        CadenceToken("SYMBOL", "word", 1, ""),
        CadenceToken("SYMBOL", "word", 1, ""),
        CadenceToken("SYMBOL", "word", 1, ""),
    ]
    loops = detect_loops(tokens)
    assert len(loops) == 0


def test_detect_loops_empty():
    assert detect_loops([]) == []


# ── build_signature ───────────────────────────────────────────────────────────

def test_build_signature_returns_signature():
    from cadence_lexer import lex_text
    from rhythm_parser import parse_cadence
    from tic_signature import TicSignature

    tokens = lex_text(
        "pipeline deploy compile board proof contradiction "
        "pipeline deploy compile board proof contradiction "
        "pipeline deploy compile board proof"
    )
    patterns = parse_cadence(tokens)
    sig = build_signature(patterns)
    assert isinstance(sig, TicSignature)
    assert 0.0 <= sig.invention_probability <= 1.0
    assert 0.0 <= sig.loop_ratio <= 1.0
    assert sig.cadence_mode in (
        "rapid_associative", "deep_focus", "exploratory", "inventive"
    )


def test_build_signature_empty_patterns():
    from tic_signature import TicSignature
    sig = build_signature([])
    assert isinstance(sig, TicSignature)
    assert sig.cadence_mode == "exploratory"


# ── detect_motifs ─────────────────────────────────────────────────────────────

def test_detect_motifs_finds_rapid_associative():
    from tic_signature import TicSignature
    sig = TicSignature(
        sig_id="TEST-001",
        signals=["pipeline", "compile", "deploy", "build", "iterate", "rapid", "engineering"],
        cadence_mode="rapid_associative",
        dominant_pos="SPIKE",
        dominant_board="BOARD-38",
        loop_ratio=0.20,
        invention_probability=0.70,
    )
    motifs = detect_motifs(sig)
    assert "rapid_associative_engineering" in motifs


def test_detect_motifs_baby_lookii():
    from tic_signature import TicSignature
    sig = TicSignature(
        sig_id="TEST-002",
        signals=["baby lookii", "eureka", "found it", "pattern", "connection", "novel"],
        cadence_mode="inventive",
        dominant_pos="PHRASE",
        dominant_board="BOARD-38",
        loop_ratio=0.10,
        invention_probability=0.85,
    )
    motifs = detect_motifs(sig)
    assert "baby_lookii" in motifs


def test_detect_motifs_empty_signals():
    from tic_signature import TicSignature
    sig = TicSignature(
        sig_id="TEST-003",
        signals=[],
        cadence_mode="exploratory",
        dominant_pos="SYMBOL",
        dominant_board="BOARD-37",
        loop_ratio=0.05,
        invention_probability=0.40,
    )
    # With no signals, no motifs should fire (or few at best)
    motifs = detect_motifs(sig)
    assert isinstance(motifs, list)


# ── Run all tests manually if called directly ─────────────────────────────────

if __name__ == "__main__":
    import traceback

    tests = [
        test_lex_text_basic,
        test_lex_text_empty,
        test_lex_text_tic_detected,
        test_lex_text_returns_cadence_tokens,
        test_lex_word_frequency,
        test_detect_loops_finds_repeats,
        test_detect_loops_threshold,
        test_detect_loops_empty,
        test_build_signature_returns_signature,
        test_build_signature_empty_patterns,
        test_detect_motifs_finds_rapid_associative,
        test_detect_motifs_baby_lookii,
        test_detect_motifs_empty_signals,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n  {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
