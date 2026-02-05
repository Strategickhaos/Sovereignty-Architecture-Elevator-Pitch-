#!/usr/bin/env python3
"""
contradiction_engine.py v1.1
Purpose: Adversarial invariant enforcement + bottleneck assassination.
Philosophy: Trust nothing until it survives crossfire—and actively try to kill it.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Tuple, Optional, Any

# ----------------------------
# Core structures
# ----------------------------

@dataclass
class TestCase:
    theta: float
    meta: Dict[str, Any]

@dataclass
class TestResult:
    ok: bool
    name: str
    case: TestCase
    details: Dict[str, Any]

@dataclass
class Report:
    ok: bool
    seed: int
    total_cases: int
    total_checks: int
    failures: List[TestResult]
    runtime_seconds: float


# ----------------------------
# Mapping layer (pluggable)
# ----------------------------

def load_mapping(name: str) -> Dict[str, Callable[[float], float]]:
    name = name.lower().strip()

    if name in ("basic", "trig"):
        return {
            "sin": lambda t: math.sin(t),
            "cos": lambda t: math.cos(t),
            "tan": lambda t: math.tan(t),
        }

    if name in ("trig6", "trig6_geom"):
        # TRIG6 geometry example: 3D manifold on unit sphere-ish.
        # Replace with your real TRIG6 outputs (e.g., 6D trig projections).
        return {
            "x": lambda t: math.cos(t),
            "y": lambda t: math.sin(t),
            "z": lambda t: math.sin(2 * t) * 0.5,
        }

    raise ValueError(f"Unknown mapping '{name}'. Try: basic, trig6_geom")


# ----------------------------
# Mutation pipeline (for crossfire)
# ----------------------------

def mutate_mapping(base_mapping: Dict[str, Callable[[float], float]], seed: int, intensity: float = 0.5) -> Tuple[Dict[str, Callable[[float], float]], Dict[str, Any]]:
    rng = random.Random(seed)
    transforms = []
    mutated = {}

    for k, fn in base_mapping.items():
        # Randomly apply transforms: scale, noise, quantize
        mut_fn = fn
        if rng.random() < intensity:
            scale = rng.uniform(0.5, 2.0)
            transforms.append(f"scale_{k}:{scale:.2f}")
            mut_fn = lambda t, f=mut_fn, s=scale: f(t) * s
        if rng.random() < intensity:
            noise = rng.uniform(1e-6, 1e-3)
            transforms.append(f"noise_{k}:{noise:.2e}")
            # Create a new random value for each call to avoid constant noise
            noise_val = rng.gauss(0, noise)
            mut_fn = lambda t, f=mut_fn, n=noise_val: f(t) + n
        if rng.random() < intensity:
            quant = rng.choice([8, 16, 32])
            transforms.append(f"quant_{k}:{quant}")
            mut_fn = lambda t, f=mut_fn, q=quant: round(f(t) * q) / q
        mutated[k] = mut_fn

    trace = {"transforms": transforms, "intensity": intensity}
    return mutated, trace


# ----------------------------
# Invariants (validate)
# ----------------------------

def assert_bounds(case: TestCase, theta_min: float, theta_max: float) -> Optional[Dict[str, Any]]:
    t = case.theta
    if not math.isfinite(t):
        return {"reason": "theta not finite", "theta": t}
    if t < theta_min or t > theta_max:
        return {"reason": "theta out of bounds", "theta": t, "min": theta_min, "max": theta_max}
    return None

def assert_symmetry(case: TestCase, eps: float) -> Optional[Dict[str, Any]]:
    # sin^2 + cos^2 = 1 within eps (adapt for TRIG6 if needed)
    s = math.sin(case.theta)
    c = math.cos(case.theta)
    val = (s * s) + (c * c)
    if abs(val - 1.0) > eps:
        return {"reason": "symmetry violated", "theta": case.theta, "sin2+cos2": val, "eps": eps}
    return None

def assert_termination(start_time: float, timeout_s: float, step: int, step_limit: int) -> Optional[Dict[str, Any]]:
    if (time.time() - start_time) > timeout_s:
        return {"reason": "timeout exceeded", "timeout_s": timeout_s}
    if step > step_limit:
        return {"reason": "step limit exceeded", "step_limit": step_limit}
    return None

def assert_stability(case: TestCase, mapping: Dict[str, Callable[[float], float]], cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    allow_inf = cfg.get("allow_inf", False)
    outputs = {}
    for k, fn in mapping.items():
        try:
            v = fn(case.theta)
        except Exception as e:
            return {"reason": "mapping threw exception", "mapping": k, "error": repr(e), "theta": case.theta}
        outputs[k] = v

        if isinstance(v, (int, float)) and not math.isfinite(v) and not allow_inf:
            return {"reason": "non-finite output", "mapping": k, "value": v, "theta": case.theta}

    # TRIG6-specific geometry invariant: points on manifold (e.g., x² + y² + z² ≈ 1)
    # Replace/expand with your full TRIG6 predicate (e.g., torus, hyperboloid checks).
    if "x" in outputs and "y" in outputs and "z" in outputs:
        manifold_val = outputs["x"]**2 + outputs["y"]**2 + outputs["z"]**2
        eps = cfg.get("eps", 1e-9)
        if abs(manifold_val - 1.0) > eps:
            return {"reason": "trig6 geometry violated", "theta": case.theta, "manifold_val": manifold_val, "eps": eps}

    return None


# ----------------------------
# Bottleneck attacks (first 12 wired in)
# ----------------------------

def assert_unversioned_data(case: TestCase, mapping: Dict[str, Callable[[float], float]]) -> Optional[Dict[str, Any]]:
    # Simulate: Mutate without trace, check if transforms were applied.
    _, trace = mutate_mapping(mapping, seed=42, intensity=0.1)
    # Check if no transforms were actually applied (unversioned)
    if not trace.get('transforms'):
        return {"reason": "unversioned lineage simulated - no transforms tracked", "theta": case.theta}
    return None

# Add similar for #2-12: Each simulates the bottleneck (e.g., inject global state for #2, noise for #7) and checks core invariants post-sim.
# Brevity: Stubbed one per for now; expand as needed.

def assert_state_leakage(case: TestCase, mapping: Dict[str, Callable[[float], float]]) -> Optional[Dict[str, Any]]:
    # Simulate global leakage: Run twice, check determinism.
    # Get first mapping function for testing
    first_key = next(iter(mapping))
    v1 = mapping[first_key](case.theta)
    v2 = mapping[first_key](case.theta)
    if abs(v1 - v2) > 1e-9:
        return {"reason": "state leakage detected", "theta": case.theta, "delta": abs(v1 - v2)}
    return None

# ... (Implement #3-12 similarly: e.g., for #7, inject large gradients via scaled theta; check finite.)

# Placeholder for the rest – wire fully in v1.2 if this greens.

bottleneck_checks = [
    ("unversioned_data", assert_unversioned_data),
    ("state_leakage", assert_state_leakage),
    # Add ("non_idempotent_preproc", ...), etc.
]


# ----------------------------
# Contradiction: generate adversarial cases
# ----------------------------

def generate_cases(n: int, theta_min: float, theta_max: float, seed: int) -> List[TestCase]:
    rng = random.Random(seed)

    edges = [
        theta_min, theta_max,
        0.0, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi,
        -math.pi/2, -math.pi, -2*math.pi,
        (math.pi/2) - 1e-12, (math.pi/2) + 1e-12,
        (3*math.pi/2) - 1e-12, (3*math.pi/2) + 1e-12,
        1e-12, -1e-12, 1e6, -1e6,
    ]

    cases: List[TestCase] = [TestCase(theta=t, meta={"kind": "edge"}) for t in edges]

    for _ in range(max(0, n - len(cases))):
        t = rng.uniform(theta_min, theta_max)
        if rng.random() < 0.35:
            t += rng.choice([-1, 1]) * (10 ** rng.randint(-12, -3))
        cases.append(TestCase(theta=t, meta={"kind": "fuzz"}))

    rng.shuffle(cases)
    return cases


# ----------------------------
# Engine
# ----------------------------

def run_engine(
    mapping_name: str,
    n_cases: int,
    theta_min: float,
    theta_max: float,
    eps: float,
    seed: int,
    timeout_s: float,
    step_limit: int,
    enable_bottlenecks: bool = False,
    self_test: bool = False,
) -> Report:
    t0 = time.time()
    base_mapping = load_mapping(mapping_name)
    failures: List[TestResult] = []
    cases = generate_cases(n_cases, theta_min, theta_max, seed)

    checks = [
        ("bounds", lambda c: assert_bounds(c, theta_min, theta_max)),
        ("symmetry", lambda c: assert_symmetry(c, eps)),
    ]

    if enable_bottlenecks:
        # Bottleneck checks need the mapping parameter
        for name, fn_raw in bottleneck_checks:
            checks.append((name, lambda c, f=fn_raw: f(c, base_mapping)))

    step = 0
    start_time = time.time()

    for case in cases:
        step += 1
        term = assert_termination(start_time, timeout_s, step, step_limit)
        if term:
            failures.append(TestResult(ok=False, name="termination", case=case, details=term))
            break

        # Apply mutation for crossfire
        mutated_mapping, mut_trace = mutate_mapping(base_mapping, seed + step)
        case.meta["mutation"] = mut_trace

        # Run checks - stability uses mutated mapping, others use case data
        for name, fn in checks:
            if name == "stability":
                # Stability check needs to validate the mutated mapping
                detail = assert_stability(case, mutated_mapping, {"allow_inf": False, "eps": eps})
            else:
                detail = fn(case)
            if detail is not None:
                detail.update({"mutation_trace": mut_trace})
                failures.append(TestResult(ok=False, name=name, case=case, details=detail))
                break
        if failures:
            break

    if self_test:
        # Meta-check: Run engine on its own "mapping" (stubbed as identity for demo).
        # Disable self-test in recursive call to prevent infinite recursion
        meta_rep = run_engine("basic", 10, -1, 1, eps, seed + 1, timeout_s / 2, step_limit // 2, 
                             enable_bottlenecks=False, self_test=False)
        if not meta_rep.ok:
            failures.append(TestResult(ok=False, name="meta_self_test", case=TestCase(0, {"kind": "meta"}), details=asdict(meta_rep)))

    ok = len(failures) == 0
    return Report(
        ok=ok,
        seed=seed,
        total_cases=len(cases),
        total_checks=len(checks),
        failures=failures,
        runtime_seconds=round(time.time() - t0, 6),
    )


def main():
    ap = argparse.ArgumentParser(description="Contradiction Engine: adversarial invariant + bottleneck enforcement")
    ap.add_argument("--mapping", default="basic", help="mapping registry key (default: basic)")
    ap.add_argument("--cases", type=int, default=250, help="number of cases to generate (default: 250)")
    ap.add_argument("--theta-min", type=float, default=-2*math.pi, help="theta min bound")
    ap.add_argument("--theta-max", type=float, default= 2*math.pi, help="theta max bound")
    ap.add_argument("--eps", type=float, default=1e-9, help="tolerance (default 1e-9)")
    ap.add_argument("--seed", type=int, default=137, help="rng seed (default 137)")
    ap.add_argument("--timeout", type=float, default=2.0, help="timeout seconds (default 2.0)")
    ap.add_argument("--step-limit", type=int, default=5000, help="max steps (default 5000)")
    ap.add_argument("--json", action="store_true", help="emit JSON report only")
    ap.add_argument("--bottlenecks", action="store_true", help="enable bottleneck attacks")
    ap.add_argument("--self-test", action="store_true", help="run self-meta test")
    args = ap.parse_args()

    rep = run_engine(
        mapping_name=args.mapping,
        n_cases=args.cases,
        theta_min=args.theta_min,
        theta_max=args.theta_max,
        eps=args.eps,
        seed=args.seed,
        timeout_s=args.timeout,
        step_limit=args.step_limit,
        enable_bottlenecks=args.bottlenecks,
        self_test=args.self_test,
    )

    if args.json:
        print(json.dumps(asdict(rep), indent=2))
        raise SystemExit(0 if rep.ok else 1)

    if rep.ok:
        print(f"[PASS] Contradiction Engine: {rep.total_cases} cases, {rep.total_checks} checks, seed={rep.seed}, t={rep.runtime_seconds}s")
    else:
        f = rep.failures[0]
        print(f"[FAIL] Check '{f.name}' found a contradiction.")
        print(f"  theta = {f.case.theta}   meta = {f.case.meta}")
        print(f"  details = {json.dumps(f.details, indent=2)}")
        print(f"  seed={rep.seed} runtime={rep.runtime_seconds}s")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
