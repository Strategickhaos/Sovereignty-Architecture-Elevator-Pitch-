# trig6_core.py
"""
TRIG6 Math Engine - Core projections, blends, and danger zone detection.
Implements raw/blended projections, resonance, drift, noise calculations.
"""

import math
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class DangerZone:
    """Represents a danger zone where projections may diverge."""
    theta: float
    reason: str
    severity: str  # 'warning' or 'critical'


class Trig6Core:
    """Core TRIG6 mathematical operations and projections."""
    
    # Danger zones (radians)
    DANGER_ZONES = [
        (math.pi / 2, "tan/cot singularity", "critical"),
        (math.pi, "phase flip boundary", "warning"),
        (3 * math.pi / 2, "tan/cot singularity", "critical"),
        (0, "cot singularity", "critical"),
        (2 * math.pi, "cot singularity", "critical"),
    ]
    
    def __init__(self):
        self.epsilon = 1e-6  # Small value to avoid division by zero
    
    def raw_projections(self, theta: float) -> Tuple[float, float, float, float, float, float]:
        """
        Compute raw TRIG6 projections (sin, cos, tan, csc, sec, cot).
        Returns: (sin, cos, tan, csc, sec, cot)
        """
        sin_val = math.sin(theta)
        cos_val = math.cos(theta)
        
        # Avoid division by zero with epsilon
        tan_val = sin_val / (cos_val + self.epsilon) if abs(cos_val) > self.epsilon else float('inf')
        csc_val = 1.0 / (sin_val + self.epsilon) if abs(sin_val) > self.epsilon else float('inf')
        sec_val = 1.0 / (cos_val + self.epsilon) if abs(cos_val) > self.epsilon else float('inf')
        cot_val = cos_val / (sin_val + self.epsilon) if abs(sin_val) > self.epsilon else float('inf')
        
        return (sin_val, cos_val, tan_val, csc_val, sec_val, cot_val)
    
    def blended_projection(self, theta: float, alpha: float) -> float:
        """
        Compute blended projection with alpha [0,1].
        alpha=0: pure circular (sin)
        alpha=1: full hyperbolic (sinh)
        
        Returns: blended value
        """
        alpha = max(0.0, min(1.0, alpha))  # Clamp alpha to [0,1]
        
        circular = math.sin(theta)
        hyperbolic = math.sinh(theta)
        
        return (1 - alpha) * circular + alpha * hyperbolic
    
    def compute_resonance(self, theta: float, theta_opt: float, alpha: float) -> float:
        """
        Compute resonance metric: how well theta aligns with optimal theta.
        Higher values (closer to 1.0) indicate better resonance.
        
        Returns: resonance value [0, 1]
        """
        # Simple resonance based on angular distance
        angular_distance = abs(theta - theta_opt)
        # Normalize to [0, pi] and invert
        normalized_distance = min(angular_distance, 2 * math.pi - angular_distance) / math.pi
        
        # Resonance is higher when distance is smaller
        base_resonance = 1.0 - normalized_distance
        
        # Alpha affects resonance (hyperbolic blending can reduce resonance)
        alpha_factor = 1.0 - 0.3 * alpha  # Up to 30% reduction at full hyperbolic
        
        return base_resonance * alpha_factor
    
    def compute_drift(self, theta: float, theta_opt: float) -> float:
        """
        Compute drift: how far theta has drifted from optimal.
        
        Returns: drift value [0, 1]
        """
        angular_distance = abs(theta - theta_opt)
        # Normalize to [0, pi]
        normalized_distance = min(angular_distance, 2 * math.pi - angular_distance) / math.pi
        
        return normalized_distance
    
    def compute_noise(self, theta: float, alpha: float) -> float:
        """
        Compute noise: instability metric based on proximity to danger zones.
        Higher noise indicates more unstable configuration.
        
        Returns: noise value [0, 1]
        """
        min_danger_distance = float('inf')
        
        for danger_theta, _, severity in self.DANGER_ZONES:
            distance = abs(theta - danger_theta)
            # Consider wrap-around distance
            distance = min(distance, 2 * math.pi - distance)
            
            if distance < min_danger_distance:
                min_danger_distance = distance
        
        # Noise increases as we get closer to danger zones
        # Full noise at danger zone (0 distance), decays with distance
        danger_threshold = 0.2  # Within 0.2 radians is noisy
        
        if min_danger_distance < danger_threshold:
            base_noise = 1.0 - (min_danger_distance / danger_threshold)
        else:
            base_noise = 0.0
        
        # Alpha can increase noise (hyperbolic more unstable)
        alpha_noise = 0.2 * alpha
        
        return min(1.0, base_noise + alpha_noise)
    
    def check_danger_zones(self, theta: float, tolerance: float = 0.1) -> Optional[DangerZone]:
        """
        Check if theta is in or near a danger zone.
        
        Args:
            theta: angle in radians
            tolerance: proximity threshold (radians)
        
        Returns: DangerZone if near danger, None otherwise
        """
        for danger_theta, reason, severity in self.DANGER_ZONES:
            distance = abs(theta - danger_theta)
            # Consider wrap-around
            distance = min(distance, 2 * math.pi - distance)
            
            if distance < tolerance:
                return DangerZone(theta=danger_theta, reason=reason, severity=severity)
        
        return None
    
    def safe_compute(self, theta: float, alpha: float = 0.0) -> dict:
        """
        Safely compute all projections and metrics with danger checking.
        
        Returns: Dictionary with all computed values and warnings
        """
        result = {
            'theta': theta,
            'alpha': alpha,
            'raw_projections': {},
            'blended': None,
            'danger': None,
        }
        
        # Check danger zones first
        danger = self.check_danger_zones(theta)
        if danger:
            result['danger'] = {
                'theta': danger.theta,
                'reason': danger.reason,
                'severity': danger.severity,
            }
        
        # Compute raw projections
        sin_val, cos_val, tan_val, csc_val, sec_val, cot_val = self.raw_projections(theta)
        result['raw_projections'] = {
            'sin': sin_val,
            'cos': cos_val,
            'tan': tan_val,
            'csc': csc_val,
            'sec': sec_val,
            'cot': cot_val,
        }
        
        # Compute blended projection
        result['blended'] = self.blended_projection(theta, alpha)
        
        return result


# Example usage
if __name__ == "__main__":
    core = Trig6Core()
    
    # Test at various angles
    test_angles = [0, math.pi/4, math.pi/2, math.pi, 3*math.pi/2]
    
    for theta in test_angles:
        print(f"\n=== θ = {theta:.4f} rad ({math.degrees(theta):.1f}°) ===")
        result = core.safe_compute(theta, alpha=0.5)
        
        print(f"Raw projections: sin={result['raw_projections']['sin']:.4f}, "
              f"cos={result['raw_projections']['cos']:.4f}")
        print(f"Blended (α=0.5): {result['blended']:.4f}")
        
        if result['danger']:
            print(f"⚠️  DANGER: {result['danger']['reason']} "
                  f"(severity: {result['danger']['severity']})")
