# bci_trig6_gate.py - Neuralink-style BCI stability gate with TRIG6
from dataclasses import dataclass

@dataclass
class BCITrig6:
    R: float   # Spike coherence [0,1]
    D: float   # Drift from baseline [0,1]
    N: float   # Signal instability [0,1]
    eq: float  # Safety alignment [0,1]
    
    def score(self) -> float:
        return self.R * (1 - self.D) * (1 - self.N) * self.eq

def bci_gate(metrics: BCITrig6,
             warn: float = 0.6,
             abort: float = 0.4) -> str:
    f = metrics.score()
    if f < abort:
        return "ABORT_SESSION"  # e.g., shutdown BCI
    if f < warn:
        return "DEGRADED_MODE"  # e.g., reduce features
    return "NORMAL"  # e.g., full aug

# Example
if __name__ == "__main__":
    # ADHD burst metrics
    burst = BCITrig6(R=0.85, D=0.15, N=0.25, eq=0.9)
    print(f"Score: {burst.score():.4f}, Verdict: {bci_gate(burst)}")  # 0.459, DEGRADED_MODE
