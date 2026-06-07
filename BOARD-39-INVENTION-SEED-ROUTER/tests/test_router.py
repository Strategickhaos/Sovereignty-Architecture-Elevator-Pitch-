"""
tests/test_router.py — unit tests for BOARD-39 Invention Seed Router.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure src/ is on path
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from priority_queue import score_seed, rank_seeds, auto_name_board, SeedPriority
from seed_harvester import harvest_all
from eru_verifier   import verify_board


# ── Fixtures ──────────────────────────────────────────────────────────────────

SAMPLE_SEEDS = [
    {"seed_id": "S1", "title": "reusable compiler core", "source": "missing_links",
     "invention_prob": 0.8, "bond_order_gap": 0.9},
    {"seed_id": "S2", "title": "eru variance annotator", "source": "lattice_gap",
     "invention_prob": 0.6, "bond_order_gap": 0.5},
    {"seed_id": "S3", "title": "scaffold-to-board bridge", "source": "open_case",
     "invention_prob": 0.4, "bond_order_gap": 0.3},
    {"seed_id": "S4", "title": "pattern to music bridge", "source": "pattern",
     "invention_prob": 0.95, "bond_order_gap": 0.1},
]


# ── Test: score_seed produces float in [0, 1] ─────────────────────────────────

def test_score_seed_returns_float_in_range():
    for raw in SAMPLE_SEEDS:
        sp = score_seed(raw)
        assert isinstance(sp.priority_score, float), "priority_score must be float"
        assert 0.0 <= sp.priority_score <= 1.0, (
            f"priority_score {sp.priority_score} out of [0,1] for seed {raw['seed_id']}"
        )


def test_score_seed_formula():
    raw = {"seed_id": "F1", "title": "test", "source": "missing_links",
           "invention_prob": 1.0, "bond_order_gap": 1.0}
    sp = score_seed(raw)
    assert abs(sp.priority_score - 1.0) < 1e-6

    raw2 = {"seed_id": "F2", "title": "test2", "source": "missing_links",
            "invention_prob": 0.0, "bond_order_gap": 0.0}
    sp2 = score_seed(raw2)
    assert abs(sp2.priority_score - 0.0) < 1e-6


# ── Test: rank_seeds is sorted descending by priority_score ───────────────────

def test_rank_seeds_sorted_descending():
    ranked = rank_seeds(SAMPLE_SEEDS)
    scores = [sp.priority_score for sp in ranked]
    assert scores == sorted(scores, reverse=True), (
        f"rank_seeds not sorted descending: {scores}"
    )


def test_rank_seeds_returns_all():
    ranked = rank_seeds(SAMPLE_SEEDS)
    assert len(ranked) == len(SAMPLE_SEEDS)


# ── Test: auto_name_board slug generation ─────────────────────────────────────

def test_auto_name_board_basic():
    result = auto_name_board("reusable compiler core")
    assert result == "BOARD-AUTO-REUSABLE-COMPILER-CORE"


def test_auto_name_board_special_chars():
    result = auto_name_board("scaffold-to-board bridge!")
    assert result.startswith("BOARD-AUTO-")
    assert result == result.upper()
    assert "!" not in result


def test_auto_name_board_empty():
    result = auto_name_board("")
    assert result.startswith("BOARD-AUTO-")


def test_auto_name_board_long():
    long_title = "a" * 200
    result = auto_name_board(long_title)
    # Should be capped
    assert len(result) < 80


# ── Test: verify_board on known good / missing path ───────────────────────────

def test_verify_board_missing_path(tmp_path):
    result = verify_board(tmp_path / "nonexistent_board")
    assert result["verified"] is False
    assert any("does not exist" in w for w in result["warnings"])


def test_verify_board_empty_dir(tmp_path):
    board_dir = tmp_path / "empty_board"
    board_dir.mkdir()
    result = verify_board(board_dir)
    assert result["verified"] is False
    assert result["atom_count"] == 0
    assert result["bond_count"] == 0


def test_verify_board_well_formed(tmp_path):
    """A board with board.yaml, atoms/, bonds/ should verify."""
    board_dir = tmp_path / "good_board"
    board_dir.mkdir()
    (board_dir / "board.yaml").write_text("board_id: TEST\ndistrict: genesis\n")
    atoms_dir = board_dir / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "atom_1.yaml").write_text("name: concept_a\n")
    (atoms_dir / "atom_2.yaml").write_text("name: concept_b\n")
    bonds_dir = board_dir / "bonds"
    bonds_dir.mkdir()
    (bonds_dir / "bond_1.yaml").write_text("from: concept_a\nto: concept_b\n")

    result = verify_board(board_dir)
    assert result["verified"] is True
    assert result["atom_count"] == 2
    assert result["bond_count"] == 1
    assert result["stability"] > 0.0


# ── Test: harvest_all returns list even with empty sources ────────────────────

def test_harvest_all_returns_list():
    result = harvest_all()
    assert isinstance(result, list), "harvest_all must return a list"


def test_harvest_all_items_have_required_fields():
    result = harvest_all()
    for item in result:
        assert "seed_id"        in item, f"seed missing seed_id: {item}"
        assert "title"          in item, f"seed missing title: {item}"
        assert "source"         in item, f"seed missing source: {item}"
        assert "invention_prob" in item, f"seed missing invention_prob: {item}"
        assert "bond_order_gap" in item, f"seed missing bond_order_gap: {item}"
