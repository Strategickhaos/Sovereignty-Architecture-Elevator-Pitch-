"""
Convergence Analyzer - Fitness and Stability Analysis

Analyzes convergence of efficiency claims and calculates fitness scores.
Determines when proofs are stable and reproducible.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
import statistics


@dataclass
class ConvergenceResult:
    """Result of convergence analysis"""
    converged: bool
    fitness: float
    stability: float
    mean_efficiency: float
    std_deviation: float
    sample_count: int


class ConvergenceAnalyzer:
    """
    Analyzes convergence and stability of efficiency measurements
    
    Used to determine when proof claims are stable enough to certify.
    """
    
    def __init__(self, convergence_threshold: float = 0.90):
        self.convergence_threshold = convergence_threshold
    
    def analyze(self, efficiency_samples: List[float]) -> ConvergenceResult:
        """
        Analyze convergence of efficiency samples
        
        Args:
            efficiency_samples: List of efficiency measurements
        
        Returns:
            ConvergenceResult with analysis
        """
        if len(efficiency_samples) < 3:
            # Need at least 3 samples for meaningful analysis
            return ConvergenceResult(
                converged=False,
                fitness=0.0,
                stability=0.0,
                mean_efficiency=0.0,
                std_deviation=0.0,
                sample_count=len(efficiency_samples)
            )
        
        # Calculate statistics
        mean_eff = statistics.mean(efficiency_samples)
        std_dev = statistics.stdev(efficiency_samples)
        
        # Calculate stability (inverse of coefficient of variation)
        # Low std dev relative to mean = high stability
        if mean_eff > 0:
            coefficient_of_variation = std_dev / mean_eff
            stability = max(0, 1 - coefficient_of_variation)
        else:
            stability = 0
        
        # Calculate fitness
        # Combines mean efficiency and stability
        fitness = self._calculate_fitness(mean_eff, stability, std_dev)
        
        # Check convergence
        converged = fitness >= self.convergence_threshold
        
        return ConvergenceResult(
            converged=converged,
            fitness=fitness,
            stability=stability,
            mean_efficiency=mean_eff,
            std_deviation=std_dev,
            sample_count=len(efficiency_samples)
        )
    
    def _calculate_fitness(self, 
                          mean_eff: float, 
                          stability: float,
                          std_dev: float) -> float:
        """
        Calculate fitness score
        
        Fitness combines:
        - Mean efficiency (60% weight)
        - Stability (30% weight)
        - Low variance bonus (10% weight)
        
        Returns:
            Fitness score (0-1)
        """
        # Component 1: Mean efficiency (0-0.6)
        eff_component = mean_eff * 0.6
        
        # Component 2: Stability (0-0.3)
        stability_component = stability * 0.3
        
        # Component 3: Low variance bonus (0-0.1)
        # Reward std dev < 0.05 (5% variance)
        variance_bonus = max(0, (0.05 - std_dev) / 0.05) * 0.1
        
        fitness = eff_component + stability_component + variance_bonus
        
        return min(fitness, 1.0)
    
    def check_ratio_convergence(self,
                                code_samples: List[float],
                                gui_samples: List[float]) -> Dict:
        """
        Check convergence of efficiency ratio between two workflows
        
        Args:
            code_samples: Efficiency samples for code workflow
            gui_samples: Efficiency samples for GUI workflow
        
        Returns:
            Dict with ratio convergence analysis
        """
        # Analyze individual convergence
        code_result = self.analyze(code_samples)
        gui_result = self.analyze(gui_samples)
        
        # Calculate ratio stability
        ratios = [c / g if g > 0 else float('inf') 
                 for c, g in zip(code_samples, gui_samples)]
        
        mean_ratio = statistics.mean([r for r in ratios if r != float('inf')])
        
        if len([r for r in ratios if r != float('inf')]) > 1:
            ratio_std = statistics.stdev([r for r in ratios if r != float('inf')])
        else:
            ratio_std = 0
        
        # Overall fitness is minimum of both workflows
        overall_fitness = min(code_result.fitness, gui_result.fitness)
        
        # Check if ratio is stable (< 10% variation)
        ratio_stable = (ratio_std / mean_ratio) < 0.10 if mean_ratio > 0 else False
        
        return {
            'code_convergence': code_result,
            'gui_convergence': gui_result,
            'mean_ratio': mean_ratio,
            'ratio_std': ratio_std,
            'ratio_stable': ratio_stable,
            'overall_fitness': overall_fitness,
            'converged': code_result.converged and gui_result.converged and ratio_stable
        }


def check_convergence(efficiency_samples: List[float],
                     threshold: float = 0.90) -> bool:
    """
    Convenience function to check if samples have converged
    
    Args:
        efficiency_samples: List of efficiency measurements
        threshold: Convergence threshold (default: 0.90)
    
    Returns:
        True if converged, False otherwise
    """
    analyzer = ConvergenceAnalyzer(convergence_threshold=threshold)
    result = analyzer.analyze(efficiency_samples)
    return result.converged


def calculate_fitness(efficiency_samples: List[float]) -> float:
    """
    Convenience function to calculate fitness score
    
    Args:
        efficiency_samples: List of efficiency measurements
    
    Returns:
        Fitness score (0-1)
    """
    analyzer = ConvergenceAnalyzer()
    result = analyzer.analyze(efficiency_samples)
    return result.fitness


# Example usage
if __name__ == "__main__":
    print("CONVERGENCE ANALYZER - Stability and Fitness Analysis")
    print("=" * 80)
    
    # Simulated code workflow samples (stable, high efficiency)
    code_samples = [0.802, 0.804, 0.806, 0.803, 0.805, 0.804, 0.803]
    
    # Simulated GUI workflow samples (stable, low efficiency)
    gui_samples = [0.0065, 0.0067, 0.0066, 0.0068, 0.0067, 0.0066, 0.0067]
    
    print("\nCode Workflow Convergence:")
    print("-" * 80)
    
    analyzer = ConvergenceAnalyzer()
    code_result = analyzer.analyze(code_samples)
    
    print(f"Converged:        {code_result.converged}")
    print(f"Fitness:          {code_result.fitness:.3f}")
    print(f"Stability:        {code_result.stability:.3f}")
    print(f"Mean Efficiency:  {code_result.mean_efficiency:.4f}")
    print(f"Std Deviation:    {code_result.std_deviation:.6f}")
    print(f"Sample Count:     {code_result.sample_count}")
    
    print("\nGUI Workflow Convergence:")
    print("-" * 80)
    
    gui_result = analyzer.analyze(gui_samples)
    
    print(f"Converged:        {gui_result.converged}")
    print(f"Fitness:          {gui_result.fitness:.3f}")
    print(f"Mean Efficiency:  {gui_result.mean_efficiency:.4f}")
    
    print("\nRatio Convergence Analysis:")
    print("-" * 80)
    
    ratio_analysis = analyzer.check_ratio_convergence(code_samples, gui_samples)
    
    print(f"Mean Ratio:       {ratio_analysis['mean_ratio']:.1f}x")
    print(f"Ratio Stable:     {ratio_analysis['ratio_stable']}")
    print(f"Overall Fitness:  {ratio_analysis['overall_fitness']:.3f}")
    print(f"Converged:        {ratio_analysis['converged']}")
