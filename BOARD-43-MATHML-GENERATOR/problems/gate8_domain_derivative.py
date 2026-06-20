"""
Gate 8 — Domain of derivative + Chain Rule evaluation
f(x) = sqrt(2 - 74x)
domain of f: (-inf, 1/37]
domain of f': (-inf, 1/37)
f'(-79/74) = -37/9
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import blank, text_row


def frac(n, d):
    return MFrac(MRow([Mn(str(n))]), MRow([Mn(str(d))]))


def sqrt_node(*children):
    return MRow([Mo("√"), Mo("("), *children, Mo(")")])


def build() -> Math:
    return Math([MTable([

        text_row("To find the domain of f′(x) and evaluate it, we start with:"),

        MTr([MTd([
            Mi("f"), Mo("("), Mi("x"), Mo(")"), Mo("="),
            Mo("√"), Mo("("),
            Mn("2"), Mo("−"), Mn("74"), Mi("x"),
            Mo(")"),
        ])]),

        blank(),

        # ── Domain of f ────────────────────────────────────────────────
        text_row("Step 1: Domain of f(x) — radicand must be ≥ 0:"),

        MTr([MTd([
            Mn("2"), Mo("−"), Mn("74"), Mi("x"),
            Mo("≥"), Mn("0"),
            Mo("⟹"),
            Mi("x"), Mo("≤"),
            frac(1, 37),
        ])]),

        MTr([MTd([
            MText("Domain of f:  "),
            Mo("("), Mo("−∞"), Mo(","),
            frac(1, 37),
            Mo("]"),
        ])]),

        blank(),

        # ── Chain Rule derivative ───────────────────────────────────────
        text_row("Step 2: Differentiate using the Chain Rule:"),

        MTr([MTd([
            MSup(Mi("f"), Mo("′")), Mo("("), Mi("x"), Mo(")"),
            Mo("="),
            MFrac(
                MRow([Mo("−"), Mn("37")]),
                MRow([Mo("√"), Mo("("), Mn("2"), Mo("−"), Mn("74"), Mi("x"), Mo(")")]),
            ),
        ])]),

        blank(),

        # ── Domain of f' ───────────────────────────────────────────────
        text_row("Step 3: Domain of f′(x) — denominator cannot be zero:"),

        MTr([MTd([
            MText("Exclude "),
            Mi("x"), Mo("="), frac(1, 37),
            MText("  ⟹  Domain of f′:  "),
            Mo("("), Mo("−∞"), Mo(","),
            frac(1, 37),
            Mo(")"),
        ])]),

        blank(),

        # ── Evaluate at x = -79/74 ─────────────────────────────────────
        MTr([MTd([
            MText("Step 4: Evaluate at "),
            Mi("x"), Mo("="),
            MFrac(MRow([Mo("−"), Mn("79")]), MRow([Mn("74")])),
            MText(":"),
        ])]),

        MTr([MTd([
            Mn("2"), Mo("−"), Mn("74"),
            Mo("("),
            MFrac(MRow([Mo("−"), Mn("79")]), MRow([Mn("74")])),
            Mo(")"),
            Mo("="),
            Mn("2"), Mo("+"), Mn("79"),
            Mo("="),
            Mn("81"),
            MText("  ⟹  "),
            Mo("√"), Mn("81"),
            Mo("="),
            Mn("9"),
        ])]),

        blank(),

        # ── Final answer ────────────────────────────────────────────────
        text_row("Therefore:"),

        MTr([MTd([
            MSup(Mi("f"), Mo("′")),
            Mo("("),
            MFrac(MRow([Mo("−"), Mn("79")]), MRow([Mn("74")])),
            Mo(")"),
            Mo("="),
            MFrac(
                MRow([Mo("−"), Mn("37")]),
                MRow([Mn("9")]),
            ),
        ])]),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
