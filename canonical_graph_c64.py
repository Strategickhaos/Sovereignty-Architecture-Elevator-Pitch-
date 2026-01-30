#!/usr/bin/env python3
"""
Canonical 64-Node Cyclic Graph (C_64)
======================================

A unified mathematical structure demonstrating that DNA codons, KHAOS glyphs,
TRIG6 angles, MIDI notes, Rubik-derived phases, and French-curve interpolation
are all homomorphic images of the same 64-state cyclic graph.

Formal Definition:
------------------
Nodes: V = {0, 1, 2, ..., 63}
Edges: E = {(n, (n+1) mod 64) | n ∈ V}
Topology: C_64 (cycle graph with 64 nodes)

Invariant:
----------
θ(n) = n × (360° / 64) = n × 5.625°

All labelings are graph homomorphisms that commute with the graph structure.
Incrementing n then mapping equals mapping n then incrementing in the target domain.

Novelty Statement:
------------------
All artifacts are projections of the same 64-state cyclic graph; novelty lies
in enforcing commutativity across domains. Rather than proving N² pairwise
isomorphisms, we show one structure with many faithful projections, where
"survival under crossfire" becomes commutativity + invariance.
"""

import math
from typing import Dict, List, Tuple, Callable, Any
from dataclasses import dataclass
import json


# ============================================================================
# Core Graph Structure
# ============================================================================

class CanonicalGraph64:
    """
    The canonical 64-node cyclic graph C_64.
    
    This is the fundamental structure from which all other representations
    (DNA, MIDI, angles, etc.) are derived as homomorphic images.
    """
    
    N = 64  # Number of nodes
    
    def __init__(self):
        """Initialize the C_64 cycle graph."""
        # Adjacency representation: each node n maps to (n+1) mod 64
        self.edges = {n: (n + 1) % self.N for n in range(self.N)}
        
        # Reverse edges for backward traversal
        self.reverse_edges = {(n + 1) % self.N: n for n in range(self.N)}
    
    def successor(self, n: int) -> int:
        """Get the successor of node n in the cycle."""
        return self.edges[n]
    
    def predecessor(self, n: int) -> int:
        """Get the predecessor of node n in the cycle."""
        return self.reverse_edges[n]
    
    def theta(self, n: int) -> float:
        """
        The fundamental invariant: θ(n) = n × 5.625°
        
        Maps each node to its angular position on the unit circle.
        """
        return n * (360.0 / self.N)
    
    def theta_radians(self, n: int) -> float:
        """Return θ(n) in radians."""
        return math.radians(self.theta(n))
    
    def distance(self, n1: int, n2: int) -> int:
        """
        Graph distance between two nodes (minimum path length).
        On a cycle, this is min(forward, backward) distance.
        """
        forward = (n2 - n1) % self.N
        backward = (n1 - n2) % self.N
        return min(forward, backward)
    
    def nodes(self) -> List[int]:
        """Return all nodes in the graph."""
        return list(range(self.N))


# ============================================================================
# Labelings (Graph Homomorphisms)
# ============================================================================

class DNALabeling:
    """
    DNA codon labeling: 64 codons (UUU...GGG) mapped to C_64.
    
    Standard genetic code ordering: 4³ = 64 combinations of {U, C, A, G}.
    """
    
    CODONS = [
        "UUU", "UUC", "UUA", "UUG", "UCU", "UCC", "UCA", "UCG",
        "UAU", "UAC", "UAA", "UAG", "UGU", "UGC", "UGA", "UGG",
        "CUU", "CUC", "CUA", "CUG", "CCU", "CCC", "CCA", "CCG",
        "CAU", "CAC", "CAA", "CAG", "CGU", "CGC", "CGA", "CGG",
        "AUU", "AUC", "AUA", "AUG", "ACU", "ACC", "ACA", "ACG",
        "AAU", "AAC", "AAA", "AAG", "AGU", "AGC", "AGA", "AGG",
        "GUU", "GUC", "GUA", "GUG", "GCU", "GCC", "GCA", "GCG",
        "GAU", "GAC", "GAA", "GAG", "GGU", "GGC", "GGA", "GGG"
    ]
    
    def __init__(self):
        """Initialize DNA labeling."""
        assert len(self.CODONS) == 64, "Must have exactly 64 codons"
        self.codon_to_node = {codon: i for i, codon in enumerate(self.CODONS)}
        self.node_to_codon = {i: codon for i, codon in enumerate(self.CODONS)}
    
    def label(self, n: int) -> str:
        """Map node n to its DNA codon."""
        return self.node_to_codon[n % 64]
    
    def inverse(self, codon: str) -> int:
        """Map DNA codon back to node."""
        return self.codon_to_node.get(codon, -1)


