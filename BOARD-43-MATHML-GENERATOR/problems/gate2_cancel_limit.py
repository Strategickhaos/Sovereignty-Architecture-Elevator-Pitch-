"""
Gate 2 — Factor and cancel, removable discontinuity
g(x) = (x+7)/(x²-49), lim x→-7 = -1/14
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import blank, text_row


def lim_neg7():
    return MUnder(
        Mo("lim"),
        MRow([Mi("x"), Mo("→"), Mo("−"), Mn("7")])
    )


def frac(num_nodes, den_nodes):
    return MFrac(MRow(num_nodes), MRow(den_nodes))


def build() -> Math:
    return Math([MTable([

        text_row("To evaluate the limit, we factor the denominator and cancel common factors."),
        blank(),

        # ── Step 1: Factor ─────────────────────────────────────────────
        text_row("Step 1: Factor the denominator:"),
        MTr([MTd([
            MSup(Mi("x"), Mn("2")), Mo("−"), Mn("49"),
            Mo("="),
            Mo("("), Mi("x"), Mo("+"), Mn("7"), Mo(")"),
            Mo("("), Mi("x"), Mo("−"), Mn("7"), Mo(")"),
        ])]),

        MTr([MTd([
            MText("Function undefined at  "),
            Mi("x"), Mo("="), Mo("−"), Mn("7"),
            MText("  and  "),
            Mi("x"), Mo("="), Mn("7"),
            MText("  (denominator = 0)"),
        ])]),

        blank(),

        # ── Step 2: Cancel ─────────────────────────────────────────────
        text_row("Step 2: Cancel the common factor (x + 7):"),
        MTr([MTd([
            frac(
                [Mi("x"), Mo("+"), Mn("7")],
                [Mo("("), Mi("x"), Mo("+"), Mn("7"), Mo(")"),
                 Mo("("), Mi("x"), Mo("−"), Mn("7"), Mo(")")],
            ),
            Mo("="),
            frac([Mn("1")], [Mi("x"), Mo("−"), Mn("7")]),
            MText("  (removable discontinuity at x = −7)"),
        ])]),

        blank(),

        # ── Step 3: Substitute ─────────────────────────────────────────
        text_row("Step 3: Evaluate the limit by direct substitution:"),
        MTr([MTd([
            lim_neg7(),
            frac([Mn("1")], [Mi("x"), Mo("−"), Mn("7")]),
            Mo("="),
            frac([Mn("1")], [Mo("−"), Mn("7"), Mo("−"), Mn("7")]),
            Mo("="),
            frac([Mn("1")], [Mo("−"), Mn("14")]),
            Mo("="),
            Mo("−"),
            frac([Mn("1")], [Mn("14")]),
        ])]),

        blank(),

        # ── Conclusion ─────────────────────────────────────────────────
        text_row("The factor (x + 7) cancels — removable discontinuity, limit exists:"),
        MTr([MTd([
            lim_neg7(),
            frac(
                [Mi("x"), Mo("+"), Mn("7")],
                [MSup(Mi("x"), Mn("2")), Mo("−"), Mn("49")],
            ),
            Mo("="),
            Mo("−"),
            frac([Mn("1")], [Mn("14")]),
        ])]),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
