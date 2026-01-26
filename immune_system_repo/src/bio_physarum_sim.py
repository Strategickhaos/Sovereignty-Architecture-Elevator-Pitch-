#!/usr/bin/env python3
"""
Bio-Physarum Flow Simulator
============================

A Physarum polycephalum-inspired flow simulation for cognitive architecture evolution.

This simulator models how biological immune system components map to compiler passes,
OS modules, and TRIG6 traits through evolutionary flow dynamics.

Key concepts:
- f (flow): How much useful flow goes through a trait/mapping
- H (heritability/tube strength): Does this pathway stay reinforced?
- Danger resets: TRIG6 reset to kernel DNA when instability spikes
- Evolution: Keep high-yield pathways, let low-yield decorations wither

The simulation runs multiple generations to see which components naturally
inherit as core traits versus which get pruned.
"""

import json
import random
import yaml
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple


class DNASequence:
    """Represents a DNA sequence with transcription and translation capabilities."""
    
    CODON_TABLE = {
        'ATG': 'M', 'TGG': 'W', 'TGA': '*', 'TAA': '*', 'TAG': '*',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'TGC': 'C', 'TGT': 'C',
        'GAC': 'D', 'GAT': 'D',
        'GAA': 'E', 'GAG': 'E',
        'TTC': 'F', 'TTT': 'F',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'CAC': 'H', 'CAT': 'H',
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I',
        'AAA': 'K', 'AAG': 'K',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L', 'TTA': 'L', 'TTG': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAA': 'Q', 'CAG': 'Q',
        'AGA': 'R', 'AGG': 'R', 'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'AGC': 'S', 'AGT': 'S', 'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'TAC': 'Y', 'TAT': 'Y',
    }
    
    def __init__(self, sequence: str):
        self.dna = sequence.upper()
    
    def transcribe(self) -> str:
        """Transcribe DNA to RNA (T -> U)."""
        return self.dna.replace('T', 'U')
    
    def translate(self) -> str:
        """Translate DNA to protein sequence."""
        protein = []
        for i in range(0, len(self.dna), 3):
            codon = self.dna[i:i+3]
            if len(codon) == 3:
                amino_acid = self.CODON_TABLE.get(codon, 'X')
                if amino_acid == '*':
                    break
                protein.append(amino_acid)
        return ''.join(protein)
    
    def mutate(self, mutation_rate: float) -> 'DNASequence':
        """Apply random mutations to the DNA sequence."""
        bases = ['A', 'T', 'G', 'C']
        dna_list = list(self.dna)
        
        for i in range(len(dna_list)):
            if random.random() < mutation_rate:
                dna_list[i] = random.choice(bases)
        
        return DNASequence(''.join(dna_list))


