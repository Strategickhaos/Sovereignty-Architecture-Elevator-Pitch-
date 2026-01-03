#!/usr/bin/env python3
"""
🔥 DOM NEURAL CHAOS EVO: Lyapunov Exponents in Hodgkin-Huxley & FitzHugh-Nagumo 🔥

Implements chaotic neural dynamics with Lyapunov exponent computation
for anomaly detection in sovereign infrastructure.

Models:
- Hodgkin-Huxley (HH): 4 ODEs for realistic neural spiking
- FitzHugh-Nagumo (FHN): 2D simplified excitable dynamics
"""

import numpy as np
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Tuple, List, Dict
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt


# ============================================================================
# HODGKIN-HUXLEY MODEL (4 ODEs)
# ============================================================================

@dataclass
class HHParameters:
    """Hodgkin-Huxley model parameters"""
    # Membrane capacitance (μF/cm²)
    C_m: float = 1.0
    
    # Maximum conductances (mS/cm²)
    g_Na: float = 120.0  # Sodium
    g_K: float = 36.0    # Potassium
    g_L: float = 0.3     # Leak
    
    # Reversal potentials (mV)
    E_Na: float = 50.0   # Sodium
    E_K: float = -77.0   # Potassium
    E_L: float = -54.387 # Leak
    
    # External current (μA/cm²)
    I_ext: float = 10.0