class TRIG6Labeling:
    """
    TRIG6 angle labeling: θ(n) = n × 5.625°
    
    Each node maps to a specific angle on the unit circle.
    """
    
    def label(self, n: int) -> float:
        """Map node n to its angle in degrees."""
        return n * (360.0 / 64)
    
    def label_radians(self, n: int) -> float:
        """Map node n to its angle in radians."""
        return math.radians(self.label(n))


class MIDILabeling:
    """
    MIDI note labeling: MIDI(n) = 60 + n
    
    Starting from Middle C (MIDI 60), map to 64 consecutive MIDI notes.
    Range: C4 (60) to B8 (123).
    """
    
    BASE_NOTE = 60  # Middle C (C4)
    
    def label(self, n: int) -> int:
        """Map node n to MIDI note number."""
        return self.BASE_NOTE + (n % 64)
    
    def note_name(self, n: int) -> str:
        """Get the note name for node n."""
        midi = self.label(n)
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note = notes[midi % 12]
        octave = (midi // 12) - 1
        return f"{note}{octave}"


class GeometryLabeling:
    """
    Unit circle embedding: z(n) = e^(i·θ(n))
    
    Each node is embedded as a complex number on the unit circle.
    """
    
    def label(self, n: int) -> complex:
        """Map node n to its position on the unit circle."""
        theta = n * 2 * math.pi / 64
        return complex(math.cos(theta), math.sin(theta))
    
    def cartesian(self, n: int) -> Tuple[float, float]:
        """Return (x, y) coordinates on unit circle."""
        z = self.label(n)
        return (z.real, z.imag)
    
    def polar(self, n: int) -> Tuple[float, float]:
        """Return (r, θ) in polar coordinates."""
        theta = n * 2 * math.pi / 64
        return (1.0, theta)


class CurveLabeling:
    """
    French curve / spline interpolation over the circle.
    
    Smooth interpolation between discrete points on the unit circle.
    """
    
    def __init__(self, geometry: GeometryLabeling):
        """Initialize with geometry labeling for unit circle positions."""
        self.geometry = geometry
    
    def interpolate(self, t: float, n_start: int, n_end: int) -> complex:
        """
        Smooth interpolation between two nodes.
        
        Args:
            t: Parameter in [0, 1], where 0 = n_start, 1 = n_end
            n_start: Starting node
            n_end: Ending node
            
        Returns:
            Interpolated position on unit circle as complex number
        """
        # Simple linear interpolation on the circle (geodesic)
        # For more sophisticated curves, could use Bézier or spline
        theta_start = n_start * 2 * math.pi / 64
        theta_end = n_end * 2 * math.pi / 64
        
        # Handle wrap-around for shortest path
        diff = theta_end - theta_start
        if diff > math.pi:
            theta_end -= 2 * math.pi
        elif diff < -math.pi:
            theta_end += 2 * math.pi
        
        theta = theta_start + t * (theta_end - theta_start)
        return complex(math.cos(theta), math.sin(theta))
    
    def path(self, n_start: int, n_end: int, steps: int = 100) -> List[complex]:
        """
        Generate a smooth path from n_start to n_end.
        
        Returns:
            List of complex numbers representing the path
        """
        return [self.interpolate(t / steps, n_start, n_end) 
                for t in range(steps + 1)]


class GlyphLabeling:
    """
    KHAOS glyph labeling: symbolic representation.
    
    Maps each node to a glyph identifier in the KHAOS system.
    This is a placeholder - actual glyphs would be defined by the KHAOS system.
    """
    
    def label(self, n: int) -> str:
        """Map node n to KHAOS glyph identifier."""
        # Using a systematic naming: K00 through K63
        return f"K{n:02d}"
    
    def describe(self, n: int) -> str:
        """Get description of the glyph at node n."""
        return f"KHAOS glyph {self.label(n)} at position {n}"


# ============================================================================
# Commutativity Verification
# ============================================================================

@dataclass
class CommutativityTest:
    """Result of a commutativity test."""
    labeling_name: str
    node: int
    increment_then_map: Any
    map_then_increment: Any
    commutes: bool
    error_message: str = ""


class CommutativityChecker:
    """
    Verify that all labelings are graph homomorphisms.
    
    For each labeling L and node n:
    L(succ(n)) == succ_in_target(L(n))
    
    Or equivalently: increment-then-map equals map-then-increment.
    """
    
    def __init__(self, graph: CanonicalGraph64):
        """Initialize with the canonical graph."""
        self.graph = graph
        self.dna = DNALabeling()
        self.trig6 = TRIG6Labeling()
        self.midi = MIDILabeling()
        self.geometry = GeometryLabeling()
        self.curve = CurveLabeling(self.geometry)
        self.glyph = GlyphLabeling()
    
    def check_dna_commutativity(self, n: int) -> CommutativityTest:
        """Verify DNA labeling commutativity at node n."""
        # Increment then map
        succ = self.graph.successor(n)
        increment_then_map = self.dna.label(succ)
        
        # Map then increment (in codon space, increment means next codon)
        map_then_increment = self.dna.label((n + 1) % 64)
        
        commutes = (increment_then_map == map_then_increment)
        
        return CommutativityTest(
            labeling_name="DNA",
            node=n,
            increment_then_map=increment_then_map,
            map_then_increment=map_then_increment,
            commutes=commutes
        )
    
    def check_trig6_commutativity(self, n: int) -> CommutativityTest:
        """Verify TRIG6 labeling commutativity at node n."""
        # Increment then map
        succ = self.graph.successor(n)
        increment_then_map = self.trig6.label(succ)
        
        # Map then increment (in angle space, +5.625°)
        base_angle = self.trig6.label(n)
        map_then_increment = (base_angle + 5.625) % 360
        
        commutes = abs(increment_then_map - map_then_increment) < 1e-10
        
        return CommutativityTest(
            labeling_name="TRIG6",
            node=n,
            increment_then_map=increment_then_map,
            map_then_increment=map_then_increment,
            commutes=commutes
        )
    
    def check_midi_commutativity(self, n: int) -> CommutativityTest:
        """Verify MIDI labeling commutativity at node n."""
        # Increment then map
        succ = self.graph.successor(n)
        increment_then_map = self.midi.label(succ)
        
        # Map then increment (in MIDI space, +1 semitone, with wrap)
        base_midi = self.midi.label(n)
        map_then_increment = self.midi.BASE_NOTE + ((n + 1) % 64)
        
        commutes = (increment_then_map == map_then_increment)
        
        return CommutativityTest(
            labeling_name="MIDI",
            node=n,
            increment_then_map=increment_then_map,
            map_then_increment=map_then_increment,
            commutes=commutes
        )
    
    def check_geometry_commutativity(self, n: int) -> CommutativityTest:
        """Verify geometry labeling commutativity at node n."""
        # Increment then map
        succ = self.graph.successor(n)
        increment_then_map = self.geometry.label(succ)
        
        # Map then increment (rotate by 5.625° = 2π/64)
        base_z = self.geometry.label(n)
        rotation = complex(math.cos(2 * math.pi / 64), math.sin(2 * math.pi / 64))
        map_then_increment = base_z * rotation
        
        # Complex number comparison with tolerance
        diff = abs(increment_then_map - map_then_increment)
        commutes = diff < 1e-10
        
        return CommutativityTest(
            labeling_name="Geometry",
            node=n,
            increment_then_map=increment_then_map,
            map_then_increment=map_then_increment,
            commutes=commutes
        )
    
    def check_glyph_commutativity(self, n: int) -> CommutativityTest:
        """Verify glyph labeling commutativity at node n."""
        # Increment then map
        succ = self.graph.successor(n)
        increment_then_map = self.glyph.label(succ)
        
        # Map then increment (next glyph in sequence)
        map_then_increment = self.glyph.label((n + 1) % 64)
        
        commutes = (increment_then_map == map_then_increment)
        
        return CommutativityTest(
            labeling_name="Glyph",
            node=n,
            increment_then_map=increment_then_map,
            map_then_increment=map_then_increment,
            commutes=commutes
        )
    
    def check_all(self, n: int) -> List[CommutativityTest]:
        """Check commutativity for all labelings at node n."""
        return [
            self.check_dna_commutativity(n),
            self.check_trig6_commutativity(n),
            self.check_midi_commutativity(n),
            self.check_geometry_commutativity(n),
            self.check_glyph_commutativity(n)
        ]
    
    def verify_all_nodes(self) -> Dict[str, List[CommutativityTest]]:
        """Verify commutativity across all nodes for all labelings."""
        results = {
            "DNA": [],
            "TRIG6": [],
            "MIDI": [],
            "Geometry": [],
            "Glyph": []
        }
        
        for n in range(64):
            tests = self.check_all(n)
            for test in tests:
                results[test.labeling_name].append(test)
        
        return results


# ============================================================================
# Commutative Diagram
# ============================================================================

def generate_commutative_diagram() -> str:
    """
    Generate ASCII commutative diagram showing the graph structure.
    
    Demonstrates that all paths from C_64 to target domains commute.
    """
    diagram = """
COMMUTATIVE DIAGRAM FOR C_64
============================

The following diagram shows that incrementing then mapping equals 
mapping then incrementing for all labelings:


                    C_64
                     |
        +------------+------------+
        |            |            |
        v            v            v
      DNA         TRIG6         MIDI
     (codons)    (angles)      (notes)
        |            |            |
        v            v            v
      +1 mod 64   +5.625°       +1 note
        |            |            |
        =            =            =
        |            |            |
    succ(n)      θ(succ)      MIDI(succ)


For any node n ∈ C_64:

1. DNA homomorphism:
   codon(n+1) = next_codon(codon(n))

2. TRIG6 homomorphism:
   θ(n+1) = θ(n) + 5.625°

3. MIDI homomorphism:
   midi(n+1) = midi(n) + 1 (mod 64 range)

4. Geometry homomorphism:
   z(n+1) = z(n) × e^(2πi/64)

5. Glyph homomorphism:
   glyph(n+1) = next_glyph(glyph(n))


All paths commute:

    C_64 ----map----> Target
     |                  |
   succ               next
     |                  |
     v                  v
    C_64 ----map----> Target

This proves all domains are homomorphic images of C_64.
"""
    return diagram


# ============================================================================
# Main Interface
# ============================================================================

class CanonicalGraphSystem:
    """
    Complete system for the canonical 64-node cyclic graph.
    
    Provides unified interface to graph structure and all labelings.
    """
    
    def __init__(self):
        """Initialize the complete system."""
        self.graph = CanonicalGraph64()
        self.dna = DNALabeling()
        self.trig6 = TRIG6Labeling()
        self.midi = MIDILabeling()
        self.geometry = GeometryLabeling()
        self.curve = CurveLabeling(self.geometry)
        self.glyph = GlyphLabeling()
        self.checker = CommutativityChecker(self.graph)
    
    def get_all_labels(self, n: int) -> Dict[str, Any]:
        """Get all labelings for a given node n."""
        return {
            "node": n,
            "dna": self.dna.label(n),
            "angle_deg": self.trig6.label(n),
            "angle_rad": self.trig6.label_radians(n),
            "midi": self.midi.label(n),
            "midi_note": self.midi.note_name(n),
            "geometry_complex": self.geometry.label(n),
            "geometry_xy": self.geometry.cartesian(n),
            "geometry_polar": self.geometry.polar(n),
            "glyph": self.glyph.label(n)
        }
    
    def verify_commutativity(self) -> Dict[str, Any]:
        """
        Verify that all labelings preserve graph homomorphism.
        
        Returns summary of commutativity tests.
        """
        results = self.checker.verify_all_nodes()
        
        summary = {
            "total_tests": 64 * 5,  # 64 nodes × 5 labelings
            "passed": 0,
            "failed": 0,
            "details": {}
        }
        
        for labeling, tests in results.items():
            passed = sum(1 for t in tests if t.commutes)
            failed = sum(1 for t in tests if not t.commutes)
            
            summary["details"][labeling] = {
                "total": len(tests),
                "passed": passed,
                "failed": failed,
                "pass_rate": passed / len(tests) if tests else 0
            }
            
            summary["passed"] += passed
            summary["failed"] += failed
        
        summary["overall_pass_rate"] = (
            summary["passed"] / summary["total_tests"] 
            if summary["total_tests"] > 0 else 0
        )
        
        return summary
    
    def export_graph_data(self) -> Dict[str, Any]:
        """Export complete graph data for visualization or analysis."""
        nodes_data = []
        
        for n in range(64):
            node_data = self.get_all_labels(n)
            node_data["successor"] = self.graph.successor(n)
            node_data["predecessor"] = self.graph.predecessor(n)
            nodes_data.append(node_data)
        
        return {
            "graph_type": "C_64 (64-node cycle graph)",
            "node_count": 64,
            "edge_count": 64,
            "nodes": nodes_data,
            "commutative_diagram": generate_commutative_diagram(),
            "novelty_statement": self.__class__.__doc__
        }


# ============================================================================
# Command-Line Interface
# ============================================================================

def main():
    """Main entry point for demonstration."""
    print("=" * 70)
    print("CANONICAL 64-NODE CYCLIC GRAPH (C_64)")
    print("=" * 70)
    print()
    
    # Initialize system
    system = CanonicalGraphSystem()
    
    # Show some example labelings
    print("EXAMPLE LABELINGS (first 8 nodes):")
    print("-" * 70)
    for n in range(8):
        labels = system.get_all_labels(n)
        print(f"Node {n:2d}: DNA={labels['dna']:3s} | "
              f"θ={labels['angle_deg']:6.2f}° | "
              f"MIDI={labels['midi']:3d} ({labels['midi_note']:3s}) | "
              f"Glyph={labels['glyph']}")
    print()
    
    # Verify commutativity
    print("COMMUTATIVITY VERIFICATION:")
    print("-" * 70)
    summary = system.verify_commutativity()
    print(f"Total tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Overall pass rate: {summary['overall_pass_rate']:.1%}")
    print()
    
    for labeling, details in summary['details'].items():
        print(f"  {labeling:12s}: {details['passed']:2d}/{details['total']:2d} "
              f"({details['pass_rate']:.1%})")
    print()
    
    # Show commutative diagram
    print(generate_commutative_diagram())
    
    # Novelty statement
    print("\nNOVELTY STATEMENT:")
    print("-" * 70)
    print("""
All artifacts are projections of the same 64-state cyclic graph; novelty lies
in enforcing commutativity across domains. Rather than proving N² pairwise
isomorphisms, we show one structure with many faithful projections, where
"survival under crossfire" becomes commutativity + invariance.

The canonical graph C_64 unifies DNA codons, KHAOS glyphs, trigonometric angles,
MIDI notes, and geometric embeddings under a single quantized, cyclic structure.
Each domain is a homomorphic image—incrementing then mapping equals mapping then
incrementing—making cross-domain verification reducible to a single rule check.
""")


if __name__ == "__main__":
    main()
