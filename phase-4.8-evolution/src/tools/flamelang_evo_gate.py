#!/usr/bin/env python3
"""
FlameLang Evolution Gate v1.0
Fitness-based selection with hard gates for gene evolution

DNA: TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1-ARROWEVO1
"""

import yaml
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class EvolutionGate:
    """
    Evolution gate implementing fitness-based selection with hard constraints.
    
    Selection criteria:
    - Fitness > Champion (comparative selection)
    - Equilibrium ≥ 0.99 (hard gate)
    - Noise ≤ 0.25 (hard gate)
    - Drift ≤ 0.35 (hard gate)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.champion_fitness = 0.0
        self.generation = 0
        self.evolution_log = []
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load evolution gate configuration."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            'hard_gates': {
                'min_equilibrium': 0.99,
                'max_noise': 0.25,
                'max_drift': 0.35
            },
            'selection': {
                'method': 'fitness_based',
                'auto_commit': True
            },
            'visualization': {
                'neurograph_enabled': True
            }
        }
    
    def evaluate_gene(self, gene_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a gene against hard gates and fitness criteria.
        
        Args:
            gene_data: Dictionary containing gene parameters and metrics
            
        Returns:
            Evaluation results with pass/fail status and fitness score
        """
        # Extract metrics
        metrics = gene_data.get('metrics', {})
        equilibrium = metrics.get('equilibrium', 0.0)
        noise = metrics.get('noise', 1.0)
        drift = metrics.get('drift', 1.0)
        fitness = metrics.get('fitness', 0.0)
        
        # Check hard gates
        hard_gates = self.config['hard_gates']
        gates_passed = {
            'equilibrium': equilibrium >= hard_gates['min_equilibrium'],
            'noise': noise <= hard_gates['max_noise'],
            'drift': drift <= hard_gates['max_drift']
        }
        
        all_gates_passed = all(gates_passed.values())
        
        # Check fitness against champion
        fitness_superior = fitness > self.champion_fitness
        
        # Overall evaluation
        passed = all_gates_passed and fitness_superior
        
        result = {
            'gene_id': gene_data.get('metadata', {}).get('gene_id', 'unknown'),
            'generation': self.generation,
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {
                'equilibrium': equilibrium,
                'noise': noise,
                'drift': drift,
                'fitness': fitness
            },
            'gates': gates_passed,
            'all_gates_passed': all_gates_passed,
            'fitness_superior': fitness_superior,
            'passed': passed,
            'champion_fitness': self.champion_fitness
        }
        
        # Update champion if this gene passed
        if passed:
            self.champion_fitness = fitness
            result['new_champion'] = True
        
        # Log evolution event
        self.evolution_log.append(result)
        
        return result
    
    def select_from_population(self, population: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Select genes from population based on fitness and hard gates.
        
        Args:
            population: List of gene data dictionaries
            
        Returns:
            List of selected genes that passed all criteria
        """
        selected = []
        
        for gene in population:
            result = self.evaluate_gene(gene)
            if result['passed']:
                selected.append({
                    'gene': gene,
                    'evaluation': result
                })
        
        self.generation += 1
        
        return selected
    
    def auto_commit_evolution(self, selected_genes: List[Dict[str, Any]]) -> bool:
        """
        Auto-commit evolution results if enabled.
        
        Args:
            selected_genes: List of genes that passed selection
            
        Returns:
            True if commit was successful, False otherwise
        """
        if not self.config['selection'].get('auto_commit', False):
            return False
        
        if not selected_genes:
            return False
        
        # Prepare evolution report
        report = {
            'generation': self.generation,
            'timestamp': datetime.utcnow().isoformat(),
            'selected_count': len(selected_genes),
            'champion_fitness': self.champion_fitness,
            'genes': [g['evaluation'] for g in selected_genes]
        }
        
        # Save evolution report
        report_path = Path('evolution_reports')
        report_path.mkdir(exist_ok=True)
        
        report_file = report_path / f'generation_{self.generation:04d}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Evolution committed: {report_file}")
        print(f"✓ Selected {len(selected_genes)} genes")
        print(f"✓ Champion fitness: {self.champion_fitness:.4f}")
        
        return True
    
    def generate_neurograph(self, evolution_data: Dict[str, Any]) -> str:
        """
        Generate neurograph visualization of evolution.
        
        Args:
            evolution_data: Evolution results and metrics
            
        Returns:
            Path to generated neurograph file
        """
        if not self.config['visualization'].get('neurograph_enabled', False):
            return ""
        
        # Simple ASCII neurograph
        neurograph = [
            "=" * 60,
            f"FLAMELANG EVOLUTION NEUROGRAPH - Generation {self.generation}",
            "=" * 60,
            f"Champion Fitness: {self.champion_fitness:.4f}",
            f"Timestamp: {datetime.utcnow().isoformat()}",
            "",
            "Evolution Path:",
        ]
        
        for i, log_entry in enumerate(self.evolution_log[-10:]):  # Last 10 entries
            status = "✓" if log_entry['passed'] else "✗"
            fitness = log_entry['metrics']['fitness']
            gene_id = log_entry['gene_id']
            neurograph.append(f"  {status} Gen {log_entry['generation']} | Gene {gene_id} | Fitness: {fitness:.4f}")
        
        neurograph_text = "\n".join(neurograph)
        
        # Save neurograph
        graph_path = Path('neurographs')
        graph_path.mkdir(exist_ok=True)
        
        graph_file = graph_path / f'neurograph_gen_{self.generation:04d}.txt'
        with open(graph_file, 'w') as f:
            f.write(neurograph_text)
        
        print(f"✓ Neurograph generated: {graph_file}")
        
        return str(graph_file)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get evolution statistics."""
        passed_count = sum(1 for log in self.evolution_log if log['passed'])
        total_count = len(self.evolution_log)
        
        return {
            'generation': self.generation,
            'total_evaluated': total_count,
            'total_passed': passed_count,
            'pass_rate': passed_count / total_count if total_count > 0 else 0.0,
            'champion_fitness': self.champion_fitness,
            'evolution_log_size': total_count
        }


def main():
    """Main execution for evolution gate."""
    # Example usage
    gate = EvolutionGate()
    
    # Test with sample genes
    test_genes = [
        {
            'metadata': {'gene_id': '3.35', 'gene_name': 'draw_half_arrow'},
            'metrics': {
                'equilibrium': 0.99,
                'noise': 0.20,
                'drift': 0.30,
                'fitness': 0.92
            }
        },
        {
            'metadata': {'gene_id': '3.36', 'gene_name': 'count_input'},
            'metrics': {
                'equilibrium': 0.995,
                'noise': 0.15,
                'drift': 0.25,
                'fitness': 0.95
            }
        }
    ]
    
    # Run selection
    selected = gate.select_from_population(test_genes)
    
    # Auto-commit if configured
    gate.auto_commit_evolution(selected)
    
    # Generate neurograph
    gate.generate_neurograph({'selected': selected})
    
    # Print statistics
    stats = gate.get_statistics()
    print("\n" + "=" * 60)
    print("EVOLUTION GATE STATISTICS")
    print("=" * 60)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