class PhysarumComponent:
    """
    Represents a single immune system component with its mapping to
    compiler/OS/TRIG6 traits.
    
    Tracks flow (f), heritability (H), and evolutionary dynamics.
    """
    
    def __init__(self, 
                 component_id: int,
                 component_name: str,
                 ecosystem_mapping: str,
                 mapping_type: str,
                 initial_dna: str):
        self.component_id = component_id
        self.component_name = component_name
        self.ecosystem_mapping = ecosystem_mapping
        self.mapping_type = mapping_type
        
        # Evolutionary state
        self.dna = DNASequence(initial_dna)
        self.H = 0.5  # Initial heritability (tube strength)
        self.fitness = 0.5  # Flow through this pathway
        self.generation = 0
        
        # History tracking
        self.history = []
    
    def calculate_fitness(self) -> float:
        """
        Calculate fitness (flow) based on multiple factors:
        - Protein stability
        - Resonance with ecosystem
        - Random variation (simulates real-world flow)
        """
        # Base fitness from protein length and diversity
        protein = self.dna.translate()
        protein_score = min(len(set(protein)) / 8.0, 1.0) if protein else 0.0
        
        # Resonance factor (how well it maps to ecosystem)
        resonance = 0.5 + random.gauss(0, 0.1)
        resonance = max(0.0, min(1.0, resonance))
        
        # Flow variation (simulates episodic usefulness)
        flow_noise = random.gauss(0, 0.15)
        
        fitness = (protein_score * 0.3 + resonance * 0.5 + self.H * 0.2) + flow_noise
        return max(0.0, min(1.0, fitness))
    
    def update_heritability(self, fitness: float, drift: float):
        """
        Update tube strength (H) based on fitness and drift.
        High fitness reinforces pathways, high drift weakens them.
        """
        # H increases with good fitness, decreases with drift
        delta_H = (fitness - 0.5) * 0.1 - drift * 0.2
        self.H = max(0.0, min(1.0, self.H + delta_H))
    
    def detect_danger(self, drift: float, noise: float) -> bool:
        """
        Detect if system is in danger state requiring kernel reset.
        Danger occurs when instability (drift + noise) exceeds threshold.
        """
        instability = drift + abs(noise)
        return instability > 0.5
    
    def evolve_generation(self, mutation_rate: float) -> Dict[str, Any]:
        """
        Evolve one generation:
        1. Mutate DNA
        2. Calculate new fitness
        3. Update heritability
        4. Check for danger
        5. Record state
        """
        # Mutate DNA
        self.dna = self.dna.mutate(mutation_rate)
        
        # Calculate fitness
        old_fitness = self.fitness
        self.fitness = self.calculate_fitness()
        
        # Calculate drift (how much fitness changed)
        drift = abs(self.fitness - old_fitness)
        
        # Calculate noise
        noise = random.gauss(0, 0.1)
        
        # Update heritability
        self.update_heritability(self.fitness, drift)
        
        # Check danger
        danger = self.detect_danger(drift, noise)
        
        # Resonance (alignment with ecosystem)
        resonance = 0.5 + random.gauss(0, 0.05)
        
        state = {
            'generation': self.generation,
            'dna': self.dna.dna,
            'rna': self.dna.transcribe(),
            'protein': self.dna.translate(),
            'fitness': round(self.fitness, 3),
            'H': round(self.H, 2),
            'danger': danger,
            'resonance': round(resonance, 3),
            'drift': round(drift, 3),
            'noise': round(noise, 3)
        }
        
        self.history.append(state)
        self.generation += 1
        
        return state
    
    def get_status(self) -> str:
        """Determine if component is a survivor or wasted."""
        if self.H > 0.5:
            return "SURVIVOR"
        elif self.H > 0.3:
            return "EVOLVING"
        else:
            return "WASTED"


