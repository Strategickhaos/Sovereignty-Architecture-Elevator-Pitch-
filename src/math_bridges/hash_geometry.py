"""
Bridge 8: Hash Collisions ↔ Geometry (Security Link)

This bridge explains why hash collisions have structure through the birthday bound.

Formulas:
    P ≈ 1 - e^(-k²/2N)
    
Geometric interpretation:
- N = angular bins
- k = sampled states
- Collision = overlapping arc lengths
"""

import numpy as np
from typing import List, Tuple


class HashGeometry:
    """Bridges cryptographic hashing and geometric collision analysis."""
    
    @staticmethod
    def birthday_bound_probability(k: int, N: int) -> float:
        """
        Compute probability of collision using birthday bound.
        
        Formula: P ≈ 1 - e^(-k²/2N)
        
        Args:
            k: Number of sampled states
            N: Size of hash space
            
        Returns:
            Probability of at least one collision
        """
        if k <= 0 or N <= 0:
            raise ValueError("k and N must be positive")
        
        # Exact formula for small k relative to N
        if k > N:
            return 1.0
        
        # Use approximation for large values
        exponent = -(k ** 2) / (2 * N)
        probability = 1 - np.exp(exponent)
        
        return min(probability, 1.0)
    
    @staticmethod
    def birthday_bound_exact(k: int, N: int) -> float:
        """
        Compute exact probability of collision (for small k).
        
        Args:
            k: Number of sampled states
            N: Size of hash space
            
        Returns:
            Exact probability of at least one collision
        """
        if k <= 0 or N <= 0:
            raise ValueError("k and N must be positive")
        
        if k > N:
            return 1.0
        
        # Probability of no collision
        no_collision = 1.0
        for i in range(k):
            no_collision *= (N - i) / N
        
        return 1 - no_collision
    
    @staticmethod
    def samples_for_collision_probability(target_prob: float, N: int) -> int:
        """
        Compute number of samples needed for target collision probability.
        
        Args:
            target_prob: Desired collision probability (0-1)
            N: Size of hash space
            
        Returns:
            Number of samples needed
        """
        if target_prob <= 0 or target_prob >= 1:
            raise ValueError("Target probability must be in (0, 1)")
        
        # Solve: target_prob = 1 - e^(-k²/2N)
        # k ≈ sqrt(2N * ln(1/(1-target_prob)))
        
        k = np.sqrt(2 * N * np.log(1 / (1 - target_prob)))
        
        return int(np.ceil(k))
    
    @staticmethod
    def hash_to_angular_bin(hash_value: int, N: int) -> float:
        """
        Map hash value to angular bin on a circle.
        
        Args:
            hash_value: Hash value
            N: Number of angular bins
            
        Returns:
            Angle in radians
        """
        bin_index = hash_value % N
        angle = 2 * np.pi * bin_index / N
        
        return angle
    
    @staticmethod
    def collision_as_arc_overlap(hash1: int, hash2: int, N: int, 
                                  bin_width: float = None) -> bool:
        """
        Determine if two hashes collide based on arc overlap.
        
        Args:
            hash1: First hash value
            hash2: Second hash value
            N: Number of angular bins
            bin_width: Width of each bin in radians (default: 2π/N)
            
        Returns:
            True if arcs overlap (collision)
        """
        if bin_width is None:
            bin_width = 2 * np.pi / N
        
        angle1 = HashGeometry.hash_to_angular_bin(hash1, N)
        angle2 = HashGeometry.hash_to_angular_bin(hash2, N)
        
        # Angular distance
        diff = abs(angle1 - angle2)
        diff = min(diff, 2 * np.pi - diff)  # Handle wrap-around
        
        # Check if within bin width
        return diff < bin_width
    
    @staticmethod
    def hash_distribution_entropy(hashes: List[int], N: int) -> float:
        """
        Compute entropy of hash distribution over bins.
        
        Args:
            hashes: List of hash values
            N: Number of bins
            
        Returns:
            Shannon entropy in bits
        """
        if not hashes:
            return 0.0
        
        # Count hashes per bin
        bins = np.zeros(N)
        for h in hashes:
            bins[h % N] += 1
        
        # Normalize to probabilities
        probabilities = bins / len(hashes)
        
        # Compute entropy
        entropy = 0
        for p in probabilities:
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy
    
    @staticmethod
    def collision_clusters_2d(hashes: List[int], grid_size: int = 8) -> np.ndarray:
        """
        Map hash collisions to 2D grid for visualization.
        
        Args:
            hashes: List of hash values
            grid_size: Size of grid (grid_size x grid_size)
            
        Returns:
            2D array with collision counts
        """
        N = grid_size * grid_size
        grid = np.zeros((grid_size, grid_size))
        
        for h in hashes:
            bin_index = h % N
            row = bin_index // grid_size
            col = bin_index % grid_size
            grid[row, col] += 1
        
        return grid
    
    @staticmethod
    def avalanche_effect_angle(input1: str, input2: str, hash_func=hash) -> float:
        """
        Measure avalanche effect as angular distance.
        
        Args:
            input1: First input string
            input2: Second input string
            hash_func: Hash function to use
            
        Returns:
            Angular distance in radians
        """
        h1 = hash_func(input1)
        h2 = hash_func(input2)
        
        # Map to angles
        angle1 = (h1 % 360) * np.pi / 180
        angle2 = (h2 % 360) * np.pi / 180
        
        # Angular distance
        diff = abs(angle1 - angle2)
        diff = min(diff, 2 * np.pi - diff)
        
        return diff
