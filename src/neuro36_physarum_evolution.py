#!/usr/bin/env python3
"""
NEURO-36 Physarum DNA Evolution Layer

Extends the immune system simulation with:
- DNA → RNA → Protein translation
- 50-generation evolution per component
- Physarum flow-based adaptation (H conductivity)
- TRIG6 fitness gating

Based on Dom's Biological-Computational Equivalence Map v1.0

Strategickhaos DAO LLC
Author: Domenic Gabriel Garza (Inventor)
"""

from __future__ import annotations

import math
import random
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from enum import Enum

# Codon table (standard genetic code)
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

# Ecosystem mappings for the 36 components
ECOSYSTEM_MAPPINGS = [
    "TRIG6 Trait: Resonance Gate",
    "Compiler Pass: Parsing",
    "OS Module: Wave Core",
    "TRIG6 Trait: Drift Detector",
    "Compiler Pass: Codegen",
    "OS Module: Scheduler",
    "TRIG6 Trait: Noise Filter",
    "Compiler Pass: AST Building",
    "OS Module: Memory Manager",
    "TRIG6 Trait: Equilibrium Balancer",
    "Compiler Pass: IR Generation",
    "OS Module: ALU Agent",
    "TRIG6 Trait: Danger Reset",
    "Compiler Pass: Proof Gate",
    "OS Module: Control Unit",
    "TRIG6 Trait: Heritability Boost",
    "Compiler Pass: Lexer",
    "OS Module: Entanglement Core",
    "TRIG6 Trait: Flow Adapter",
    "Compiler Pass: Semantic Analysis",
    "OS Module: Register Memory",
    "TRIG6 Trait: Mutation Engine",
    "Compiler Pass: Optimization",
    "OS Module: Cognitive Mapping",
    "TRIG6 Trait: Pivot Shifter",
    "Compiler Pass: Linker",
    "OS Module: Quantum Gate Array",
    "TRIG6 Trait: Bio-Sim Integrator",
    "Compiler Pass: Runtime Check",
    "OS Module: Processor Emulation",
    "TRIG6 Trait: Nervisticism Model",
    "Compiler Pass: Debug Gate",
    "OS Module: Soul Execution",
    "TRIG6 Trait: Life Protocol",
    "Compiler Pass: Prior Eval",
    "OS Module: Physarum Evolver",
]

# 36 immune components from mind maps
IMMUNE_COMPONENTS = [
    "Skin",
    "Sebum",
    "Anti-microbial elements",
    "Probiotics",
    "Holistic organ nose mouth throat",
    "Inheleten exhibition",
    "Harmonious Coexistens Symbosis",
    "Pathogens",
    "Mucus membrane",
    "Coughing",
    "Innate Immune System",
    "Adaptive Immune System",
    "Cilia",
    "Oral cavity",
    "Lucoside",
    "Neutrophil",
    "Bone marrow",
    "Immune cell",
    "Blood stream",
    "Weak adhesion",
    "Strong adhesion",
    "Receptor",
    "Asymmetric",
    "Synthe cells",
    "Division and maturation of neutrophils",
    "Nucleosides",
    "Progenitor cell",
    "Stem cells",
    "Connective Tissue",
    "Bacteria",
    "Toxins",
    "Nutritional",
    "Tumor Necrosis",
    "Antigens",
    "Thymus",
    "Transition/Run/Gain/Advance/Set back",
]


def dna_to_rna(dna: str) -> str:
    """Transcribe DNA to RNA (T → U)"""
    return dna.replace('T', 'U')


def rna_to_protein(rna: str) -> str:
    """Translate RNA to protein using codon table"""
    # Convert RNA back to DNA codons for lookup
    dna_for_lookup = rna.replace('U', 'T')
    protein = []
    # Process all complete codons (length must be divisible by 3)
    for i in range(0, len(dna_for_lookup), 3):
        if i + 3 > len(dna_for_lookup):
            break  # Incomplete codon at end
        codon = dna_for_lookup[i:i+3]
        if codon in CODON_TABLE:
            aa = CODON_TABLE[codon]
            if aa == '*':  # Stop codon
                break
            protein.append(aa)
    return ''.join(protein)


