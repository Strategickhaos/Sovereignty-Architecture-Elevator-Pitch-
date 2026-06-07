"""
Board/citizen graph using pure adjacency dict.
Nodes represent citizens or menu items; edges represent connections.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Node:
    node_id: str
    label: str
    data: dict = field(default_factory=dict)
    conductivity: float = 1.0


@dataclass
class Edge:
    src: str
    dst: str
    weight: float = 1.0
    flow: float = 0.0


class Graph:
    """Directed weighted graph with adjacency dict."""

    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self._adj: Dict[str, List[Edge]] = {}  # src -> edges

    def add_node(self, node_id: str, label: str = "", data: dict = None) -> Node:
        node = Node(node_id, label or node_id, data or {})
        self.nodes[node_id] = node
        return node

    def add_edge(self, src: str, dst: str, weight: float = 1.0) -> Edge:
        if src not in self.nodes:
            self.add_node(src)
        if dst not in self.nodes:
            self.add_node(dst)
        edge = Edge(src, dst, weight)
        self.edges.append(edge)
        self._adj.setdefault(src, []).append(edge)
        return edge

    def neighbors(self, node_id: str) -> List[str]:
        return [e.dst for e in self._adj.get(node_id, [])]

    def get_edge(self, src: str, dst: str) -> Optional[Edge]:
        for e in self._adj.get(src, []):
            if e.dst == dst:
                return e
        return None

    def total_flow(self) -> float:
        return sum(e.flow for e in self.edges)

    def to_dict(self) -> dict:
        return {
            "nodes": [{"id": n.node_id, "label": n.label, "conductivity": n.conductivity}
                      for n in self.nodes.values()],
            "edges": [{"src": e.src, "dst": e.dst, "weight": e.weight, "flow": e.flow}
                      for e in self.edges],
        }

    def from_rows(self, rows: list, id_field: str = "ID", label_field: str = "Item",
                  connect_by: str = "Category") -> "Graph":
        """Build graph from data rows. Nodes = items, edges = shared category."""
        for row in rows:
            nid = str(row.get(id_field, ""))
            label = str(row.get(label_field, nid))
            self.add_node(nid, label, dict(row))

        # Connect items in same category
        by_cat: dict = {}
        for row in rows:
            cat = str(row.get(connect_by, ""))
            nid = str(row.get(id_field, ""))
            by_cat.setdefault(cat, []).append(nid)

        for cat, nids in by_cat.items():
            for i in range(len(nids)):
                for j in range(i + 1, min(i + 3, len(nids))):  # connect to next 2
                    self.add_edge(nids[i], nids[j])
                    self.add_edge(nids[j], nids[i])

        return self
