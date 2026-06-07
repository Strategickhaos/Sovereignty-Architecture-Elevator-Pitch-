"""
Gate 11 — Implicit differentiation, tangent line to cardioid at (2,0)
Builds MathML as a tree, not a string.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import row, blank, text_row, prime, double_prime, nth_deriv, inline

def build() -> Math:
    return Math([MTable([

        text_row("To find the tangent line at (2, 0) we use implicit differentiation."),

        blank(),

        # Curve
        MTr([MTd([
            MText("Given: "),
            MSup(Mi("x"), Mn("2")),
            Mo("+"),
            MSup(Mi("y"), Mn("2")),
            Mo("="),
            MSup(
                MRow([
                    Mo("("),
                    Mn("12"), MSup(Mi("x"), Mn("2")),
                    Mo("+"),
                    Mn("12"), MSup(Mi("y"), Mn("2")),
                    Mo("−"), Mi("y"),
                    Mo(")"),
                ]),
                Mn("2")
            ),
        ])]),

        blank(),

        text_row("Differentiating both sides with respect to x (Chain Rule on right side):"),

        # dy/dx general form
        MTr([MTd([
            MText("Implicit diff ⇒ "),
            MFrac(
                MRow([Mi("d"), Mi("y")]),
                MRow([Mi("d"), Mi("x")]),
            ),
            Mo("="),
            MText(" (expression in x and y)"),
        ])]),

        blank(),

        text_row("Substituting the point (2, 0):"),

        # slope evaluation
        MTr([MTd([
            MFrac(
                MRow([Mi("d"), Mi("y")]),
                MRow([Mi("d"), Mi("x")]),
            ),
            Mo("|"),
            MTd([MRow([
                MSub(Mi(""), MRow([Mo("("), Mn("2"), Mo(","), Mn("0"), Mo(")")])),
            ])]),
            Mo("="),
            Mn("1"),
        ])]),

        blank(),

        text_row("Point-slope form with slope = 1 through (2, 0):"),

        # point-slope
        MTr([MTd([
            Mi("y"),
            Mo("−"),
            Mn("0"),
            Mo("="),
            Mn("1"),
            Mo("("),
            Mi("x"),
            Mo("−"),
            Mn("2"),
            Mo(")"),
        ])]),

        blank(),

        text_row("Tangent line equation:"),

        # final answer
        MTr([MTd([
            Mi("y"),
            Mo("="),
            Mi("x"),
            Mo("−"),
            Mn("2"),
        ])]),

        blank(),

        text_row("This line is tangent to the cardioid at (2, 0)."),

    ])])


if __name__ == "__main__":
    import sys
    tree = build()
    if "--compact" in sys.argv:
        print(render_compact(tree))
    else:
        print(render(tree))
