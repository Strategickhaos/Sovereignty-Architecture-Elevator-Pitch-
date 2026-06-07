"""MathML AST nodes — Python port of mathml-cords/src/mathml/node.rs"""
from dataclasses import dataclass, field
from typing import List, Union

MathNode = Union[
    "Math", "MTable", "MTr", "MTd",
    "MRow", "MText", "Mi", "Mo", "Mn",
    "MFrac", "MSup", "MSub", "MSpace",
]

@dataclass
class Math:      children: List = field(default_factory=list)
@dataclass
class MTable:    children: List = field(default_factory=list); align: str = "left"; rowspacing: str = "0.8em"
@dataclass
class MTr:       children: List = field(default_factory=list)
@dataclass
class MTd:       children: List = field(default_factory=list)
@dataclass
class MRow:      children: List = field(default_factory=list)
@dataclass
class MText:     text: str = ""
@dataclass
class Mi:        text: str = ""
@dataclass
class Mo:        text: str = ""
@dataclass
class Mn:        text: str = ""
@dataclass
class MFrac:     num: object = None; den: object = None
@dataclass
class MSup:      base: object = None; sup: object = None
@dataclass
class MSub:      base: object = None; sub: object = None
@dataclass
class MSpace:    height: str = "0.5em"
@dataclass
class MUnder:    base: object = None; under: object = None
