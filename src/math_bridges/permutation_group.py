"""
Bridge 4: Rubik's Cube ↔ Group Theory (Permutation Representation)

This bridge connects cube algorithms to group theory, giving direction to permutations.

Formula:
    G = ⟨R, L, U, D, F, B⟩
    Each move = permutation matrix
    phase(g) = arg(λ_max(P_g))

This is how algorithms gain "direction" and connects to:
- 57 OLL cases
- 36 fallacies
- permutations vs angles
"""

import numpy as np
from typing import List, Tuple, Optional


class PermutationGroup:
    """Bridges Rubik's cube algorithms and group theory."""
    
    # Standard permutation for basic moves on a 3x3 cube
    # Each move permutes the 48 edge/corner pieces (excluding center stickers)
    
    @staticmethod
    def create_permutation_matrix(permutation: List[int]) -> np.ndarray:
        """
        Create a permutation matrix from a permutation list.
        
        Args:
            permutation: List where permutation[i] indicates where element i goes
            
        Returns:
            Permutation matrix P where P[i,j] = 1 if j goes to i
        """
        n = len(permutation)
        P = np.zeros((n, n))
        
        for i, j in enumerate(permutation):
            P[j, i] = 1
        
        return P
    
    @staticmethod
    def compose_permutations(perm1: List[int], perm2: List[int]) -> List[int]:
        """
        Compose two permutations (apply perm2 after perm1).
        
        Args:
            perm1: First permutation
            perm2: Second permutation
            
        Returns:
            Composed permutation
        """
        if len(perm1) != len(perm2):
            raise ValueError("Permutations must have same length")
        
        return [perm2[perm1[i]] for i in range(len(perm1))]
    
    @staticmethod
    def permutation_phase(permutation_matrix: np.ndarray) -> complex:
        """
        Extract phase from permutation matrix using dominant eigenvalue.
        
        Formula: phase(g) = arg(λ_max(P_g))
        
        Args:
            permutation_matrix: Permutation matrix P
            
        Returns:
            Complex phase angle
        """
        eigenvalues = np.linalg.eigvals(permutation_matrix)
        
        # Find dominant eigenvalue (largest magnitude)
        idx = np.argmax(np.abs(eigenvalues))
        lambda_max = eigenvalues[idx]
        
        return lambda_max
    
    @staticmethod
    def permutation_angle(permutation_matrix: np.ndarray) -> float:
        """
        Get angular direction of permutation.
        
        Args:
            permutation_matrix: Permutation matrix P
            
        Returns:
            Angle in radians
        """
        phase = PermutationGroup.permutation_phase(permutation_matrix)
        return np.angle(phase)
    
    @staticmethod
    def algorithm_to_direction(moves: List[str]) -> float:
        """
        Convert a cube algorithm (sequence of moves) to a directional angle.
        
        Args:
            moves: List of move strings like ["R", "U", "R'", "U'"]
            
        Returns:
            Net angular direction in radians
        """
        # Simplified: each move type gets a base angle
        move_angles = {
            'R': 0,
            'L': np.pi,
            'U': np.pi/2,
            'D': -np.pi/2,
            'F': np.pi/4,
            'B': -3*np.pi/4,
        }
        
        total_angle = 0
        for move in moves:
            # Remove prime (') and double (2) notations
            base_move = move.rstrip("'2")
            angle = move_angles.get(base_move, 0)
            
            # Adjust for prime (counterclockwise)
            if "'" in move:
                angle = -angle
            # Adjust for double turn
            if "2" in move:
                angle = 2 * angle
                
            total_angle += angle
        
        # Normalize to [-π, π]
        total_angle = np.arctan2(np.sin(total_angle), np.cos(total_angle))
        
        return total_angle
    
    @staticmethod
    def oll_case_to_geometry(oll_index: int) -> Tuple[float, float]:
        """
        Map OLL case (1-57) to 2D geometric coordinates.
        
        Args:
            oll_index: OLL case number (1-57)
            
        Returns:
            (x, y): 2D coordinates on unit circle
        """
        if oll_index < 1 or oll_index > 57:
            raise ValueError(f"OLL index {oll_index} must be in range [1, 57]")
        
        # Map to angle on circle
        angle = 2 * np.pi * (oll_index - 1) / 57
        
        x = np.cos(angle)
        y = np.sin(angle)
        
        return (x, y)
    
    @staticmethod
    def permutation_order(permutation: List[int]) -> int:
        """
        Calculate the order of a permutation (how many applications return to identity).
        
        Args:
            permutation: Permutation list
            
        Returns:
            Order of the permutation
        """
        n = len(permutation)
        visited = [False] * n
        cycle_lengths = []
        
        for i in range(n):
            if not visited[i]:
                cycle_length = 0
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = permutation[j]
                    cycle_length += 1
                cycle_lengths.append(cycle_length)
        
        # Order is LCM of all cycle lengths
        order = 1
        for length in cycle_lengths:
            order = np.lcm(order, length)
        
        return order
