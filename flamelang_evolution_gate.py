#!/usr/bin/env python3
"""
🧬 FLAMELANG EVOLUTION GATE v1.0
Darwinian Compiler Evolution with Fitness Selection

Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
Inventor: Domenic Gabriel Garza (Dom / Me10101)
Generated: 2026-01-25

This module implements the evolution gate for FlameLang compiler optimization.
Each zyBooks lab becomes a new gene, with fitness-based selection.
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CompilerCandidate:
    """Represents a compiler candidate (mutation)"""
    name: str
    version: str
    gene_source: str  # e.g., "zyBooks Lab 3.14"
    equivalence: float  # Test pass rate [0-1], must be >= 0.99
    resonance_score: float  # From TRIG6
    drift_score: float
    noise_entropy: float
    invention_density: float
    phase_coherence: float  # Wave phase alignment
    flamebench_p_success: float  # FlameBench probability of success
    timestamp: str
    
    def __str__(self):
        return f"{self.name} v{self.version} (eq={self.equivalence:.3f}, fitness={self.compute_fitness():.3f})"


class FlameLangEvolutionGate:
    """
    Evolution Gate for FlameLang Compiler
    
    Uses Darwinian selection to evolve the compiler through lab exercises.
    Each lab generates a new candidate gene that must pass fitness evaluation.
    """
    
    # Fitness function weights
    RHO = 0.3  # Phase coherence weight
    GAMMA = 0.3  # FlameBench weight
    
    # Hard gate: equivalence must be >= 0.99
    MIN_EQUIVALENCE = 0.99
    
    # Champion must be beaten by at least 2% to be replaced
    MIN_FITNESS_IMPROVEMENT = 0.02
    
    def __init__(self):
        """Initialize evolution gate"""
        self.champion: Optional[CompilerCandidate] = None
        self.generation = 0
        self.history = []
        
    def compute_fitness(
        self,
        resonance: float,
        drift: float,
        noise_entropy: float,
        invention_density: float,
        equivalence: float,
        phase_coherence: float,
        flamebench_p_success: float
    ) -> float:
        """
        Compute fitness function for compiler candidate
        
        Formula:
            f = r * (1-d) * (1-h) * i * eq + ρ*p + γ*b
        
        Where:
            r  = resonance_score (TRIG6)
            d  = drift_score
            h  = noise_entropy (normalized)
            i  = invention_density
            eq = equivalence (test pass rate, must be ≥0.99)
            p  = phase_coherence
            b  = FlameBench p_success
            ρ  = prior weight for phase coherence (0.3)
            γ  = prior weight for FlameBench (0.3)
        
        Returns:
            Fitness score [0-∞], higher is better
        """
        # Normalize noise entropy (typical range 0-3)
        h_norm = min(noise_entropy / 3.0, 1.0)
        
        # Core fitness components
        core = resonance * (1 - drift) * (1 - h_norm) * invention_density * equivalence
        
        # Prior contributions
        priors = self.RHO * phase_coherence + self.GAMMA * flamebench_p_success
        
        # Total fitness
        fitness = core + priors
        
        return fitness
    
    def evaluate_candidate(self, candidate: CompilerCandidate) -> Tuple[bool, str, float]:
        """
        Evaluate a compiler candidate through the evolution gate
        
        Returns:
            Tuple of (accepted, reason, fitness)
        """
        # HARD GATE: Check equivalence (correctness)
        if candidate.equivalence < self.MIN_EQUIVALENCE:
            reason = f"❌ REJECTED: Equivalence {candidate.equivalence:.3f} < {self.MIN_EQUIVALENCE} (correctness gate)"
            return False, reason, 0.0
        
        # Compute fitness
        fitness = self.compute_fitness(
            resonance=candidate.resonance_score,
            drift=candidate.drift_score,
            noise_entropy=candidate.noise_entropy,
            invention_density=candidate.invention_density,
            equivalence=candidate.equivalence,
            phase_coherence=candidate.phase_coherence,
            flamebench_p_success=candidate.flamebench_p_success
        )
        
        # If no champion exists, accept first valid candidate
        if self.champion is None:
            reason = f"✅ ACCEPTED: First champion (fitness={fitness:.3f})"
            return True, reason, fitness
        
        # Compute champion fitness
        champion_fitness = self.compute_fitness(
            resonance=self.champion.resonance_score,
            drift=self.champion.drift_score,
            noise_entropy=self.champion.noise_entropy,
            invention_density=self.champion.invention_density,
            equivalence=self.champion.equivalence,
            phase_coherence=self.champion.phase_coherence,
            flamebench_p_success=self.champion.flamebench_p_success
        )
        
        # Check if candidate beats champion by threshold
        improvement = fitness - champion_fitness
        
        if improvement > self.MIN_FITNESS_IMPROVEMENT:
            reason = f"✅ ACCEPTED: Beats champion by {improvement:.3f} (threshold={self.MIN_FITNESS_IMPROVEMENT})"
            return True, reason, fitness
        else:
            reason = f"❌ REJECTED: Improvement {improvement:.3f} < threshold {self.MIN_FITNESS_IMPROVEMENT}"
            return False, reason, fitness
    
    def submit_candidate(self, candidate: CompilerCandidate) -> Dict:
        """
        Submit a candidate to the evolution gate
        
        Returns:
            Dict with evaluation results
        """
        self.generation += 1
        
        # Evaluate candidate
        accepted, reason, fitness = self.evaluate_candidate(candidate)
        
        # Record in history
        result = {
            'generation': self.generation,
            'candidate': candidate,
            'accepted': accepted,
            'reason': reason,
            'fitness': fitness,
            'timestamp': datetime.now().isoformat()
        }
        self.history.append(result)
        
        # If accepted, update champion
        if accepted:
            old_champion = self.champion
            self.champion = candidate
            result['old_champion'] = old_champion
            result['new_champion'] = candidate
        
        return result
    
    def generate_report(self) -> str:
        """Generate evolution gate report"""
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              FLAMELANG EVOLUTION GATE REPORT v1.0                            ║
║                  Darwinian Compiler Evolution                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generation: {self.generation}
Total Submissions: {len(self.history)}

════════════════════════════════════════════════════════════════════════════════
CURRENT CHAMPION
════════════════════════════════════════════════════════════════════════════════
"""
        
        if self.champion:
            champ_fitness = self.compute_fitness(
                resonance=self.champion.resonance_score,
                drift=self.champion.drift_score,
                noise_entropy=self.champion.noise_entropy,
                invention_density=self.champion.invention_density,
                equivalence=self.champion.equivalence,
                phase_coherence=self.champion.phase_coherence,
                flamebench_p_success=self.champion.flamebench_p_success
            )
            
            report += f"""
Name:                {self.champion.name}
Version:             {self.champion.version}
Gene Source:         {self.champion.gene_source}
Fitness:             {champ_fitness:.4f}

Metrics:
  Equivalence:       {self.champion.equivalence:.3f} {'✅' if self.champion.equivalence >= self.MIN_EQUIVALENCE else '❌'}
  Resonance:         {self.champion.resonance_score:.3f}
  Drift:             {self.champion.drift_score:.3f}
  Noise Entropy:     {self.champion.noise_entropy:.3f}
  Invention Density: {self.champion.invention_density:.3f}
  Phase Coherence:   {self.champion.phase_coherence:.3f}
  FlameBench:        {self.champion.flamebench_p_success:.3f}

Timestamp:           {self.champion.timestamp}
"""
        else:
            report += "\nNo champion yet. Awaiting first valid candidate.\n"
        
        # Statistics
        accepted = sum(1 for h in self.history if h['accepted'])
        rejected = len(self.history) - accepted
        
        report += f"""
════════════════════════════════════════════════════════════════════════════════
STATISTICS
════════════════════════════════════════════════════════════════════════════════
Total Submissions:   {len(self.history)}
Accepted:            {accepted} ({accepted/len(self.history)*100:.1f}% if len(self.history) > 0 else 0)
Rejected:            {rejected} ({rejected/len(self.history)*100:.1f}% if len(self.history) > 0 else 0)
"""
        
        # Recent submissions (last 5)
        if self.history:
            report += f"""
════════════════════════════════════════════════════════════════════════════════
RECENT SUBMISSIONS (Last 5)
════════════════════════════════════════════════════════════════════════════════
"""
            for entry in self.history[-5:]:
                status = "✅ ACCEPTED" if entry['accepted'] else "❌ REJECTED"
                report += f"\nGen {entry['generation']}: {entry['candidate'].name} v{entry['candidate'].version}\n"
                report += f"  {status}\n"
                report += f"  Fitness: {entry['fitness']:.4f}\n"
                report += f"  Reason: {entry['reason']}\n"
        
        report += f"""
════════════════════════════════════════════════════════════════════════════════
FITNESS FUNCTION
════════════════════════════════════════════════════════════════════════════════
f = r * (1-d) * (1-h) * i * eq + ρ*p + γ*b

Where:
  r  = resonance_score (TRIG6)
  d  = drift_score
  h  = noise_entropy (normalized)
  i  = invention_density
  eq = equivalence (test pass rate, MUST be ≥ {self.MIN_EQUIVALENCE})
  p  = phase_coherence
  b  = FlameBench p_success
  ρ  = {self.RHO} (phase weight)
  γ  = {self.GAMMA} (bench weight)

Selection Rule:
  IF eq < {self.MIN_EQUIVALENCE}: REJECT (hard gate - correctness)
  IF fitness(candidate) > fitness(champion) + {self.MIN_FITNESS_IMPROVEMENT}: ACCEPT
  ELSE: REJECT (keep champion)

════════════════════════════════════════════════════════════════════════════════
🧬 Evolution Gate Report Complete
════════════════════════════════════════════════════════════════════════════════
"""
        
        return report


