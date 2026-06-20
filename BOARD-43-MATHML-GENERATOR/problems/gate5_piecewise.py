"""
Gate 5 — Piecewise continuity
A=0, B=-9, C=-5, D=-4
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import blank, text_row


def build() -> Math:
    return Math([MTable([

        text_row("For a continuous path, left-hand limit = right-hand limit = function value at each transition point."),
        blank(),

        # ── x = -2: find A ─────────────────────────────────────────────
        text_row("• At x = −2  (find A):"),
        MTr([MTd([
            Mo("−"), Mn("4"), Mo("("), Mo("−"), Mn("2"), Mo(")"),
            Mo("+"), Mi("A"), Mo("="), Mn("8"),
            Mo("⟹"),
            Mn("8"), Mo("+"), Mi("A"), Mo("="), Mn("8"),
            Mo("⟹"),
            Mi("A"), Mo("="), Mn("0"),
        ])]),

        blank(),

        # ── x = -1: find B ─────────────────────────────────────────────
        text_row("• At x = −1  (find B, using A = 0):"),
        MTr([MTd([
            MText("Left piece at −1: "),
            Mo("−"), Mn("4"), Mo("("), Mo("−"), Mn("1"), Mo(")"),
            Mo("+"), Mn("0"), Mo("="), Mn("4"),
        ])]),
        MTr([MTd([
            Mi("B"), Mo("("), Mo("−"), Mn("1"), Mo(")"),
            Mo("−"), Mn("5"), Mo("="), Mn("4"),
            Mo("⟹"),
            Mo("−"), Mi("B"), Mo("="), Mn("9"),
            Mo("⟹"),
            Mi("B"), Mo("="), Mo("−"), Mn("9"),
        ])]),

        blank(),

        # ── x = 0: find C ──────────────────────────────────────────────
        text_row("• At x = 0  (find C):"),
        MTr([MTd([
            MText("Left piece at 0: "),
            Mi("B"), Mo("("), Mn("0"), Mo(")"),
            Mo("−"), Mn("5"), Mo("="), Mo("−"), Mn("5"),
        ])]),
        MTr([MTd([
            Mn("16"), Mo("("), Mn("0"), Mo(")"),
            Mo("+"), Mi("C"), Mo("="), Mo("−"), Mn("5"),
            Mo("⟹"),
            Mi("C"), Mo("="), Mo("−"), Mn("5"),
        ])]),

        blank(),

        # ── x = 1: find D ──────────────────────────────────────────────
        text_row("• At x = 1  (find D, using C = −5):"),
        MTr([MTd([
            Mn("16"), Mo("("), Mn("1"), Mo(")"),
            Mo("+"), Mo("("), Mo("−"), Mn("5"), Mo(")"),
            Mo("="), Mn("11"),
        ])]),
        MTr([MTd([
            Mi("D"), Mo("("), Mn("1"), Mo(")"),
            Mo("+"), Mn("15"), Mo("="), Mn("11"),
            Mo("⟹"),
            Mi("D"), Mo("="), Mo("−"), Mn("4"),
        ])]),

        blank(),

        # ── x = 2: confirm D ───────────────────────────────────────────
        text_row("• At x = 2  (confirm D = −4):"),
        MTr([MTd([
            Mo("("), Mo("−"), Mn("4"), Mo(")"),
            Mo("("), Mn("2"), Mo(")"),
            Mo("+"), Mn("15"), Mo("="),
            Mo("−"), Mn("8"), Mo("+"), Mn("15"),
            Mo("="), Mn("7"), Mo("✓"),
        ])]),

        blank(),

        # ── Answer ─────────────────────────────────────────────────────
        text_row("Constants that produce a continuous path:"),
        MTr([MTd([
            Mi("A"), Mo("="), Mn("0"),
            MText(",   "),
            Mi("B"), Mo("="), Mo("−"), Mn("9"),
            MText(",   "),
            Mi("C"), Mo("="), Mo("−"), Mn("5"),
            MText(",   "),
            Mi("D"), Mo("="), Mo("−"), Mn("4"),
        ])]),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
