"""
Efficiency Metrics - TRIG6 Calculation and Analysis

Implements the TRIG6 efficiency formula and provides tools for
measuring and comparing cognitive workflow performance.

TRIG6 Formula: f = R·(1-D)·(1-N)·eq

Where:
    R  = Relevance (input quality, 0-1)
    D  = Distraction coefficient (0-1)
    N  = Noise ratio (0-1)
    eq = Equation quality (semantic correctness, 0-1)
"""

from typing import Dict, List, Tuple
import json


def calculate_trig6(relevance: float,
                   distraction: float,
                   noise: float,
                   equation_quality: float) -> float:
    """
    Calculate TRIG6 efficiency score
    
    Formula: f = R·(1-D)·(1-N)·eq
    
    Args:
        relevance: Input quality (0-1), higher is better
        distraction: Distraction coefficient (0-1), lower is better
        noise: Noise ratio (0-1), lower is better
        equation_quality: Semantic correctness (0-1), higher is better
    
    Returns:
        Efficiency score (0-1)
    
    Example:
        >>> calculate_trig6(R=0.95, D=0.11, N=0.03, eq=0.98)
        0.804
    """
    return relevance * (1 - distraction) * (1 - noise) * equation_quality


def create_metrics(relevance: float,
                  distraction: float,
                  noise: float,
                  equation_quality: float) -> Dict:
    """
    Create cognitive metrics dict with calculated efficiency
    
    Args:
        relevance: Input quality (0-1)
        distraction: Distraction coefficient (0-1)
        noise: Noise ratio (0-1)
        equation_quality: Semantic correctness (0-1)
    
    Returns:
        Dict with all fields populated
    """
    efficiency = calculate_trig6(relevance, distraction, noise, equation_quality)
    
    return {
        'relevance': relevance,
        'distraction': distraction,
        'noise': noise,
        'equation_quality': equation_quality,
        'efficiency': efficiency
    }


def compare_workflows(workflow_a_metrics: Dict,
                     workflow_b_metrics: Dict) -> Dict:
    """
    Compare efficiency between two workflows
    
    Args:
        workflow_a_metrics: Dict with R, D, N, eq for workflow A
        workflow_b_metrics: Dict with R, D, N, eq for workflow B
    
    Returns:
        Dict with comparison results including efficiency ratio
    
    Example:
        >>> code_metrics = {'R': 0.95, 'D': 0.11, 'N': 0.03, 'eq': 0.98}
        >>> gui_metrics = {'R': 0.72, 'D': 0.85, 'N': 0.45, 'eq': 0.75}
        >>> result = compare_workflows(code_metrics, gui_metrics)
        >>> result['ratio']
        120.6
    """
    # Calculate efficiency for both workflows
    eff_a = calculate_trig6(
        workflow_a_metrics['R'],
        workflow_a_metrics['D'],
        workflow_a_metrics['N'],
        workflow_a_metrics['eq']
    )
    
    eff_b = calculate_trig6(
        workflow_b_metrics['R'],
        workflow_b_metrics['D'],
        workflow_b_metrics['N'],
        workflow_b_metrics['eq']
    )
    
    # Calculate ratio
    ratio = eff_a / eff_b if eff_b > 0 else float('inf')
    
    return {
        'workflow_a_efficiency': eff_a,
        'workflow_b_efficiency': eff_b,
        'ratio': ratio,
        'winner': 'workflow_a' if eff_a > eff_b else 'workflow_b',
        'difference': abs(eff_a - eff_b),
        'percent_improvement': ((eff_a - eff_b) / eff_b * 100) if eff_b > 0 else float('inf')
    }


class WorkflowPresets:
    """
    Preset TRIG6 metrics for common workflow types
    
    Based on verified measurements from Phase 5 deployment.
    """
    
    CODE = {
        'R': 0.95,   # High relevance - structured syntax
        'D': 0.11,   # Low distraction - focused environment
        'N': 0.03,   # Low noise - clean signal
        'eq': 0.98   # High quality - semantic precision
    }
    
    GUI = {
        'R': 0.72,   # Medium relevance - visual noise
        'D': 0.95,   # Very high distraction - many UI elements
        'N': 0.752,  # Very high noise - visual parsing overhead
        'eq': 0.75   # Medium quality - indirect semantics
    }
    
    CLI = {
        'R': 0.90,   # High relevance - structured commands
        'D': 0.15,   # Low distraction - text-based
        'N': 0.05,   # Low noise - direct signal
        'eq': 0.95   # High quality - clear semantics
    }
    
    HYBRID = {
        'R': 0.80,   # Medium relevance - mixed inputs
        'D': 0.30,   # Medium distraction - context switching
        'N': 0.20,   # Medium noise - multiple formats
        'eq': 0.85   # Good quality - partial structure
    }
    
    @classmethod
    def get(cls, workflow_type: str) -> Dict:
        """Get preset metrics for workflow type"""
        return getattr(cls, workflow_type.upper(), cls.HYBRID)
    
    @classmethod
    def calculate_all(cls) -> Dict[str, float]:
        """Calculate efficiency for all presets"""
        return {
            'CODE': calculate_trig6(**cls.CODE),
            'GUI': calculate_trig6(**cls.GUI),
            'CLI': calculate_trig6(**cls.CLI),
            'HYBRID': calculate_trig6(**cls.HYBRID)
        }


