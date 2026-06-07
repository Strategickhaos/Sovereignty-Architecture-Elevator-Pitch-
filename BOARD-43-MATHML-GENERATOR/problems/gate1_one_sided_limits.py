"""
Gate 1 — One-sided limits, sign analysis, vertical asymptote
lim x→a- (x-9)/(x-a) = +∞
lim x→a+ (x-9)/(x-a) = -∞
lim x→a  (x-9)/(x-a) = NA (does not exist)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import blank, text_row


def lim_side(side: str):
    """side: 'a-', 'a+', or 'a'"""
    if side == "a-":
        approach = MRow([Mi("a"), MSup(Mo(""), Mo("−"))])
    elif side == "a+":
        approach = MRow([Mi("a"), MSup(Mo(""), Mo("+"))])
    else:
        approach = Mi("a")
    return MUnder(Mo("lim"), MRow([Mi("x"), Mo("→"), approach]))


def frac_xa():
    return MFrac(
        MRow([Mi("x"), Mo("−"), Mn("9")]),
        MRow([Mi("x"), Mo("−"), Mi("a")]),
    )


def build() -> Math:
    return Math([MTable([

        text_row("Given: 0 < a < 9.  We use sign analysis and one-sided limits."),
        blank(),

        # Numerator sign
        text_row("Numerator (x − 9): since a < 9, as x → a the numerator → (a − 9) < 0."),
        blank(),

        # ── Left-hand limit ────────────────────────────────────────────
        text_row("• Left-hand limit  (x → a⁻):"),

        MTr([MTd([
            MText("IF  "),
            Mo("("), Mi("x"), Mo("−"), Mi("a"), Mo(")"),
            MText("  is small negative  AND  numerator is negative  THEN:"),
        ])]),
        MTr([MTd([
            MText("  negative ÷ negative = positive  ⟹  grows without bound"),
        ])]),

        MTr([MTd([
            lim_side("a-"),
            frac_xa(),
            Mo("="),
            Mo("+"), Mo("∞"),
        ])]),

        blank(),

        # ── Right-hand limit ───────────────────────────────────────────
        text_row("• Right-hand limit  (x → a⁺):"),

        MTr([MTd([
            MText("IF  "),
            Mo("("), Mi("x"), Mo("−"), Mi("a"), Mo(")"),
            MText("  is small positive  AND  numerator is negative  THEN:"),
        ])]),
        MTr([MTd([
            MText("  negative ÷ positive = negative  ⟹  decreases without bound"),
        ])]),

        MTr([MTd([
            lim_side("a+"),
            frac_xa(),
            Mo("="),
            Mo("−"), Mo("∞"),
        ])]),

        blank(),

        # ── Two-sided comparison ───────────────────────────────────────
        text_row("• Two-sided limit comparison:"),

        MTr([MTd([
            MText("IF  left-hand limit = right-hand limit  THEN  two-sided limit exists."),
        ])]),
        MTr([MTd([
            MText("However:  "),
            Mo("+"), Mo("∞"),
            Mo("≠"),
            Mo("−"), Mo("∞"),
        ])]),
        MTr([MTd([
            MText("THEREFORE  "),
            lim_side("a"),
            frac_xa(),
            MText("  does not exist  "),
            Mo("⟹"),
            MText("  NA"),
        ])]),

        blank(),

        text_row("Method: sign analysis of numerator and denominator at each one-sided approach."),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
