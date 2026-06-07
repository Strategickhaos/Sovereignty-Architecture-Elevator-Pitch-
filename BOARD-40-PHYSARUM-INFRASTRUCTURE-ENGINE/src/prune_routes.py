"""
BOARD-40-PHYSARUM-INFRASTRUCTURE-ENGINE — prune_routes.py
Prune low-conductance edges: mark alive=False when conductance < threshold.
"""


def prune(graph, threshold: float = 0.01):
    """
    Mark edges with conductance < threshold as dead (alive=False).
    Returns the same graph (mutated in place).
    """
    pruned_count = 0
    for edge in graph.edges:
        if edge.alive and edge.conductance < threshold:
            edge.alive = False
            pruned_count += 1
    return graph
