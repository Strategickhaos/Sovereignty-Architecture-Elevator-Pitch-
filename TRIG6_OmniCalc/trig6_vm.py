# trig6_vm.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from trig6_core import (
    Trig6Projections,
    blend_trig_hyper,
    compute_noise,
    compute_drift,
    compute_resonance,
    danger_zones,
)


@dataclass
class Trig6State:
    theta: float = 0.0
    alpha: float = 0.0  # blend
    theta_opt: float = 0.0
    last_proj: Optional[Trig6Projections] = None
    proj: Optional[Trig6Projections] = None
    noise: float = 0.0
    drift: float = 0.0
    resonance: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "theta": self.theta,
            "alpha": self.alpha,
            "theta_opt": self.theta_opt,
            "noise": self.noise,
            "drift": self.drift,
            "resonance": self.resonance,
            "danger_zones": danger_zones(self.theta),
            "proj": self.proj.as_dict() if self.proj else None,
        }


class Trig6VM:
    """
    Minimal VM for TRIG6 "programs".
    You can extend this with a bytecode later.
    """

    def __init__(self, theta: float = 0.0, alpha: float = 0.0, theta_opt: float = 0.0):
        self.state = Trig6State(theta=theta, alpha=alpha, theta_opt=theta_opt)

    # --- Primitive ops ---

    def op_set_theta(self, theta: float) -> None:
        self.state.theta = theta

    def op_set_alpha(self, alpha: float) -> None:
        self.state.alpha = max(0.0, min(1.0, alpha))

    def op_set_theta_opt(self, theta_opt: float) -> None:
        self.state.theta_opt = theta_opt

    def op_step(self) -> None:
        """
        Core "tick": recompute projections, noise, drift, resonance.
        """
        proj = blend_trig_hyper(self.state.theta, self.state.alpha)
        noise = compute_noise(proj, self.state.proj)
        drift = compute_drift(self.state.theta, self.state.theta_opt)
        resonance = compute_resonance(drift, noise)

        self.state.last_proj = self.state.proj
        self.state.proj = proj
        self.state.noise = noise
        self.state.drift = drift
        self.state.resonance = resonance

    # --- Introspection ---

    def snapshot(self) -> Dict[str, Any]:
        return self.state.to_dict()
