#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    NEURO-36 IMMUNE DASHBOARD & CLASSIFICATION SYSTEM
    
    Analyzes the 36-node immune system architecture with TRIG6 geometry
    and Physarum DNA evolution to classify nodes and generate policy rules.
    
    Classification System:
    - RAIL: Chronic danger + high fitness (non-negotiable safety rails)
    - GATE: High H + mid fitness (structural holders with exploration)
    - SANDBOX: Low fitness/H (exploration zones, never trusted with core)
    - CHAMPION: High fitness (f >= 0.8)
    - MUTANT: Low fitness (f < 0.3)
    - CULL: Zero heritability (H == 0)
    - EVOLVING: Middle range (default state)
    
    Homeostatic Protein: MACQGILP
    DNA: ATGGCATGCCAAGGTATCTTACCG
    RNA: AUGGCAUGCCAAGGUAUCUUACCG
    
    The init process - everything else is deviations around this attractor.
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import sys
from dataclasses import dataclass
from typing import List, Dict, Tuple
from pathlib import Path


@dataclass
class ComponentClassification:
    """Classification result for an immune component"""
    component_id: int
    component_name: str
    ecosystem_mapping: str
    final_status: str
    final_dna: str
    final_rna: str
    final_protein: str
    final_fitness: float
    final_H: float
    danger_count: int
    total_checkpoints: int
    classification: str
    os_role: str
    policy_guidance: str


class ImmuneClassifier:
    """Classifies immune components based on NEURO-36 metrics"""
    
    # Thresholds for classification
    CHAMPION_FITNESS = 0.8
    MUTANT_FITNESS = 0.3
    HIGH_FITNESS = 0.45
    MID_FITNESS_MIN = 0.35
    MID_FITNESS_MAX = 0.50
    HIGH_H = 0.5
    LOW_H = 0.3
    CHRONIC_DANGER_RATIO = 0.8  # 80% of checkpoints
    
    KERNEL_PROTEIN = "MACQGILP"
    KERNEL_DNA = "ATGGCATGCCAAGGTATCTTACCG"
    
    @staticmethod
    def classify_component(comp: Dict) -> ComponentClassification:
        """Classify a single component based on its metrics"""
        
        # Extract basic info
        comp_id = comp['component_id']
        name = comp['component_name']
        mapping = comp['ecosystem_mapping']
        status = comp['final_status']
        dna = comp['final_dna']
        rna = comp['final_rna']
        protein = comp['final_protein']
        fitness = comp['final_fitness']
        H = comp['final_H']
        
        # Count dangers
        summaries = comp.get('summaries', [])
        danger_count = sum(1 for s in summaries if s.get('danger', False))
        total_checkpoints = len(summaries)
        danger_ratio = danger_count / total_checkpoints if total_checkpoints > 0 else 0
        
        # Classification logic
        classification = "EVOLVING"  # Default
        os_role = "General Process"
        policy = "Standard exploration and mutation allowed"
        
        # RAIL: Chronic danger with high fitness
        if danger_ratio >= ImmuneClassifier.CHRONIC_DANGER_RATIO and fitness >= ImmuneClassifier.HIGH_FITNESS:
            classification = "RAIL"
            os_role = "Hard-wired Reflex Arc / Safety Rail"
            policy = "DNA locked, no mutations allowed, high priority watchdog, tight TRIG6 thresholds"
        
        # CHAMPION: Exceptional fitness
        elif fitness >= ImmuneClassifier.CHAMPION_FITNESS:
            classification = "CHAMPION"
            os_role = "High-Performance Core Service"
            policy = "Preserve and optimize, increase resource allocation, fast-path eligible"
        
        # MUTANT: Very low fitness
        elif fitness < ImmuneClassifier.MUTANT_FITNESS:
            classification = "MUTANT"
            os_role = "Unstable / Experimental Process"
            policy = "Sandbox isolation, no core access, high mutation allowed, candidate for reset"
        
        # CULL: Zero heritability
        elif H == 0:
            classification = "CULL"
            os_role = "Failed/Dead Process"
            policy = "Mark for cleanup, no resource allocation, consider reset to kernel"
        
        # GATE: High H with mid fitness
        elif H >= ImmuneClassifier.HIGH_H and ImmuneClassifier.MID_FITNESS_MIN <= fitness <= ImmuneClassifier.MID_FITNESS_MAX:
            classification = "GATE"
            os_role = "Structural Holder / Gateway"
            policy = "Maintain wiring, controlled exploration, moderate mutation rate, buffer zone"
        
        # SANDBOX: Low fitness and low H
        elif fitness < ImmuneClassifier.MID_FITNESS_MAX and H < ImmuneClassifier.LOW_H:
            classification = "SANDBOX"
            os_role = "Exploration Zone / Peripheral Interface"
            policy = "Wild exploration allowed, never trusted with core flows, high mutation rate"
        
        # Kernel protein detection
        if protein == ImmuneClassifier.KERNEL_PROTEIN:
            os_role += " [KERNEL PROTEIN - Init Process]"
            if classification == "EVOLVING":
                policy = "Homeostatic attractor - system defaults to this state"
        
        return ComponentClassification(
            component_id=comp_id,
            component_name=name,
            ecosystem_mapping=mapping,
            final_status=status,
            final_dna=dna,
            final_rna=rna,
            final_protein=protein,
            final_fitness=fitness,
            final_H=H,
            danger_count=danger_count,
            total_checkpoints=total_checkpoints,
            classification=classification,
            os_role=os_role,
            policy_guidance=policy
        )
    
    @staticmethod
    def analyze_protein_convergence(components: List[Dict]) -> Dict:
        """Analyze how many components converge to kernel protein"""
        kernel_count = 0
        protein_freq = {}
        
        for comp in components:
            protein = comp['final_protein']
            if protein == ImmuneClassifier.KERNEL_PROTEIN:
                kernel_count += 1
            protein_freq[protein] = protein_freq.get(protein, 0) + 1
        
        return {
            'kernel_protein': ImmuneClassifier.KERNEL_PROTEIN,
            'kernel_dna': ImmuneClassifier.KERNEL_DNA,
            'convergence_count': kernel_count,
            'convergence_ratio': kernel_count / len(components),
            'unique_proteins': len(protein_freq),
            'protein_frequency': protein_freq
        }


