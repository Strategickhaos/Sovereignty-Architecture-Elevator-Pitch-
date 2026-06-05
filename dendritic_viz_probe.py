#!/usr/bin/env python3
"""
Proto-Elamite Dendritic Visualization Probe
An instrumented probe for mapping symbol mutations with evolutionary gates

This is a PROBE, not production code - for visualization and analysis only.
No auto-promotion to canonical mappings.
"""

import json
import random
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
from pathlib import Path


@dataclass
class SymbolMapping:
    """Represents a symbol's current mapping state"""
    symbol: str
    value: str
    fitness: float  # f value
    danger: float   # danger metric


@dataclass
class MutationEdge:
    """Represents a mutation edge for visualization"""
    symbol: str
    old_value: str
    new_value: str
    f_old: float
    f_new: float
    danger_old: float
    danger_new: float
    alpha: float
    accepted: bool
    color: str  # green, yellow, red


class ProtoDendriticProbe:
    """Instrumented probe for Proto-Elamite symbol mutation visualization"""
    
    def __init__(self, max_mutations_per_symbol: int = 50):
        self.max_mutations_per_symbol = max_mutations_per_symbol
        self.edges: List[MutationEdge] = []
        
        # Proto-Elamite symbols to focus on
        self.proto_elamite_symbols = [
            "impressed circle",
            "wedge cluster",
            "bar",
            "dot series"
        ]
        
        # Proverbs baseline anchor (simplified representation)
        self.proverbs_baseline = {
            "wisdom": {"value": "knowledge_path", "fitness": 0.85, "danger": 2.0},
            "guidance": {"value": "direction_map", "fitness": 0.80, "danger": 1.5},
            "truth": {"value": "reality_anchor", "fitness": 0.90, "danger": 1.0},
        }
        
        # Initialize symbol mappings
        self.symbol_mappings = self._initialize_symbols()
    
    def _initialize_symbols(self) -> Dict[str, SymbolMapping]:
        """Initialize Proto-Elamite symbols with baseline mappings"""
        mappings = {}
        
        # Proto-Elamite symbol initialization
        initial_values = {
            "impressed circle": "circular_count",
            "wedge cluster": "angular_group",
            "bar": "linear_mark",
            "dot series": "point_sequence"
        }
        
        for symbol in self.proto_elamite_symbols:
            mappings[symbol] = SymbolMapping(
                symbol=symbol,
                value=initial_values[symbol],
                fitness=0.5 + random.uniform(-0.1, 0.1),  # Start near neutral
                danger=random.uniform(1.0, 3.0)
            )
        
        return mappings
    
    def _calculate_fitness(self, symbol: str, value: str) -> float:
        """
        Calculate fitness of a symbol-value mapping
        Uses a simple heuristic based on value complexity and consistency
        """
        # Base fitness from value length (normalized)
        base_fitness = min(0.5, len(value) / 30.0)
        
        # Add randomness to simulate real mutation dynamics
        variation = random.uniform(-0.2, 0.3)
        
        # Check consistency with Proverbs baseline
        proverbs_bonus = 0.0
        for proverb_key, proverb_data in self.proverbs_baseline.items():
            if proverb_key in value or proverb_data["value"] in value:
                proverbs_bonus = 0.15
                break
        
        fitness = base_fitness + variation + proverbs_bonus
        return max(0.0, min(1.0, fitness))  # Clamp to [0, 1]
    
    def _calculate_danger(self, symbol: str, value: str, fitness: float) -> float:
        """
        Calculate danger metric for a mapping
        Lower fitness generally means higher danger
        """
        # Inverse relationship with fitness
        base_danger = (1.0 - fitness) * 5.0
        
        # Add complexity penalty
        complexity_penalty = len(value.split("_")) * 0.3
        
        # Random variation
        variation = random.uniform(-0.5, 0.5)
        
        danger = base_danger + complexity_penalty + variation
        return max(0.1, danger)  # Minimum danger
    
    def _mutate_value(self, current_value: str) -> str:
        """Generate a mutated value for a symbol"""
        mutation_types = [
            lambda v: v + "_variant",
            lambda v: v.replace("_", "_new_"),
            lambda v: v.split("_")[0] + "_modified",
            lambda v: "evolved_" + v,
            lambda v: v + "_form",
            lambda v: v.replace("count", "measure").replace("group", "cluster"),
        ]
        
        mutation = random.choice(mutation_types)
        return mutation(current_value)
    
    def _calculate_alpha(self, f_old: float, f_new: float, danger_old: float, danger_new: float) -> float:
        """
        Calculate acceptance probability (alpha)
        Evolutionary gate mechanism
        """
        # Fitness improvement factor
        fitness_delta = f_new - f_old
        
        # Danger change factor (negative if danger increases)
        danger_delta = danger_old - danger_new
        
        # Combine factors
        alpha = 0.5 + (fitness_delta * 0.5) + (danger_delta * 0.1)
        
        return max(0.0, min(1.0, alpha))  # Clamp to [0, 1]
    
    def _evolutionary_gate(self, alpha: float) -> bool:
        """
        Evolutionary gate: Accept or reject mutation
        """
        return random.random() < alpha
    
    def _assign_color(self, edge: MutationEdge) -> str:
        """
        Assign color based on fitness and danger changes
        - Green: f_new - f_old >= 0.05 AND danger_new <= danger_old
        - Yellow: small |Δf| but safer (danger_new < danger_old)
        - Red: f_new > f_old but danger_new > danger_old
        """
        f_delta = edge.f_new - edge.f_old
        
        # Green: significant fitness improvement AND not more dangerous
        if f_delta >= 0.05 and edge.danger_new <= edge.danger_old:
            return "green"
        
        # Yellow: small fitness change but safer
        if abs(f_delta) < 0.05 and edge.danger_new < edge.danger_old:
            return "yellow"
        
        # Red: fitness improvement but more dangerous
        if edge.f_new > edge.f_old and edge.danger_new > edge.danger_old:
            return "red"
        
        # Default to yellow for other cases
        return "yellow"
    
    def _should_drop_edge(self, edge: MutationEdge) -> bool:
        """
        Hard rails: Drop edges that meet certain criteria
        - danger_new > danger_old * 2
        - f_new < 0.01
        """
        if edge.danger_new > edge.danger_old * 2:
            return True
        
        if edge.f_new < 0.01:
            return True
        
        return False
    
    def run_mutation_pass(self):
        """
        Execute the dendritic visualization pass
        Run mutations for each symbol and log edges
        """
        print("🧬 PROTO-ELAMITE DENDRITIC VISUALIZATION PROBE")
        print("=" * 60)
        print(f"Scope: {len(self.proto_elamite_symbols)} Proto-Elamite symbols")
        print(f"Max mutations per symbol: {self.max_mutations_per_symbol}")
        print(f"Proverbs baseline anchors: {len(self.proverbs_baseline)}")
        print()
        
        for symbol in self.proto_elamite_symbols:
            print(f"Processing: {symbol}")
            current_mapping = self.symbol_mappings[symbol]
            
            mutations_accepted = 0
            mutations_rejected = 0
            
            for mutation_num in range(self.max_mutations_per_symbol):
                # Store old state
                old_value = current_mapping.value
                old_fitness = current_mapping.fitness
                old_danger = current_mapping.danger
                
                # Generate mutation
                new_value = self._mutate_value(old_value)
                new_fitness = self._calculate_fitness(symbol, new_value)
                new_danger = self._calculate_danger(symbol, new_value, new_fitness)
                
                # Calculate alpha and apply evolutionary gate
                alpha = self._calculate_alpha(old_fitness, new_fitness, old_danger, new_danger)
                accepted = self._evolutionary_gate(alpha)
                
                # Create edge
                edge = MutationEdge(
                    symbol=symbol,
                    old_value=old_value,
                    new_value=new_value,
                    f_old=old_fitness,
                    f_new=new_fitness,
                    danger_old=old_danger,
                    danger_new=new_danger,
                    alpha=alpha,
                    accepted=accepted,
                    color=""  # Will be assigned later
                )
                
                # Assign color
                edge.color = self._assign_color(edge)
                
                # Apply hard rails filter
                if not self._should_drop_edge(edge):
                    self.edges.append(edge)
                    
                    # Update mapping if accepted
                    if accepted:
                        current_mapping.value = new_value
                        current_mapping.fitness = new_fitness
                        current_mapping.danger = new_danger
                        mutations_accepted += 1
                    else:
                        mutations_rejected += 1
            
            print(f"  ✓ {mutations_accepted} accepted, {mutations_rejected} rejected")
        
        print()
        print(f"Total edges logged: {len(self.edges)}")
    
    def generate_output(self, output_path: str = "neurograph/proto_elamite_pelsim1_dendrites.json"):
        """
        Generate JSON output file
        NO AUTO-PROMOTION to canonical mappings
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare output structure
        output_data = {
            "metadata": {
                "probe_type": "dendritic_visualization",
                "scope": "proto_elamite",
                "symbols": self.proto_elamite_symbols,
                "max_mutations_per_symbol": self.max_mutations_per_symbol,
                "proverbs_baseline_anchors": list(self.proverbs_baseline.keys()),
                "total_edges": len(self.edges),
                "warning": "PROBE DATA - NOT FOR CANONICAL PROMOTION"
            },
            "color_legend": {
                "green": "f_new - f_old >= 0.05 AND danger_new <= danger_old",
                "yellow": "small |Δf| but safer (danger_new < danger_old)",
                "red": "f_new > f_old but danger_new > danger_old (outline only)"
            },
            "hard_rails": {
                "dropped_if": [
                    "danger_new > danger_old * 2",
                    "f_new < 0.01"
                ]
            },
            "edges": [asdict(edge) for edge in self.edges],
            "final_mappings": {
                symbol: asdict(mapping) 
                for symbol, mapping in self.symbol_mappings.items()
            }
        }
        
        # Write JSON
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✓ Output written to: {output_file}")
        print(f"  Edges: {len(self.edges)}")
        print(f"  Color distribution:")
        
        color_counts = {"green": 0, "yellow": 0, "red": 0}
        for edge in self.edges:
            color_counts[edge.color] += 1
        
        for color, count in color_counts.items():
            print(f"    {color}: {count}")
        
        return str(output_file)


def main():
    """Execute the dendritic visualization probe"""
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create and run probe
    probe = ProtoDendriticProbe(max_mutations_per_symbol=50)
    probe.run_mutation_pass()
    
    # Generate output
    output_path = probe.generate_output()
    
    print()
    print("🎯 DENDRITIC VISUALIZATION PROBE COMPLETE")
    print("=" * 60)
    print("⚠️  IMPORTANT: This is instrumented probe data")
    print("   NO auto-promotion to canonical mappings")
    print("   For visualization and analysis purposes only")
    print()
    print(f"📊 Next steps:")
    print(f"   1. Load {output_path} in your neurograph viewer")
    print(f"   2. Filter/visualize edges by color coding")
    print(f"   3. Analyze mutation patterns and evolutionary dynamics")
    

if __name__ == "__main__":
    main()
