"""
Bridge 7: DNA Codons ↔ Base-64 (Legitimate Encoding)

This bridge formalizes the codon → 64-bit space mapping with explicit indexing.

Formula:
    index = 16*b₁ + 4*b₂ + b₃
    where b_i ∈ {0,1,2,3} for {A,C,G,T}

Now:
- 64 codons ↔ 6-bit space
- Matches your 64 grid formally
"""

import numpy as np
from typing import Tuple, List


class CodonEncoding:
    """Bridges genetic code and binary encoding."""
    
    # Base encoding
    BASE_TO_INDEX = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    INDEX_TO_BASE = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}
    
    @staticmethod
    def codon_to_index(codon: str) -> int:
        """
        Convert a 3-letter codon to an index (0-63).
        
        Formula: index = 16*b₁ + 4*b₂ + b₃
        
        Args:
            codon: 3-letter string like "ATG", "CCC", etc.
            
        Returns:
            Index from 0 to 63
        """
        if len(codon) != 3:
            raise ValueError(f"Codon must be 3 letters, got: {codon}")
        
        codon = codon.upper()
        
        try:
            b1 = CodonEncoding.BASE_TO_INDEX[codon[0]]
            b2 = CodonEncoding.BASE_TO_INDEX[codon[1]]
            b3 = CodonEncoding.BASE_TO_INDEX[codon[2]]
        except KeyError as e:
            raise ValueError(f"Invalid base in codon: {e}")
        
        index = 16 * b1 + 4 * b2 + b3
        
        return index
    
    @staticmethod
    def index_to_codon(index: int) -> str:
        """
        Convert an index (0-63) to a 3-letter codon.
        
        Args:
            index: Index from 0 to 63
            
        Returns:
            3-letter codon string
        """
        if index < 0 or index >= 64:
            raise ValueError(f"Index must be 0-63, got: {index}")
        
        b1 = index // 16
        b2 = (index % 16) // 4
        b3 = index % 4
        
        codon = (CodonEncoding.INDEX_TO_BASE[b1] + 
                 CodonEncoding.INDEX_TO_BASE[b2] + 
                 CodonEncoding.INDEX_TO_BASE[b3])
        
        return codon
    
    @staticmethod
    def codon_to_6bit(codon: str) -> str:
        """
        Convert codon to 6-bit binary string.
        
        Args:
            codon: 3-letter codon
            
        Returns:
            6-bit binary string
        """
        index = CodonEncoding.codon_to_index(codon)
        return format(index, '06b')
    
    @staticmethod
    def sixbit_to_codon(bits: str) -> str:
        """
        Convert 6-bit binary string to codon.
        
        Args:
            bits: 6-bit binary string
            
        Returns:
            3-letter codon
        """
        if len(bits) != 6:
            raise ValueError(f"Must be 6 bits, got: {bits}")
        
        index = int(bits, 2)
        return CodonEncoding.index_to_codon(index)
    
    @staticmethod
    def dna_sequence_to_grid_64(sequence: str) -> List[int]:
        """
        Convert DNA sequence to sequence of 64-grid indices.
        
        Args:
            sequence: DNA sequence (length must be multiple of 3)
            
        Returns:
            List of indices (0-63)
        """
        if len(sequence) % 3 != 0:
            raise ValueError(f"Sequence length must be multiple of 3, got: {len(sequence)}")
        
        indices = []
        for i in range(0, len(sequence), 3):
            codon = sequence[i:i+3]
            indices.append(CodonEncoding.codon_to_index(codon))
        
        return indices
    
    @staticmethod
    def grid_64_to_coordinates(index: int) -> Tuple[int, int]:
        """
        Convert 64-grid index to 2D coordinates (8x8 grid).
        
        Args:
            index: Index from 0 to 63
            
        Returns:
            (row, col): Position on 8x8 grid
        """
        if index < 0 or index >= 64:
            raise ValueError(f"Index must be 0-63, got: {index}")
        
        row = index // 8
        col = index % 8
        
        return (row, col)
    
    @staticmethod
    def codon_to_coordinates(codon: str) -> Tuple[int, int]:
        """
        Convert codon directly to 2D coordinates on 8x8 grid.
        
        Args:
            codon: 3-letter codon
            
        Returns:
            (row, col): Position on 8x8 grid
        """
        index = CodonEncoding.codon_to_index(codon)
        return CodonEncoding.grid_64_to_coordinates(index)
    
    @staticmethod
    def base4_to_base2(base4_digits: List[int]) -> str:
        """
        Convert base-4 digits to base-2 (binary).
        
        Args:
            base4_digits: List of base-4 digits (0-3)
            
        Returns:
            Binary string
        """
        # Each base-4 digit = 2 binary bits
        binary = ''
        for digit in base4_digits:
            if digit < 0 or digit > 3:
                raise ValueError(f"Base-4 digit must be 0-3, got: {digit}")
            binary += format(digit, '02b')
        
        return binary
    
    @staticmethod
    def codon_hamming_distance(codon1: str, codon2: str) -> int:
        """
        Compute Hamming distance between two codons.
        
        Args:
            codon1: First codon
            codon2: Second codon
            
        Returns:
            Hamming distance (0-3)
        """
        if len(codon1) != 3 or len(codon2) != 3:
            raise ValueError("Both codons must be 3 letters")
        
        distance = sum(b1 != b2 for b1, b2 in zip(codon1.upper(), codon2.upper()))
        
        return distance
