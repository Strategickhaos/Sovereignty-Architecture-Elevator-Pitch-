"""
Bridge 5: 36 Fallacies ↔ Geometry (Graph Laplacian Embedding)

This bridge makes fallacy relationships measurable through graph theory.

Formula:
    L = D - A
    where A = adjacency matrix, D = degree matrix
    
    X = eig(L)

Now:
- 36 fallacies → 2D or 3D geometry
- Chess board mapping becomes measurable
"""

import numpy as np
from typing import List, Tuple, Optional


class GraphLaplacian:
    """Bridges abstract concept spaces to geometric embeddings."""
    
    @staticmethod
    def compute_laplacian(adjacency_matrix: np.ndarray) -> np.ndarray:
        """
        Compute the graph Laplacian from an adjacency matrix.
        
        Formula: L = D - A
        
        Args:
            adjacency_matrix: Square adjacency matrix A
            
        Returns:
            Laplacian matrix L
        """
        # Compute degree matrix D
        degrees = np.sum(adjacency_matrix, axis=1)
        D = np.diag(degrees)
        
        # Compute Laplacian
        L = D - adjacency_matrix
        
        return L
    
    @staticmethod
    def compute_normalized_laplacian(adjacency_matrix: np.ndarray) -> np.ndarray:
        """
        Compute the normalized graph Laplacian.
        
        Formula: L_norm = D^(-1/2) * L * D^(-1/2) = I - D^(-1/2) * A * D^(-1/2)
        
        Args:
            adjacency_matrix: Square adjacency matrix A
            
        Returns:
            Normalized Laplacian matrix
        """
        # Compute degree matrix D
        degrees = np.sum(adjacency_matrix, axis=1)
        
        # Avoid division by zero
        degrees_inv_sqrt = np.zeros_like(degrees)
        non_zero = degrees > 0
        degrees_inv_sqrt[non_zero] = 1.0 / np.sqrt(degrees[non_zero])
        
        D_inv_sqrt = np.diag(degrees_inv_sqrt)
        
        # Compute normalized Laplacian
        L_norm = np.eye(len(adjacency_matrix)) - D_inv_sqrt @ adjacency_matrix @ D_inv_sqrt
        
        return L_norm
    
    @staticmethod
    def spectral_embedding(laplacian: np.ndarray, dimensions: int = 2) -> np.ndarray:
        """
        Compute spectral embedding of graph nodes.
        
        Args:
            laplacian: Graph Laplacian matrix
            dimensions: Number of embedding dimensions (default 2)
            
        Returns:
            Embedding matrix X of shape (n_nodes, dimensions)
        """
        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
        
        # Sort by eigenvalue (smallest first, skip the first zero eigenvalue)
        idx = np.argsort(eigenvalues)[1:dimensions+1]
        
        # Return eigenvectors corresponding to smallest non-zero eigenvalues
        embedding = eigenvectors[:, idx]
        
        return embedding
    
    @staticmethod
    def fallacy_space_embedding(fallacy_transitions: np.ndarray, dimensions: int = 2) -> np.ndarray:
        """
        Embed 36 fallacies into geometric space.
        
        Args:
            fallacy_transitions: 36x36 adjacency matrix of fallacy transitions
            dimensions: Embedding dimensions (2 for chess board, 3 for space)
            
        Returns:
            36 x dimensions matrix of fallacy positions
        """
        if fallacy_transitions.shape != (36, 36):
            raise ValueError("Expected 36x36 adjacency matrix for 36 fallacies")
        
        L = GraphLaplacian.compute_normalized_laplacian(fallacy_transitions)
        embedding = GraphLaplacian.spectral_embedding(L, dimensions)
        
        return embedding
    
    @staticmethod
    def create_chess_board_adjacency() -> np.ndarray:
        """
        Create adjacency matrix for 6x6 chess board (36 squares).
        
        Returns:
            36x36 adjacency matrix
        """
        board_size = 6
        n_squares = board_size * board_size
        A = np.zeros((n_squares, n_squares))
        
        for i in range(n_squares):
            row, col = divmod(i, board_size)
            
            # Add edges to adjacent squares (4-connected)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < board_size and 0 <= new_col < board_size:
                    j = new_row * board_size + new_col
                    A[i, j] = 1
        
        return A
    
    @staticmethod
    def fallacy_to_chess_position(fallacy_index: int) -> Tuple[int, int]:
        """
        Map fallacy index (0-35) to chess board position.
        
        Args:
            fallacy_index: Index of fallacy (0-35)
            
        Returns:
            (row, col): Position on 6x6 chess board
        """
        if fallacy_index < 0 or fallacy_index >= 36:
            raise ValueError(f"Fallacy index {fallacy_index} must be in range [0, 35]")
        
        row = fallacy_index // 6
        col = fallacy_index % 6
        
        return (row, col)
    
    @staticmethod
    def compute_fallacy_distance(fallacy1: int, fallacy2: int, 
                                  embedding: Optional[np.ndarray] = None) -> float:
        """
        Compute distance between two fallacies in embedding space.
        
        Args:
            fallacy1: First fallacy index
            fallacy2: Second fallacy index
            embedding: Optional pre-computed embedding (if None, uses chess board)
            
        Returns:
            Euclidean distance
        """
        if embedding is None:
            # Use chess board layout
            pos1 = GraphLaplacian.fallacy_to_chess_position(fallacy1)
            pos2 = GraphLaplacian.fallacy_to_chess_position(fallacy2)
            distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        else:
            # Use spectral embedding
            distance = np.linalg.norm(embedding[fallacy1] - embedding[fallacy2])
        
        return distance
