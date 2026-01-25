#!/usr/bin/env python3
"""
dna_codon_registry.py

SAGCO-OS DNA-Based Evolution Tracking System

Implements biological-metaphor encoding for software evolution with codon
registry, dependency ordering, and mutation logging.

Part of: Self-Amplifying Generative Cognitive Operating System
DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1-LOM1-TRIG6-WAVE1-HYBRID1-NEURO1-OPS1-BOOT1

Copyright (c) 2026 Strategickhaos DAO LLC
Inventor: Dom Garza
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


class MutationType(Enum):
    """Types of mutations"""
    APPEND = "append"
    INCREMENT = "increment"
    INSERT = "insert"
    DELETE = "delete"


@dataclass
class Codon:
    """Codon representing a software subsystem with version"""
    code: str
    subsystem: str
    version: str
    position: int = 0
    dependencies: List[str] = field(default_factory=list)
    description: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.code}"


@dataclass
class Mutation:
    """Mutation record for evolution tracking"""
    mutation_type: MutationType
    codon_code: str
    old_version: Optional[str]
    new_version: str
    timestamp: float
    author: str
    justification: str
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['mutation_type'] = self.mutation_type.value
        return data


class DNAStrand:
    """
    DNA strand representing software evolution
    
    Implements Claim 2: Software evolution tracking using biological metaphor
    """
    
    # Mandatory start codon
    START_CODON = "ATG"
    
    def __init__(self, organism: str = "SAGCO"):
        """
        Initialize DNA strand
        
        Args:
            organism: Organism identifier (default: SAGCO)
        """
        self.organism = organism
        self.codons: List[Codon] = []
        self.mutation_history: List[Mutation] = []
        
        # Add mandatory start codon
        self._add_start_codon()
    
    def _add_start_codon(self):
        """Add mandatory ATG start codon"""
        start = Codon(
            code=self.START_CODON,
            subsystem="Start codon",
            version="Required",
            position=0,
            description="Mandatory start codon (analogous to biological ATG)"
        )
        self.codons.append(start)
    
    def add_codon(self, codon: Codon, author: str, justification: str) -> bool:
        """
        Append codon to end of strand
        
        Implements Claim 2(c)(i): Mutation module - append operation
        
        Args:
            codon: Codon to add
            author: Author of mutation
            justification: Justification for mutation
            
        Returns:
            True if successful, False otherwise
        """
        # Validate dependencies
        if not self._validate_dependencies(codon):
            return False
        
        # Set position
        codon.position = len(self.codons)
        
        # Add codon
        self.codons.append(codon)
        
        # Log mutation
        mutation = Mutation(
            mutation_type=MutationType.APPEND,
            codon_code=codon.code,
            old_version=None,
            new_version=codon.version,
            timestamp=time.time(),
            author=author,
            justification=justification,
            metadata={"position": codon.position}
        )
        self.mutation_history.append(mutation)
        
        return True
    
    def increment_version(self, codon_code: str, new_version: str,
                         author: str, justification: str) -> bool:
        """
        Increment version of existing codon
        
        Implements Claim 2(c)(i): Mutation module - increment operation
        
        Args:
            codon_code: Code of codon to update
            new_version: New version string
            author: Author of mutation
            justification: Justification for mutation
            
        Returns:
            True if successful, False otherwise
        """
        # Find codon
        codon = self._find_codon(codon_code)
        if codon is None:
            return False
        
        old_version = codon.version
        codon.version = new_version
        
        # Log mutation
        mutation = Mutation(
            mutation_type=MutationType.INCREMENT,
            codon_code=codon_code,
            old_version=old_version,
            new_version=new_version,
            timestamp=time.time(),
            author=author,
            justification=justification
        )
        self.mutation_history.append(mutation)
        
        return True
    
    def insert_codon(self, codon: Codon, position: int,
                    author: str, justification: str) -> bool:
        """
        Insert codon at specific position (respecting dependencies)
        
        Implements Claim 2(c)(i): Mutation module - insert operation
        Implements Claim 2(c)(ii): Enforce dependency ordering
        
        Args:
            codon: Codon to insert
            position: Position to insert at (must be > 0 to preserve ATG)
            author: Author of mutation
            justification: Justification for mutation
            
        Returns:
            True if successful, False otherwise
        """
        # Cannot insert before start codon
        if position <= 0:
            return False
        
        # Validate dependencies
        if not self._validate_dependencies(codon, position):
            return False
        
        # Insert codon
        codon.position = position
        self.codons.insert(position, codon)
        
        # Update positions of subsequent codons
        for i in range(position + 1, len(self.codons)):
            self.codons[i].position = i
        
        # Log mutation
        mutation = Mutation(
            mutation_type=MutationType.INSERT,
            codon_code=codon.code,
            old_version=None,
            new_version=codon.version,
            timestamp=time.time(),
            author=author,
            justification=justification,
            metadata={"position": position}
        )
        self.mutation_history.append(mutation)
        
        return True
    
    def _find_codon(self, codon_code: str) -> Optional[Codon]:
        """Find codon by code"""
        for codon in self.codons:
            if codon.code == codon_code:
                return codon
        return None
    
    def _validate_dependencies(self, codon: Codon, 
                              position: Optional[int] = None) -> bool:
        """
        Validate that codon dependencies are satisfied
        
        Implements Claim 2(c)(ii): Enforce dependency ordering
        
        Args:
            codon: Codon to validate
            position: Optional position for insert operation
            
        Returns:
            True if dependencies are satisfied, False otherwise
        """
        if not codon.dependencies:
            return True
        
        # Get existing codon codes up to position
        if position is None:
            existing_codes = {c.code for c in self.codons}
        else:
            existing_codes = {c.code for c in self.codons[:position]}
        
        # Check all dependencies are present
        for dep in codon.dependencies:
            if dep not in existing_codes:
                return False
        
        return True
    
    def get_strand_string(self) -> str:
        """
        Get full DNA strand string
        
        Implements Claim 2(a): DNA strand format
        
        Returns:
            Strand string in format: SAGCO-ATG-[CODON1]-[CODON2]-...
        """
        codon_str = "-".join(c.code for c in self.codons)
        return f"{self.organism}-{codon_str}"
    
    def get_mutation_history(self) -> List[Dict]:
        """
        Get complete mutation history
        
        Implements Claim 2(d): Lineage tracker
        
        Returns:
            List of mutations
        """
        return [m.to_dict() for m in self.mutation_history]
    
    def export_json(self) -> str:
        """Export strand and history as JSON"""
        data = {
            "organism": self.organism,
            "strand": self.get_strand_string(),
            "codons": [c.to_dict() for c in self.codons],
            "mutation_history": self.get_mutation_history()
        }
        return json.dumps(data, indent=2)
    
    def __str__(self) -> str:
        """String representation"""
        return self.get_strand_string()


class CodonRegistry:
    """
    Codon registry defining valid codons and their dependencies
    
    Implements Claim 2(b): Codon registry
    """
    
    def __init__(self):
        """Initialize the codon registry with standard codons"""
        self.codons: Dict[str, Codon] = {}
        self._initialize_standard_codons()
    
    def _initialize_standard_codons(self):
        """Initialize standard SAGCO codons"""
        standard_codons = [
            Codon("ATG", "Start codon", "Required", 0, [], 
                  "Mandatory start codon"),
            Codon("FLM2", "FlameLang compiler", "v2.0", 1, ["ATG"],
                  "FlameLang compiler subsystem"),
            Codon("MSMC2", "Message passing", "v2.0", 2, ["ATG", "FLM2"],
                  "Message passing and communication layer"),
            Codon("P16", "Protocol", "v16", 3, ["ATG", "MSMC2"],
                  "Core protocol implementation"),
            Codon("CMD27", "Command set", "v27", 4, ["ATG", "P16"],
                  "Command interface and execution"),
            Codon("ISO103", "Isolation layer", "v103", 5, ["ATG"],
                  "Process isolation and sandboxing"),
            Codon("MESH5", "Mesh networking", "v5.0", 6, ["ATG", "MSMC2"],
                  "Distributed mesh network topology"),
            Codon("ORB1", "Orchestration", "v1.0", 7, ["ATG", "CMD27", "MESH5"],
                  "Multi-agent orchestration system"),
            Codon("BENCH1", "FlameBench", "v1.0", 8, ["ATG", "ORB1"],
                  "Performance benchmarking system"),
            Codon("LOM1", "Legion of Minds", "v1.0", 9, ["ATG", "ORB1"],
                  "Collective intelligence framework"),
            Codon("TRIG6", "Trigonometric layer", "v6.0", 10, ["ATG", "ORB1"],
                  "TRIG6 trigonometric projection system"),
            Codon("WAVE1", "Wave core", "v1.0", 11, ["ATG", "TRIG6"],
                  "Wave function core state management"),
            Codon("HYBRID1", "Hybrid blend", "v1.0", 12, ["ATG", "TRIG6", "WAVE1"],
                  "Hybrid trigonometric/hyperbolic blend controller"),
            Codon("NEURO1", "Neurograph", "v1.0", 13, ["ATG", "TRIG6"],
                  "Neurograph cognitive topology visualization"),
            Codon("OPS1", "Operations mesh", "v1.0", 14, ["ATG", "MESH5"],
                  "Operational telemetry and monitoring"),
            Codon("BOOT1", "Boot architecture", "v1.0", 15, ["ATG"],
                  "System initialization and bootstrap")
        ]
        
        for codon in standard_codons:
            self.register_codon(codon)
    
    def register_codon(self, codon: Codon):
        """Register a new codon in the registry"""
        self.codons[codon.code] = codon
    
    def get_codon(self, code: str) -> Optional[Codon]:
        """Get codon definition by code"""
        return self.codons.get(code)
    
    def validate_codon(self, codon: Codon) -> bool:
        """Validate a codon against the registry"""
        if codon.code not in self.codons:
            return False
        return True
    
    def list_codons(self) -> List[Codon]:
        """List all registered codons"""
        return sorted(self.codons.values(), key=lambda c: c.position)
    
    def export_markdown_table(self) -> str:
        """Export registry as markdown table"""
        lines = [
            "| Codon | Subsystem | Current Version | Dependencies | Description |",
            "|-------|-----------|-----------------|--------------|-------------|"
        ]
        
        for codon in self.list_codons():
            deps = ", ".join(codon.dependencies) if codon.dependencies else "None"
            lines.append(f"| {codon.code} | {codon.subsystem} | {codon.version} | "
                        f"{deps} | {codon.description} |")
        
        return "\n".join(lines)


def main():
    """Example usage and demonstration"""
    print("=" * 80)
    print("SAGCO-OS DNA-Based Evolution Tracking System")
    print("=" * 80)
    print()
    
    # Initialize registry
    registry = CodonRegistry()
    print(f"Codon Registry initialized with {len(registry.codons)} standard codons\n")
    
    # Create DNA strand
    strand = DNAStrand("SAGCO")
    print(f"Initial strand: {strand}")
    print()
    
    # Add codons from registry
    codons_to_add = ["FLM2", "MSMC2", "P16", "CMD27", "ISO103", "MESH5", 
                     "ORB1", "BENCH1", "LOM1", "TRIG6", "WAVE1", "HYBRID1", 
                     "NEURO1", "OPS1", "BOOT1"]
    
    author = "Dom Garza"
    
    print("Building DNA strand by adding codons...")
    for codon_code in codons_to_add:
        codon_def = registry.get_codon(codon_code)
        if codon_def:
            # Create a copy of the codon
            codon = Codon(
                code=codon_def.code,
                subsystem=codon_def.subsystem,
                version=codon_def.version,
                dependencies=codon_def.dependencies.copy(),
                description=codon_def.description
            )
            
            success = strand.add_codon(
                codon, 
                author=author,
                justification=f"Initial system setup: {codon.subsystem}"
            )
            
            if success:
                print(f"  ✓ Added {codon_code} ({codon.subsystem})")
            else:
                print(f"  ✗ Failed to add {codon_code} (dependencies not met)")
    
    print(f"\nComplete strand: {strand}\n")
    
    # Demonstrate version increment
    print("Incrementing TRIG6 version...")
    strand.increment_version(
        "TRIG6", 
        "v6.1",
        author=author,
        justification="Added singularity detection enhancements"
    )
    print(f"Updated strand: {strand}\n")
    
    # Show mutation history
    print("Mutation History:")
    print("-" * 80)
    for i, mutation in enumerate(strand.mutation_history[-5:], 1):
        print(f"{i}. {mutation.mutation_type.value.upper()}: {mutation.codon_code} "
              f"v{mutation.old_version or 'new'} → v{mutation.new_version}")
        print(f"   Author: {mutation.author}")
        print(f"   Justification: {mutation.justification}")
        print()
    
    # Export to JSON
    json_file = "/tmp/sagco_dna_strand.json"
    with open(json_file, 'w') as f:
        f.write(strand.export_json())
    print(f"DNA strand exported to: {json_file}\n")
    
    # Export registry table
    print("\nCodon Registry Table:")
    print("=" * 80)
    print(registry.export_markdown_table())
    print("=" * 80)


if __name__ == "__main__":
    main()
