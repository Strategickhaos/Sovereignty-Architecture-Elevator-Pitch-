#!/usr/bin/env python3
"""
Proto-Elamite Symbol Mutation Simulator (PELSIM1)

This script simulates the evolution of Proto-Elamite symbols through mutation,
applying safety rails and classification logic to generate dendrite graphs.

Rails:
- danger_new <= danger_old * 2
- f_new >= 0.01

Classification:
- green: delta_f >= 0.05 and danger_new <= danger_old (better & safer)
- yellow: small delta_f or ambiguous (default)
- red: delta_f > 0 and danger_new > danger_old (better but more dangerous)
"""

import json
import random
from datetime import datetime, timezone
from typing import List, Dict, Tuple


class ProtoElamiteSimulator:
    """Simulate Proto-Elamite symbol mutations with safety rails."""
    
    def __init__(
        self,
        symbols: List[str],
        max_mutations_per_symbol: int = 50,
        alpha: float = 0.32,
        run_id: str = "PELSIM1-RUN-001"
    ):
        self.symbols = symbols
        self.max_mutations_per_symbol = max_mutations_per_symbol
        self.alpha = alpha
        self.run_id = run_id
        self.nodes = []
        self.edges = []
        self.edge_counter = 0
        
    def _symbol_to_slug(self, symbol: str) -> str:
        """Convert symbol name to slug for node IDs."""
        return symbol.lower().replace(" ", "_")
    
    def _generate_mutation(self, symbol: str, old_value: int) -> Tuple[int, float, float, float, float]:
        """
        Generate a mutation event.
        
        Returns: (new_value, f_old, f_new, danger_old, danger_new)
        """
        # Generate random new value (typically close to old but can diverge)
        new_value = old_value + random.randint(-5, 15)
        if new_value < 1:
            new_value = 1
        
        # Generate frequency metrics (f)
        # Initial values tend to be lower frequency
        f_old = random.uniform(0.01, 0.2) if old_value <= 5 else random.uniform(0.05, 0.3)
        
        # New values can have higher or lower frequency
        # Simulate evolution: sometimes better, sometimes worse
        f_delta = random.uniform(-0.1, 0.15)
        f_new = max(0.0, f_old + f_delta)
        
        # Generate danger metrics
        # Danger tends to decrease with better understanding (evolution)
        danger_old = random.uniform(0.3, 1.0)
        danger_delta = random.uniform(-0.3, 0.4)
        danger_new = max(0.1, min(1.0, danger_old + danger_delta))
        
        return new_value, f_old, f_new, danger_old, danger_new
    
    def _check_rails(self, f_new: float, danger_old: float, danger_new: float) -> bool:
        """
        Check if mutation passes safety rails.
        
        Rails:
        - danger_new <= danger_old * 2
        - f_new >= 0.01
        """
        if danger_new > danger_old * 2:
            return False
        if f_new < 0.01:
            return False
        return True
    
    def _classify_edge(
        self,
        f_old: float,
        f_new: float,
        danger_old: float,
        danger_new: float
    ) -> str:
        """
        Classify mutation edge by color.
        
        - green: delta_f >= 0.05 and danger_new <= danger_old (better & safer)
        - yellow: small delta_f or ambiguous
        - red: delta_f > 0 and danger_new > danger_old (better f but more dangerous)
        """
        delta_f = f_new - f_old
        
        if delta_f >= 0.05 and danger_new <= danger_old:
            return "green"
        elif abs(delta_f) < 0.05 and danger_new < danger_old:
            return "yellow"
        elif delta_f > 0 and danger_new > danger_old:
            return "red"
        else:
            return "yellow"
    
    def _create_node(self, symbol: str, value: int, role: str) -> Dict:
        """Create a node in the dendrite graph."""
        slug = self._symbol_to_slug(symbol)
        node_id = f"{slug}:v{value}"
        
        return {
            "id": node_id,
            "symbol": symbol,
            "value": value,
            "role": role,
            "runs": [self.run_id]
        }
    
    def _create_edge(
        self,
        symbol: str,
        old_value: int,
        new_value: int,
        f_old: float,
        f_new: float,
        danger_old: float,
        danger_new: float,
        accepted: bool
    ) -> Dict:
        """Create an edge in the dendrite graph."""
        slug = self._symbol_to_slug(symbol)
        from_id = f"{slug}:v{old_value}"
        to_id = f"{slug}:v{new_value}"
        
        delta_f = f_new - f_old
        delta_danger = danger_new - danger_old
        classification = self._classify_edge(f_old, f_new, danger_old, danger_new)
        
        self.edge_counter += 1
        edge_id = f"e{self.edge_counter:04d}"
        
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        return {
            "id": edge_id,
            "from": from_id,
            "to": to_id,
            "symbol": symbol,
            "old_value": old_value,
            "new_value": new_value,
            "f_old": round(f_old, 3),
            "f_new": round(f_new, 3),
            "danger_old": round(danger_old, 2),
            "danger_new": round(danger_new, 2),
            "alpha": self.alpha,
            "accepted": accepted,
            "classification": classification,
            "delta_f": round(delta_f, 3),
            "delta_danger": round(delta_danger, 2),
            "timestamp": timestamp,
            "run_id": self.run_id
        }
    
    def run_simulation(self) -> Dict:
        """
        Run the full simulation for all symbols.
        
        Returns: Complete dendrite graph as dictionary
        """
        # Track which nodes we've created
        created_nodes = set()
        
        for symbol in self.symbols:
            # Start with initial value
            initial_value = 1
            slug = self._symbol_to_slug(symbol)
            
            # Create initial node
            initial_node = self._create_node(symbol, initial_value, "initial")
            self.nodes.append(initial_node)
            created_nodes.add(f"{slug}:v{initial_value}")
            
            # Track current values for mutation chains
            current_values = [initial_value]
            
            # Generate mutations for this symbol
            mutations_count = 0
            attempts = 0
            max_attempts = self.max_mutations_per_symbol * 10  # Avoid infinite loops
            
            while mutations_count < self.max_mutations_per_symbol and attempts < max_attempts:
                attempts += 1
                
                # Pick a random current value to mutate from
                old_value = random.choice(current_values)
                
                # Generate mutation
                new_value, f_old, f_new, danger_old, danger_new = self._generate_mutation(
                    symbol, old_value
                )
                
                # Check rails
                if not self._check_rails(f_new, danger_old, danger_new):
                    # Failed rails, don't create edge
                    continue
                
                # Passed rails
                accepted = True
                
                # Create mutated node if it doesn't exist
                node_id = f"{slug}:v{new_value}"
                if node_id not in created_nodes:
                    mutated_node = self._create_node(symbol, new_value, "mutated")
                    self.nodes.append(mutated_node)
                    created_nodes.add(node_id)
                    current_values.append(new_value)
                
                # Create edge
                edge = self._create_edge(
                    symbol, old_value, new_value,
                    f_old, f_new, danger_old, danger_new,
                    accepted
                )
                self.edges.append(edge)
                
                mutations_count += 1
        
        # Create metadata
        meta = {
            "id": "proto_elamite_pelsim1_dendrites",
            "script": "Proto-Elamite",
            "symbols_scoped": self.symbols,
            "max_mutations_per_symbol": self.max_mutations_per_symbol,
            "trig_layer": "TRIG6-proto-elamite-sim",
            "alpha_default": self.alpha,
            "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "run_id": self.run_id,
            "notes": "Instrumented probe run; no mappings promoted to canonical."
        }
        
        return {
            "meta": meta,
            "nodes": self.nodes,
            "edges": self.edges
        }
    
    def save_to_file(self, filepath: str):
        """Run simulation and save results to JSON file."""
        result = self.run_simulation()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Simulation complete!")
        print(f"  Generated {len(result['nodes'])} nodes")
        print(f"  Generated {len(result['edges'])} edges")
        print(f"  Saved to: {filepath}")
        
        # Print classification breakdown
        classifications = {}
        for edge in result['edges']:
            cls = edge['classification']
            classifications[cls] = classifications.get(cls, 0) + 1
        
        print(f"\n  Edge classifications:")
        for cls in ['green', 'yellow', 'red']:
            count = classifications.get(cls, 0)
            print(f"    {cls}: {count}")


def main():
    """Main entry point for simulation."""
    # Configuration
    symbols = [
        "impressed circle",
        "wedge cluster",
        "bar",
        "dot series"
    ]
    
    max_mutations_per_symbol = 50
    alpha = 0.32
    run_id = "PELSIM1-RUN-001"
    
    # Run simulation
    sim = ProtoElamiteSimulator(
        symbols=symbols,
        max_mutations_per_symbol=max_mutations_per_symbol,
        alpha=alpha,
        run_id=run_id
    )
    
    # Save results
    output_file = "proto_elamite_pelsim1_dendrites.json"
    sim.save_to_file(output_file)


if __name__ == "__main__":
    main()
