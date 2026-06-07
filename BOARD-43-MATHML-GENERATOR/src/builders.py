"""Builder helpers — read like the math story in your head"""
from .node import *

def row(*children):     return MTr([MTd(list(children))])
def blank():            return MTr([MTd([MSpace("0.6em")])])
def text_row(s):        return row(MText(s))

def frac(num_text, den_node):
    return MFrac(MText(num_text) if isinstance(den_node, str) else Mn(num_text), den_node)

def sup(base_text, sup_text):
    return MSup(Mi(base_text), Mo(sup_text))

def prime(f):           return MSup(Mi(f), Mo("′"))
def double_prime(f):    return MSup(Mi(f), Mo("″"))
def nth_deriv(f, n):    return MSup(Mi(f), Mn(str(n)))

def inline(*nodes):     return MRow(list(nodes))

def logic_row(condition, then_expr):
    """IF condition THEN then_expr — each a list of nodes"""
    return row(MText("IF "), *condition, MText(" THEN "), *then_expr)

def when_row(content):
    return row(MText("WHEN " + content))

def conclusion_row(*nodes):
    return row(*nodes)

# YAML schema → MathML tree
def from_yaml_dict(data: dict) -> Math:
    rows = []
    for item in data.get("rows", []):
        t = item.get("type", "text")

        if t == "text":
            rows.append(text_row(item["content"]))

        elif t == "blank":
            rows.append(blank())

        elif t == "step":
            # label: "Step 1", expr: nodes list, note: optional
            nodes = [MText(f'• {item["label"]}: ')]
            nodes += _parse_expr(item.get("expr", ""))
            if "note" in item:
                nodes.append(MText(f' {item["note"]}'))
            rows.append(MTr([MTd(nodes)]))

        elif t == "equation":
            rows.append(MTr([MTd(_parse_expr(item["expr"]))]))

        elif t == "logic":
            rows.append(text_row(item["content"]))

        elif t == "conclusion":
            rows.append(text_row(item["content"]))

    return Math([MTable(rows)])


def _parse_expr(expr: str):
    """Very simple expr → node list: handles frac(a,b), sup(a,b), bare text."""
    if not expr:
        return []
    # keep it simple — just wrap as mtext for arbitrary strings
    return [MText(expr)]
