"""
Gate 4 — Limits as x→∞ (rational function degree comparison)
a/c, +∞, 0
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import blank, text_row


def lim_inf():
    return MRow([
        MUnder(Mo("lim"), MRow([Mi("x"), Mo("→"), Mo("∞")])),
    ])


def frac(num_nodes, den_nodes):
    return MFrac(MRow(num_nodes), MRow(den_nodes))


def poly(coeff, var, exp, dots=True):
    nodes = [Mn(coeff), MSup(Mi(var), Mn(exp))]
    if dots:
        nodes += [Mo("+"), Mo("⋯")]
    return nodes


def build() -> Math:
    return Math([MTable([

        text_row("To evaluate limits as x → ∞, we compare degrees of numerator and denominator."),
        blank(),

        # ── Case 1: equal degrees ──────────────────────────────────────
        text_row("• When degrees are equal — limit = ratio of leading coefficients:"),

        MTr([MTd([
            MText("IF  deg(num) = deg(den) = 99  THEN  "),
            lim_inf(),
            frac(poly("a", "x", "99"), poly("c", "x", "99")),
            Mo("="),
            frac([Mi("a")], [Mi("c")]),
        ])]),

        blank(),

        # ── Case 2: numerator degree higher ───────────────────────────
        text_row("• When numerator degree exceeds denominator — function grows without bound:"),

        MTr([MTd([
            MText("IF  deg(num) = 99 > deg(den) = 96  THEN  "),
            lim_inf(),
            frac(poly("a", "x", "99"), poly("c", "x", "96")),
            Mo("="),
            Mo("+"), Mo("∞"),
        ])]),

        blank(),

        # ── Case 3: denominator degree higher ─────────────────────────
        text_row("• When denominator degree exceeds numerator — function approaches zero:"),

        MTr([MTd([
            MText("IF  deg(num) = 96 < deg(den) = 99  THEN  "),
            lim_inf(),
            frac(poly("a", "x", "96"), poly("c", "x", "99")),
            Mo("="),
            Mn("0"),
        ])]),

        blank(),

        # ── General rule ───────────────────────────────────────────────
        text_row("General rule for rational functions as x → ∞:"),

        MTr([MTd([
            MText("deg(num) = deg(den)  ⟹  "),
            frac([Mi("a")], [Mi("c")]),
        ])]),
        MTr([MTd([
            MText("deg(num) > deg(den)  ⟹  ±∞"),
        ])]),
        MTr([MTd([
            MText("deg(num) < deg(den)  ⟹  0"),
        ])]),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