def gc_content(dna: str) -> float:
    """Calculate GC content (proxy for resonance/coherence)"""
    if len(dna) == 0:
        return 0.0
    gc = sum(1 for base in dna if base in 'GC')
    return gc / len(dna)


def mutate_dna(dna: str, mutation_rate: float) -> str:
    """Mutate DNA sequence"""
    bases = ['A', 'T', 'G', 'C']
    result = list(dna)
    for i in range(len(result)):
        if random.random() < mutation_rate:
            # Point mutation to different base
            current = result[i]
            options = [b for b in bases if b != current]
            result[i] = random.choice(options)
    return ''.join(result)


@dataclass
class PhysarumState:
    """
    Physarum-inspired state for a single immune component.
    
    H (heritability/conductivity): How well this correlation propagates
    Flow: Sum of fitness from activations
    """
    H: float = 0.5          # Heritability/conductivity [0, 1]
    flow: float = 0.0       # Accumulated flow
    decay_rate: float = 0.9 # Decay per unused generation
    neighbor_avg: float = 0.5  # Average neighbor conductivity


@dataclass
class EvolutionState:
    """State for one immune component's evolution"""
    component_id: int
    component_name: str
    ecosystem_mapping: str
    
    # DNA state
    dna: str
    rna: str = ""
    protein: str = ""
    
    # TRIG6 metrics
    theta: float = 0.0
    resonance: float = 0.5
    drift: float = 0.0
    noise: float = 0.0
    fitness: float = 0.5
    danger: bool = False
    
    # Physarum state
    physarum: PhysarumState = field(default_factory=PhysarumState)
    
    # History
    generation: int = 0
    history: List[Dict] = field(default_factory=list)
    
    # Constants
    TARGET_PROTEIN_LENGTH: int = 8  # Optimal protein length for fitness calculation
    
    def __post_init__(self):
        self.rna = dna_to_rna(self.dna)
        self.protein = rna_to_protein(self.rna)
    
    def compute_fitness(self) -> float:
        """
        TRIG6 fitness: f = R × (1-D) × (1-N) × eq
        R derived from GC content (coherence proxy)
        """
        self.resonance = gc_content(self.dna)
        eq = 1.0 - abs(len(self.protein) - self.TARGET_PROTEIN_LENGTH) / self.TARGET_PROTEIN_LENGTH
        eq = max(0.0, min(1.0, eq))
        
        self.fitness = self.resonance * (1 - self.drift) * (1 - self.noise) * eq
        return self.fitness
    
    def check_danger(self, tan_limit: float = 10.0) -> bool:
        """Check TRIG6 danger zone"""
        tan_val = abs(math.tan(self.theta)) if abs(math.cos(self.theta)) > 0.01 else 100.0
        self.danger = tan_val > tan_limit or self.fitness < 0.3
        return self.danger
    
    def update_physarum(self, flow_contribution: float):
        """
        Physarum-style update:
        - High flow reinforces H
        - Low flow decays H
        """
        self.physarum.flow += flow_contribution
        
        if flow_contribution > 0.4:
            # High fitness - reinforce conductivity
            self.physarum.H = min(1.0, self.physarum.H + 0.05 * flow_contribution)
        else:
            # Low fitness - decay
            self.physarum.H = max(0.0, self.physarum.H * self.physarum.decay_rate)
    
    def snapshot(self) -> Dict:
        """Create snapshot of current state"""
        return {
            "generation": self.generation,
            "dna": self.dna,
            "rna": self.rna,
            "protein": self.protein,
            "fitness": round(self.fitness, 3),
            "H": round(self.physarum.H, 2),
            "danger": self.danger,
            "resonance": round(self.resonance, 3),
            "drift": round(self.drift, 3),
            "noise": round(self.noise, 3),
        }


