# trig6_core.py
import math
from dataclasses import dataclass
from typing import List, Dict


EPS = 1e-6


@dataclass
class Trig6Projections:
    theta: float
    sin_: float
    cos_: float
    tan_: float
    csc_: float
    sec_: float
    cot_: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "theta": self.theta,
            "sin": self.sin_,
            "cos": self.cos_,
            "tan": self.tan_,
            "csc": self.csc_,
            "sec": self.sec_,
            "cot": self.cot_,
        }


def clamp(x: float, limit: float = 10.0) -> float:
    if x > limit:
        return limit
    if x < -limit:
        return -limit
    return x


def safe_tan(theta: float) -> float:
    return clamp(math.tan(theta))


def safe_cot(theta: float) -> float:
    t = math.tan(theta)
    if abs(t) < EPS:
        return clamp(1.0 / EPS)
    return clamp(1.0 / t)


def safe_sec(theta: float) -> float:
    c = math.cos(theta)
    if abs(c) < EPS:
        return clamp(1.0 / EPS)
    return clamp(1.0 / c)


def safe_csc(theta: float) -> float:
    s = math.sin(theta)
    if abs(s) < EPS:
        return clamp(1.0 / EPS)
    return clamp(1.0 / s)


def compute_trig6(theta: float) -> Trig6Projections:
    """Raw TRIG6 projections (clamped)."""
    return Trig6Projections(
        theta=theta,
        sin_=math.sin(theta),
        cos_=math.cos(theta),
        tan_=safe_tan(theta),
        csc_=safe_csc(theta),
        sec_=safe_sec(theta),
        cot_=safe_cot(theta),
    )


@dataclass
class BlendParams:
    alpha: float  # 0 = trig only, 1 = hyperbolic only


def blend_trig_hyper(theta: float, alpha: float) -> Trig6Projections:
    """
    Hybrid trigonometric-hyperbolic blend.
    alpha in [0,1]
    """
    base = compute_trig6(theta)

    # Hyperbolic counterparts (clamped + squashed)
    sinh_ = math.sinh(theta)
    cosh_ = math.cosh(theta)
    tanh_ = math.tanh(theta)

    # Use tanh as squash on hyperbolics for boundedness
    h_sin = math.tanh(sinh_)
    h_cos = math.tanh(cosh_)
    h_tan = tanh_
    # For simplicity, reuse same hyperbolic values for reciprocals
    h_csc = math.tanh(1.0 / (sinh_ if abs(sinh_) > EPS else EPS))
    h_sec = math.tanh(1.0 / (cosh_ if abs(cosh_) > EPS else EPS))
    h_cot = math.tanh(1.0 / (tanh_ if abs(tanh_) > EPS else EPS))

    def mix(a: float, b: float) -> float:
        return (1 - alpha) * a + alpha * b

    return Trig6Projections(
        theta=theta,
        sin_=mix(base.sin_, h_sin),
        cos_=mix(base.cos_, h_cos),
        tan_=mix(base.tan_, h_tan),
        csc_=mix(base.csc_, h_csc),
        sec_=mix(base.sec_, h_sec),
        cot_=mix(base.cot_, h_cot),
    )


def compute_noise(current: Trig6Projections, previous: Trig6Projections | None) -> float:
    if previous is None:
        return 0.0
    diffs = [
        current.sin_ - previous.sin_,
        current.cos_ - previous.cos_,
        current.tan_ - previous.tan_,
        current.csc_ - previous.csc_,
        current.sec_ - previous.sec_,
        current.cot_ - previous.cot_,
    ]
    # Simple L1-based noise metric
    return sum(abs(d) for d in diffs) / len(diffs)


def compute_drift(theta: float, theta_opt: float) -> float:
    """Absolute angular deviation, normalized to [0, 1]."""
    raw = abs(theta - theta_opt)
    # Wrap to [0, pi]
    raw = min(raw, abs(2 * math.pi - raw))
    return raw / math.pi


def compute_resonance(drift: float, noise: float) -> float:
    """
    Simple resonance heuristic:
    R = cos(drift * pi/2) * (1 - noise_clamped)
    """
    noise_clamped = max(0.0, min(1.0, noise))
    return math.cos(drift * math.pi / 2.0) * (1.0 - noise_clamped)


def danger_zones(theta: float, threshold: float = 0.15) -> List[str]:
    """
    Detect proximity to singularities for tan / cot / sec / csc.
    Returns human-readable flags, e.g. ["tan_singularity"].
    """
    zones = []
    # π/2 + kπ for tan / sec
    dist_to_pi2 = min(abs(theta - math.pi / 2.0), abs(theta - 3 * math.pi / 2.0))
    if dist_to_pi2 < threshold:
        zones.append("tan_sec_singularity")

    # 0, π, 2π for cot / csc
    dist_to_0 = min(abs(theta - 0.0), abs(theta - math.pi), abs(theta - 2 * math.pi))
    if dist_to_0 < threshold:
        zones.append("cot_csc_singularity")

    return zones
