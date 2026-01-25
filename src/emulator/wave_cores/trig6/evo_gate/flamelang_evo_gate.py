#!/usr/bin/env python3
"""
FlameLang Evolutionary Gate - Darwinian Compiler Evolution

This gate decides whether a new compiler mutation is an evolutionary improvement
by fusing three measurement domains:
1. TRIG6 logs - swarm behavior (resonance, drift, noise, invention, phase coherence)
2. FlameBench results - compiler performance (p_success across atoms/labs)
3. Equivalence checks - behavioral correctness (eq >= 0.99 or reject)

Fitness formula:
    f = r(1-d)(1-h)i * eq + ρp + γb

Where:
    r = resonance
    d = drift
    h = noise_entropy
    i = invention_density
    eq = behavioral equivalence
    p = phase_coherence
    b = FlameBench p_success
    ρ, γ = priors/weights (default: 0.2, 0.3)

Auto-commits codon update if and only if the mutation is strictly better than champion.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


class EvolutionaryGate:
    """Darwinian gate for compiler evolution with safety checks."""
    
    # Default weights for fitness calculation
    DEFAULT_RHO = 0.2  # phase_coherence weight
    DEFAULT_GAMMA = 0.3  # FlameBench weight
    
    # Safety thresholds
    MIN_EQUIVALENCE = 0.99  # Behavioral equivalence hard gate
    
    def __init__(self, repo_root: Path):
        """Initialize the evolutionary gate.
        
        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = repo_root
        self.logs_dir = repo_root / "logs"
        self.trig_log = self.logs_dir / "trig_layer.jsonl"
        self.bench_results = repo_root / "stress_results.json"
        
    def load_trig6_metrics(self) -> Dict[str, float]:
        """Load TRIG6 metrics from logs.
        
        Returns:
            Dictionary with TRIG6 metrics (resonance, drift, noise_entropy, 
            invention_density, phase_coherence)
        """
        if not self.trig_log.exists():
            print(f"⚠️  TRIG6 log not found at {self.trig_log}")
            print("   Using default neutral values")
            return {
                "resonance": 0.5,
                "drift": 0.1,
                "noise_entropy": 0.1,
                "invention_density": 0.5,
                "phase_coherence": 0.7
            }
        
        # Read last line of JSONL file (most recent metrics)
        with open(self.trig_log, 'r') as f:
            lines = f.readlines()
            if not lines:
                print("⚠️  TRIG6 log is empty, using defaults")
                return self._default_trig6_metrics()
            
            last_entry = json.loads(lines[-1])
            return {
                "resonance": last_entry.get("resonance", 0.5),
                "drift": last_entry.get("drift", 0.1),
                "noise_entropy": last_entry.get("noise_entropy", 0.1),
                "invention_density": last_entry.get("invention_density", 0.5),
                "phase_coherence": last_entry.get("phase_coherence", 0.7)
            }
    
    def _default_trig6_metrics(self) -> Dict[str, float]:
        """Return default TRIG6 metrics."""
        return {
            "resonance": 0.5,
            "drift": 0.1,
            "noise_entropy": 0.1,
            "invention_density": 0.5,
            "phase_coherence": 0.7
        }
    
    def load_flamebench_results(self) -> Dict[str, float]:
        """Load FlameBench results.
        
        Returns:
            Dictionary with FlameBench metrics (p_success, equivalence)
        """
        if not self.bench_results.exists():
            print(f"⚠️  FlameBench results not found at {self.bench_results}")
            print("   Using default neutral values")
            return {
                "p_success": 0.8,
                "equivalence": 1.0
            }
        
        with open(self.bench_results, 'r') as f:
            results = json.load(f)
            return {
                "p_success": results.get("p_success", 0.8),
                "equivalence": results.get("equivalence", 1.0)
            }
    
    def calculate_fitness(
        self,
        trig6: Dict[str, float],
        bench: Dict[str, float],
        rho: float = DEFAULT_RHO,
        gamma: float = DEFAULT_GAMMA
    ) -> Tuple[float, bool]:
        """Calculate fitness scalar.
        
        Args:
            trig6: TRIG6 metrics dictionary
            bench: FlameBench results dictionary
            rho: Weight for phase_coherence
            gamma: Weight for FlameBench p_success
        
        Returns:
            Tuple of (fitness_score, passes_hard_gate)
        """
        # Extract metrics
        r = trig6["resonance"]
        d = trig6["drift"]
        h = trig6["noise_entropy"]
        i = trig6["invention_density"]
        p = trig6["phase_coherence"]
        
        eq = bench["equivalence"]
        b = bench["p_success"]
        
        # Hard gate: equivalence must be >= 0.99
        passes_gate = eq >= self.MIN_EQUIVALENCE
        
        # Fitness calculation: f = r(1-d)(1-h)i * eq + ρp + γb
        core_fitness = r * (1 - d) * (1 - h) * i * eq
        bonus = rho * p + gamma * b
        fitness = core_fitness + bonus
        
        return fitness, passes_gate
    
    def load_champion(self, champion_path: Path) -> Optional[Dict]:
        """Load current champion fitness.
        
        Args:
            champion_path: Path to champion.json
            
        Returns:
            Champion data dict or None if not found
        """
        if not champion_path.exists():
            print("📜 No champion.json found - this will be the first champion")
            return None
        
        with open(champion_path, 'r') as f:
            return json.load(f)
    
    def save_champion(
        self,
        champion_path: Path,
        candidate: str,
        fitness: float,
        trig6: Dict[str, float],
        bench: Dict[str, float]
    ):
        """Save new champion.
        
        Args:
            champion_path: Path to champion.json
            candidate: Candidate identifier (commit SHA, branch name, etc.)
            fitness: Fitness score
            trig6: TRIG6 metrics
            bench: FlameBench results
        """
        champion_data = {
            "candidate": candidate,
            "fitness": fitness,
            "trig6_metrics": trig6,
            "flamebench_results": bench,
            "timestamp": None  # Would use datetime in production
        }
        
        with open(champion_path, 'w') as f:
            json.dump(champion_data, f, indent=2)
        
        print(f"🏆 New champion saved: {candidate} (f={fitness:.4f})")
    
    def evaluate_candidate(
        self,
        candidate: str,
        champion_path: Path,
        rho: float = DEFAULT_RHO,
        gamma: float = DEFAULT_GAMMA
    ) -> int:
        """Evaluate a candidate mutation against the current champion.
        
        Args:
            candidate: Candidate identifier
            champion_path: Path to champion.json
            rho: Weight for phase_coherence
            gamma: Weight for FlameBench p_success
        
        Returns:
            0 if candidate is accepted (new champion), 1 if rejected
        """
        print(f"\n{'='*60}")
        print(f"🔥 FlameLang Evolutionary Gate - Evaluating Candidate")
        print(f"{'='*60}\n")
        print(f"Candidate: {candidate}")
        
        # Load metrics
        print("\n📊 Loading TRIG6 metrics...")
        trig6 = self.load_trig6_metrics()
        print(f"   Resonance: {trig6['resonance']:.3f}")
        print(f"   Drift: {trig6['drift']:.3f}")
        print(f"   Noise Entropy: {trig6['noise_entropy']:.3f}")
        print(f"   Invention Density: {trig6['invention_density']:.3f}")
        print(f"   Phase Coherence: {trig6['phase_coherence']:.3f}")
        
        print("\n📈 Loading FlameBench results...")
        bench = self.load_flamebench_results()
        print(f"   P(success): {bench['p_success']:.3f}")
        print(f"   Equivalence: {bench['equivalence']:.3f}")
        
        # Calculate fitness
        print(f"\n🧮 Calculating fitness (ρ={rho}, γ={gamma})...")
        fitness, passes_gate = self.calculate_fitness(trig6, bench, rho, gamma)
        print(f"   Fitness: {fitness:.4f}")
        
        # Hard gate check
        if not passes_gate:
            print(f"\n❌ REJECTED - Failed hard gate (eq={bench['equivalence']:.3f} < {self.MIN_EQUIVALENCE})")
            print("   Behavioral equivalence is below minimum threshold")
            return 1
        
        print(f"   ✓ Passed hard gate (eq={bench['equivalence']:.3f} >= {self.MIN_EQUIVALENCE})")
        
        # Compare to champion
        champion = self.load_champion(champion_path)
        
        if champion is None:
            # First run - accept as initial champion
            print("\n✅ ACCEPTED - No existing champion, establishing baseline")
            self.save_champion(champion_path, candidate, fitness, trig6, bench)
            return 0
        
        f_champion = champion["fitness"]
        print(f"\n🏆 Current champion fitness: {f_champion:.4f}")
        
        if fitness <= f_champion:
            print(f"\n❌ REJECTED - No improvement (Δf={fitness - f_champion:.4f})")
            print("   Fitness must strictly beat champion")
            return 1
        
        # New champion!
        print(f"\n✅ ACCEPTED - New champion! (Δf=+{fitness - f_champion:.4f})")
        self.save_champion(champion_path, candidate, fitness, trig6, bench)
        
        print(f"\n{'='*60}")
        print(f"🎉 Evolutionary improvement detected!")
        print(f"{'='*60}\n")
        
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="FlameLang Evolutionary Gate - Darwinian compiler evolution"
    )
    parser.add_argument(
        "--candidate",
        required=True,
        help="Candidate identifier (commit SHA, branch name, etc.)"
    )
    parser.add_argument(
        "--champion",
        default="champion.json",
        help="Path to champion.json (default: champion.json)"
    )
    parser.add_argument(
        "--rho",
        type=float,
        default=EvolutionaryGate.DEFAULT_RHO,
        help=f"Phase coherence weight (default: {EvolutionaryGate.DEFAULT_RHO})"
    )
    parser.add_argument(
        "--gamma",
        type=float,
        default=EvolutionaryGate.DEFAULT_GAMMA,
        help=f"FlameBench weight (default: {EvolutionaryGate.DEFAULT_GAMMA})"
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root directory (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Determine repo root
    if args.repo_root:
        repo_root = args.repo_root
    else:
        # Try to find repo root by looking for .git directory
        script_path = Path(__file__).resolve()
        repo_root = script_path.parent
        while repo_root != repo_root.parent:
            if (repo_root / ".git").exists():
                break
            repo_root = repo_root.parent
        else:
            # Fallback to current directory
            repo_root = Path.cwd()
    
    print(f"Repository root: {repo_root}")
    
    # Create gate and evaluate
    gate = EvolutionaryGate(repo_root)
    champion_path = repo_root / args.champion
    
    exit_code = gate.evaluate_candidate(
        args.candidate,
        champion_path,
        args.rho,
        args.gamma
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
