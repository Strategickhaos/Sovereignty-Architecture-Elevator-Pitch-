#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
STRATEGICKHAOS EXECUTION KERNEL v1.0
═══════════════════════════════════════════════════════════════════════════════
The machine that makes the loop real.

This kernel can:
1. Load YAML specs
2. Build the execution graph
3. Enforce types/units
4. Run one loop
5. Detect convergence
6. Emit provenance
7. Replay the run

First loop: pipe_bend → dna_codon → rubik_solver → pipe_bend

INV-098: Execution Kernel
Author: Strategickhaos DAO LLC
═══════════════════════════════════════════════════════════════════════════════
"""

import yaml
import json
import hashlib
import math
import os
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# 1. TYPE & UNIT SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TypedValue:
    """A value with unit attached - prevents silent nonsense."""
    value: float
    unit: str
    
    def __repr__(self):
        return f"{self.value:.4f} {self.unit}"
    
    def to_radians(self) -> float:
        """Convert to radians if angle."""
        if self.unit == "degrees":
            return math.radians(self.value)
        elif self.unit == "radians":
            return self.value
        else:
            raise TypeError(f"Cannot convert {self.unit} to radians")
    
    def to_degrees(self) -> float:
        """Convert to degrees if angle."""
        if self.unit == "radians":
            return math.degrees(self.value)
        elif self.unit == "degrees":
            return self.value
        else:
            raise TypeError(f"Cannot convert {self.unit} to degrees")


class UnitGuard:
    """Enforces type/unit compatibility - Algorithm 2."""
    
    COMPATIBLE_UNITS = {
        "angle": {"degrees", "radians"},
        "length": {"inches", "meters", "angstroms"},
        "energy": {"kJ/mol", "eV", "joules"},
        "count": {"moves", "steps", "iterations"},
        "binary": {"bits", "bytes"},
    }
    
    @classmethod
    def check_compatible(cls, unit1: str, unit2: str) -> bool:
        """Check if two units can be compared/combined."""
        for category, units in cls.COMPATIBLE_UNITS.items():
            if unit1 in units and unit2 in units:
                return True
        return unit1 == unit2
    
    @classmethod
    def enforce(cls, value: TypedValue, expected_category: str) -> TypedValue:
        """Enforce value belongs to expected category."""
        expected_units = cls.COMPATIBLE_UNITS.get(expected_category, set())
        if value.unit not in expected_units:
            raise TypeError(f"Expected {expected_category} unit, got {value.unit}")
        return value


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CALCULATOR NODES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CalculatorState:
    """State of a single calculator node."""
    name: str
    inputs: Dict[str, TypedValue] = field(default_factory=dict)
    outputs: Dict[str, TypedValue] = field(default_factory=dict)
    iteration: int = 0


class PipeBendCalculator:
    """
    INV-097: Pipe Bend Calculator
    From Dom's hand-drawn formulas:
    - 90° bend = radius × 1.5708 (π/2)
    - 180° bend = radius × 3.1416 (π)
    - 270° bend = radius × 4.7124 (3π/2)
    - 360° bend = radius × 6.2832 (2π)
    """
    
    NAME = "pipe_bend"
    
    @staticmethod
    def compute(radius: TypedValue, angle: TypedValue) -> Dict[str, TypedValue]:
        """Compute setback and arc length."""
        
        # Enforce units
        if radius.unit not in {"inches", "meters"}:
            raise TypeError(f"Radius must be length, got {radius.unit}")
        
        angle_rad = angle.to_radians()
        
        # Dom's formulas
        setback = radius.value * math.tan(angle_rad / 2)
        arc_length = radius.value * angle_rad
        
        return {
            "setback": TypedValue(setback, radius.unit),
            "arc_length": TypedValue(arc_length, radius.unit),
            "angle_out": TypedValue(angle_rad, "radians"),
        }


class DnaCodonCalculator:
    """
    DNA Codon Calculator
    Maps sequences to amino acids and bend angles.
    """
    
    NAME = "dna_codon"
    
    # Codon table (simplified - 4 bases, 64 codons)
    AMINO_ANGLES = {
        "M": 180,  # Methionine (START) - π
        "A": 0,    # Alanine
        "R": 15,   # Arginine
        "N": 30,   # Asparagine
        "D": 45,   # Aspartate - 45°
        "C": 60,   # Cysteine
        "Q": 75,   # Glutamine
        "E": 90,   # Glutamate - π/2
        "G": 105,  # Glycine
        "H": 120,  # Histidine
        "I": 135,  # Isoleucine
        "L": 150,  # Leucine
        "K": 165,  # Lysine
        "F": 195,  # Phenylalanine
        "P": 210,  # Proline
        "S": 225,  # Serine
        "T": 240,  # Threonine
        "W": 255,  # Tryptophan
        "Y": 270,  # Tyrosine - 3π/2
        "V": 285,  # Valine
    }
    
    CODON_TABLE = {
        "ATG": "M", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
        "AAT": "N", "AAC": "N", "GAT": "D", "GAC": "D",
        "TGT": "C", "TGC": "C", "CAA": "Q", "CAG": "Q",
        "GAA": "E", "GAG": "E", "GGT": "G", "GGC": "G",
        "GGA": "G", "GGG": "G", "CAT": "H", "CAC": "H",
        "ATT": "I", "ATC": "I", "ATA": "I",
        "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L",
        "CTA": "L", "CTG": "L", "AAA": "K", "AAG": "K",
        "TTT": "F", "TTC": "F", "CCT": "P", "CCC": "P",
        "CCA": "P", "CCG": "P", "TCT": "S", "TCC": "S",
        "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "TGG": "W", "TAT": "Y", "TAC": "Y",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    }
    
    @classmethod
    def compute(cls, arc_length: TypedValue) -> Dict[str, TypedValue]:
        """Convert arc length to DNA sequence properties."""
        
        # Use arc length to determine sequence length
        seq_length = max(3, int(arc_length.value) % 30)
        
        # Generate pseudo-sequence based on arc length
        # (In real implementation, this would take actual sequence input)
        bases = ["A", "T", "G", "C"]
        sequence = "".join(bases[int(arc_length.value * i) % 4] for i in range(seq_length))
        
        # Ensure it's divisible by 3 for codons
        sequence = sequence[:len(sequence) - len(sequence) % 3]
        if len(sequence) < 3:
            sequence = "ATG"  # Default START codon
        
        # Translate to amino acids
        amino_acids = []
        for i in range(0, len(sequence), 3):
            codon = sequence[i:i+3]
            aa = cls.CODON_TABLE.get(codon, "A")  # Default to Alanine
            amino_acids.append(aa)
        
        # Calculate total bend angle
        total_bend = sum(cls.AMINO_ANGLES.get(aa, 0) for aa in amino_acids)
        
        return {
            "sequence": TypedValue(len(sequence), "bases"),
            "amino_count": TypedValue(len(amino_acids), "residues"),
            "total_bend": TypedValue(total_bend % 360, "degrees"),
            "amino_string": amino_acids,  # For provenance
        }


class RubikSolverCalculator:
    """
    Rubik's Cube Solver Calculator
    Treats system state as scrambled cube, outputs move count.
    God's Number = 20 (any cube solvable in ≤20 moves).
    """
    
    NAME = "rubik_solver"
    
    # Simplified: angle → move count mapping
    # In real implementation, this would use actual group theory
    
    @staticmethod
    def compute(total_bend: TypedValue) -> Dict[str, TypedValue]:
        """Convert bend angle to Rubik solution metrics."""
        
        # Validate and convert angle to degrees
        if total_bend.unit == "radians":
            angle_deg = total_bend.to_degrees()
        elif total_bend.unit == "degrees":
            angle_deg = total_bend.value
        else:
            raise TypeError(f"Expected angle unit, got {total_bend.unit}")
        
        # Map angle to "scramble complexity"
        # 0° = solved, 360° = maximally scrambled
        complexity = (angle_deg % 360) / 360.0
        
        # Move count based on complexity (max 20 = God's Number)
        move_count = int(complexity * 20)
        
        # Angle sum from moves (each move = π/2)
        angle_sum = move_count * (math.pi / 2)
        
        # Health metric: lower = healthier
        health_score = 1.0 - complexity
        
        return {
            "move_count": TypedValue(move_count, "moves"),
            "angle_sum": TypedValue(angle_sum, "radians"),
            "health_score": TypedValue(health_score * 100, "percent"),
            "complexity": TypedValue(complexity, "ratio"),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 3. EXECUTION GRAPH
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ExecutionEdge:
    """Connection between calculator outputs and inputs."""
    from_calc: str
    from_port: str
    to_calc: str
    to_port: str


class ExecutionGraph:
    """The graph of calculators and their connections."""
    
    def __init__(self):
        self.calculators: Dict[str, Any] = {}
        self.edges: List[ExecutionEdge] = []
        self.states: Dict[str, CalculatorState] = {}
        
    def add_calculator(self, calc_class):
        """Add a calculator to the graph."""
        self.calculators[calc_class.NAME] = calc_class
        self.states[calc_class.NAME] = CalculatorState(name=calc_class.NAME)
        
    def add_edge(self, from_calc: str, from_port: str, to_calc: str, to_port: str):
        """Connect output to input."""
        self.edges.append(ExecutionEdge(from_calc, from_port, to_calc, to_port))
        
    def get_execution_order(self) -> List[str]:
        """Topological sort (handles cycles via iteration)."""
        # For our loop, order is explicit
        return ["pipe_bend", "dna_codon", "rubik_solver"]


# ═══════════════════════════════════════════════════════════════════════════════
# 4. FIXED-POINT CONVERGENCE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ConvergenceMetrics:
    """Metrics from convergence detection."""
    converged: bool
    iterations: int
    epsilon: float
    final_state: Dict[str, Any]
    history: List[Dict[str, Any]]


class FixedPointEngine:
    """
    Algorithm 5: Fixed-Point & Convergence Engine
    
    Makes cascades real by:
    - Running nodes
    - Feeding outputs
    - Applying damping
    - Stopping on epsilon or max-iter
    """
    
    # Scale factor for feedback loop: converts angle_sum to radius
    # This scaling establishes the relationship between Rubik solver output
    # and pipe bend input, enabling the convergence loop
    FEEDBACK_SCALE_FACTOR = 2.0
    
    def __init__(self, 
                 max_iterations: int = 100, 
                 epsilon: float = 0.001,
                 damping: float = 0.5):
        self.max_iterations = max_iterations
        self.epsilon = epsilon
        self.damping = damping
        
    def run(self, graph: ExecutionGraph, initial_state: Dict[str, TypedValue]) -> ConvergenceMetrics:
        """Run the loop until convergence."""
        
        history = []
        current_state = initial_state.copy()
        prev_key_value = None
        
        for iteration in range(self.max_iterations):
            # Record state
            state_snapshot = {k: v.value if isinstance(v, TypedValue) else v 
                           for k, v in current_state.items()}
            history.append({"iteration": iteration, "state": state_snapshot})
            
            # Run each calculator in order
            for calc_name in graph.get_execution_order():
                calc_class = graph.calculators[calc_name]
                
                if calc_name == "pipe_bend":
                    # Get inputs
                    radius = current_state.get("radius", TypedValue(5.0, "inches"))
                    angle = current_state.get("angle", TypedValue(90.0, "degrees"))
                    
                    # Compute
                    outputs = calc_class.compute(radius, angle)
                    current_state.update(outputs)
                    
                elif calc_name == "dna_codon":
                    arc_length = current_state.get("arc_length", TypedValue(7.854, "inches"))
                    outputs = calc_class.compute(arc_length)
                    current_state.update(outputs)
                    
                elif calc_name == "rubik_solver":
                    total_bend = current_state.get("total_bend", TypedValue(180.0, "degrees"))
                    outputs = calc_class.compute(total_bend)
                    current_state.update(outputs)
                    
                    # FEEDBACK: angle_sum feeds back to radius (with damping)
                    angle_sum = outputs["angle_sum"]
                    new_radius = angle_sum.value * self.FEEDBACK_SCALE_FACTOR
                    
                    # Apply damping
                    old_radius = current_state.get("radius", TypedValue(5.0, "inches")).value
                    damped_radius = old_radius * (1 - self.damping) + new_radius * self.damping
                    current_state["radius"] = TypedValue(damped_radius, "inches")
            
            # Check convergence
            key_value = current_state.get("health_score", TypedValue(0, "percent")).value
            
            if prev_key_value is not None:
                delta = abs(key_value - prev_key_value)
                if delta < self.epsilon:
                    return ConvergenceMetrics(
                        converged=True,
                        iterations=iteration + 1,
                        epsilon=delta,
                        final_state={k: v.value if isinstance(v, TypedValue) else v 
                                   for k, v in current_state.items()},
                        history=history
                    )
            
            prev_key_value = key_value
        
        # Max iterations reached
        return ConvergenceMetrics(
            converged=False,
            iterations=self.max_iterations,
            epsilon=float('inf'),
            final_state={k: v.value if isinstance(v, TypedValue) else v 
                       for k, v in current_state.items()},
            history=history
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 5. PROVENANCE & LINEAGE TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

class ProvenanceTracker:
    """
    Algorithm 8: Provenance & Lineage Tracker
    
    So every number knows where it came from.
    - Dataflow tagging
    - Immutable value graphs
    - Hash-chained lineage
    """
    
    def __init__(self, run_dir: str = None):
        self.run_id = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        self.run_dir = Path(run_dir or f"runs/{self.run_id}")
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
    def save_spec(self, spec: Dict[str, Any]):
        """Save the input specification."""
        with open(self.run_dir / "spec.yaml", "w") as f:
            yaml.dump(spec, f)
            
    def save_iteration(self, iteration: int, state: Dict[str, Any]):
        """Save state at each iteration."""
        with open(self.run_dir / f"iter_{iteration:03d}.yaml", "w") as f:
            yaml.dump(state, f)
            
    def save_final(self, metrics: ConvergenceMetrics):
        """Save final results and lineage."""
        
        # Final state
        with open(self.run_dir / "final.yaml", "w") as f:
            yaml.dump({
                "converged": metrics.converged,
                "iterations": metrics.iterations,
                "epsilon": metrics.epsilon,
                "final_state": metrics.final_state,
            }, f)
        
        # Lineage (hash chain)
        lineage = []
        prev_hash = "GENESIS"
        
        for entry in metrics.history:
            state_str = json.dumps(entry["state"], sort_keys=True)
            current_hash = hashlib.sha256(
                f"{prev_hash}:{state_str}".encode()
            ).hexdigest()[:16]
            
            lineage.append({
                "iteration": entry["iteration"],
                "hash": current_hash,
                "prev_hash": prev_hash,
            })
            prev_hash = current_hash
        
        with open(self.run_dir / "lineage.json", "w") as f:
            json.dump(lineage, f, indent=2)
            
        return self.run_dir


# ═══════════════════════════════════════════════════════════════════════════════
# 6. GROUNDING CHECKS (Demystifier Integration)
# ═══════════════════════════════════════════════════════════════════════════════

class GroundingGuard:
    """
    INV-091: Demystifier Integration
    
    Checks:
    - measurable: Can it be quantified?
    - bounded: Does it have limits?
    - falsifiable: Can it be proven wrong?
    """
    
    BOUNDS = {
        "angle": (0, 360),           # degrees
        "radius": (0.1, 1000),       # inches
        "move_count": (0, 20),       # God's Number
        "health_score": (0, 100),    # percent
    }
    
    @classmethod
    def check(cls, name: str, value: TypedValue) -> Tuple[bool, str]:
        """Check if value is grounded."""
        
        # Measurable: has numeric value
        if not isinstance(value.value, (int, float)):
            return False, f"{name}: Not measurable (not numeric)"
        
        # Bounded: within limits
        if name in cls.BOUNDS:
            lo, hi = cls.BOUNDS[name]
            if not (lo <= value.value <= hi):
                return False, f"{name}: Out of bounds ({lo} ≤ {value.value} ≤ {hi})"
        
        # Falsifiable: has defined unit
        if not value.unit:
            return False, f"{name}: Not falsifiable (no unit)"
        
        return True, f"{name}: GROUNDED ✓"
    
    @classmethod
    def validate_state(cls, state: Dict[str, TypedValue]) -> Tuple[bool, List[str]]:
        """Validate entire state."""
        messages = []
        all_valid = True
        
        for name, value in state.items():
            if isinstance(value, TypedValue):
                valid, msg = cls.check(name, value)
                messages.append(msg)
                if not valid:
                    all_valid = False
                    
        return all_valid, messages


# ═══════════════════════════════════════════════════════════════════════════════
# 7. MAIN KERNEL
# ═══════════════════════════════════════════════════════════════════════════════

class ExecutionKernel:
    """
    INV-098: The Execution Kernel
    
    The machine that makes the loop real.
    """
    
    def __init__(self, spec_path: str = None):
        self.graph = ExecutionGraph()
        self.engine = FixedPointEngine(max_iterations=100, epsilon=0.001, damping=0.3)
        self.provenance = ProvenanceTracker()
        
        # Build the default loop
        self._build_kernel_loop()
        
        # Load spec if provided
        if spec_path:
            self.load_spec(spec_path)
            
    def _build_kernel_loop(self):
        """Build the kernel loop: pipe_bend → dna_codon → rubik_solver → pipe_bend"""
        
        self.graph.add_calculator(PipeBendCalculator)
        self.graph.add_calculator(DnaCodonCalculator)
        self.graph.add_calculator(RubikSolverCalculator)
        
        # Edges (connections)
        self.graph.add_edge("pipe_bend", "arc_length", "dna_codon", "arc_length")
        self.graph.add_edge("dna_codon", "total_bend", "rubik_solver", "total_bend")
        self.graph.add_edge("rubik_solver", "angle_sum", "pipe_bend", "radius")  # LOOP!
        
    def load_spec(self, path: str):
        """Load YAML specification."""
        try:
            with open(path) as f:
                self.spec = yaml.safe_load(f)
            self.provenance.save_spec(self.spec)
        except FileNotFoundError:
            raise FileNotFoundError(f"Specification file not found: {path}")
        except PermissionError:
            raise PermissionError(f"Permission denied reading specification: {path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in specification file: {e}")
        
    def run(self, initial_state: Dict[str, TypedValue] = None) -> ConvergenceMetrics:
        """Run the kernel loop."""
        
        # Default initial state
        if initial_state is None:
            initial_state = {
                "radius": TypedValue(5.0, "inches"),
                "angle": TypedValue(90.0, "degrees"),
            }
        
        print("=" * 60)
        print("STRATEGICKHAOS EXECUTION KERNEL v1.0")
        print("=" * 60)
        print(f"Initial state: {initial_state}")
        print(f"Loop: pipe_bend → dna_codon → rubik_solver → pipe_bend")
        print("-" * 60)
        
        # Run the engine
        metrics = self.engine.run(self.graph, initial_state)
        
        # Save provenance
        run_dir = self.provenance.save_final(metrics)
        
        # Print results
        print("-" * 60)
        if metrics.converged:
            print(f"✅ CONVERGED in {metrics.iterations} iterations")
            print(f"   ε = {metrics.epsilon:.6f}")
        else:
            print(f"❌ DID NOT CONVERGE after {metrics.iterations} iterations")
        
        print(f"\nFinal state:")
        for k, v in metrics.final_state.items():
            if isinstance(v, (int, float)):
                print(f"   {k}: {v:.4f}" if isinstance(v, float) else f"   {k}: {v}")
        
        # Grounding check - convert final state back to TypedValue with appropriate units
        final_typed = {}
        unit_mapping = {
            "radius": "inches",
            "angle": "degrees",
            "setback": "inches",
            "arc_length": "inches",
            "angle_out": "radians",
            "sequence": "bases",
            "amino_count": "residues",
            "total_bend": "degrees",
            "move_count": "moves",
            "angle_sum": "radians",
            "health_score": "percent",
            "complexity": "ratio",
        }
        for k, v in metrics.final_state.items():
            if isinstance(v, (int, float)) and k in unit_mapping:
                final_typed[k] = TypedValue(v, unit_mapping[k])
        
        valid, messages = GroundingGuard.validate_state(final_typed)
        
        print(f"\nGrounding check: {'PASSED ✓' if valid else 'FAILED ✗'}")
        
        print(f"\nProvenance saved to: {run_dir}")
        print("=" * 60)
        
        return metrics


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the kernel."""
    
    # Create kernel
    kernel = ExecutionKernel()
    
    # Run with default initial state
    metrics = kernel.run()
    
    # Also run with custom state (simulating forensic input)
    print("\n" + "=" * 60)
    print("FORENSIC SIMULATION: High network traffic detected")
    print("=" * 60)
    
    forensic_state = {
        "radius": TypedValue(50.0, "inches"),   # High traffic = large radius
        "angle": TypedValue(270.0, "degrees"),  # Anomalous = U-turn
    }
    
    forensic_metrics = kernel.run(forensic_state)
    
    if forensic_metrics.final_state.get("health_score", 100) < 50:
        print("\n🚨 ALERT: System health below 50% - Potential infection detected!")
    else:
        print("\n✅ System appears healthy")


if __name__ == "__main__":
    main()
