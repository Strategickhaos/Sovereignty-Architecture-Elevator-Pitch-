#!/usr/bin/env python3
"""
F1 - Bounded Product Lemma
A trivial but correct product inequality: Γ ≤ 1
Provides stability/decay bounds for sequences

Mathematical Foundation:
Given three stepwise multiplicative bounds, you get a 3-step bound:
F_{n+3} ≥ F_n · Γ

This is a legit little lemma about stability/decay of a sequence.
NOT cosmology. Just math about sequences.
"""

from dataclasses import dataclass
from typing import List, Optional
import math


@dataclass
class SequenceBound:
    """Bound for a sequence value"""
    index: int
    value: float
    gamma: float  # Multiplicative bound factor


class F1Lemma:
    """
    F1 Bounded Product Lemma
    
    For a sequence {F_n} with multiplicative bounds Γ_i ≤ 1:
    F_{n+k} ≥ F_n · Γ_1 · Γ_2 · ... · Γ_k
    
    Special case (k=3):
    F_{n+3} ≥ F_n · Γ
    where Γ = Γ_1 · Γ_2 · Γ_3 ≤ 1
    
    This is useful for:
    - Proving stability bounds in iterative systems
    - Tracking decay rates in resource allocation
    - Establishing convergence properties
    """
    
    def __init__(self):
        self.history: List[SequenceBound] = []
    
    @staticmethod
    def validate_gamma(gamma: float) -> bool:
        """
        Validate that Γ ≤ 1
        
        This is the core constraint of F1.
        If Γ > 1, the system is growing, not stable/decaying.
        """
        return 0 <= gamma <= 1
    
    @staticmethod
    def compute_product_bound(gammas: List[float]) -> float:
        """
        Compute product bound Γ = Γ_1 · Γ_2 · ... · Γ_k
        
        Args:
            gammas: List of individual bounds, each ≤ 1
        
        Returns:
            Product Γ ≤ 1
        
        Raises:
            ValueError: If any gamma > 1
        """
        if not all(0 <= g <= 1 for g in gammas):
            raise ValueError("All gammas must be in [0, 1]")
        
        product = 1.0
        for g in gammas:
            product *= g
        
        return product
    
    @staticmethod
    def compute_3step_bound(F_n: float, gamma1: float, gamma2: float, gamma3: float) -> float:
        """
        Compute 3-step bound: F_{n+3} ≥ F_n · Γ
        
        Args:
            F_n: Initial value
            gamma1, gamma2, gamma3: Three multiplicative bounds
        
        Returns:
            Lower bound for F_{n+3}
        """
        gamma = F1Lemma.compute_product_bound([gamma1, gamma2, gamma3])
        return F_n * gamma
    
    @staticmethod
    def compute_kstep_bound(F_n: float, gammas: List[float]) -> float:
        """
        Compute k-step bound: F_{n+k} ≥ F_n · Γ
        
        Args:
            F_n: Initial value
            gammas: k multiplicative bounds
        
        Returns:
            Lower bound for F_{n+k}
        """
        gamma = F1Lemma.compute_product_bound(gammas)
        return F_n * gamma
    
    def add_bound(self, index: int, value: float, gamma: float) -> SequenceBound:
        """
        Add a sequence bound to history
        
        Args:
            index: Sequence index
            value: Value at this index
            gamma: Multiplicative bound for next step
        
        Returns:
            SequenceBound
        """
        if not self.validate_gamma(gamma):
            raise ValueError(f"Gamma must be ≤ 1, got {gamma}")
        
        bound = SequenceBound(index=index, value=value, gamma=gamma)
        self.history.append(bound)
        return bound
    
    def verify_bound(self, n: int, k: int) -> Optional[dict]:
        """
        Verify bound: F_{n+k} ≥ F_n · Γ
        
        Args:
            n: Starting index
            k: Step size
        
        Returns:
            dict with verification results, or None if insufficient data
        """
        # Find bounds at index n and n+k
        bound_n = next((b for b in self.history if b.index == n), None)
        bound_nk = next((b for b in self.history if b.index == n + k), None)
        
        if not bound_n or not bound_nk:
            return None
        
        # Get gammas between n and n+k
        gammas = [b.gamma for b in self.history if n <= b.index < n + k]
        
        if len(gammas) != k:
            return None
        
        # Compute expected lower bound
        expected_lower_bound = self.compute_kstep_bound(bound_n.value, gammas)
        
        # Verify
        satisfied = bound_nk.value >= expected_lower_bound
        
        return {
            'n': n,
            'k': k,
            'F_n': bound_n.value,
            'F_nk': bound_nk.value,
            'gammas': gammas,
            'product_gamma': self.compute_product_bound(gammas),
            'expected_lower_bound': expected_lower_bound,
            'satisfied': satisfied,
            'margin': bound_nk.value - expected_lower_bound
        }
    
    def get_stability_rate(self, window: int = 3) -> Optional[float]:
        """
        Get average stability rate (Γ) over recent window
        
        Args:
            window: Number of recent steps to average
        
        Returns:
            Average Γ, or None if insufficient data
        """
        if len(self.history) < window:
            return None
        
        recent = self.history[-window:]
        gammas = [b.gamma for b in recent]
        return self.compute_product_bound(gammas)
    
    def predict_value(self, n: int, k: int) -> Optional[float]:
        """
        Predict F_{n+k} using bound
        
        This gives a conservative (lower bound) estimate.
        Actual value may be higher.
        
        Args:
            n: Current index (must be in history)
            k: Steps ahead to predict
        
        Returns:
            Predicted lower bound, or None if can't predict
        """
        bound_n = next((b for b in self.history if b.index == n), None)
        if not bound_n:
            return None
        
        # Use the k most recent gammas for prediction
        # Filter to bounds at or after index (n - k) to get recent context
        recent_gammas = [b.gamma for b in self.history if b.index >= (n - k + 1) and b.index <= n]
        
        if not recent_gammas:
            # Fallback to last known gamma if no recent history
            recent_gammas = [self.history[-1].gamma] * k
        
        # Pad or trim to exactly k elements
        if len(recent_gammas) < k:
            # Pad with the last gamma
            recent_gammas = recent_gammas + [recent_gammas[-1]] * (k - len(recent_gammas))
        else:
            # Trim to k most recent
            recent_gammas = recent_gammas[-k:]
        
        return self.compute_kstep_bound(bound_n.value, recent_gammas)


