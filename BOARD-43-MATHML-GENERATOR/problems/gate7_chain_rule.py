"""
Gate 7 — Chain Rule: find a where f'(2) = -188
f(t) = (1/a) * u(t)^47,  u(t) = 2t^3 - 15t^2 + 45
Answer: a = 9
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

        text_row("To find a such that f′(2) = −188, we differentiate using the Chain Rule."),
        blank(),

        # Given function
        text_row("Given:"),
        MTr([MTd([
            Mi("f"), Mo("("), Mi("t"), Mo(")"), Mo("="),
            frac([Mn("1")], [Mi("a")]),
            Mo("·"),
            MSup(
                MRow([Mi("u"), Mo("("), Mi("t"), Mo(")")]),
                Mn("47")
            ),
            MText(",   where  "),
            Mi("u"), Mo("("), Mi("t"), Mo(")"), Mo("="),
            Mn("2"), MSup(Mi("t"), Mn("3")),
            Mo("−"), Mn("15"), MSup(Mi("t"), Mn("2")),
            Mo("+"), Mn("45"),
        ])]),

        blank(),

        # Chain Rule
        text_row("By the Chain Rule:"),
        MTr([MTd([
            MSup(Mi("f"), Mo("′")), Mo("("), Mi("t"), Mo(")"), Mo("="),
            frac([Mn("1")], [Mi("a")]),
            Mo("·"), Mn("47"), Mo("·"),
            MSup(
                MRow([Mi("u"), Mo("("), Mi("t"), Mo(")")]),
                Mn("46")
            ),
            Mo("·"),
            MSup(Mi("u"), Mo("′")), Mo("("), Mi("t"), Mo(")"),
        ])]),

        blank(),

        # u'(t)
        MTr([MTd([
            MText("where  "),
            MSup(Mi("u"), Mo("′")), Mo("("), Mi("t"), Mo(")"), Mo("="),
            Mn("6"), MSup(Mi("t"), Mn("2")),
            Mo("−"), Mn("30"), Mi("t"),
        ])]),

        blank(),

        # Evaluate at t=2
        text_row("At t = 2:"),
        MTr([MTd([
            Mi("u"), Mo("("), Mn("2"), Mo(")"), Mo("="),
            Mn("2"), Mo("("), Mn("8"), Mo(")"),
            Mo("−"), Mn("15"), Mo("("), Mn("4"), Mo(")"),
            Mo("+"), Mn("45"),
            Mo("="), Mn("16"), Mo("−"), Mn("60"), Mo("+"), Mn("45"),
            Mo("="), Mn("1"),
        ])]),

        MTr([MTd([
            MSup(Mi("u"), Mo("′")), Mo("("), Mn("2"), Mo(")"), Mo("="),
            Mn("6"), Mo("("), Mn("4"), Mo(")"),
            Mo("−"), Mn("30"), Mo("("), Mn("2"), Mo(")"),
            Mo("="), Mn("24"), Mo("−"), Mn("60"),
            Mo("="), Mo("−"), Mn("36"),
        ])]),

        blank(),

        # f'(2) substitution
        text_row("Substituting into f′(2):"),
        MTr([MTd([
            MSup(Mi("f"), Mo("′")), Mo("("), Mn("2"), Mo(")"), Mo("="),
            frac([Mn("1")], [Mi("a")]),
            Mo("·"), Mn("47"), Mo("·"),
            MSup(MRow([Mn("1")]), Mn("46")),
            Mo("·"), Mo("("), Mo("−"), Mn("36"), Mo(")"),
            Mo("="),
            frac([Mo("−"), Mn("1692")], [Mi("a")]),
        ])]),

        blank(),

        # Set equal to -188
        text_row("Set equal to −188 and solve:"),
        MTr([MTd([
            frac([Mo("−"), Mn("1692")], [Mi("a")]),
            Mo("="), Mo("−"), Mn("188"),
            Mo("⟹"),
            Mi("a"), Mo("="),
            frac([Mn("1692")], [Mn("188")]),
            Mo("="), Mn("9"),
        ])]),

    ])])


if __name__ == "__main__":
    tree = build()
    if "--compact" in sys.argv:
        from src.render import render_compact
        print(render_compact(tree))
    else:
        print(render(tree))
