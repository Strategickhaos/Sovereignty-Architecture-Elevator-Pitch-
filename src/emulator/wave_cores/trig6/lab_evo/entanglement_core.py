"""
Entanglement Core: Encoding Correlations
Phase 4.13: Arrow DNA Exploration - Encoding Correlations
"""

from typing import Dict, List, Tuple
import math
import logging

logger = logging.getLogger(__name__)


class EncodingCorrelator:
    """
    Entanglement Core for DNA encoding correlations.
    Computes quantum-inspired correlations between codon encodings.
    """
    
    def __init__(self, dna_config: Dict):
        """
        Initialize Encoding Correlator.
        
        Args:
            dna_config: DNA encoding configuration
        """
        self.codon_map = dna_config.get('codon_map', {})
        self.mutations = dna_config.get('mutations', [])
        
    def correlate_encodings(self, 
                           sequence: str,
                           mutations: List[Dict]) -> Dict:
        """
        Correlate encodings across DNA sequence and mutations.
        
        Args:
            sequence: DNA sequence
            mutations: Mutation list from control unit
            
        Returns:
            Correlation matrix and entanglement scores
        """
        codons = sequence.split('-')
        
        # Build correlation matrix
        n = len(codons)
        correlation_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    correlation_matrix[i][j] = 1.0
                else:
                    # Correlation based on codon similarity and position
                    correlation_matrix[i][j] = self._compute_correlation(
                        codons[i], codons[j], i, j
                    )
        
        # Compute entanglement score
        entanglement_score = self._compute_entanglement(correlation_matrix)
        
        # Identify correlated pairs
        correlated_pairs = []
        for i in range(n):
            for j in range(i+1, n):
                if correlation_matrix[i][j] > 0.5:
                    correlated_pairs.append({
                        'codon1': codons[i],
                        'codon2': codons[j],
                        'position1': i,
                        'position2': j,
                        'correlation': correlation_matrix[i][j]
                    })
        
        return {
            'correlation_matrix': correlation_matrix,
            'entanglement_score': entanglement_score,
            'correlated_pairs': correlated_pairs,
            'mutation_correlations': self._correlate_mutations(mutations)
        }
    
    def _compute_correlation(self, 
                            codon1: str,
                            codon2: str,
                            pos1: int,
                            pos2: int) -> float:
        """
        Compute correlation between two codons.
        
        Args:
            codon1, codon2: Codon strings
            pos1, pos2: Positions in sequence
            
        Returns:
            Correlation score [0, 1]
        """
        # Base correlation on nucleotide similarity
        matching_bases = sum(
            1 for a, b in zip(codon1, codon2) if a == b
        )
        base_correlation = matching_bases / 3.0
        
        # Position-based decay
        position_distance = abs(pos2 - pos1)
        position_factor = math.exp(-position_distance / 3.0)
        
        # Combined correlation
        correlation = base_correlation * position_factor
        
        return correlation
    
    def _compute_entanglement(self, matrix: List[List[float]]) -> float:
        """
        Compute overall entanglement score from correlation matrix.
        
        Args:
            matrix: Correlation matrix
            
        Returns:
            Entanglement score [0, 1]
        """
        n = len(matrix)
        if n == 0:
            return 0.0
        
        # Sum off-diagonal correlations
        total_correlation = 0.0
        count = 0
        
        for i in range(n):
            for j in range(i+1, n):
                total_correlation += matrix[i][j]
                count += 1
        
        if count == 0:
            return 0.0
        
        # Normalize to [0, 1]
        avg_correlation = total_correlation / count
        
        return avg_correlation
    
    def _correlate_mutations(self, mutations: List[Dict]) -> List[Dict]:
        """
        Find correlations between mutations.
        
        Args:
            mutations: List of mutations
            
        Returns:
            Correlated mutation pairs
        """
        correlated = []
        
        for i, mut1 in enumerate(mutations):
            for mut2 in mutations[i+1:]:
                # Check if mutations are related
                pos_distance = abs(
                    mut1.get('position', 0) - mut2.get('position', 0)
                )
                
                if pos_distance <= 1:
                    correlated.append({
                        'mutation1': mut1,
                        'mutation2': mut2,
                        'correlation_type': 'adjacent',
                        'strength': 0.8
                    })
        
        return correlated
