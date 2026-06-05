import json
import math
import numpy as np
from scipy.optimize import bisect

# Config
FLAME_MAP_JSON = "flame_trig6_map.json"  # Input from gen
OUT_JSON = "phase_sweep_trig6_weights.json"
Pe_vals = np.logspace(-1, 2, 5)  # Demo; scale to 10+
Da0 = 0.1
Bi = 1.0
Da_min, Da_max = 0.01, 50.0
tol = 1e-3
NORM_CAP = 200.0  # Cap for norm^2 values to prevent overflow

# Placeholder sim (swap with real PDE/BVP)
def placeholder_sim(Pe, Da_g, Da0, Da_gamma, Bi):
    # Toy proxy: survival if xi_crit <1
    xi_crit = (Da0 + Da_gamma - Da_g) / Da_gamma if Da_gamma > 0 else 2.0
    survived = 1 if xi_crit < 1 else 0
    return {"survived": survived, "xi_crit_local": xi_crit, "amax_T": survived * 0.5, "mass_T": survived * 0.8}

def survives(out):
    return out["survived"] > 0.5

def find_Da_g_crit(sim_fn, Pe, Da0, Da_gamma, Bi, Da_min=Da_min, Da_max=Da_max, tol=tol):
    def f(Da_g):
        out = sim_fn(Pe, Da_g, Da0, Da_gamma, Bi)
        return 1.0 if survives(out) else -1.0

    if f(Da_min) > 0:
        return Da_min
    if f(Da_max) < 0:
        return np.nan

    return bisect(f, Da_min, Da_max, xtol=tol)

def main():
    with open(FLAME_MAP_JSON, "r") as f:
        flame_map = json.load(f)

    results = []
    for codon, entry in flame_map.items():
        # Da_gamma from norm (capped)
        norm2 = entry.get("Norm^2", 0.0)
        Da_gamma = NORM_CAP if (isinstance(norm2, float) and math.isinf(norm2)) or norm2 > NORM_CAP else float(norm2)

        # Sweep per Pe
        boundary = []
        for Pe in Pe_vals:
            Da_g_crit = find_Da_g_crit(placeholder_sim, Pe, Da0, Da_gamma, Bi)
            boundary.append({"Pe": float(Pe), "Da_g_crit": float(Da_g_crit) if np.isfinite(Da_g_crit) else "extinct"})

        results.append({
            "codon": codon,
            "atomic_num": entry["Atomic #"],
            "Da_gamma": Da_gamma,
            "boundary": boundary
        })

    # SAGCO schema (versioned, structured)
    output = {
        "version": "SAGCO-TRIG6-PHASE-1.0",
        "generated_at": "2026-02-03T11:48:00CST",  # Placeholder; use datetime.now()
        "params": {"Da0": Da0, "Bi": Bi, "Pe_vals": list(Pe_vals.tolist()), "tol": tol},
        "entries": results
    }

    with open(OUT_JSON, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote: {OUT_JSON}")
    print("Sample entry (first codon):", results[0])

# Validator func (SAGCO-ready)
def validate_sagco_phase(data):
    if data.get("version") != "SAGCO-TRIG6-PHASE-1.0":
        return False, "Version mismatch"
    if len(data["entries"]) != 64:
        return False, "Must have 64 codon entries"
    for e in data["entries"]:
        if "codon" not in e or len(e["boundary"]) != len(data["params"]["Pe_vals"]):
            return False, "Entry structure invalid"
    return True, "Valid"

if __name__ == "__main__":
    main()
    # Test validator
    with open(OUT_JSON, "r") as f:
        out_data = json.load(f)
    valid, msg = validate_sagco_phase(out_data)
    print(f"Validation: {msg}")
