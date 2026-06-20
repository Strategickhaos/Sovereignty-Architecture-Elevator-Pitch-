"""
Gate 10 — Ordering derivatives f'(1), h'(1), g'(1) from least to greatest
f(x) = a^x ln(x)   → Product Rule
h(x) = ln(x)/sqrt(128x)  → Quotient Rule
g(x) = e^(πx)      → Chain Rule
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.node import *
from src.render import render, render_compact
from src.builders import blank, text_row


def _frac(num_nodes, den_nodes):
    return MFrac(MRow(num_nodes), MRow(den_nodes))


def _sup(base, sup):
    return MSup(Mi(base), Mo(sup) if len(sup) == 1 else MText(sup))


def _eval_row(label, derivative_nodes, result_nodes, note=""):
    nodes = [MText(f"• {label}:  ")]
    nodes += derivative_nodes
    nodes.append(Mo("="))
    nodes += result_nodes
    if note:
        nodes.append(MText(f"  {note}"))
    return MTr([MTd(nodes)])


def build() -> Math:
    return Math([MTable([

        text_row("To order f′(1), h′(1), g′(1) from least to greatest, we compute the derivatives at x = 1."),
        blank(),

        # ── f(x) = a^x · ln(x), Product Rule ──────────────────────────
        MTr([MTd([
            MText("• For "),
            Mi("f"), Mo("("), Mi("x"), Mo(")"), Mo("="),
            MSup(Mi("a"), Mi("x")),
            Mi("ln"), Mo("("), Mi("x"), Mo(")"),
            MText(",  by Product Rule:"),
        ])]),

        MTr([MTd([
            MText("  "),
            MSup(Mi("f"), Mo("′")), Mo("("), Mn("1"), Mo(")"),
            Mo("="),
            MSup(Mi("a"), Mn("1")),
            Mi("ln"), Mo("("), Mn("1"), Mo(")"),
            Mo("+"),
            MSup(Mi("a"), Mn("1")),
            Mo("·"),
            _frac([Mn("1")], [Mn("1")]),
            Mo("="),
            Mi("a"), Mo("·"), Mn("0"), Mo("+"), Mi("a"),
            Mo("="),
            Mi("a"),
        ])]),

        blank(),

        # ── h(x) = ln(x)/sqrt(128x), Quotient Rule ────────────────────
        MTr([MTd([
            MText("• For "),
            Mi("h"), Mo("("), Mi("x"), Mo(")"), Mo("="),
            _frac(
                [Mi("ln"), Mo("("), Mi("x"), Mo(")")],
                [Mo("√"), Mo("("), Mn("128"), Mi("x"), Mo(")")],
            ),
            MText(",  by Quotient Rule:"),
        ])]),

        MTr([MTd([
            MText("  "),
            MSup(Mi("h"), Mo("′")), Mo("("), Mn("1"), Mo(")"),
            Mo("="),
            _frac(
                [_frac([Mn("1")], [Mn("1")]),
                 Mo("·"), Mo("√"), Mn("128"),
                 Mo("−"),
                 Mi("ln"), Mo("("), Mn("1"), Mo(")"),
                 Mo("·"),
                 _frac([Mn("1")], [Mn("2"), Mo("√"), Mn("128")])],
                [Mn("128")],
            ),
            Mo("="),
            _frac([Mn("1")], [Mo("√"), Mn("128")]),
            Mo("="),
            _frac([Mn("1")], [MSup(Mn("8"), Mo("√")), Mn("2")]),
        ])]),

        blank(),

        # ── g(x) = e^(πx), Chain Rule ──────────────────────────────────
        MTr([MTd([
            MText("• For "),
            Mi("g"), Mo("("), Mi("x"), Mo(")"), Mo("="),
            MSup(Mi("e"), MRow([Mi("π"), Mi("x")])),
            MText(",  by Chain Rule:"),
        ])]),

        MTr([MTd([
            MText("  "),
            MSup(Mi("g"), Mo("′")), Mo("("), Mn("1"), Mo(")"),
            Mo("="),
            Mi("π"),
            MSup(Mi("e"), Mi("π")),
        ])]),

        blank(),

        # ── Comparison ─────────────────────────────────────────────────
        text_row("Since a ≥ 2:"),

        MTr([MTd([
            _frac([Mn("1")], [Mo("√"), Mn("128")]),
            Mo("<"),
            Mi("a"),
            Mo("<"),
            Mi("π"), MSup(Mi("e"), Mi("π")),
        ])]),

        blank(),

        text_row("Correct order from least to greatest:"),

        MTr([MTd([
            MSup(Mi("h"), Mo("′")), Mo("("), Mn("1"), Mo(")"),
            Mo("<"),
            MSup(Mi("f"), Mo("′")), Mo("("), Mn("1"), Mo(")"),
            Mo("<"),
            MSup(Mi("g"), Mo("′")), Mo("("), Mn("1"), Mo(")"),
        ])]),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
