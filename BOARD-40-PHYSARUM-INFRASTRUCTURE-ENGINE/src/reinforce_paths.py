"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — reinforce_paths.py
Reinforce high-flow edges: conductance += |flow| * growth_rate
"""

from typing import Dict


def reinforce(graph, flow_map: Dict[str, float], growth_rate: float = 0.1):
    """
    For each alive edge, increase conductance proportional to its flow.
    Returns the same graph (mutated in place).
    """
    for edge in graph.edges:
        if not edge.alive:
            continue
        key = f"{edge.source}→{edge.target}"
        flow = abs(flow_map.get(key, edge.flow))
        if flow > 0:
            edge.conductance += flow * growth_rate
    return graph
