"""
Gate 6 — Product Rule + Quotient Rule
m'(-1) = 790,  n'(8) = 18
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import blank, text_row


def frac(num_nodes, den_nodes):
    return MFrac(MRow(num_nodes), MRow(den_nodes))


def build() -> Math:
    return Math([MTable([

        text_row("To find the passcode, we compute m′(x) and n′(x) using differentiation rules."),
        blank(),

        # ── Product Rule ───────────────────────────────────────────────
        text_row("• Product Rule:"),

        MTr([MTd([
            MText("If  "),
            Mi("m"), Mo("("), Mi("x"), Mo(")"), Mo("="),
            Mi("f"), Mo("("), Mi("x"), Mo(")"),
            Mo("·"),
            Mi("g"), Mo("("), Mi("x"), Mo(")"),
            MText("  then:"),
        ])]),

        MTr([MTd([
            MSup(Mi("m"), Mo("′")), Mo("("), Mi("x"), Mo(")"), Mo("="),
            MSup(Mi("f"), Mo("′")), Mo("("), Mi("x"), Mo(")"),
            Mi("g"), Mo("("), Mi("x"), Mo(")"),
            Mo("+"),
            Mi("f"), Mo("("), Mi("x"), Mo(")"),
            MSup(Mi("g"), Mo("′")), Mo("("), Mi("x"), Mo(")"),
        ])]),

        blank(),

        text_row("Evaluating at x = −1:"),

        MTr([MTd([
            MSup(Mi("m"), Mo("′")),
            Mo("("), Mo("−"), Mn("1"), Mo(")"),
            Mo("="),
            Mn("790"),
        ])]),

        blank(),

        # ── Quotient Rule ──────────────────────────────────────────────
        text_row("• Quotient Rule:"),

        MTr([MTd([
            MText("If  "),
            Mi("n"), Mo("("), Mi("x"), Mo(")"), Mo("="),
            frac(
                [Mi("g"), Mo("("), Mi("x"), Mo(")")],
                [Mi("h"), Mo("("), Mi("x"), Mo(")")],
            ),
            MText("  then:"),
        ])]),

        MTr([MTd([
            MSup(Mi("n"), Mo("′")), Mo("("), Mi("x"), Mo(")"), Mo("="),
            frac(
                [
                    MSup(Mi("g"), Mo("′")), Mo("("), Mi("x"), Mo(")"),
                    Mi("h"), Mo("("), Mi("x"), Mo(")"),
                    Mo("−"),
                    Mi("g"), Mo("("), Mi("x"), Mo(")"),
                    MSup(Mi("h"), Mo("′")), Mo("("), Mi("x"), Mo(")"),
                ],
                [
                    MSup(
                        MRow([Mi("h"), Mo("("), Mi("x"), Mo(")")]),
                        Mn("2")
                    ),
                ],
            ),
        ])]),

        blank(),

        text_row("Evaluating at x = 8  (where h(8) ≠ 0):"),

        MTr([MTd([
            MSup(Mi("n"), Mo("′")),
            Mo("("), Mn("8"), Mo(")"),
            Mo("="),
            Mn("18"),
        ])]),

        blank(),

        # ── Passcode ───────────────────────────────────────────────────
        text_row("Passcode for the Fifth Gate:"),

        MTr([MTd([
            MSup(Mi("m"), Mo("′")),
            Mo("("), Mo("−"), Mn("1"), Mo(")"),
            Mo("="), Mn("790"),
            MText("   and   "),
            MSup(Mi("n"), Mo("′")),
            Mo("("), Mn("8"), Mo(")"),
            Mo("="), Mn("18"),
        ])]),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
