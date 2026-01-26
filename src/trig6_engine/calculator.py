"""
TRIG6 Calculator - Efficiency Computation Engine

Provides calculation functions for TRIG6 efficiency formula.
Supports single calculations and batch processing.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class EfficiencyResult:
    """Result of TRIG6 efficiency calculation"""
    relevance: float
    distraction: float
    noise: float
    equation_quality: float
    efficiency: float
    
    def __repr__(self) -> str:
        return f"EfficiencyResult(eff={self.efficiency:.4f})"


class TRIG6Calculator:
    """
    TRIG6 efficiency calculator
    
    Implements the TRIG6 formula with validation and batch processing.
    """
    
    @staticmethod
    def calculate(R: float, D: float, N: float, eq: float) -> float:
        """
        Calculate TRIG6 efficiency
        
        Formula: f = R·(1-D)·(1-N)·eq
        
        Args:
            R: Relevance (0-1)
            D: Distraction (0-1)
            N: Noise (0-1)
            eq: Equation quality (0-1)
        
        Returns:
            Efficiency score (0-1)
        """
        # Validate inputs
        TRIG6Calculator._validate_param(R, 'R')
        TRIG6Calculator._validate_param(D, 'D')
        TRIG6Calculator._validate_param(N, 'N')
        TRIG6Calculator._validate_param(eq, 'eq')
        
        # Calculate
        return R * (1 - D) * (1 - N) * eq
    
    @staticmethod
    def calculate_with_details(R: float, D: float, N: float, eq: float) -> EfficiencyResult:
        """
        Calculate TRIG6 efficiency with detailed result
        
        Returns:
            EfficiencyResult with all parameters and calculated efficiency
        """
        efficiency = TRIG6Calculator.calculate(R, D, N, eq)
        
        return EfficiencyResult(
            relevance=R,
            distraction=D,
            noise=N,
            equation_quality=eq,
            efficiency=efficiency
        )
    
    @staticmethod
    def batch_calculate(metrics_list: List[Dict]) -> List[EfficiencyResult]:
        """
        Calculate TRIG6 for multiple metric sets
        
        Args:
            metrics_list: List of dicts with R, D, N, eq keys
        
        Returns:
            List of EfficiencyResult objects
        """
        results = []
        
        for metrics in metrics_list:
            result = TRIG6Calculator.calculate_with_details(
                R=metrics['R'],
                D=metrics['D'],
                N=metrics['N'],
                eq=metrics['eq']
            )
            results.append(result)
        
        return results
    
    @staticmethod
    def _validate_param(value: float, name: str):
        """Validate parameter is in range [0, 1]"""
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be in range [0, 1], got {value}")


def calculate_efficiency(R: float, D: float, N: float, eq: float) -> float:
    """
    Convenience function for TRIG6 calculation
    
    Args:
        R: Relevance (0-1)
        D: Distraction (0-1)
        N: Noise (0-1)
        eq: Equation quality (0-1)
    
    Returns:
        Efficiency score (0-1)
    """
    return TRIG6Calculator.calculate(R, D, N, eq)


def batch_calculate(metrics_list: List[Dict]) -> List[EfficiencyResult]:
    """
    Convenience function for batch calculation
    
    Args:
        metrics_list: List of dicts with R, D, N, eq keys
    
    Returns:
        List of EfficiencyResult objects
    """
    return TRIG6Calculator.batch_calculate(metrics_list)


# Example usage
if __name__ == "__main__":
    print("TRIG6 CALCULATOR - Efficiency Computation")
    print("=" * 80)
    
    # Single calculation
    print("\nSingle Calculation:")
    print("-" * 80)
    
    eff = calculate_efficiency(R=0.95, D=0.11, N=0.03, eq=0.98)
    print(f"Code Workflow Efficiency: {eff:.4f}")
    
    # Detailed calculation
    print("\nDetailed Calculation:")
    print("-" * 80)
    
    result = TRIG6Calculator.calculate_with_details(
        R=0.95, D=0.11, N=0.03, eq=0.98
    )
    print(result)
    
    # Batch calculation
    print("\nBatch Calculation:")
    print("-" * 80)
    
    workflows = [
        {'R': 0.95, 'D': 0.11, 'N': 0.03, 'eq': 0.98},  # Code
        {'R': 0.72, 'D': 0.85, 'N': 0.45, 'eq': 0.75},  # GUI
        {'R': 0.90, 'D': 0.15, 'N': 0.05, 'eq': 0.95},  # CLI
    ]
    
    results = batch_calculate(workflows)
    
    for i, result in enumerate(results):
        workflow_names = ['Code', 'GUI', 'CLI']
        print(f"{workflow_names[i]}: {result.efficiency:.4f}")
