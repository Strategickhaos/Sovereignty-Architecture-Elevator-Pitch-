# trig6_vm.py
"""
TRIG6 Virtual Machine - Stateful execution environment for TRIG6 operations.
Maintains state (theta, alpha, theta_opt) and provides operations for manipulation.
"""

import math
import json
from dataclasses import dataclass, asdict
from typing import Optional

from trig6_core import Trig6Core, DangerZone


@dataclass
class VMState:
    """Virtual machine state for TRIG6 calculations."""
    theta: float = 0.0              # Current angle (radians)
    alpha: float = 0.0              # Blend factor [0,1]
    theta_opt: float = math.pi / 4  # Optimal angle (radians)
    
    # Computed metrics (updated by step operation)
    resonance: float = 0.0
    drift: float = 0.0
    noise: float = 0.0
    
    # Last computed projections
    sin: float = 0.0
    cos: float = 0.0
    tan: float = 0.0
    csc: float = 0.0
    sec: float = 0.0
    cot: float = 0.0
    blended: float = 0.0
    
    # Danger warning
    danger: Optional[dict] = None


class Trig6VM:
    """Virtual Machine for executing TRIG6 operations."""
    
    def __init__(self):
        self.state = VMState()
        self.core = Trig6Core()
    
    # === State Setters (Operations) ===
    
    def op_set_theta(self, theta: float) -> None:
        """Set theta (angle in radians)."""
        self.state.theta = theta
    
    def op_set_alpha(self, alpha: float) -> None:
        """Set alpha (blend factor [0,1])."""
        self.state.alpha = max(0.0, min(1.0, alpha))
    
    def op_set_theta_opt(self, theta_opt: float) -> None:
        """Set optimal theta."""
        self.state.theta_opt = theta_opt
    
    def op_set_theta_degrees(self, degrees: float) -> None:
        """Set theta using degrees (converts to radians)."""
        self.state.theta = degrees * math.pi / 180.0
    
    def op_toggle_blend(self, enable: bool = True) -> None:
        """Toggle blend mode (alpha=1 for on, alpha=0 for off)."""
        self.state.alpha = 1.0 if enable else 0.0
    
    # === Computation Operation ===
    
    def op_step(self) -> None:
        """
        Main computation step: Update all projections, metrics, and danger checks.
        This is the core operation that recomputes the entire state.
        """
        # Compute raw projections
        sin_val, cos_val, tan_val, csc_val, sec_val, cot_val = \
            self.core.raw_projections(self.state.theta)
        
        self.state.sin = sin_val
        self.state.cos = cos_val
        self.state.tan = tan_val
        self.state.csc = csc_val
        self.state.sec = sec_val
        self.state.cot = cot_val
        
        # Compute blended projection
        self.state.blended = self.core.blended_projection(
            self.state.theta, self.state.alpha
        )
        
        # Compute metrics
        self.state.resonance = self.core.compute_resonance(
            self.state.theta, self.state.theta_opt, self.state.alpha
        )
        self.state.drift = self.core.compute_drift(
            self.state.theta, self.state.theta_opt
        )
        self.state.noise = self.core.compute_noise(
            self.state.theta, self.state.alpha
        )
        
        # Check danger zones
        danger = self.core.check_danger_zones(self.state.theta)
        if danger:
            self.state.danger = {
                'theta': danger.theta,
                'reason': danger.reason,
                'severity': danger.severity,
            }
        else:
            self.state.danger = None
    
    # === Query Operations ===
    
    def snapshot(self) -> str:
        """
        Return current state as JSON string.
        Useful for debugging and state inspection.
        """
        state_dict = asdict(self.state)
        return json.dumps(state_dict, indent=2)
    
    def get_state(self) -> VMState:
        """Return current VM state object."""
        return self.state
    
    def print_state(self) -> None:
        """Print formatted state to console."""
        print("\n" + "=" * 60)
        print("TRIG6 VM STATE")
        print("=" * 60)
        print(f"θ (theta):     {self.state.theta:.6f} rad ({math.degrees(self.state.theta):.2f}°)")
        print(f"α (alpha):     {self.state.alpha:.6f}")
        print(f"θ_opt:         {self.state.theta_opt:.6f} rad ({math.degrees(self.state.theta_opt):.2f}°)")
        print()
        print("--- Projections ---")
        print(f"sin(θ):        {self.state.sin:.6f}")
        print(f"cos(θ):        {self.state.cos:.6f}")
        print(f"tan(θ):        {self.state.tan:.6f}")
        print(f"csc(θ):        {self.state.csc:.6f}")
        print(f"sec(θ):        {self.state.sec:.6f}")
        print(f"cot(θ):        {self.state.cot:.6f}")
        print(f"blended:       {self.state.blended:.6f}")
        print()
        print("--- Metrics ---")
        print(f"Resonance:     {self.state.resonance:.6f}")
        print(f"Drift:         {self.state.drift:.6f}")
        print(f"Noise:         {self.state.noise:.6f}")
        
        if self.state.danger:
            print()
            print(f"⚠️  DANGER ZONE: {self.state.danger['reason']}")
            print(f"   Severity: {self.state.danger['severity']}")
        
        print("=" * 60 + "\n")
    
    # === Utility Operations ===
    
    def reset(self) -> None:
        """Reset VM to initial state."""
        self.state = VMState()


# Example usage
if __name__ == "__main__":
    vm = Trig6VM()
    
    # Example 1: Basic operations
    print("Example 1: Basic operations")
    vm.op_set_theta(math.pi / 4)
    vm.op_set_alpha(0.5)
    vm.op_step()
    vm.print_state()
    
    # Example 2: Danger zone
    print("\nExample 2: Near danger zone (π/2)")
    vm.op_set_theta(math.pi / 2)
    vm.op_step()
    vm.print_state()
    
    # Example 3: Degrees input
    print("\nExample 3: Using degrees (45°)")
    vm.op_set_theta_degrees(45)
    vm.op_set_alpha(0.0)  # Pure circular
    vm.op_step()
    vm.print_state()
