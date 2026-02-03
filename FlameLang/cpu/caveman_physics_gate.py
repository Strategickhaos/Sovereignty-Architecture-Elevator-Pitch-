from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple


# ----------------------------
# Claim packet (optional but makes it real)
# ----------------------------
@dataclass
class Claim:
    text: str

    # These are your "5 rocks" signals.
    # If you don't know, leave as None and the gate will default to SANDBOX.
    violates_energy: Optional[bool] = None
    violates_causality: Optional[bool] = None
    has_bounds: Optional[bool] = None
    reproducible: Optional[bool] = None
    fails_safe: Optional[bool] = None

    # Optional confidence 0..1 (if you're estimating)
    confidence: Optional[float] = None


# ----------------------------
# Caveman Gate
# ----------------------------
class CavemanPhysicsGate:
    """
    Caveman OS:
      - Does it compute? If not: fuck 'em.
      - If maybe: TRIG6 it (6 independent viewpoints).
      - If yes: ship.

    No belief. No identity. Constraints only.
    """

    def __init__(self):
        # Perspective names (these are your 6 "views")
        # Note: Using 6 perspectives symbolically represents TRIG6 (hexagonal viewpoints)
        # The 6 angles [0, 60, 120, 180, 240, 300] degrees represent this geometry conceptually
        self.views = [
            ("energy", "free energy / conservation"),
            ("causality", "cause->effect order"),
            ("bounds", "limits / caps / thresholds"),
            ("repro", "repeatability"),
            ("failsafe", "failure mode safety"),
            ("adversary", "what breaks under hostile conditions"),
        ]

    # ---------- TRIG6: six views ----------
    def trig6_views(self, claim: Claim) -> List[Tuple[str, str, str]]:
        """
        Returns list of (view_key, view_desc, verdict)
        verdict: "pass" | "fail" | "unknown"
        """
        v = []

        # View 1: energy
        v.append(("energy", "free energy / conservation",
                  "fail" if claim.violates_energy is True else ("pass" if claim.violates_energy is False else "unknown")))

        # View 2: causality
        v.append(("causality", "cause->effect order",
                  "fail" if claim.violates_causality is True else ("pass" if claim.violates_causality is False else "unknown")))

        # View 3: bounds
        v.append(("bounds", "limits / caps / thresholds",
                  "pass" if claim.has_bounds is True else ("fail" if claim.has_bounds is False else "unknown")))

        # View 4: reproducibility
        v.append(("repro", "repeatability",
                  "pass" if claim.reproducible is True else ("fail" if claim.reproducible is False else "unknown")))

        # View 5: fail safe
        v.append(("failsafe", "failure mode safety",
                  "pass" if claim.fails_safe is True else ("fail" if claim.fails_safe is False else "unknown")))

        # View 6: adversary (always unknown unless you set confidence high)
        # This keeps caveman honest: if you haven't threat-modeled, it's unknown.
        if claim.confidence is not None and claim.confidence >= 0.85:
            adv = "pass"
        else:
            adv = "unknown"
        v.append(("adversary", "hostile conditions / misuse", adv))

        return v

    # ---------- "5 rocks" gate ----------
    def evaluate(self, claim: Claim) -> Dict[str, object]:
        """
        Returns a structured verdict + rationale.
        """
        views = self.trig6_views(claim)

        fails = [x for x in views if x[2] == "fail"]
        unknowns = [x for x in views if x[2] == "unknown"]

        # Hard rejects: energy or causality fail
        hard_fail_keys = {"energy", "causality"}
        if any(k in hard_fail_keys for k, _, verdict in views if verdict == "fail"):
            return {
                "verdict": "NOPE",
                "reason": "violates physics gate (energy/causality)",
                "views": views,
                "caveman": "NOPE → fuck 'em"
            }

        # If any of these are explicitly bad, route to FIX+TOSS
        if any(k == "failsafe" for k, _, verdict in views if verdict == "fail"):
            return {
                "verdict": "FIX+TOSS",
                "reason": "fails unsafe; must be corrected or discarded",
                "views": views,
                "caveman": "FAILSAFE BAD → fix or toss"
            }

        # If bounds or reproducibility fail, you don't ship
        if any(k in {"bounds", "repro"} for k, _, verdict in views if verdict == "fail"):
            return {
                "verdict": "SANDBOX",
                "reason": "unbounded or non-reproducible; keep isolated and test",
                "views": views,
                "caveman": "MAYBE → sandbox"
            }

        # If too many unknowns, sandbox
        if len(unknowns) >= 2:
            return {
                "verdict": "SANDBOX",
                "reason": "too many unknowns; TRIG6 says not enough signal",
                "views": views,
                "caveman": "MAYBE → TRIG6 → sandbox"
            }

        # Otherwise ship (bounded + reproducible + safe)
        return {
            "verdict": "SHIP",
            "reason": "passes constraints; bounded, repeatable, safe enough",
            "views": views,
            "caveman": "YES → ship"
        }


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    gate = CavemanPhysicsGate()

    examples = [
        Claim(
            text="Magic crystals heal everything instantly.",
            violates_energy=True,
            violates_causality=True,
            has_bounds=False,
            reproducible=False,
            fails_safe=False
        ),
        Claim(
            text="Energy is conserved in closed systems.",
            violates_energy=False,
            violates_causality=False,
            has_bounds=True,
            reproducible=True,
            fails_safe=True,
            confidence=0.95
        ),
        Claim(
            text="Maybe this PDE boundary is fuzzy.",
            violates_energy=None,
            violates_causality=None,
            has_bounds=None,
            reproducible=None,
            fails_safe=None,
            confidence=0.4
        ),
    ]

    for c in examples:
        out = gate.evaluate(c)
        print(f'\nClaim: {c.text}')
        print(out["caveman"])
        print("Verdict:", out["verdict"])
        print("Reason:", out["reason"])
        # Uncomment if you want details:
        # print("Views:", out["views"])
