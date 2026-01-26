#!/usr/bin/env python3
"""
NEURO-36 Immune Dashboard

Loads the immune policy configuration and displays system status.
Classifies nodes, shows hardware candidates, and generates Sister Protocol reports.

Strategickhaos DAO LLC
Author: Domenic Gabriel Garza (Inventor)
"""

from __future__ import annotations

import yaml
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class Classification(Enum):
    RAIL = "RAIL"
    GATE = "GATE"
    SANDBOX = "SANDBOX"
    CHAMPION = "CHAMPION"
    CHAMPION_CANDIDATE = "CHAMPION_CANDIDATE"
    MUTANT = "MUTANT"
    CULL = "CULL"


@dataclass
class ComponentStatus:
    """Status of a single immune component"""
    id: int
    name: str
    bio_role: str
    theta_deg: float
    mapping_domain: str
    mapping_trait: str
    final_H: float
    final_fitness: float
    danger_rate: float
    classification: Classification
    execution_policy: str
    mutation_allowed: bool
    hardware_candidate: bool
    notes: str


class ImmuneDashboard:
    """
    Dashboard for monitoring NEURO-36 immune system status.
    """
    
    def __init__(self, policy_path: Optional[Path] = None):
        if policy_path is None:
            policy_path = Path(__file__).parent.parent / "config" / "neuro36_policy.yaml"
        
        try:
            with open(policy_path, 'r') as f:
                self.policy = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Policy configuration not found at: {policy_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in policy configuration: {e}")
        
        self.components = self._load_components()
    
    def _load_components(self) -> List[ComponentStatus]:
        """Load all components from policy"""
        components = []
        
        for comp in self.policy.get('components', []):
            status = ComponentStatus(
                id=comp['id'],
                name=comp['name'],
                bio_role=comp['bio_role'],
                theta_deg=comp['theta_deg'],
                mapping_domain=comp['mapping']['domain'],
                mapping_trait=comp['mapping']['trait'],
                final_H=comp['simulation']['final_H'],
                final_fitness=comp['simulation']['final_fitness'],
                danger_rate=comp['simulation']['danger_rate'],
                classification=Classification(comp['classification']),
                execution_policy=comp['policy']['execution'],
                mutation_allowed=comp['policy']['mutation_allowed'],
                hardware_candidate=comp['policy']['hardware_candidate'],
                notes=comp.get('notes', '')
            )
            components.append(status)
        
        return components
    
    def get_by_classification(self, classification: Classification) -> List[ComponentStatus]:
        """Get all components of a specific classification"""
        return [c for c in self.components if c.classification == classification]
    
    def get_hardware_candidates(self) -> List[ComponentStatus]:
        """Get all hardware synthesis candidates"""
        return [c for c in self.components if c.hardware_candidate]
    
    def get_threats(self) -> List[ComponentStatus]:
        """Get all threat nodes"""
        threat_ids = self.policy.get('sister_protocol', {}).get('threat_policy', {}).get('nodes', [])
        return [c for c in self.components if c.id in threat_ids]
    
    def print_status_table(self):
        """Print full status table"""
        print("\n" + "=" * 120)
        print("NEURO-36 IMMUNE DASHBOARD")
        print("=" * 120)
        print(f"{'ID':>3} | {'Name':<35} | {'Class':<12} | {'H':>5} | {'f':>5} | {'Danger':>6} | {'Mapping':<25} | {'HW':>3}")
        print("-" * 120)
        
        for c in sorted(self.components, key=lambda x: x.id):
            class_emoji = {
                Classification.RAIL: "🛤️",
                Classification.GATE: "🚪",
                Classification.SANDBOX: "🏖️",
                Classification.CHAMPION: "🏆",
                Classification.CHAMPION_CANDIDATE: "⭐",
                Classification.MUTANT: "🧟",
                Classification.CULL: "💀",
            }.get(c.classification, "❓")
            
            hw = "✓" if c.hardware_candidate else ""
            mapping = f"{c.mapping_domain}: {c.mapping_trait}"[:25]
            
            print(f"{c.id:>3} | {c.name:<35} | {class_emoji} {c.classification.value:<9} | {c.final_H:>5.2f} | {c.final_fitness:>5.3f} | {c.danger_rate:>6.2f} | {mapping:<25} | {hw:>3}")
        
        print("=" * 120)
    
    def print_classification_summary(self):
        """Print summary by classification"""
        print("\n" + "=" * 60)
        print("CLASSIFICATION SUMMARY")
        print("=" * 60)
        
        for classification in Classification:
            nodes = self.get_by_classification(classification)
            if nodes:
                print(f"\n{classification.value} ({len(nodes)} nodes):")
                for n in nodes:
                    print(f"  {n.id:2d}. {n.name}")
    
    def print_sister_protocol(self):
        """Print Sister Protocol execution rules"""
        print("\n" + "=" * 60)
        print("SISTER PROTOCOL EXECUTION RULES")
        print("=" * 60)
        
        sp = self.policy.get('sister_protocol', {})
        
        for policy_name in ['rail_policy', 'gate_policy', 'sandbox_policy', 'champion_policy', 'threat_policy']:
            policy = sp.get(policy_name, {})
            if policy:
                print(f"\n{policy_name.upper().replace('_', ' ')}")
                print(f"  Description: {policy.get('description', 'N/A')}")
                print(f"  Nodes: {policy.get('nodes', [])}")
                print("  Rules:")
                for rule in policy.get('rules', []):
                    print(f"    • {rule}")
    
    def print_hardware_candidates(self):
        """Print hardware synthesis candidates"""
        print("\n" + "=" * 60)
        print("HARDWARE SYNTHESIS CANDIDATES")
        print("=" * 60)
        
        hw = self.policy.get('hardware_candidates', {})
        
        for priority in ['priority_1', 'priority_2']:
            candidates = hw.get(priority, [])
            if candidates:
                print(f"\n{priority.upper().replace('_', ' ')}:")
                for c in candidates:
                    print(f"  {c['id']:2d}. {c['name']:<30} - {c['reason']}")
    
    def print_kernel_ligand(self):
        """Print kernel protein ligand analysis"""
        print("\n" + "=" * 60)
        print("KERNEL PROTEIN LIGAND: MACQGILP")
        print("=" * 60)
        
        kl = self.policy.get('kernel_ligand', {})
        
        print("\nAmino Acid Composition:")
        for aa, desc in kl.get('amino_acids', {}).items():
            print(f"  {aa}: {desc}")
        
        print("\nInstruction Biases:")
        for bias, desc in kl.get('instruction_biases', {}).items():
            print(f"  {bias}: {desc}")
        
        print("\nDefault Profile:")
        print(kl.get('default_profile', 'N/A'))
    
    def print_danger_zones(self):
        """Print nodes at TRIG6 danger zones"""
        print("\n" + "=" * 60)
        print("TRIG6 DANGER ZONES")
        print("=" * 60)
        
        # Danger zones are at π/2 (90°) and 3π/2 (270°)
        # Use tolerance for floating point comparison
        danger_nodes = [c for c in self.components if abs(c.theta_deg - 90) < 1e-6 or abs(c.theta_deg - 270) < 1e-6]
        
        print("\nNodes at tan(θ) = ∞:")
        for n in danger_nodes:
            print(f"  {n.id:2d}. {n.name:<30} @ θ={n.theta_deg}° (danger_rate={n.danger_rate:.2f})")
        
        # Also show high danger rate nodes
        high_danger = [c for c in self.components if c.danger_rate > 0.5]
        if high_danger:
            print("\nHigh Danger Rate Nodes (>50%):")
            for n in high_danger:
                print(f"  {n.id:2d}. {n.name:<30} danger_rate={n.danger_rate:.2f}")
    
    def export_json(self, output_path: Path):
        """Export dashboard data to JSON"""
        data = {
            "metadata": self.policy.get('metadata', {}),
            "components": [
                {
                    "id": c.id,
                    "name": c.name,
                    "bio_role": c.bio_role,
                    "theta_deg": c.theta_deg,
                    "mapping": f"{c.mapping_domain}: {c.mapping_trait}",
                    "H": c.final_H,
                    "fitness": c.final_fitness,
                    "danger_rate": c.danger_rate,
                    "classification": c.classification.value,
                    "execution": c.execution_policy,
                    "mutation_allowed": c.mutation_allowed,
                    "hardware_candidate": c.hardware_candidate,
                }
                for c in self.components
            ],
            "summary": {
                "total_nodes": len(self.components),
                "rails": len(self.get_by_classification(Classification.RAIL)),
                "gates": len(self.get_by_classification(Classification.GATE)),
                "sandboxes": len(self.get_by_classification(Classification.SANDBOX)),
                "champions": len(self.get_by_classification(Classification.CHAMPION)),
                "hardware_candidates": len(self.get_hardware_candidates()),
                "avg_H": sum(c.final_H for c in self.components) / len(self.components) if self.components else 0,
                "avg_fitness": sum(c.final_fitness for c in self.components) / len(self.components) if self.components else 0,
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n💾 Dashboard exported to: {output_path}")


def main():
    """Run immune dashboard"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     NEURO-36 IMMUNE DASHBOARD                                 ║
    ║     Sister Protocol Status Monitor                            ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    dashboard = ImmuneDashboard()
    
    # Print all reports
    dashboard.print_status_table()
    dashboard.print_classification_summary()
    dashboard.print_danger_zones()
    dashboard.print_hardware_candidates()
    dashboard.print_sister_protocol()
    dashboard.print_kernel_ligand()
    
    # Export
    output_path = Path(__file__).parent.parent / "artifacts" / "immune_dashboard.json"
    output_path.parent.mkdir(exist_ok=True)
    dashboard.export_json(output_path)


if __name__ == "__main__":
    main()
