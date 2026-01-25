#!/usr/bin/env python3
"""
Lab Convert Sim v1.0
Mutation sandbox for generating compiler variations

Purpose: Generates variation through controlled mutation
Role: Darwin's finches - variation engine

Takes a baseline compiler implementation and generates
mutated variants for evolutionary testing.
"""

import sys
import random
import json
import copy
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MutationConfig:
    """Configuration for mutation generation"""
    mutation_rate: float = 0.15          # Probability of any given mutation
    max_mutations_per_run: int = 3       # Max mutations to apply
    seed: int = None                      # Random seed for reproducibility


class MutationEngine:
    """Generates controlled mutations of compiler behavior"""
    
    MUTATION_TYPES = [
        'optimization_level',
        'error_tolerance',
        'memory_strategy',
        'parse_strategy',
        'code_generation',
        'register_allocation',
        'instruction_scheduling',
    ]
    
    def __init__(self, config: MutationConfig = None):
        self.config = config or MutationConfig()
        if self.config.seed is not None:
            random.seed(self.config.seed)
    
    def mutate_optimization_level(self, params: Dict) -> Dict:
        """Mutate compiler optimization settings"""
        params = copy.deepcopy(params)
        
        if 'optimization' not in params:
            params['optimization'] = {}
        
        # Mutate optimization level
        levels = ['O0', 'O1', 'O2', 'O3', 'Os', 'Oz']
        params['optimization']['level'] = random.choice(levels)
        
        # Mutate specific flags
        flags = params['optimization'].get('flags', [])
        
        possible_flags = [
            'inline-functions',
            'unroll-loops',
            'vectorize',
            'dead-code-elimination',
            'constant-folding',
            'tail-call-optimization',
        ]
        
        # Add or remove a random flag
        if random.random() < 0.5 and possible_flags:
            new_flag = random.choice(possible_flags)
            if new_flag not in flags:
                flags.append(new_flag)
        elif flags:
            flags.pop(random.randint(0, len(flags) - 1))
        
        params['optimization']['flags'] = flags
        
        return params
    
    def mutate_error_tolerance(self, params: Dict) -> Dict:
        """Mutate error handling and tolerance"""
        params = copy.deepcopy(params)
        
        if 'error_handling' not in params:
            params['error_handling'] = {}
        
        # Mutate strictness level
        params['error_handling']['strict_mode'] = random.choice([True, False])
        params['error_handling']['warning_as_error'] = random.choice([True, False])
        
        # Mutate error recovery strategy
        strategies = ['abort', 'skip', 'recover', 'fallback']
        params['error_handling']['recovery_strategy'] = random.choice(strategies)
        
        return params
    
    def mutate_memory_strategy(self, params: Dict) -> Dict:
        """Mutate memory allocation and GC strategy"""
        params = copy.deepcopy(params)
        
        if 'memory' not in params:
            params['memory'] = {}
        
        # Mutate GC strategy
        gc_strategies = ['mark-sweep', 'reference-counting', 'generational', 'none']
        params['memory']['gc_strategy'] = random.choice(gc_strategies)
        
        # Mutate allocation strategy
        alloc_strategies = ['stack', 'heap', 'pool', 'arena']
        params['memory']['allocation_strategy'] = random.choice(alloc_strategies)
        
        # Mutate heap size
        params['memory']['initial_heap_mb'] = random.choice([64, 128, 256, 512, 1024])
        
        return params
    
    def mutate_parse_strategy(self, params: Dict) -> Dict:
        """Mutate parsing strategy"""
        params = copy.deepcopy(params)
        
        if 'parser' not in params:
            params['parser'] = {}
        
        # Mutate parser type
        parser_types = ['recursive-descent', 'lr', 'lalr', 'earley', 'packrat']
        params['parser']['type'] = random.choice(parser_types)
        
        # Mutate lookahead
        params['parser']['lookahead'] = random.choice([1, 2, 3, 5])
        
        return params
    
    def mutate_code_generation(self, params: Dict) -> Dict:
        """Mutate code generation strategy"""
        params = copy.deepcopy(params)
        
        if 'codegen' not in params:
            params['codegen'] = {}
        
        # Mutate target architecture
        architectures = ['x86_64', 'arm64', 'wasm', 'bytecode', 'ast-interpreter']
        params['codegen']['target'] = random.choice(architectures)
        
        # Mutate calling convention
        conventions = ['cdecl', 'stdcall', 'fastcall', 'vectorcall']
        params['codegen']['calling_convention'] = random.choice(conventions)
        
        return params
    
    def mutate_register_allocation(self, params: Dict) -> Dict:
        """Mutate register allocation strategy"""
        params = copy.deepcopy(params)
        
        if 'register_allocation' not in params:
            params['register_allocation'] = {}
        
        # Mutate allocation algorithm
        algorithms = ['linear-scan', 'graph-coloring', 'greedy', 'optimal']
        params['register_allocation']['algorithm'] = random.choice(algorithms)
        
        # Mutate spill strategy
        spill_strategies = ['furthest-use', 'least-recently-used', 'cost-based']
        params['register_allocation']['spill_strategy'] = random.choice(spill_strategies)
        
        return params
    
    def mutate_instruction_scheduling(self, params: Dict) -> Dict:
        """Mutate instruction scheduling"""
        params = copy.deepcopy(params)
        
        if 'scheduling' not in params:
            params['scheduling'] = {}
        
        # Mutate scheduling algorithm
        algorithms = ['list', 'trace', 'software-pipelining', 'none']
        params['scheduling']['algorithm'] = random.choice(algorithms)
        
        return params
    
    def generate_mutations(self, baseline_params: Dict) -> Dict:
        """
        Generate a mutated variant of baseline parameters
        
        Returns mutated parameters with metadata
        """
        mutated = copy.deepcopy(baseline_params)
        mutations_applied = []
        
        # Determine how many mutations to apply
        num_mutations = random.randint(1, self.config.max_mutations_per_run)
        
        # Select random mutation types
        mutation_types = random.sample(
            self.MUTATION_TYPES, 
            min(num_mutations, len(self.MUTATION_TYPES))
        )
        
        # Apply mutations
        for mutation_type in mutation_types:
            if random.random() < self.config.mutation_rate:
                method_name = f"mutate_{mutation_type}"
                if hasattr(self, method_name):
                    mutated = getattr(self, method_name)(mutated)
                    mutations_applied.append(mutation_type)
        
        # Add mutation metadata
        mutated['_mutation_metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'mutations_applied': mutations_applied,
            'mutation_rate': self.config.mutation_rate,
            'seed': self.config.seed,
        }
        
        return mutated


