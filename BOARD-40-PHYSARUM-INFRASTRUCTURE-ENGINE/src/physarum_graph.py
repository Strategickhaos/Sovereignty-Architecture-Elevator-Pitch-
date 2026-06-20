"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — physarum_graph.py
Models the SAGCO board network as a Physarum polycephalum slime mold graph.

Nodes = boards/citizens  (nutrient = how "fed" / active they are)
Edges = dependencies/bonds (conductance = connection strength)
Growth = reinforce high-flow paths
Pruning = starve weak / low-conductance paths
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import math


PRUNE_THRESHOLD = 0.01
DECAY_RATE      = 0.05
GROWTH_RATE     = 0.10


@dataclass
class PhysarumNode:
    node_id:  str
    name:     str
    district: str
    nutrient: float   # 0-1: how "fed" this node is
    flow:     float = 0.0   # current signal flow through it
    alive:    bool  = True  # False if pruned/hazarded beyond repair
    pressure: float = 0.0   # Poiseuille pressure at this node


@dataclass
class PhysarumEdge:
    source:      str
    target:      str
    conductance: float  # how strong the connection is
    flow:        float = 0.0
    edge_type:   str   = "dependency"  # dependency | bond | prerequisite
    alive:       bool  = True


class PhysarumGraph:
    def __init__(self, nodes: List[PhysarumNode], edges: List[PhysarumEdge]):
        self.nodes: Dict[str, PhysarumNode] = {n.node_id: n for n in nodes}
        self.edges: List[PhysarumEdge] = edges
        self._step_count = 0
        self._history: List[dict] = []

    # ── Adjacency helpers ───────────────────────────────────────────────────

    def neighbors(self, node_id: str) -> List[str]:
        result = []
        for e in self.edges:
            if not e.alive:
                continue
            if e.source == node_id:
                result.append(e.target)
            elif e.target == node_id:
                result.append(e.source)
        return result

    def get_edge(self, a: str, b: str) -> Optional[PhysarumEdge]:
        for e in self.edges:
            if (e.source == a and e.target == b) or (e.source == b and e.target == a):
                return e
        return None

    def alive_nodes(self) -> List[PhysarumNode]:
        return [n for n in self.nodes.values() if n.alive]

    def alive_edges(self) -> List[PhysarumEdge]:
        return [e for e in self.edges if e.alive]

    # ── Core simulation step ─────────────────────────────────────────────────

    def step(self, food_sources: List[str], hazards: List[str]):
        """
        Simulate one Physarum time step:
        1. Assign pressures (food sources = high, sinks = low)
        2. Compute flow on each edge
        3. Reinforce high-flow edges
        4. Decay all edges
        5. Prune edges below threshold
        6. Heal hazarded nodes if possible
        """
        self._step_count += 1

        # Step 1 — assign pressures
        for nid, node in self.nodes.items():
            if not node.alive:
                node.pressure = 0.0
            elif nid in food_sources:
                node.pressure = node.nutrient  # source pressure = nutrient
            else:
                node.pressure = node.nutrient * 0.3  # sinks have lower pressure

        # Step 2 — compute flow Q = conductance * (P_i - P_j)
        for edge in self.edges:
            if not edge.alive:
                edge.flow = 0.0
                continue
            src = self.nodes.get(edge.source)
            tgt = self.nodes.get(edge.target)
            if src and tgt:
                edge.flow = edge.conductance * abs(src.pressure - tgt.pressure)
            else:
                edge.flow = 0.0

        # Step 3 — reinforce: conductance += flow * growth_rate
        for edge in self.edges:
            if edge.alive:
                edge.conductance += edge.flow * GROWTH_RATE

        # Step 4 — decay: conductance -= decay_rate
        for edge in self.edges:
            if edge.alive:
                edge.conductance = max(0.0, edge.conductance - DECAY_RATE)

        # Step 5 — prune weak edges
        for edge in self.edges:
            if edge.alive and edge.conductance < PRUNE_THRESHOLD:
                edge.alive = False

        # Step 6 — update node flow (sum of incoming edge flows)
        for node in self.nodes.values():
            if node.alive:
                incoming = [e.flow for e in self.edges if e.alive and e.target == node.node_id]
                node.flow = sum(incoming)

        # Step 7 — hazard handling
        for haz in hazards:
            if haz in self.nodes:
                node = self.nodes[haz]
                node.nutrient = max(0.0, node.nutrient - 0.05)
                if node.nutrient < 0.1:
                    node.alive = False

        # Record snapshot
        self._history.append({
            "step": self._step_count,
            "alive_nodes": sum(1 for n in self.nodes.values() if n.alive),
            "alive_edges": sum(1 for e in self.edges if e.alive),
            "total_flow":  round(sum(e.flow for e in self.edges if e.alive), 4),
        })

    def optimize(self, steps: int = 20, food_sources: List[str] = None,
                 hazards: List[str] = None) -> dict:
        """Run N steps and return final state summary."""
        if food_sources is None:
            # Use high-nutrient nodes as food sources
            food_sources = [
                nid for nid, n in self.nodes.items() if n.nutrient >= 0.85
            ]
        if hazards is None:
            hazards = []

        for _ in range(steps):
            self.step(food_sources, hazards)

        return self.report()

    def report(self) -> dict:
        """Return strongest paths, pruned edges, isolated nodes."""
        alive_nodes = [n.node_id for n in self.nodes.values() if n.alive]
        dead_nodes  = [n.node_id for n in self.nodes.values() if not n.alive]
        alive_edges = [e for e in self.edges if e.alive]
        dead_edges  = [e for e in self.edges if not e.alive]

        # Strongest edges by conductance
        strongest = sorted(alive_edges, key=lambda e: e.conductance, reverse=True)[:10]

        # Isolated: alive nodes with no alive edges
        connected_ids = set()
        for e in alive_edges:
            connected_ids.add(e.source)
            connected_ids.add(e.target)
        isolated = [nid for nid in alive_nodes if nid not in connected_ids]

        return {
            "steps_run":    self._step_count,
            "alive_nodes":  len(alive_nodes),
            "dead_nodes":   len(dead_nodes),
            "alive_edges":  len(alive_edges),
            "pruned_edges": len(dead_edges),
            "isolated_nodes": isolated,
            "strongest_paths": [
                {
                    "source":      e.source,
                    "target":      e.target,
                    "conductance": round(e.conductance, 4),
                    "flow":        round(e.flow, 4),
                    "type":        e.edge_type,
                }
                for e in strongest
            ],
            "history": self._history[-5:],  # last 5 steps
        }
