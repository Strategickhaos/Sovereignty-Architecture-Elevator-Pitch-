#!/usr/bin/env python3
"""
FlameLang Evolutionary Gate v1.0
Natural selection for compiler micro-evolution

DNA Strand: TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1

Selection Criteria:
- Hard gates (must pass ALL):
  * eq < 0.99   (equivalence drift)
  * noise > 0.25 (entropy injection)
  * drift > 0.35 (behavioral variance)
  * coherence < 0.70 (anti-brittleness)

- Soft fitness scalar:
  f = r(1-d)(1-h)·i·eq + ρp + γb
  where:
    r  = resilience score
    d  = drift magnitude
    h  = noise level
    i  = innovation metric
    eq = equivalence score
    ρ  = performance weight
    p  = performance score
    γ  = bias correction weight
    b  = bias score

Champion Comparison:
- f > f_champion → commit with codon tagging
- f ≤ f_champion → reject, keep champion

Auto-commit with codon tagging for DNA strand tracking.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Metrics:
    """Test metrics for evolutionary fitness evaluation"""
    equivalence: float      # eq - correctness vs reference
    noise: float           # h - entropy/stochastic behavior
    drift: float           # d - behavioral variance
    coherence: float       # anti-brittleness measure
    resilience: float      # r - error recovery
    innovation: float      # i - novel solution quality
    performance: float     # p - speed/efficiency
    bias: float           # b - fairness/bias correction


@dataclass
class FitnessWeights:
    """Weights for fitness function components"""
    rho: float = 0.3      # ρ - performance weight
    gamma: float = 0.1    # γ - bias correction weight


class EvoGate:
    """Evolutionary gate for compiler natural selection"""
    
    # Hard gate thresholds
    HARD_GATES = {
        'equivalence_max': 0.99,    # Must have some variation
        'noise_min': 0.25,          # Must inject entropy
        'drift_min': 0.35,          # Must show behavioral variance
        'coherence_max': 0.70,      # Must avoid brittleness
    }
    
    def __init__(self, champion_file: str = ".champion_fitness.json"):
        self.champion_file = Path(champion_file)
        self.weights = FitnessWeights()
        self.champion_fitness = self._load_champion()
    
    def _load_champion(self) -> Optional[float]:
        """Load current champion fitness score"""
        if self.champion_file.exists():
            try:
                with open(self.champion_file) as f:
                    data = json.load(f)
                    return data.get('fitness')
            except (json.JSONDecodeError, IOError):
                return None
        return None
    
    def _save_champion(self, fitness: float, metrics: Metrics, codon: str):
        """Save new champion with metadata"""
        data = {
            'fitness': fitness,
            'timestamp': datetime.now().isoformat(),
            'codon': codon,
            'metrics': {
                'equivalence': metrics.equivalence,
                'noise': metrics.noise,
                'drift': metrics.drift,
                'coherence': metrics.coherence,
                'resilience': metrics.resilience,
                'innovation': metrics.innovation,
                'performance': metrics.performance,
                'bias': metrics.bias,
            }
        }
        with open(self.champion_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def check_hard_gates(self, metrics: Metrics) -> Tuple[bool, str]:
        """
        Check if candidate passes all hard gates
        
        Returns:
            (passed: bool, reason: str)
        """
        if metrics.equivalence >= self.HARD_GATES['equivalence_max']:
            return False, f"equivalence too high: {metrics.equivalence:.3f} >= {self.HARD_GATES['equivalence_max']}"
        
        if metrics.noise < self.HARD_GATES['noise_min']:
            return False, f"noise too low: {metrics.noise:.3f} < {self.HARD_GATES['noise_min']}"
        
        if metrics.drift < self.HARD_GATES['drift_min']:
            return False, f"drift too low: {metrics.drift:.3f} < {self.HARD_GATES['drift_min']}"
        
        if metrics.coherence >= self.HARD_GATES['coherence_max']:
            return False, f"coherence too high: {metrics.coherence:.3f} >= {self.HARD_GATES['coherence_max']}"
        
        return True, "All hard gates passed"
    
    def calculate_fitness(self, metrics: Metrics) -> float:
        """
        Calculate fitness score using soft scalar formula
        
        f = r(1-d)(1-h)·i·eq + ρp + γb
        """
        # Core fitness: resilience × anti-drift × anti-noise × innovation × equivalence
        core = (metrics.resilience * 
                (1 - metrics.drift) * 
                (1 - metrics.noise) * 
                metrics.innovation * 
                metrics.equivalence)
        
        # Performance component
        performance_component = self.weights.rho * metrics.performance
        
        # Bias correction component
        bias_component = self.weights.gamma * metrics.bias
        
        fitness = core + performance_component + bias_component
        
        return fitness
    
    def evaluate(self, metrics: Metrics, codon: str) -> Tuple[bool, str, float]:
        """
        Full evaluation: hard gates + fitness comparison
        
        Returns:
            (accept: bool, reason: str, fitness: float)
        """
        # Check hard gates first
        passed, reason = self.check_hard_gates(metrics)
        if not passed:
            return False, f"Hard gate failed: {reason}", 0.0
        
        # Calculate fitness
        fitness = self.calculate_fitness(metrics)
        
        # Compare with champion
        if self.champion_fitness is None:
            # First candidate becomes champion
            self._save_champion(fitness, metrics, codon)
            return True, f"First champion established: f={fitness:.4f}", fitness
        
        if fitness > self.champion_fitness:
            # New champion!
            improvement = ((fitness - self.champion_fitness) / self.champion_fitness) * 100
            self._save_champion(fitness, metrics, codon)
            return True, f"New champion! f={fitness:.4f} (↑{improvement:.2f}%), previous={self.champion_fitness:.4f}", fitness
        else:
            # Rejected
            deficit = ((self.champion_fitness - fitness) / self.champion_fitness) * 100
            return False, f"Rejected: f={fitness:.4f} (↓{deficit:.2f}%), champion={self.champion_fitness:.4f}", fitness
    
    def auto_commit(self, codon: str, fitness: float, message: str = None):
        """
        Auto-commit with codon tagging for DNA strand tracking
        """
        if message is None:
            message = f"Evolution: {codon} | fitness={fitness:.4f}"
        
        try:
            # Stage all changes
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            
            # Commit with codon tag
            commit_msg = f"[{codon}] {message}"
            subprocess.run(['git', 'commit', '-m', commit_msg], 
                         check=True, capture_output=True)
            
            print(f"✓ Auto-committed: {commit_msg}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Auto-commit failed: {e}", file=sys.stderr)
            return False


def load_metrics_from_file(metrics_file: str) -> Metrics:
    """Load metrics from JSON file"""
    with open(metrics_file) as f:
        data = json.load(f)
    
    return Metrics(
        equivalence=data.get('equivalence', 0.0),
        noise=data.get('noise', 0.0),
        drift=data.get('drift', 0.0),
        coherence=data.get('coherence', 0.0),
        resilience=data.get('resilience', 0.0),
        innovation=data.get('innovation', 0.0),
        performance=data.get('performance', 0.0),
        bias=data.get('bias', 0.0),
    )


def main():
    """Main entry point for evolutionary gate"""
    if len(sys.argv) < 3:
        print("Usage: flamelang_evo_gate.py <metrics.json> <codon>")
        print("\nExample:")
        print("  flamelang_evo_gate.py test_results.json TRIG6-001")
        sys.exit(1)
    
    metrics_file = sys.argv[1]
    codon = sys.argv[2]
    
    # Load metrics
    try:
        metrics = load_metrics_from_file(metrics_file)
    except Exception as e:
        print(f"✗ Failed to load metrics: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Create gate and evaluate
    gate = EvoGate()
    
    print("=" * 60)
    print("FlameLang Evolutionary Gate v1.0")
    print("=" * 60)
    print(f"Candidate: {codon}")
    print(f"\nMetrics:")
    print(f"  equivalence: {metrics.equivalence:.3f}")
    print(f"  noise:       {metrics.noise:.3f}")
    print(f"  drift:       {metrics.drift:.3f}")
    print(f"  coherence:   {metrics.coherence:.3f}")
    print(f"  resilience:  {metrics.resilience:.3f}")
    print(f"  innovation:  {metrics.innovation:.3f}")
    print(f"  performance: {metrics.performance:.3f}")
    print(f"  bias:        {metrics.bias:.3f}")
    
    # Evaluate
    accept, reason, fitness = gate.evaluate(metrics, codon)
    
    print(f"\n{'=' * 60}")
    print(f"Result: {'✓ ACCEPTED' if accept else '✗ REJECTED'}")
    print(f"Fitness: {fitness:.4f}")
    print(f"Reason: {reason}")
    print(f"{'=' * 60}")
    
    if accept:
        # Auto-commit if accepted
        if gate.auto_commit(codon, fitness, reason):
            print(f"\n🧬 DNA strand updated with codon: {codon}")
        sys.exit(0)
    else:
        print(f"\n🚫 Mutation rejected. Champion retained.")
        sys.exit(1)


if __name__ == '__main__':
    main()
