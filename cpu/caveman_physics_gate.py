import math
import numpy as np

class CavemanPhysicsGate:
    """
    Caveman OS: "Does this shit compute?"
    If no → fuck 'em (discard / sandbox).
    If maybe → TRIG6 it (test from more angles).
    If yes → keep building / ship.
    
    TRIG6: 6 angles for fuzzy checks.
    Blow-up at any angle → reject.
    Bounded → keep.
    Resonates narrow → handle gently.
    
    No belief. No identity. Just angles.
    """
    
    def __init__(self):
        self.n_angles = 6
        self.angles_deg = np.linspace(0, 360 - (360 / self.n_angles), self.n_angles)
        self.angles_rad = np.deg2rad(self.angles_deg)
        self.norms, self.vectors = self.compute_trig6()
        
    def compute_trig6(self):
        norms = []
        vectors = []
        eps = 1e-12
        inf_cap = 1e6
        for theta in self.angles_rad:
            s, c = math.sin(theta), math.cos(theta)
            t = s / c if abs(c) > eps else inf_cap
            csc = 1 / s if abs(s) > eps else inf_cap
            sec = 1 / c if abs(c) > eps else inf_cap
            cot = c / s if abs(s) > eps else inf_cap
            vec = [s, c, t, csc, sec, cot]
            norm_sq = sum(min(v**2, inf_cap**2) for v in vec)
            vectors.append(vec)
            norms.append(norm_sq)
        return norms, vectors
    
    def trig6_check(self, claim):
        """TRIG6 it: Test from 6 angles (change assumptions)."""
        idx = hash(claim) % self.n_angles  # Map to angle
        norm = self.norms[idx]
        if norm == float('inf') or norm > 1e5:
            return "BLOWS UP → REJECT WITH LOVE"
        if norm > 50:
            return "UNBOUNDED → FUCK EM"
        if 6 < norm < 8:
            return "RESONATES NARROW → HANDLE GENTLY"
        return "BOUNDED → KEEP"

    def check_claim(self, claim):
        """Caveman Physics Gate: 5 rocks."""
        checks = [
            ("Energy", "Does it require free energy?", "If yes → nope."),
            ("Causality", "Does effect come after cause?", "If no → nope."),
            ("Constraints", "Can I bound it (limits, caps, thresholds)?", "If no → sandbox."),
            ("Reproducibility", "Can I make it happen again?", "If no → log + ignore."),
            ("Failure mode", "When it fails, does it fail loud and safe?", "If no → fix or toss.")
        ]
        
        for check_type, question, action in checks:
            # Caveman heuristic: If claim fuzzy, TRIG6 it
            if "fuzzy" in claim.lower() or "maybe" in claim.lower():
                trig_verdict = self.trig6_check(claim)
                if "REJECT" in trig_verdict or "FUCK EM" in trig_verdict:
                    return f"MAYBE → TRIG6: {trig_verdict}"
                elif "HANDLE GENTLY" in trig_verdict:
                    return f"MAYBE → TRIG6: {trig_verdict} → KEEP BUILDING"
                return f"MAYBE → TRIG6: {trig_verdict} → SHIP"
            
            # Simple fail if "magic" or unconstrained (demo)
            fails = any(word in claim.lower() for word in ["magic", "free energy", "acausal"])
            if fails:
                return action
        
        return "YES → SHIP"

# Runtime
gate = CavemanPhysicsGate()

# Example claims
claims = [
    "Magic crystals heal everything instantly.",
    "Energy is conserved in closed systems.",
    "Pipe offsets compute consciousness.",
    "Maybe this PDE boundary is fuzzy."
]

for claim in claims:
    verdict = gate.check_claim(claim)
    print(f"Claim: \"{claim}\"")
    print(verdict)
    print("\n")