class PhysarumEvolver:
    """
    Runs 50-generation DNA evolution for each of 36 immune components.
    
    Integrates:
    - DNA → RNA → Protein central dogma
    - TRIG6 fitness gating
    - Physarum flow-based adaptation
    """
    
    INITIAL_DNA = "ATGGCATGCCAAGGTATCTTACCG"  # 24bp starting sequence
    GENERATIONS = 50
    BASE_MUTATION_RATE = 0.01
    DANGER_THRESHOLD = 10.0
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.components: List[EvolutionState] = []
        self.results: List[Dict] = []
        
        # Initialize all 36 components
        for i in range(36):
            state = EvolutionState(
                component_id=i + 1,
                component_name=IMMUNE_COMPONENTS[i],
                ecosystem_mapping=ECOSYSTEM_MAPPINGS[i],
                dna=self.INITIAL_DNA,
                theta=(i / 36) * 2 * math.pi,  # Distribute around circle
            )
            self.components.append(state)
    
    def evolve_component(self, state: EvolutionState) -> Dict:
        """
        Run 50 generations of evolution for one component.
        """
        summaries = []
        
        for gen in range(self.GENERATIONS):
            state.generation = gen
            
            # Simulate episode flow (in real system, from actual logs)
            episode_flow = random.uniform(0.3, 0.7)
            
            # Add some drift and noise based on generation
            state.drift = min(1.0, state.drift + random.uniform(-0.02, 0.05))
            state.noise = min(1.0, state.noise + random.uniform(-0.01, 0.03))
            state.drift = max(0.0, state.drift)
            state.noise = max(0.0, state.noise)
            
            # Compute fitness
            fitness = state.compute_fitness()
            
            # Check danger
            danger = state.check_danger(self.DANGER_THRESHOLD)
            
            if danger:
                # Reset on danger (immune recovery simulation)
                state.dna = self.INITIAL_DNA
                state.physarum.H = 0.5
                state.drift = 0.0
                state.noise = 0.0
            else:
                # Safe - allow mutation
                mutation_rate = self.BASE_MUTATION_RATE * (1 - fitness)
                state.dna = mutate_dna(state.dna, mutation_rate)
            
            # Update RNA and protein
            state.rna = dna_to_rna(state.dna)
            state.protein = rna_to_protein(state.rna)
            
            # Physarum flow update
            state.update_physarum(fitness)
            
            # Record every 10 generations + final
            if gen % 10 == 0 or gen == self.GENERATIONS - 1:
                summaries.append(state.snapshot())
            
            state.history.append(state.snapshot())
        
        # Determine final status
        final_status = "EVOLVING" if state.physarum.H > 0 else "CULL"
        if state.fitness >= 0.8:
            final_status = "CHAMPION"
        elif state.fitness < 0.3:
            final_status = "MUTANT"
        
        return {
            "component_id": state.component_id,
            "component_name": state.component_name,
            "ecosystem_mapping": state.ecosystem_mapping,
            "final_status": final_status,
            "final_dna": state.dna,
            "final_rna": state.rna,
            "final_protein": state.protein,
            "final_fitness": round(state.fitness, 3),
            "final_H": round(state.physarum.H, 2),
            "summaries": summaries,
        }
    
    def run_all(self) -> List[Dict]:
        """Run evolution for all 36 components"""
        print("=" * 80)
        print("NEURO-36 Physarum DNA Evolution")
        print("50 generations per component, TRIG6 fitness gating")
        print("=" * 80)
        
        self.results = []
        
        for state in self.components:
            result = self.evolve_component(state)
            self.results.append(result)
            
            # Print summary
            status_emoji = {
                "CHAMPION": "🏆",
                "EVOLVING": "🧬",
                "MUTANT": "⚠️",
                "CULL": "💀",
            }.get(result["final_status"], "❓")
            
            print(f"{result['component_id']:2d}. {result['component_name']:<35} "
                  f"→ {result['ecosystem_mapping']:<30} | "
                  f"f={result['final_fitness']:.3f} H={result['final_H']:.2f} "
                  f"{status_emoji} {result['final_status']}")
        
        # Summary statistics
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        
        avg_fitness = sum(r["final_fitness"] for r in self.results) / len(self.results)
        avg_H = sum(r["final_H"] for r in self.results) / len(self.results)
        
        status_counts = {}
        for r in self.results:
            status = r["final_status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"Average Fitness: {avg_fitness:.3f}")
        print(f"Average H (Conductivity): {avg_H:.2f}")
        print(f"Status Distribution: {status_counts}")
        
        return self.results
    
    def export_results(self, output_path: Path) -> None:
        """Export results to JSON"""
        output_path.parent.mkdir(exist_ok=True)
        
        export_data = {
            "metadata": {
                "generations": self.GENERATIONS,
                "base_mutation_rate": self.BASE_MUTATION_RATE,
                "initial_dna": self.INITIAL_DNA,
                "danger_threshold": self.DANGER_THRESHOLD,
            },
            "components": self.results,
            "summary": {
                "avg_fitness": sum(r["final_fitness"] for r in self.results) / len(self.results),
                "avg_H": sum(r["final_H"] for r in self.results) / len(self.results),
                "status_counts": {},
            }
        }
        
        for r in self.results:
            status = r["final_status"]
            export_data["summary"]["status_counts"][status] = \
                export_data["summary"]["status_counts"].get(status, 0) + 1
        
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n💾 Results exported to: {output_path}")


def sweep_all_nodes_isolated():
    """
    Sweep all 36 nodes in isolation to measure individual TRIG6 signatures.
    """
    print("\n" + "=" * 80)
    print("36-NODE ISOLATION SWEEP")
    print("=" * 80)
    
    # Import the existing NEURO-36 system
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from neuro36_immune import ImmuneSystem, Trig6State
        
        results = []
        
        for i in range(36):
            # Fresh system for each node
            system = ImmuneSystem()
            system.state = Trig6State()
            system.state.resonance = 0.8
            system.state.drift = 0.0
            system.state.noise = 0.0
            
            result = system.activate_node(i + 1)
            results.append(result)
            
            danger_str = "⚠️" if result.get("is_danger_zone", False) else ""
            print(f"{result['node_id']:2d}. {result['node_name']:<30} "
                  f"Δf={result['delta_fitness']:+.3f} "
                  f"R={result['state']['R']:.2f} D={result['state']['D']:.2f} "
                  f"N={result['state']['N']:.2f} {danger_str}")
        
        return results
    except ImportError as e:
        print(f"Note: Could not import neuro36_immune: {e}")
        print("Running standalone Physarum evolution only.")
        return []


def main():
    """Run full Physarum DNA evolution simulation"""
    
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║     DOM Biological-Computational Equivalence Map v1.0                     ║
    ║     NEURO-36 Physarum DNA Evolution Layer                                 ║
    ║     50 Generations × 36 Components = 1,800 Evolution Steps                ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run isolation sweep first
    sweep_results = sweep_all_nodes_isolated()
    
    # Run Physarum DNA evolution
    evolver = PhysarumEvolver(seed=42)
    results = evolver.run_all()
    
    # Export combined results
    output_path = Path(__file__).parent.parent / "artifacts" / "physarum_evolution_36.json"
    evolver.export_results(output_path)
    
    # Also export sweep if available
    if sweep_results:
        sweep_path = Path(__file__).parent.parent / "artifacts" / "neuro36_sweep.json"
        with open(sweep_path, "w") as f:
            json.dump({"sweep_results": sweep_results}, f, indent=2)
        print(f"💾 Sweep results exported to: {sweep_path}")


if __name__ == "__main__":
    main()