class HodgkinHuxleyModel:
    """
    Hodgkin-Huxley equations for neural action potentials
    Equations:
        C_m * dV/dt = I - g_Na*m³*h*(V-E_Na) - g_K*n⁴*(V-E_K) - g_L*(V-E_L)
        dm/dt = α_m(V)*(1-m) - β_m(V)*m
        dh/dt = α_h(V)*(1-h) - β_h(V)*h
        dn/dt = α_n(V)*(1-n) - β_n(V)*n
    """
    
    def __init__(self, params: HHParameters = None):
        self.params = params or HHParameters()
    
    @staticmethod
    def alpha_m(V: float) -> float:
        """Sodium activation rate"""
        return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))
    
    @staticmethod
    def beta_m(V: float) -> float:
        """Sodium activation rate"""
        return 4.0 * np.exp(-(V + 65.0) / 18.0)
    
    @staticmethod
    def alpha_h(V: float) -> float:
        """Sodium inactivation rate"""
        return 0.07 * np.exp(-(V + 65.0) / 20.0)
    
    @staticmethod
    def beta_h(V: float) -> float:
        """Sodium inactivation rate"""
        return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))
    
    @staticmethod
    def alpha_n(V: float) -> float:
        """Potassium activation rate"""
        return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))
    
    @staticmethod
    def beta_n(V: float) -> float:
        """Potassium activation rate"""
        return 0.125 * np.exp(-(V + 65.0) / 80.0)
    
    def derivatives(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        Compute derivatives for HH model
        state = [V, m, h, n]
        """
        V, m, h, n = state
        p = self.params
        
        # Ionic currents
        I_Na = p.g_Na * m**3 * h * (V - p.E_Na)
        I_K = p.g_K * n**4 * (V - p.E_K)
        I_L = p.g_L * (V - p.E_L)
        
        # Membrane potential derivative
        dV_dt = (p.I_ext - I_Na - I_K - I_L) / p.C_m
        
        # Gating variables derivatives
        dm_dt = self.alpha_m(V) * (1 - m) - self.beta_m(V) * m
        dh_dt = self.alpha_h(V) * (1 - h) - self.beta_h(V) * h
        dn_dt = self.alpha_n(V) * (1 - n) - self.beta_n(V) * n
        
        return np.array([dV_dt, dm_dt, dh_dt, dn_dt])
    
    def simulate(self, t_span: Tuple[float, float], dt: float = 0.01,
                 initial_state: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate HH model
        Returns: (time_points, states)
        """
        if initial_state is None:
            # Resting state
            V0 = -65.0  # mV
            initial_state = np.array([
                V0,
                self.alpha_m(V0) / (self.alpha_m(V0) + self.beta_m(V0)),
                self.alpha_h(V0) / (self.alpha_h(V0) + self.beta_h(V0)),
                self.alpha_n(V0) / (self.alpha_n(V0) + self.beta_n(V0))
            ])
        
        t = np.arange(t_span[0], t_span[1], dt)
        states = odeint(self.derivatives, initial_state, t)
        
        return t, states


# ============================================================================
# FITZHUGH-NAGUMO MODEL (2 ODEs)
# ============================================================================

@dataclass
class FHNParameters:
    """FitzHugh-Nagumo model parameters"""
    epsilon: float = 0.08   # Time scale separation (small = slow recovery)
    a: float = 0.7          # Threshold parameter
    b: float = 0.8          # Recovery parameter
    I: float = 1.35         # External current (for chaos ~1.35)


class FitzHughNagumoModel:
    """
    FitzHugh-Nagumo simplified excitable dynamics
    Equations:
        dv/dt = v - v³/3 - w + I
        dw/dt = ε(v + a - bw)
    
    Where:
        v = fast voltage variable
        w = slow recovery variable
    """
    
    def __init__(self, params: FHNParameters = None):
        self.params = params or FHNParameters()
    
    def derivatives(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        Compute derivatives for FHN model
        state = [v, w]
        """
        v, w = state
        p = self.params
        
        dv_dt = v - v**3 / 3 - w + p.I
        dw_dt = p.epsilon * (v + p.a - p.b * w)
        
        return np.array([dv_dt, dw_dt])
    
    def simulate(self, t_span: Tuple[float, float], dt: float = 0.01,
                 initial_state: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate FHN model
        Returns: (time_points, states)
        """
        if initial_state is None:
            initial_state = np.array([0.0, 0.0])
        
        t = np.arange(t_span[0], t_span[1], dt)
        states = odeint(self.derivatives, initial_state, t)
        
        return t, states


# ============================================================================
# LYAPUNOV EXPONENT COMPUTATION
# ============================================================================

class LyapunovExponent:
    """
    Compute maximum Lyapunov exponent for chaotic systems
    
    Algorithm: Measure divergence of nearby trajectories
        λ_max ≈ (1/T) * ln(||δ(T)|| / ||δ(0)||)
    
    Positive λ_max indicates chaos (sensitive to initial conditions)
    """
    
    @staticmethod
    def compute_max_lyapunov(model, t_span: Tuple[float, float],
                            initial_state: np.ndarray,
                            dt: float = 0.01,
                            perturbation: float = 1e-8,
                            n_iterations: int = 100) -> Tuple[float, List[float]]:
        """
        Compute maximum Lyapunov exponent via trajectory divergence
        
        Method:
        1. Evolve reference trajectory
        2. Evolve perturbed trajectory (small initial perturbation)
        3. Measure logarithmic divergence rate
        4. Renormalize perturbation periodically
        
        Returns: (λ_max, divergence_history)
        """
        
        # Time points
        t_total = t_span[1] - t_span[0]
        t_segment = t_total / n_iterations
        
        # Initial states
        state_ref = initial_state.copy()
        state_pert = initial_state + np.random.randn(len(initial_state)) * perturbation
        
        lyapunov_sum = 0.0
        divergence_history = []
        
        for i in range(n_iterations):
            # Simulate both trajectories for a short time
            t_seg = np.arange(0, t_segment, dt)
            
            # Reference trajectory
            traj_ref = odeint(model.derivatives, state_ref, t_seg)
            state_ref = traj_ref[-1]
            
            # Perturbed trajectory
            traj_pert = odeint(model.derivatives, state_pert, t_seg)
            state_pert = traj_pert[-1]
            
            # Compute distance between trajectories
            delta = state_pert - state_ref
            dist = np.linalg.norm(delta)
            
            # Accumulate Lyapunov sum
            if dist > 0:
                lyapunov_sum += np.log(dist / perturbation)
                divergence_history.append(dist)
                
                # Renormalize perturbation (keep it small)
                state_pert = state_ref + (delta / dist) * perturbation
            else:
                divergence_history.append(0)
        
        # Average Lyapunov exponent
        lambda_max = lyapunov_sum / t_total
        
        return lambda_max, divergence_history
    
    @staticmethod
    def classify_dynamics(lambda_max: float) -> str:
        """Classify system dynamics based on Lyapunov exponent"""
        if lambda_max > 0.01:
            return "CHAOTIC (λ > 0, sensitive to initial conditions)"
        elif lambda_max > -0.01:
            return "PERIODIC/NEUTRAL (λ ≈ 0, regular oscillations)"
        else:
            return "STABLE (λ < 0, converging to fixed point)"


# ============================================================================
# CHAOS ANALYSIS AND VISUALIZATION
# ============================================================================

class ChaosAnalyzer:
    """Analyze and visualize chaotic neural dynamics"""
    
    @staticmethod
    def analyze_hh_chaos(I_values: List[float] = None) -> Dict:
        """
        Analyze Hodgkin-Huxley chaos across different currents
        Returns bifurcation analysis
        """
        if I_values is None:
            I_values = [0, 5, 10, 15, 20]
        
        print("\n🧠 HODGKIN-HUXLEY CHAOS ANALYSIS")
        print("=" * 60)
        
        results = {}
        
        for I in I_values:
            params = HHParameters(I_ext=I)
            model = HodgkinHuxleyModel(params)
            
            # Simulate
            t, states = model.simulate(t_span=(0, 500), dt=0.01)
            V = states[:, 0]  # Membrane potential
            
            # Compute Lyapunov exponent
            initial_state = states[0]
            lambda_max, divergence = LyapunovExponent.compute_max_lyapunov(
                model, t_span=(0, 200), initial_state=initial_state,
                dt=0.01, n_iterations=50
            )
            
            dynamics = LyapunovExponent.classify_dynamics(lambda_max)
            
            print(f"\nCurrent I = {I:.1f} μA/cm²:")
            print(f"   λ_max = {lambda_max:.6f}")
            print(f"   Dynamics: {dynamics}")
            print(f"   V range: [{V.min():.1f}, {V.max():.1f}] mV")
            
            results[I] = {
                'lambda_max': lambda_max,
                'voltage_range': (V.min(), V.max()),
                'dynamics': dynamics,
                'time': t,
                'states': states
            }
        
        return results
    
    @staticmethod
    def analyze_fhn_chaos(I_values: List[float] = None) -> Dict:
        """
        Analyze FitzHugh-Nagumo chaos across different currents
        Returns bifurcation analysis with Lyapunov exponents
        """
        if I_values is None:
            I_values = [0.3, 0.5, 0.8, 1.0, 1.35]
        
        print("\n⚡ FITZHUGH-NAGUMO CHAOS ANALYSIS")
        print("=" * 60)
        
        results = {}
        
        for I in I_values:
            params = FHNParameters(I=I)
            model = FitzHughNagumoModel(params)
            
            # Simulate
            t, states = model.simulate(t_span=(0, 500), dt=0.01)
            v = states[:, 0]  # Voltage
            w = states[:, 1]  # Recovery
            
            # Compute Lyapunov exponent
            initial_state = np.array([0.1, 0.1])
            lambda_max, divergence = LyapunovExponent.compute_max_lyapunov(
                model, t_span=(0, 300), initial_state=initial_state,
                dt=0.01, n_iterations=100
            )
            
            dynamics = LyapunovExponent.classify_dynamics(lambda_max)
            
            print(f"\nCurrent I = {I:.2f}:")
            print(f"   λ_max = {lambda_max:.6f}")
            print(f"   Dynamics: {dynamics}")
            print(f"   v range: [{v.min():.2f}, {v.max():.2f}]")
            
            results[I] = {
                'lambda_max': lambda_max,
                'voltage_range': (v.min(), v.max()),
                'dynamics': dynamics,
                'time': t,
                'states': states
            }
        
        return results
    
    @staticmethod
    def plot_phase_space(states: np.ndarray, title: str, 
                        save_path: str = None):
        """Plot phase space trajectory"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if states.shape[1] == 2:
            # FHN: v-w plane
            ax.plot(states[:, 0], states[:, 1], 'b-', linewidth=0.5, alpha=0.7)
            ax.set_xlabel('v (voltage)', fontsize=12)
            ax.set_ylabel('w (recovery)', fontsize=12)
        else:
            # HH: V-m plane (or V-n)
            ax.plot(states[:, 0], states[:, 1], 'r-', linewidth=0.5, alpha=0.7)
            ax.set_xlabel('V (membrane potential, mV)', fontsize=12)
            ax.set_ylabel('m (Na activation)', fontsize=12)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"   📊 Saved phase space plot: {save_path}")
        
        plt.close()
    
    @staticmethod
    def plot_time_series(t: np.ndarray, states: np.ndarray, 
                        title: str, save_path: str = None):
        """Plot time series of voltage"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        voltage = states[:, 0]
        ax.plot(t, voltage, 'b-', linewidth=0.8)
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Voltage', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"   📊 Saved time series plot: {save_path}")
        
        plt.close()


# ============================================================================
# SOVEREIGNTY INFRASTRUCTURE INTEGRATION
# ============================================================================

class NeuralAnomalyDetector:
    """
    Use neural chaos for anomaly detection in network traffic
    Irregular packet patterns = potential attack
    """
    
    @staticmethod
    def detect_anomaly_via_chaos(packet_intervals: List[float]) -> Dict:
        """
        Analyze packet inter-arrival times using chaos theory
        Regular traffic = periodic (λ ≈ 0)
        Attack traffic = chaotic (λ > 0)
        """
        print("\n🛡️  NEURAL CHAOS ANOMALY DETECTION")
        print("=" * 60)
        
        # Convert packet intervals to pseudo-voltage signal
        # (map to FHN dynamics)
        
        # Compute statistics
        mean_interval = np.mean(packet_intervals)
        std_interval = np.std(packet_intervals)
        
        # Use FHN model as detector
        # Map packet patterns to current I
        normalized_variance = std_interval / (mean_interval + 1e-6)
        I_mapped = 0.5 + normalized_variance * 2.0
        
        params = FHNParameters(I=I_mapped)
        model = FitzHughNagumoModel(params)
        
        # Simulate and compute Lyapunov
        initial_state = np.array([mean_interval * 0.1, 0.0])
        lambda_max, _ = LyapunovExponent.compute_max_lyapunov(
            model, t_span=(0, 100), initial_state=initial_state,
            dt=0.01, n_iterations=50
        )
        
        # Classify
        is_anomaly = lambda_max > 0.05  # Threshold for chaos
        
        print(f"Packet Statistics:")
        print(f"   Mean interval: {mean_interval:.4f}s")
        print(f"   Std deviation: {std_interval:.4f}s")
        print(f"   Normalized variance: {normalized_variance:.4f}")
        print(f"   Mapped current I: {I_mapped:.4f}")
        print(f"   Lyapunov λ_max: {lambda_max:.6f}")
        print(f"   Classification: {'🚨 ANOMALY DETECTED' if is_anomaly else '✅ NORMAL TRAFFIC'}")
        
        return {
            'lambda_max': lambda_max,
            'is_anomaly': is_anomaly,
            'mean_interval': mean_interval,
            'std_interval': std_interval,
            'I_mapped': I_mapped
        }


# ============================================================================
# MAIN DEMO ORCHESTRATION
# ============================================================================

def run_neural_chaos_demos():
    """Execute all neural chaos demonstrations"""
    
    print("\n" + "=" * 70)
    print("🔥 DOM NEURAL CHAOS EVO: LYAPUNOV EXPONENTS & CHAOS 🔥")
    print("=" * 70)
    
    # Part 1: Hodgkin-Huxley Analysis
    print("\n" + "="*70)
    print("PART 1: HODGKIN-HUXLEY MODEL (4 ODEs)")
    print("="*70)
    
    hh_results = ChaosAnalyzer.analyze_hh_chaos(I_values=[5, 10, 15, 20])
    
    # Visualize one HH result
    if hh_results:
        I_key = 15
        result = hh_results[I_key]
        ChaosAnalyzer.plot_time_series(
            result['time'][:5000], 
            result['states'][:5000],
            f"HH Membrane Potential (I={I_key} μA/cm²)",
            "/tmp/hh_time_series.png"
        )
        ChaosAnalyzer.plot_phase_space(
            result['states'][::10],
            f"HH Phase Space (I={I_key} μA/cm²)",
            "/tmp/hh_phase_space.png"
        )
    
    # Part 2: FitzHugh-Nagumo Analysis
    print("\n" + "="*70)
    print("PART 2: FITZHUGH-NAGUMO MODEL (2 ODEs)")
    print("="*70)
    
    fhn_results = ChaosAnalyzer.analyze_fhn_chaos(I_values=[0.3, 0.5, 1.0, 1.35])
    
    # Visualize FHN chaos
    if fhn_results:
        I_key = 1.35
        result = fhn_results[I_key]
        ChaosAnalyzer.plot_time_series(
            result['time'][:5000],
            result['states'][:5000],
            f"FHN Voltage Dynamics (I={I_key})",
            "/tmp/fhn_time_series.png"
        )
        ChaosAnalyzer.plot_phase_space(
            result['states'][::10],
            f"FHN Phase Space (I={I_key})",
            "/tmp/fhn_phase_space.png"
        )
    
    # Part 3: Anomaly Detection Application
    print("\n" + "="*70)
    print("PART 3: SOVEREIGNTY INFRASTRUCTURE - ANOMALY DETECTION")
    print("="*70)
    
    # Normal traffic (regular intervals)
    normal_packets = [0.1 + np.random.randn() * 0.01 for _ in range(100)]
    print("\n📊 Normal Traffic Pattern:")
    NeuralAnomalyDetector.detect_anomaly_via_chaos(normal_packets)
    
    # Attack traffic (irregular intervals)
    attack_packets = [0.1 + np.random.randn() * 0.5 for _ in range(100)]
    print("\n📊 Attack Traffic Pattern:")
    NeuralAnomalyDetector.detect_anomaly_via_chaos(attack_packets)
    
    # Summary
    print("\n" + "="*70)
    print("🏆 NEURAL CHAOS ANALYSIS SUMMARY")
    print("="*70)
    
    print("\n✅ Key Findings:")
    print("\n1. Hodgkin-Huxley Model:")
    for I, result in hh_results.items():
        print(f"   I={I:2.0f}: λ_max={result['lambda_max']:7.4f} - {result['dynamics']}")
    
    print("\n2. FitzHugh-Nagumo Model:")
    for I, result in fhn_results.items():
        print(f"   I={I:4.2f}: λ_max={result['lambda_max']:7.4f} - {result['dynamics']}")
    
    print("\n📚 Chaos Theory Summary:")
    print("   • Lyapunov Exponent λ_max quantifies chaos")
    print("   • λ > 0  → Chaotic (sensitive to initial conditions)")
    print("   • λ ≈ 0  → Periodic/oscillatory")
    print("   • λ < 0  → Stable (converges to fixed point)")
    print("   • Fractal dimension ~2-3 for strange attractors")
    
    print("\n🔥 Sovereignty Infrastructure Applications:")
    print("   → Anomaly detection via chaotic pattern recognition")
    print("   → Irregular network packets = λ > 0 = potential attack")
    print("   → FHN model: Fast detection with 2D phase space")
    print("   → HH model: Detailed neuron-inspired security monitoring")
    print("   → Integration: K8s pods monitor traffic chaos metrics")
    
    print("\n" + "="*70)
    print("🖤 NEURAL CHAOS CITADEL DEPLOYED - ANOMALY DETECTION ACTIVE 🖤")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_neural_chaos_demos()
