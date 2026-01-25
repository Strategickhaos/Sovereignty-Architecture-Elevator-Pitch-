# trig6_calibration.py - PMI-gun style calibration for TRIG6 scores
from dataclasses import dataclass
from sklearn.isotonic import IsotonicRegression
import numpy as np

@dataclass
class ClaimMetrics:
    R: float  # Coherence [0,1]
    D: float  # Drift [0,1]
    N: float  # Noise [0,1]
    eq: float # Equilibrium [0,1]
    
    def score(self) -> float:
        return self.R * (1 - self.D) * (1 - self.N) * self.eq

class Trig6Calibrator:
    def __init__(self):
        self._model = IsotonicRegression(out_of_bounds='clip')
        self.calibrated = False
        
    def fit(self, data: list[tuple[ClaimMetrics, float]]):
        scores = np.array([m.score() for m, _ in data])
        outcomes = np.array([y for _, y in data])
        self._model.fit(scores, outcomes)
        self.calibrated = True
        
    def predict_proba(self, m: ClaimMetrics) -> float:
        if not self.calibrated:
            raise ValueError("Calibrator not fitted")
        return float(self._model.predict([m.score()])[0])

# Example usage
if __name__ == "__main__":
    calibrator = Trig6Calibrator()
    # Sample data (expand to 30)
    data = [
        (ClaimMetrics(0.95, 0.05, 0.05, 0.95), 1.0),  # Proven theorem
        (ClaimMetrics(0.90, 0.10, 0.10, 0.90), 1.0),  # Working code
        (ClaimMetrics(0.85, 0.15, 0.15, 0.85), 1.0),  # Working unit test
        (ClaimMetrics(0.80, 0.20, 0.20, 0.80), 1.0),  # Valid parser
        (ClaimMetrics(0.75, 0.25, 0.25, 0.75), 1.0),  # Euler's identity
        (ClaimMetrics(0.30, 0.70, 0.60, 0.20), 0.0),  # Failed proof
        (ClaimMetrics(0.25, 0.75, 0.65, 0.15), 0.0),  # Buggy code
        (ClaimMetrics(0.20, 0.80, 0.70, 0.10), 0.0),  # Failed proof (contradiction)
        (ClaimMetrics(0.15, 0.85, 0.75, 0.05), 0.0),  # Infinite loop code
        (ClaimMetrics(0.10, 0.90, 0.80, 0.00), 0.0),  # False conjecture
        # Add 20 more from your work (e.g., lexer success =1, parser bug =0)
    ]
    calibrator.fit(data)
    
    # Test new claim
    new_claim = ClaimMetrics(0.8, 0.2, 0.3, 0.7)
    raw_f = new_claim.score()  # 0.336
    calibrated_p = calibrator.predict_proba(new_claim)  # e.g., 0.75 after fit
    print(f"Raw: {raw_f:.4f}, Calibrated P(correct): {calibrated_p:.4f}")
