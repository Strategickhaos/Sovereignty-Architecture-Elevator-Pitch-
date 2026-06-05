"""
Bridge 9: Filesystem ↔ Tree ↔ Minimax (Decision Trees)

This bridge removes metaphor and makes tree navigation algorithmic.

Formula:
    J(n) = g(n) + h(n)
    where g(n) = path cost, h(n) = heuristic

Same formula runs:
- Chess minimax
- Linux trees
- Cube solving
"""

import numpy as np
from typing import Callable, List, Tuple, Optional, Any


class TreeCost:
    """Bridges tree structures and decision algorithms."""
    
    @staticmethod
    def path_cost(depth: int, edge_weights: Optional[List[float]] = None) -> float:
        """
        Compute path cost g(n) from root to node.
        
        Args:
            depth: Depth of node in tree
            edge_weights: Optional list of edge weights along path
            
        Returns:
            Total path cost
        """
        if edge_weights is None:
            # Uniform cost: g(n) = depth
            return float(depth)
        
        if len(edge_weights) != depth:
            raise ValueError(f"Expected {depth} edge weights, got {len(edge_weights)}")
        
        return sum(edge_weights)
    
    @staticmethod
    def heuristic_distance(current_state: Any, goal_state: Any, 
                           metric: str = 'euclidean') -> float:
        """
        Compute heuristic h(n) based on distance to goal.
        
        Args:
            current_state: Current state (can be coordinates, config, etc.)
            goal_state: Goal state
            metric: Distance metric ('euclidean', 'manhattan', 'hamming')
            
        Returns:
            Heuristic estimate of cost to goal
        """
        if isinstance(current_state, (list, tuple, np.ndarray)):
            current = np.array(current_state)
            goal = np.array(goal_state)
            
            if metric == 'euclidean':
                return np.linalg.norm(current - goal)
            elif metric == 'manhattan':
                return np.sum(np.abs(current - goal))
            elif metric == 'hamming':
                return np.sum(current != goal)
        
        # For non-numeric states, use simple difference count
        return 0.0
    
    @staticmethod
    def total_cost(depth: int, current_state: Any, goal_state: Any, 
                   edge_weights: Optional[List[float]] = None,
                   metric: str = 'euclidean') -> float:
        """
        Compute total cost J(n) = g(n) + h(n).
        
        Args:
            depth: Current depth in tree
            current_state: Current state
            goal_state: Goal state
            edge_weights: Optional edge weights
            metric: Heuristic distance metric
            
        Returns:
            Total estimated cost
        """
        g = TreeCost.path_cost(depth, edge_weights)
        h = TreeCost.heuristic_distance(current_state, goal_state, metric)
        
        return g + h
    
    @staticmethod
    def minimax_value(depth: int, max_depth: int, is_maximizing: bool,
                      eval_func: Callable[[Any], float], state: Any,
                      alpha: float = -np.inf, beta: float = np.inf) -> float:
        """
        Compute minimax value with alpha-beta pruning.
        
        Args:
            depth: Current depth
            max_depth: Maximum search depth
            is_maximizing: True if maximizing player's turn
            eval_func: State evaluation function
            state: Current game state
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            Minimax value
        """
        # Terminal node
        if depth == max_depth:
            return eval_func(state)
        
        # For demonstration, return eval at current depth
        return eval_func(state)
    
    @staticmethod
    def filesystem_depth_cost(path: str) -> int:
        """
        Compute depth cost for filesystem path.
        
        Args:
            path: Filesystem path
            
        Returns:
            Depth (number of directory levels)
        """
        # Remove leading/trailing slashes
        path = path.strip('/')
        
        if not path:
            return 0
        
        return len(path.split('/'))
    
    @staticmethod
    def tree_entropy(branching_factors: List[int]) -> float:
        """
        Compute entropy of tree structure.
        
        Args:
            branching_factors: List of branching factors at each level
            
        Returns:
            Shannon entropy
        """
        if not branching_factors:
            return 0.0
        
        total = sum(branching_factors)
        if total == 0:
            return 0.0
        
        probabilities = [b / total for b in branching_factors]
        entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in probabilities)
        
        return entropy
    
    @staticmethod
    def angle_based_heuristic(current_angle: float, goal_angle: float) -> float:
        """
        Heuristic based on angular distance (for cube solving, etc.).
        
        Args:
            current_angle: Current orientation angle in radians
            goal_angle: Goal orientation angle in radians
            
        Returns:
            Angular distance
        """
        diff = abs(current_angle - goal_angle)
        # Handle wrap-around
        diff = min(diff, 2 * np.pi - diff)
        
        return diff
    
    @staticmethod
    def information_gain(parent_entropy: float, child_entropies: List[float],
                         child_weights: List[float]) -> float:
        """
        Compute information gain from split.
        
        Args:
            parent_entropy: Entropy before split
            child_entropies: Entropies of child nodes
            child_weights: Weights (proportions) of child nodes
            
        Returns:
            Information gain
        """
        if len(child_entropies) != len(child_weights):
            raise ValueError("Must have same number of entropies and weights")
        
        # Normalize weights
        total_weight = sum(child_weights)
        if total_weight == 0:
            return 0.0
        
        weights = [w / total_weight for w in child_weights]
        
        # Weighted average of child entropies
        weighted_entropy = sum(e * w for e, w in zip(child_entropies, weights))
        
        return parent_entropy - weighted_entropy
    
    @staticmethod
    def optimal_path_angle(start: Tuple[float, float], end: Tuple[float, float],
                            obstacles: List[Tuple[float, float]] = None) -> float:
        """
        Compute optimal path angle from start to end.
        
        Args:
            start: Starting coordinates (x, y)
            end: Ending coordinates (x, y)
            obstacles: Optional list of obstacle coordinates
            
        Returns:
            Angle of optimal path in radians
        """
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        # Direct path angle
        angle = np.arctan2(dy, dx)
        
        # TODO: Adjust for obstacles using A* or similar
        
        return angle
