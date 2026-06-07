"""Render MathML AST → XML string"""
import html
from .node import *

def render(node, indent=0) -> str:
    pad = "  " * indent
    match node:
        case Math(children=ch):
            inner = "".join(render(c, indent+1) for c in ch)
            return f'{pad}<math xmlns="http://www.w3.org/1998/Math/MathML">\n{inner}{pad}</math>\n'
        case MTable(children=ch, align=a, rowspacing=rs):
            inner = "".join(render(c, indent+1) for c in ch)
            return f'{pad}<mtable columnalign="{a}" rowspacing="{rs}">\n{inner}{pad}</mtable>\n'
        case MTr(children=ch):
            inner = "".join(render(c, indent+1) for c in ch)
            return f'{pad}<mtr>\n{inner}{pad}</mtr>\n'
        case MTd(children=ch):
            inner = "".join(render(c, indent+1) for c in ch)
            return f'{pad}<mtd>\n{inner}{pad}</mtd>\n'
        case MRow(children=ch):
            inner = "".join(render(c, indent+1) for c in ch)
            return f'{pad}<mrow>{inner}</mrow>\n'
        case MText(text=t):
            return f'{pad}<mtext>{html.escape(t)}</mtext>\n'
        case Mi(text=t):
            return f'{pad}<mi>{html.escape(t)}</mi>\n'
        case Mo(text=t):
            return f'{pad}<mo>{html.escape(t)}</mo>\n'
        case Mn(text=t):
            return f'{pad}<mn>{html.escape(t)}</mn>\n'
        case MFrac(num=n, den=d):
            return f'{pad}<mfrac>\n{render(n, indent+1)}{render(d, indent+1)}{pad}</mfrac>\n'
        case MSup(base=b, sup=s):
            return f'{pad}<msup>\n{render(b, indent+1)}{render(s, indent+1)}{pad}</msup>\n'
        case MSub(base=b, sub=s):
            return f'{pad}<msub>\n{render(b, indent+1)}{render(s, indent+1)}{pad}</msub>\n'
        case MSpace(height=h):
            return f'{pad}<mspace height="{h}"/>\n'
        case _:
            return f'{pad}<!-- unknown node: {type(node).__name__} -->\n'


def render_compact(node) -> str:
    match node:
        case Math(children=ch):
            inner = "".join(render_compact(c) for c in ch)
            return f'<math xmlns="http://www.w3.org/1998/Math/MathML">{inner}</math>'
        case MTable(children=ch, align=a, rowspacing=rs):
            inner = "".join(render_compact(c) for c in ch)
            return f'<mtable columnalign="{a}" rowspacing="{rs}">{inner}</mtable>'
        case MTr(children=ch):
            return f'<mtr>{"".join(render_compact(c) for c in ch)}</mtr>'
        case MTd(children=ch):
            return f'<mtd>{"".join(render_compact(c) for c in ch)}</mtd>'
        case MRow(children=ch):
            return f'<mrow>{"".join(render_compact(c) for c in ch)}</mrow>'
        case MText(text=t):   return f'<mtext>{html.escape(t)}</mtext>'
        case Mi(text=t):      return f'<mi>{html.escape(t)}</mi>'
        case Mo(text=t):      return f'<mo>{html.escape(t)}</mo>'
        case Mn(text=t):      return f'<mn>{html.escape(t)}</mn>'
        case MFrac(num=n, den=d):
            return f'<mfrac>{render_compact(n)}{render_compact(d)}</mfrac>'
        case MSup(base=b, sup=s):
            return f'<msup>{render_compact(b)}{render_compact(s)}</msup>'
        case MSub(base=b, sub=s):
            return f'<msub>{render_compact(b)}{render_compact(s)}</msub>'
        case MSpace(height=h):
            return f'<mspace height="{h}"/>'
        case _: return ""