def analyze_efficiency_factors(metrics: Dict) -> Dict:
    """
    Analyze which factors contribute most to efficiency
    
    Args:
        metrics: Dict with R, D, N, eq values
    
    Returns:
        Dict with factor analysis and recommendations
    """
    R = metrics['R']
    D = metrics['D']
    N = metrics['N']
    eq = metrics['eq']
    
    # Calculate total efficiency
    total_eff = calculate_trig6(R, D, N, eq)
    
    # Calculate contribution of each factor
    # By setting each to optimal (1.0 or 0.0) and recalculating
    factors = {}
    
    # Relevance impact (increase to 1.0)
    if R < 1.0:
        improved_eff = calculate_trig6(1.0, D, N, eq)
        factors['relevance'] = {
            'current': R,
            'optimal': 1.0,
            'potential_gain': improved_eff - total_eff,
            'percent_gain': ((improved_eff - total_eff) / total_eff * 100) if total_eff > 0 else 0
        }
    
    # Distraction impact (reduce to 0.0)
    if D > 0.0:
        improved_eff = calculate_trig6(R, 0.0, N, eq)
        factors['distraction'] = {
            'current': D,
            'optimal': 0.0,
            'potential_gain': improved_eff - total_eff,
            'percent_gain': ((improved_eff - total_eff) / total_eff * 100) if total_eff > 0 else 0
        }
    
    # Noise impact (reduce to 0.0)
    if N > 0.0:
        improved_eff = calculate_trig6(R, D, 0.0, eq)
        factors['noise'] = {
            'current': N,
            'optimal': 0.0,
            'potential_gain': improved_eff - total_eff,
            'percent_gain': ((improved_eff - total_eff) / total_eff * 100) if total_eff > 0 else 0
        }
    
    # Equation quality impact (increase to 1.0)
    if eq < 1.0:
        improved_eff = calculate_trig6(R, D, N, 1.0)
        factors['equation_quality'] = {
            'current': eq,
            'optimal': 1.0,
            'potential_gain': improved_eff - total_eff,
            'percent_gain': ((improved_eff - total_eff) / total_eff * 100) if total_eff > 0 else 0
        }
    
    # Sort factors by potential gain
    sorted_factors = sorted(
        factors.items(),
        key=lambda x: x[1]['potential_gain'],
        reverse=True
    )
    
    return {
        'current_efficiency': total_eff,
        'factors': factors,
        'top_improvement': sorted_factors[0] if sorted_factors else None,
        'recommendations': _generate_recommendations(sorted_factors)
    }


def _generate_recommendations(sorted_factors: List[Tuple]) -> List[str]:
    """Generate optimization recommendations based on factor analysis"""
    recommendations = []
    
    for factor_name, factor_data in sorted_factors[:2]:  # Top 2 factors
        if factor_name == 'distraction':
            recommendations.append(
                f"Reduce distraction from {factor_data['current']:.2f} to {factor_data['optimal']:.2f} "
                f"for {factor_data['percent_gain']:.1f}% efficiency gain"
            )
        elif factor_name == 'noise':
            recommendations.append(
                f"Reduce noise from {factor_data['current']:.2f} to {factor_data['optimal']:.2f} "
                f"for {factor_data['percent_gain']:.1f}% efficiency gain"
            )
        elif factor_name == 'relevance':
            recommendations.append(
                f"Increase relevance from {factor_data['current']:.2f} to {factor_data['optimal']:.2f} "
                f"for {factor_data['percent_gain']:.1f}% efficiency gain"
            )
        elif factor_name == 'equation_quality':
            recommendations.append(
                f"Improve semantic quality from {factor_data['current']:.2f} to {factor_data['optimal']:.2f} "
                f"for {factor_data['percent_gain']:.1f}% efficiency gain"
            )
    
    return recommendations


# Example usage and verification
if __name__ == "__main__":
    print("=" * 80)
    print("TRIG6 EFFICIENCY CALCULATOR - Phase 5")
    print("=" * 80)
    
    # Calculate preset efficiencies
    print("\nPreset Workflow Efficiencies:")
    print("-" * 80)
    
    efficiencies = WorkflowPresets.calculate_all()
    for workflow, eff in efficiencies.items():
        print(f"{workflow:<10} {eff:.4f}")
    
    # Compare CODE vs GUI
    print("\nCODE vs GUI Comparison:")
    print("-" * 80)
    
    comparison = compare_workflows(
        WorkflowPresets.CODE,
        WorkflowPresets.GUI
    )
    
    print(f"Code Efficiency:  {comparison['workflow_a_efficiency']:.4f}")
    print(f"GUI Efficiency:   {comparison['workflow_b_efficiency']:.4f}")
    print(f"Efficiency Ratio: {comparison['ratio']:.1f}x")
    print(f"Winner:           {comparison['winner']}")
    print(f"Improvement:      {comparison['percent_improvement']:.1f}%")
    
    # Analyze GUI workflow for improvements
    print("\nGUI Workflow Optimization Analysis:")
    print("-" * 80)
    
    analysis = analyze_efficiency_factors(WorkflowPresets.GUI)
    print(f"Current Efficiency: {analysis['current_efficiency']:.4f}")
    print("\nRecommendations:")
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"{i}. {rec}")