def main():
    """Demo of FlameLang Evolution Gate"""
    print("🧬 FlameLang Evolution Gate v1.0 - Demo\n")
    
    gate = FlameLangEvolutionGate()
    
    # Candidate 1: First valid candidate (becomes champion)
    print("=" * 80)
    print("Submission 1: FlameLang v2.0.0 (zyBooks Lab 1.1)")
    print("=" * 80)
    
    candidate1 = CompilerCandidate(
        name="FlameLang",
        version="2.0.0",
        gene_source="zyBooks Lab 1.1 - Basic Arithmetic",
        equivalence=0.99,  # Passes all tests
        resonance_score=0.75,
        drift_score=0.20,
        noise_entropy=0.50,
        invention_density=0.05,
        phase_coherence=0.80,
        flamebench_p_success=0.85,
        timestamp=datetime.now().isoformat()
    )
    
    result1 = gate.submit_candidate(candidate1)
    print(f"\n{result1['reason']}")
    print(f"Fitness: {result1['fitness']:.4f}")
    
    # Candidate 2: Failed equivalence (rejected)
    print("\n" + "=" * 80)
    print("Submission 2: FlameLang v2.0.1 (zyBooks Lab 2.3 - Loops)")
    print("=" * 80)
    
    candidate2 = CompilerCandidate(
        name="FlameLang",
        version="2.0.1",
        gene_source="zyBooks Lab 2.3 - Loops",
        equivalence=0.97,  # FAILED! < 0.99
        resonance_score=0.85,
        drift_score=0.15,
        noise_entropy=0.40,
        invention_density=0.08,
        phase_coherence=0.85,
        flamebench_p_success=0.90,
        timestamp=datetime.now().isoformat()
    )
    
    result2 = gate.submit_candidate(candidate2)
    print(f"\n{result2['reason']}")
    print(f"Fitness: {result2['fitness']:.4f}")
    
    # Candidate 3: Better fitness (accepted)
    print("\n" + "=" * 80)
    print("Submission 3: FlameLang v2.1.0 (zyBooks Lab 3.7 - Recursion)")
    print("=" * 80)
    
    candidate3 = CompilerCandidate(
        name="FlameLang",
        version="2.1.0",
        gene_source="zyBooks Lab 3.7 - Recursion",
        equivalence=1.00,  # Perfect!
        resonance_score=0.88,
        drift_score=0.10,
        noise_entropy=0.35,
        invention_density=0.12,
        phase_coherence=0.90,
        flamebench_p_success=0.92,
        timestamp=datetime.now().isoformat()
    )
    
    result3 = gate.submit_candidate(candidate3)
    print(f"\n{result3['reason']}")
    print(f"Fitness: {result3['fitness']:.4f}")
    
    # Candidate 4: Slightly better but not enough (rejected)
    print("\n" + "=" * 80)
    print("Submission 4: FlameLang v2.1.1 (zyBooks Lab 4.2 - Arrays)")
    print("=" * 80)
    
    candidate4 = CompilerCandidate(
        name="FlameLang",
        version="2.1.1",
        gene_source="zyBooks Lab 4.2 - Arrays",
        equivalence=1.00,
        resonance_score=0.89,  # Slightly better
        drift_score=0.10,
        noise_entropy=0.35,
        invention_density=0.12,
        phase_coherence=0.91,
        flamebench_p_success=0.92,
        timestamp=datetime.now().isoformat()
    )
    
    result4 = gate.submit_candidate(candidate4)
    print(f"\n{result4['reason']}")
    print(f"Fitness: {result4['fitness']:.4f}")
    
    # Generate final report
    print("\n" + "=" * 80)
    print("EVOLUTION GATE SUMMARY")
    print("=" * 80)
    print(gate.generate_report())
    
    print("\n🔥 Evolution Gate Demo Complete")


if __name__ == "__main__":
    main()