def load_baseline(baseline_file: str) -> Dict:
    """Load baseline compiler parameters"""
    with open(baseline_file) as f:
        return json.load(f)


def save_variant(variant: Dict, output_file: str):
    """Save mutated variant"""
    with open(output_file, 'w') as f:
        json.dump(variant, f, indent=2)


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Lab Convert Sim v1.0 - Mutation Sandbox")
        print("Generates compiler variations for evolutionary testing")
        print("\nUsage:")
        print("  lab_convert_sim.py <baseline.json> <output.json> [seed]")
        print("\nExample:")
        print("  lab_convert_sim.py baseline_compiler.json mutant_001.json 42")
        sys.exit(1)
    
    baseline_file = sys.argv[1]
    output_file = sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    # Load baseline
    try:
        baseline = load_baseline(baseline_file)
    except Exception as e:
        print(f"✗ Failed to load baseline: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Configure mutation engine
    config = MutationConfig(seed=seed)
    engine = MutationEngine(config)
    
    # Generate mutation
    print("=" * 60)
    print("Lab Convert Sim - Mutation Generation")
    print("=" * 60)
    print(f"Baseline: {baseline_file}")
    print(f"Output: {output_file}")
    if seed is not None:
        print(f"Seed: {seed}")
    
    mutant = engine.generate_mutations(baseline)
    
    # Save variant
    save_variant(mutant, output_file)
    
    # Report mutations
    metadata = mutant.get('_mutation_metadata', {})
    mutations = metadata.get('mutations_applied', [])
    
    print(f"\n✓ Generated mutant with {len(mutations)} mutations:")
    for mutation in mutations:
        print(f"  - {mutation}")
    
    print(f"\n✓ Saved to: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
