"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — self_heal.py
Repair damaged/hazarded nodes by restoring nutrient from neighbors.
"""

from typing import List


def heal(graph, hazards: List[str]):
    """
    For each hazarded node that is still alive, attempt self-repair:
    - Restore nutrient += 0.1 * avg(neighbor_nutrients)
    - Revive dead nodes if avg neighbor nutrient >= 0.5
    Returns the same graph (mutated in place).
    """
    for haz_id in hazards:
        node = graph.nodes.get(haz_id)
        if node is None:
            continue

        neighbors = graph.neighbors(haz_id)
        neighbor_nutrients = [
            graph.nodes[nid].nutrient
            for nid in neighbors
            if nid in graph.nodes and graph.nodes[nid].alive
        ]

        if not neighbor_nutrients:
            continue

        avg_nutrient = sum(neighbor_nutrients) / len(neighbor_nutrients)

        if not node.alive and avg_nutrient >= 0.5:
            # Revive the node
            node.alive = True
            node.nutrient = avg_nutrient * 0.5  # revived at half strength
        elif node.alive:
            # Boost nutrient
            node.nutrient = min(1.0, node.nutrient + 0.1 * avg_nutrient)

    return graph
