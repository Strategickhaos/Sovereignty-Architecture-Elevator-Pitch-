"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — nutrient_flow.py
Poiseuille-like flow equations for Physarum tube networks.

Q_ij = conductance_ij * (pressure_i - pressure_j)
Update: conductance += |flow| * growth_rate - decay_rate
"""

from typing import Dict, List


def compute_flow(graph, food_sources: List[str]) -> Dict[str, float]:
    """
    Compute flow on each edge given food source pressures.
    Returns {edge_key: flow_value} where edge_key = "source→target".
    """
    # Assign pressures
    pressures = {}
    for nid, node in graph.nodes.items():
        if not node.alive:
            pressures[nid] = 0.0
        elif nid in food_sources:
            pressures[nid] = node.nutrient
        else:
            pressures[nid] = node.nutrient * 0.3

    flow_map = {}
    for edge in graph.edges:
        if not edge.alive:
            continue
        p_src = pressures.get(edge.source, 0.0)
        p_tgt = pressures.get(edge.target, 0.0)
        q = edge.conductance * (p_src - p_tgt)
        key = f"{edge.source}→{edge.target}"
        flow_map[key] = round(q, 6)
        # update edge flow immediately
        edge.flow = abs(q)

    return flow_map