def gamma_from_health_score(f_current: float, f_previous: float) -> float:
    """
    Compute Γ from health score ratio
    
    If health is declining: Γ < 1
    If health is stable: Γ ≈ 1
    If health is improving: Γ = 1 (capped)
    
    Args:
        f_current: Current health score
        f_previous: Previous health score
    
    Returns:
        Γ ∈ [0, 1]
    """
    if f_previous == 0:
        return 1.0 if f_current > 0 else 0.0
    
    ratio = f_current / f_previous
    # Cap at 1.0 (F1 assumes Γ ≤ 1)
    return min(1.0, max(0.0, ratio))


if __name__ == "__main__":
    # Demo usage
    print("📐 F1 Bounded Product Lemma Demo")
    print("=" * 60)
    
    f1 = F1Lemma()
    
    print("\n🔹 Scenario 1: Stable system (Γ ≈ 0.95)")
    print("   Simulating a slowly degrading system")
    
    # Simulate sequence with slight degradation
    values = [100.0]
    gamma = 0.95
    for i in range(10):
        f1.add_bound(i, values[-1], gamma)
        values.append(values[-1] * gamma)
    
    # Verify 3-step bound
    verification = f1.verify_bound(0, 3)
    if verification:
        print(f"\n   3-step verification (n=0, k=3):")
        print(f"   F_0 = {verification['F_n']:.2f}")
        print(f"   F_3 = {verification['F_nk']:.2f}")
        print(f"   Γ = {verification['product_gamma']:.4f}")
        print(f"   Expected lower bound = {verification['expected_lower_bound']:.2f}")
        print(f"   Satisfied: {verification['satisfied']} ✅" if verification['satisfied'] else "   Satisfied: {verification['satisfied']} ❌")
        print(f"   Margin: {verification['margin']:.2f}")
    
    # Predict future value
    prediction = f1.predict_value(7, 3)
    if prediction:
        print(f"\n   Prediction for F_10 (from F_7):")
        print(f"   Lower bound: {prediction:.2f}")
        print(f"   Actual F_10: {values[10]:.2f}")
        print(f"   Conservative: {prediction <= values[10]} ✅")
    
    print("\n🔹 Scenario 2: From TRIG6 health scores")
    print("   Using health score ratios as Γ")
    
    # Simulate health scores over time
    health_scores = [0.85, 0.82, 0.80, 0.78, 0.77, 0.76]
    f1_health = F1Lemma()
    
    for i, score in enumerate(health_scores):
        if i == 0:
            gamma = 1.0
        else:
            gamma = gamma_from_health_score(score, health_scores[i-1])
        f1_health.add_bound(i, score, gamma)
        print(f"   t={i}: f={score:.3f}, Γ={gamma:.4f}")
    
    # Get stability rate
    stability = f1_health.get_stability_rate(window=3)
    if stability:
        print(f"\n   Recent stability rate (3-step): Γ={stability:.4f}")
        print(f"   Interpretation: System losing {(1-stability)*100:.2f}% health per step")
    
    print("\n✅ F1 Lemma operational")
    print("\n📝 Remember: F1 is NOT cosmology.")
    print("   It's a bounded product inequality (Γ ≤ 1).")
    print("   Useful for stability tracking, not universal truth. 🎯")
