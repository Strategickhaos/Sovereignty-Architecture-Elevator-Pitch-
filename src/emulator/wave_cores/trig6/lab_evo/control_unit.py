"""
Control Unit: Mutation Sequencer
Phase 4.13: Arrow DNA Exploration - Mutation Sequencing
"""

from typing import Dict, List, Optional
import random
import logging

logger = logging.getLogger(__name__)

# Seed random for reproducibility in tests
random.seed(42)


class MutationSequencer:
    """
    Control Unit for DNA mutation sequencing.
    Manages evolution of DNA sequences through controlled mutations.
    """
    
    def __init__(self, evolution_params: Dict):
        """
        Initialize Mutation Sequencer.
        
        Args:
            evolution_params: Evolution parameters from DNA config
        """
        self.mutation_rate = evolution_params.get('mutation_rate', 0.05)
        self.selection_threshold = evolution_params.get('selection_threshold', 0.67)
        
    def sequence_mutations(self, 
                          sequence: str,
                          codon_ops: List[Dict],
                          tick: int) -> List[Dict]:
        """
        Sequence mutations based on codon operations and tick.
        
        Args:
            sequence: DNA sequence
            codon_ops: Codon operations from ALU
            tick: Current neural tick
            
        Returns:
            List of sequenced mutations
        """
        codons = sequence.split('-')
        sequenced = []
        
        for i, op in enumerate(codon_ops):
            # Determine if mutation occurs at this tick
            should_mutate = random.random() < self.mutation_rate
            
            if should_mutate:
                mutation = {
                    'tick': tick,
                    'position': i,
                    'codon': op['codon'],
                    'operation': op['operation'],
                    'type': 'point_mutation',
                    'trigger': 'neural_tick'
                }
                sequenced.append(mutation)
                logger.debug(f"Mutation sequenced at position {i}: {op['codon']}")
        
        return sequenced
    
    def generate_candidates(self, sequence: str) -> List[Dict]:
        """
        Generate mutation candidates for evolution gate.
        
        Args:
            sequence: Current DNA sequence
            
        Returns:
            List of mutation candidates with fitness predictions
        """
        # Predefined mutations based on zyBooks arrow lab
        mutation_library = [
            {
                'from': 'CGT',
                'to': 'CGA',
                'effect': 'single_loop_rect',
                'fitness_delta': -0.1,
                'risk': 0.2
            },
            {
                'from': 'GCA',
                'to': 'GCC',
                'effect': 'unicode_render',
                'fitness_delta': 0.05,
                'risk': 0.15
            },
            {
                'from': 'TAA',
                'to': 'TAG',
                'effect': 'relaxed_validation',
                'fitness_delta': -0.2,
                'risk': 0.3
            },
            {
                'from': 'CGT',
                'to': 'TGC',
                'effect': 'trig_damped_render',
                'fitness_delta': 0.15,
                'risk': 0.25
            }
        ]
        
        codons = sequence.split('-')
        candidates = []
        
        for i, codon in enumerate(codons):
            for mutation in mutation_library:
                if mutation['from'] == codon:
                    mutated_codons = codons.copy()
                    mutated_codons[i] = mutation['to']
                    
                    candidates.append({
                        'original': sequence,
                        'mutated': '-'.join(mutated_codons),
                        'position': i,
                        'mutation': f"{mutation['from']} → {mutation['to']}",
                        'effect': mutation['effect'],
                        'fitness_delta': mutation['fitness_delta'],
                        'risk': mutation['risk'],
                        'probability': self.mutation_rate * (1 - mutation['risk'])
                    })
        
        return candidates
    
    def validate_mutation(self, 
                         mutation: Dict,
                         consensus: float) -> bool:
        """
        Validate mutation against consensus threshold.
        
        Args:
            mutation: Mutation candidate
            consensus: Legion council consensus score
            
        Returns:
            True if mutation passes validation
        """
        return consensus >= self.selection_threshold