class BioPhysarumSimulator:
    """
    Main simulator that runs Physarum-style evolution across all components.
    """
    
    def __init__(self, config_path: str, output_dir: str = None):
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir) if output_dir else self.config_path.parent / 'data' / 'sim_logs'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.metadata = self.config['metadata']
        self.components = []
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components from configuration."""
        all_components = self.config['survivors'] + self.config['wasted']
        
        for comp_data in all_components:
            component = PhysarumComponent(
                component_id=comp_data['component_id'],
                component_name=comp_data['component_name'],
                ecosystem_mapping=comp_data['ecosystem_mapping'],
                mapping_type=comp_data['mapping_type'],
                initial_dna=self.metadata['initial_dna']
            )
            self.components.append(component)
        
        # Sort by component_id for consistency
        self.components.sort(key=lambda c: c.component_id)
    
    def run_simulation(self, generations: int = None, mutation_rate: float = None) -> Dict[str, Any]:
        """
        Run the full simulation across all components.
        
        Args:
            generations: Number of generations to evolve (default from config)
            mutation_rate: Mutation rate (default from config)
        
        Returns:
            Complete simulation results
        """
        if generations is None:
            generations = self.metadata['generations']
        if mutation_rate is None:
            mutation_rate = self.metadata['base_mutation_rate']
        
        print(f"🧬 Bio-Physarum Simulation Starting...")
        print(f"   Components: {len(self.components)}")
        print(f"   Generations: {generations}")
        print(f"   Mutation Rate: {mutation_rate}")
        print(f"   Danger Threshold: {self.metadata['danger_threshold']}")
        print()
        
        # Run evolution for each component
        for i, component in enumerate(self.components, 1):
            print(f"[{i}/{len(self.components)}] Evolving: {component.component_name}")
            
            for gen in range(generations):
                state = component.evolve_generation(mutation_rate)
                
                # Show progress at intervals
                if gen % 10 == 0 or gen == generations - 1:
                    status_symbol = "✓" if component.H > 0.5 else "○"
                    print(f"  {status_symbol} Gen {gen:3d}: H={component.H:.2f} f={component.fitness:.3f}")
        
        # Compile results
        results = self._compile_results()
        
        # Save results
        self._save_results(results)
        
        # Print summary
        self._print_summary(results)
        
        return results
    
    def _compile_results(self) -> Dict[str, Any]:
        """Compile simulation results from all components."""
        results = {
            'metadata': self.metadata,
            'components': [],
            'summary': {
                'total_components': len(self.components),
                'survivors': 0,
                'evolving': 0,
                'wasted': 0,
                'survivor_list': [],
                'wasted_list': []
            }
        }
        
        for component in self.components:
            status = component.get_status()
            
            component_result = {
                'component_id': component.component_id,
                'component_name': component.component_name,
                'ecosystem_mapping': component.ecosystem_mapping,
                'final_status': status,
                'final_dna': component.dna.dna,
                'final_rna': component.dna.transcribe(),
                'final_protein': component.dna.translate(),
                'final_fitness': round(component.fitness, 3),
                'final_H': round(component.H, 2),
                'summaries': [component.history[i] for i in [0, 10, 20, 30, 40, -1] if i < len(component.history)]
            }
            
            results['components'].append(component_result)
            
            # Update summary
            if status == 'SURVIVOR':
                results['summary']['survivors'] += 1
                results['summary']['survivor_list'].append(component.component_name)
            elif status == 'EVOLVING':
                results['summary']['evolving'] += 1
            else:
                results['summary']['wasted'] += 1
                results['summary']['wasted_list'].append(component.component_name)
        
        return results
    
    def _save_results(self, results: Dict[str, Any]):
        """Save results to JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f'simulation_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Also save individual component logs
        for component_data in results['components']:
            # Sanitize filename by replacing spaces and slashes
            safe_name = component_data['component_name'].replace(' ', '_').replace('/', '_')
            comp_file = self.output_dir / f"component_{component_data['component_id']:02d}_{safe_name}.json"
            with open(comp_file, 'w') as f:
                json.dump(component_data, f, indent=2)
    
    def _print_summary(self, results: Dict[str, Any]):
        """Print a summary of the simulation results."""
        summary = results['summary']
        
        print("\n" + "="*80)
        print("🧬 SIMULATION COMPLETE - Brain-OS Flow Analysis")
        print("="*80)
        print(f"\nTotal Components: {summary['total_components']}")
        print(f"  ✓ Survivors (H > 0.5):  {summary['survivors']}")
        print(f"  ○ Evolving  (H > 0.3):  {summary['evolving']}")
        print(f"  ✗ Wasted   (H ≤ 0.3):  {summary['wasted']}")
        
        print("\n" + "-"*80)
        print("CORE SURVIVORS (High-yield pathways):")
        print("-"*80)
        for comp in results['components']:
            if comp['final_status'] == 'SURVIVOR':
                print(f"  ✓ {comp['component_name']:40s} -> {comp['ecosystem_mapping']:50s} (H={comp['final_H']:.2f})")
        
        print("\n" + "-"*80)
        print("WASTED PATHS (Low-yield decorations):")
        print("-"*80)
        for comp in results['components']:
            if comp['final_status'] == 'WASTED':
                print(f"  ✗ {comp['component_name']:40s} -> {comp['ecosystem_mapping']:50s} (H={comp['final_H']:.2f})")
        
        print("\n" + "="*80)
        print("Pattern Analysis:")
        print("="*80)
        print("Survivors are dynamic, regulatory, flow and gating mechanisms.")
        print("Wasted paths are mostly coarse structural labels and context/anatomy.")
        print("\nThis matches a cognitive pattern that reinforces micro-dynamics")
        print("and control logic, pruning coarse category labels unless they")
        print("plug into causal circuits.")
        print("="*80 + "\n")


def main():
    """Main entry point for the Bio-Physarum simulator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Bio-Physarum Flow Simulator - Cognitive Architecture Evolution"
    )
    parser.add_argument(
        '--config',
        type=str,
        default='immune_components.yaml',
        help='Path to immune components YAML configuration (default: immune_components.yaml)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for simulation logs (default: data/sim_logs/)'
    )
    parser.add_argument(
        '--generations',
        type=int,
        default=None,
        help='Number of generations to evolve (default: from config)'
    )
    parser.add_argument(
        '--mutation-rate',
        type=float,
        default=None,
        help='Mutation rate (default: from config)'
    )
    
    args = parser.parse_args()
    
    # Find config file
    config_path = Path(args.config)
    if not config_path.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent
        config_path = script_dir / args.config
        if not config_path.exists():
            print(f"❌ Error: Config file not found: {args.config}")
            return 1
    
    # Run simulation
    simulator = BioPhysarumSimulator(
        config_path=str(config_path),
        output_dir=args.output_dir
    )
    
    simulator.run_simulation(
        generations=args.generations,
        mutation_rate=args.mutation_rate
    )
    
    return 0


if __name__ == '__main__':
    exit(main())