class ImmuneDashboard:
    """Generate comprehensive immune system dashboard"""
    
    def __init__(self, json_path: str):
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        
        self.metadata = self.data.get('metadata', {})
        self.components = self.data.get('components', [])
        self.classifications = []
        
    def classify_all(self):
        """Classify all 36 components"""
        for comp in self.components:
            classification = ImmuneClassifier.classify_component(comp)
            self.classifications.append(classification)
        
    def generate_summary_table(self) -> str:
        """Generate markdown table of all components"""
        lines = []
        lines.append("## NEURO-36 Immune System Dashboard")
        lines.append("")
        lines.append("| ID | Component | Class | Fitness | H | Dangers | Protein | OS Role |")
        lines.append("|----|-----------|-------|---------|---|---------|---------|---------|")
        
        for c in self.classifications:
            danger_str = f"{c.danger_count}/{c.total_checkpoints}"
            lines.append(
                f"| {c.component_id:2d} | {c.component_name[:25]:25s} | "
                f"{c.classification:8s} | {c.final_fitness:.3f} | {c.final_H:.2f} | "
                f"{danger_str:5s} | {c.final_protein[:8]:8s} | {c.os_role[:40]:40s} |"
            )
        
        return "\n".join(lines)
    
    def generate_classification_stats(self) -> str:
        """Generate statistics by classification"""
        stats = {}
        for c in self.classifications:
            stats[c.classification] = stats.get(c.classification, 0) + 1
        
        lines = []
        lines.append("## Classification Distribution")
        lines.append("")
        for cls, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- **{cls}**: {count} nodes")
        
        return "\n".join(lines)
    
    def generate_policy_guide(self) -> str:
        """Generate Sister Protocol policy guidance"""
        lines = []
        lines.append("## Sister Protocol Policy Guidance")
        lines.append("")
        
        # Group by classification
        by_class = {}
        for c in self.classifications:
            if c.classification not in by_class:
                by_class[c.classification] = []
            by_class[c.classification].append(c)
        
        for cls in ['RAIL', 'CHAMPION', 'GATE', 'EVOLVING', 'SANDBOX', 'MUTANT', 'CULL']:
            if cls not in by_class:
                continue
            
            nodes = by_class[cls]
            lines.append(f"### {cls} Nodes ({len(nodes)} total)")
            lines.append("")
            
            if nodes:
                lines.append(f"**Policy**: {nodes[0].policy_guidance}")
                lines.append("")
                lines.append("**Members**:")
                for node in nodes:
                    lines.append(f"- {node.component_name} (ID {node.component_id}): "
                               f"f={node.final_fitness:.3f}, H={node.final_H:.2f}, "
                               f"dangers={node.danger_count}/{node.total_checkpoints}")
                lines.append("")
        
        return "\n".join(lines)
    
    def generate_homeostatic_analysis(self) -> str:
        """Analyze the homeostatic protein convergence"""
        conv_data = ImmuneClassifier.analyze_protein_convergence(self.components)
        
        lines = []
        lines.append("## Homeostatic Protein Analysis")
        lines.append("")
        lines.append(f"**Kernel Protein**: {conv_data['kernel_protein']}")
        lines.append(f"**Kernel DNA**: {conv_data['kernel_dna']}")
        lines.append(f"**Convergence**: {conv_data['convergence_count']}/36 nodes "
                    f"({conv_data['convergence_ratio']*100:.1f}%) returned to kernel protein")
        lines.append("")
        lines.append("This is your **init process** - the ground state the NEURO-36 system falls back to.")
        lines.append("")
        
        # List nodes that converged
        kernel_nodes = [c for c in self.classifications 
                       if c.final_protein == conv_data['kernel_protein']]
        if kernel_nodes:
            lines.append("### Nodes at Kernel State:")
            for node in kernel_nodes:
                lines.append(f"- {node.component_name}: fitness={node.final_fitness:.3f}, H={node.final_H:.2f}")
            lines.append("")
        
        # Top proteins
        lines.append("### Protein Diversity:")
        sorted_proteins = sorted(conv_data['protein_frequency'].items(), 
                                key=lambda x: x[1], reverse=True)[:10]
        for protein, count in sorted_proteins:
            lines.append(f"- {protein}: {count} nodes")
        
        return "\n".join(lines)
    
    def generate_amino_acid_mapping(self) -> str:
        """Generate protein-to-instruction mapping"""
        lines = []
        lines.append("## Protein as Instruction Ligand")
        lines.append("")
        lines.append("### MACQGILP - Baseline Execution Profile")
        lines.append("")
        
        aa_properties = {
            'M': ('Methionine', 'Hydrophobic', 'Start codon - initialization'),
            'A': ('Alanine', 'Hydrophobic', 'Small, flexible - basic operations'),
            'C': ('Cysteine', 'Polar', 'Disulfide bonds - state locking'),
            'Q': ('Glutamine', 'Polar', 'Hydrogen bonding - connection forming'),
            'G': ('Glycine', 'Special', 'Most flexible - adaptive routing'),
            'I': ('Isoleucine', 'Hydrophobic', 'Branched - decision points'),
            'L': ('Leucine', 'Hydrophobic', 'Common - standard processing'),
            'P': ('Proline', 'Special', 'Rigid - structural enforcement')
        }
        
        lines.append("| AA | Name | Property | SAGCO Behavior Bias |")
        lines.append("|----|------|----------|---------------------|")
        
        for aa in 'MACQGILP':
            if aa in aa_properties:
                name, prop, behavior = aa_properties[aa]
                lines.append(f"| {aa} | {name} | {prop} | {behavior} |")
        
        lines.append("")
        lines.append("**Kernel Ligand Profile**:")
        lines.append("- **Hydrophobic cluster (M, A, I, L)**: Prefer local, cache-like behaviors")
        lines.append("- **Polar cluster (C, Q)**: Enable cross-node signaling, state binding")
        lines.append("- **Special residues (G, P)**: Adaptive routing + structural constraints")
        lines.append("")
        lines.append("Evolved proteins = evolved micro-policies for instruction execution.")
        
        return "\n".join(lines)
    
    def generate_full_report(self) -> str:
        """Generate complete dashboard report"""
        lines = []
        lines.append("# NEURO-36 Immune System Architecture Report")
        lines.append("")
        lines.append("**Generated from**: physarum_evolution_36.json")
        lines.append(f"**Generations**: {self.metadata.get('generations', 'N/A')}")
        lines.append(f"**Base Mutation Rate**: {self.metadata.get('base_mutation_rate', 'N/A')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        lines.append(self.generate_homeostatic_analysis())
        lines.append("")
        lines.append("---")
        lines.append("")
        
        lines.append(self.generate_summary_table())
        lines.append("")
        lines.append("---")
        lines.append("")
        
        lines.append(self.generate_classification_stats())
        lines.append("")
        lines.append("---")
        lines.append("")
        
        lines.append(self.generate_policy_guide())
        lines.append("")
        lines.append("---")
        lines.append("")
        
        lines.append(self.generate_amino_acid_mapping())
        
        return "\n".join(lines)


def main():
    """Main entry point"""
    json_path = Path(__file__).parent / 'physarum_evolution_36.json'
    
    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)
    
    print("Loading NEURO-36 data...")
    dashboard = ImmuneDashboard(str(json_path))
    
    print("Classifying 36 immune components...")
    dashboard.classify_all()
    
    print("Generating report...")
    report = dashboard.generate_full_report()
    
    # Write to file
    output_path = Path(__file__).parent / 'NEURO36_IMMUNE_DASHBOARD.md'
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\n✓ Dashboard generated: {output_path}")
    print(f"\n{report}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
