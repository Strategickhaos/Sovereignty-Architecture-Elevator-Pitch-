"""
ALU Module: Arithmetic Logic Unit for Codon Operations
Phase 4.13: Arrow DNA Exploration - Codon Arithmetic Mapping
"""

from typing import Dict, List
import math
import logging

logger = logging.getLogger(__name__)


class ArrowALU:
    """
    Arithmetic Logic Unit for DNA codon operations.
    Maps codons to arithmetic/logic operations for arrow rendering.
    """
    
    def __init__(self, dna_config: Dict):
        """
        Initialize Arrow ALU.
        
        Args:
            dna_config: DNA encoding configuration
        """
        self.codon_map = dna_config.get('codon_map', {})
        self.sequence = dna_config.get('sequence', '')
        
    def process_codons(self, sequence: str) -> List[Dict]:
        """
        Process DNA sequence and map to arithmetic operations.
        
        Args:
            sequence: DNA codon sequence (e.g., "ATG-CGT-TAA-GCA-TCG")
            
        Returns:
            List of codon operations
        """
        codons = sequence.split('-')
        operations = []
        
        for i, codon in enumerate(codons):
            operation = self.codon_map.get(codon, 'unknown')
            
            op_result = {
                'position': i,
                'codon': codon,
                'operation': operation,
                'arithmetic': self._codon_to_arithmetic(codon, operation)
            }
            
            operations.append(op_result)
        
        return operations
    
    def _codon_to_arithmetic(self, codon: str, operation: str) -> Dict:
        """
        Map codon to specific arithmetic operation.
        
        Args:
            codon: Codon string (e.g., "ATG")
            operation: Operation name (e.g., "init_scanner")
            
        Returns:
            Arithmetic operation details
        """
        # Map operations to arithmetic/logic
        arithmetic_map = {
            'init_scanner': {
                'type': 'input',
                'op': 'scan',
                'params': ['h', 'w', 'head']
            },
            'nested_rect_loop': {
                'type': 'loop',
                'op': 'multiply',
                'formula': 'h × w',
                'iterations': 'h'
            },
            'validation_gate': {
                'type': 'logic',
                'op': 'compare',
                'formula': 'head > w',
                'action': 'while_reject'
            },
            'nested_tri_loop': {
                'type': 'loop',
                'op': 'decrement',
                'formula': 'head → 1',
                'iterations': 'head'
            },
            'terminate': {
                'type': 'control',
                'op': 'exit',
                'params': []
            }
        }
        
        return arithmetic_map.get(operation, {
            'type': 'unknown',
            'op': 'nop',
            'params': []
        })
    
    def compute_render_dimensions(self, 
                                   h: int, 
                                   w: int, 
                                   head: int) -> Dict:
        """
        Compute arrow render dimensions using codon arithmetic.
        
        Args:
            h: Rectangle height
            w: Rectangle width
            head: Triangle head width
            
        Returns:
            Dimension calculations
        """
        # Rectangle: h × w
        rect_rows = h
        rect_stars = h * w
        
        # Triangle: head + (head-1) + ... + 1 = head(head+1)/2
        tri_rows = head
        tri_stars = (head * (head + 1)) // 2
        
        total_rows = rect_rows + tri_rows
        total_stars = rect_stars + tri_stars
        
        return {
            'rectangle': {
                'rows': rect_rows,
                'width': w,
                'total_stars': rect_stars
            },
            'triangle': {
                'rows': tri_rows,
                'head_width': head,
                'total_stars': tri_stars
            },
            'total': {
                'rows': total_rows,
                'stars': total_stars
            }
        }
