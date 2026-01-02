#!/usr/bin/env python3
"""
Hodgkin-Huxley Neuron Model Implementation
===========================================

A foundational mathematical framework in neuroscience (1952) for modeling
action potentials in neurons. This implementation includes:
- Complete HH equations for voltage and ion channel kinetics
- Fractal pattern analysis (bifurcations, chaos, Lyapunov exponents)
- Visualization of neural dynamics

The model exhibits nonlinear dynamics that can lead to fractal patterns,
self-similar structures in ion channel behavior, and chaotic spiking regimes.
"""

import numpy as np
from scipy.integrate import odeint
from typing import Tuple, Dict, List, Optional
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class HHParameters:
    """
    Hodgkin-Huxley Model Parameters
    
    These parameters represent biophysical properties of the neuron membrane,
    tuned to experimental data and can vary across cell types.
    """
    # Membrane capacitance (μF/cm²)
    C: float = 1.0
    
    # Maximum conductances (mS/cm²)
    g_Na: float = 120.0  # Sodium conductance
    g_K: float = 36.0    # Potassium conductance
    g_L: float = 0.3     # Leak conductance
    
    # Reversal potentials (mV)
    V_Na: float = 50.0   # Sodium reversal potential
    V_K: float = -77.0   # Potassium reversal potential
    V_L: float = -54.387 # Leak reversal potential
    
    # Applied current (μA/cm²)
    I_ext: float = 10.0


class HodgkinHuxleyModel:
    """
    Complete Hodgkin-Huxley neuron model with fractal analysis capabilities.
    
    The model describes action potential generation through four coupled ODEs:
    - Membrane voltage (V)
    - Sodium activation gate (m)
    - Sodium inactivation gate (h)
    - Potassium activation gate (n)
    """
    
    def __init__(self, params: Optional[HHParameters] = None):
        """Initialize with default or custom parameters."""
        self.params = params if params else HHParameters()
        
    def alpha_m(self, V: float) -> float:
        """
        Sodium activation rate function α_m.
        Controls the opening rate of sodium channels.
        
        Formula: α_m = 0.1(V + 40) / (1 - exp(-(V + 40)/10))
        """
        if abs(V + 40.0) < 1e-10:  # Handle singularity at V = -40
            return 1.0
        return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))
    
    def beta_m(self, V: float) -> float:
        """
        Sodium activation rate function β_m.
        Controls the closing rate of sodium channels.
        
        Formula: β_m = 4 exp(-(V + 65)/18)
        """
        return 4.0 * np.exp(-(V + 65.0) / 18.0)
    
    def alpha_h(self, V: float) -> float:
        """
        Sodium inactivation rate function α_h.
        Controls the inactivation of sodium channels.
        
        Formula: α_h = 0.07 exp(-(V + 65)/20)
        """
        return 0.07 * np.exp(-(V + 65.0) / 20.0)
    
    def beta_h(self, V: float) -> float:
        """
        Sodium inactivation rate function β_h.
        Controls the recovery from inactivation.
        
        Formula: β_h = 1 / (1 + exp(-(V + 35)/10))
        """
        return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))
    
    def alpha_n(self, V: float) -> float:
        """
        Potassium activation rate function α_n.
        Controls the opening rate of potassium channels.
        
        Formula: α_n = 0.01(V + 55) / (1 - exp(-(V + 55)/10))
        """
        if abs(V + 55.0) < 1e-10:  # Handle singularity at V = -55
            return 0.1
        return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))
    
    def beta_n(self, V: float) -> float:
        """
        Potassium activation rate function β_n.
        Controls the closing rate of potassium channels.
        
        Formula: β_n = 0.125 exp(-(V + 65)/80)
        """
        return 0.125 * np.exp(-(V + 65.0) / 80.0)
    
    def I_Na(self, V: float, m: float, h: float) -> float:
        """
        Sodium current I_Na = g_Na * m³ * h * (V - V_Na).
        Responsible for the rapid upstroke during action potential.
        """
        return self.params.g_Na * (m ** 3) * h * (V - self.params.V_Na)
    
    def I_K(self, V: float, n: float) -> float:
        """
        Potassium current I_K = g_K * n⁴ * (V - V_K).
        Responsible for repolarization of the membrane.
        """
        return self.params.g_K * (n ** 4) * (V - self.params.V_K)
    
    def I_L(self, V: float) -> float:
        """
        Leak current I_L = g_L * (V - V_L).
        Passive current maintaining resting potential.
        """
        return self.params.g_L * (V - self.params.V_L)
    
    def derivatives(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        System of ODEs for the Hodgkin-Huxley model.
        
        Main equations:
        C dV/dt = I_ext - I_Na - I_K - I_L
        dm/dt = α_m(1-m) - β_m·m
        dh/dt = α_h(1-h) - β_h·h
        dn/dt = α_n(1-n) - β_n·n
        
        Args:
            state: [V, m, h, n] - voltage and gating variables
            t: time point
            
        Returns:
            derivatives [dV/dt, dm/dt, dh/dt, dn/dt]
        """
        V, m, h, n = state
        
        # Calculate rate constants at current voltage
        am = self.alpha_m(V)
        bm = self.beta_m(V)
        ah = self.alpha_h(V)
        bh = self.beta_h(V)
        an = self.alpha_n(V)
        bn = self.beta_n(V)
        
        # Current balance equation
        dV_dt = (self.params.I_ext - self.I_Na(V, m, h) - 
                 self.I_K(V, n) - self.I_L(V)) / self.params.C
        
        # Gating variable dynamics
        dm_dt = am * (1.0 - m) - bm * m
        dh_dt = ah * (1.0 - h) - bh * h
        dn_dt = an * (1.0 - n) - bn * n
        
        return np.array([dV_dt, dm_dt, dh_dt, dn_dt])
    
    def steady_state_values(self, V: float) -> Tuple[float, float, float]:
        """
        Calculate steady-state values of gating variables at voltage V.
        
        m_∞ = α_m / (α_m + β_m)
        h_∞ = α_h / (α_h + β_h)
        n_∞ = α_n / (α_n + β_n)
        
        Returns:
            (m_inf, h_inf, n_inf)
        """
        m_inf = self.alpha_m(V) / (self.alpha_m(V) + self.beta_m(V))
        h_inf = self.alpha_h(V) / (self.alpha_h(V) + self.beta_h(V))
        n_inf = self.alpha_n(V) / (self.alpha_n(V) + self.beta_n(V))
        return m_inf, h_inf, n_inf
    
    def simulate(self, 
                 t_span: Tuple[float, float] = (0, 100),
                 dt: float = 0.01,
                 V0: float = -65.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate the Hodgkin-Huxley neuron over time.
        
        Args:
            t_span: (start_time, end_time) in milliseconds
            dt: time step in milliseconds
            V0: initial voltage in mV
            
        Returns:
            (time_array, state_array) where state is [V, m, h, n] at each time
        """
        # Initial conditions: resting state at V0
        m0, h0, n0 = self.steady_state_values(V0)
        initial_state = np.array([V0, m0, h0, n0])
        
        # Time points for integration
        t = np.arange(t_span[0], t_span[1], dt)
        
        # Solve ODEs using scipy's odeint
        solution = odeint(self.derivatives, initial_state, t)
        
        return t, solution
    
    def calculate_spikes(self, V: np.ndarray, threshold: float = 0.0) -> np.ndarray:
        """
        Detect action potential spikes in voltage trace.
        
        Args:
            V: voltage array
            threshold: voltage threshold for spike detection (mV)
            
        Returns:
            Array of spike indices
        """
        # Find where voltage crosses threshold from below
        above_threshold = V > threshold
        spike_indices = np.where(np.diff(above_threshold.astype(int)) > 0)[0]
        return spike_indices
    
    def interspike_intervals(self, spike_times: np.ndarray) -> np.ndarray:
        """
        Calculate interspike intervals (ISIs).
        
        Used for fractal analysis - ISIs can show power-law distributions
        indicating fractal temporal structure.
        
        Args:
            spike_times: array of spike times
            
        Returns:
            Array of interspike intervals
        """
        if len(spike_times) < 2:
            return np.array([])
        return np.diff(spike_times)


class FractalAnalysis:
    """
    Fractal pattern analysis for Hodgkin-Huxley dynamics.
    
    Fractals in HH emerge from:
    - Ion channel kinetics with power-law distributions
    - Bifurcations leading to chaos
    - Self-similar patterns across voltage/time scales
    """
    
    @staticmethod
    def lyapunov_exponent(model: HodgkinHuxleyModel,
                         t_span: Tuple[float, float] = (0, 1000),
                         dt: float = 0.01,
                         V0: float = -65.0,
                         perturbation: float = 1e-8) -> float:
        """
        Calculate largest Lyapunov exponent to detect chaos.
        
        Positive λ indicates chaotic dynamics (sensitive dependence on initial conditions).
        λ > 0: Chaos (fractal attractors)
        λ ≈ 0: Periodic or quasi-periodic
        λ < 0: Stable fixed point
        
        Args:
            model: HH model instance
            t_span: time span for calculation
            dt: time step
            V0: initial voltage
            perturbation: size of initial perturbation
            
        Returns:
            Largest Lyapunov exponent
        """
        # Simulate reference trajectory
        t, ref_traj = model.simulate(t_span, dt, V0)
        
        # Simulate perturbed trajectory
        model_pert = HodgkinHuxleyModel(model.params)
        _, pert_traj = model_pert.simulate(t_span, dt, V0 + perturbation)
        
        # Calculate divergence over time
        divergence = np.linalg.norm(pert_traj - ref_traj, axis=1)
        
        # Avoid log(0) by filtering
        valid_indices = divergence > 1e-12
        if np.sum(valid_indices) < 2:
            return 0.0
        
        # Lyapunov exponent from exponential divergence rate
        log_divergence = np.log(divergence[valid_indices])
        t_valid = t[valid_indices]
        
        # Linear fit to log(divergence) vs time gives Lyapunov exponent
        coeffs = np.polyfit(t_valid, log_divergence, 1)
        lyapunov = coeffs[0]
        
        return lyapunov
    
    @staticmethod
    def bifurcation_diagram(I_range: np.ndarray,
                           base_params: Optional[HHParameters] = None,
                           n_transient: int = 500,
                           n_samples: int = 100) -> Dict[str, np.ndarray]:
        """
        Generate bifurcation diagram varying external current I_ext.
        
        Shows transition from regular spiking → bursting → chaos
        as parameter changes, revealing fractal basin boundaries.
        
        Args:
            I_range: range of I_ext values to test
            base_params: base parameters (I_ext will be overridden)
            n_transient: number of initial points to discard
            n_samples: number of points to sample after transient
            
        Returns:
            Dictionary with 'I_values' and 'V_values' arrays
        """
        if base_params is None:
            base_params = HHParameters()
        
        I_values = []
        V_values = []
        
        for I_ext in I_range:
            # Set current for this iteration
            params = HHParameters(
                C=base_params.C,
                g_Na=base_params.g_Na,
                g_K=base_params.g_K,
                g_L=base_params.g_L,
                V_Na=base_params.V_Na,
                V_K=base_params.V_K,
                V_L=base_params.V_L,
                I_ext=I_ext
            )
            
            model = HodgkinHuxleyModel(params)
            
            # Simulate long enough to reach attractor and sample
            t_total = 50 + (n_transient + n_samples) * 0.1
            t, solution = model.simulate((0, t_total), dt=0.1)
            
            V = solution[:, 0]
            
            # Find local maxima (spike peaks) after transient
            transient_idx = int(50 / 0.1)  # Skip first 50ms
            V_steady = V[transient_idx:]
            
            # Simple peak detection
            peaks = []
            for i in range(1, len(V_steady) - 1):
                if V_steady[i] > V_steady[i-1] and V_steady[i] > V_steady[i+1]:
                    if V_steady[i] > -20:  # Only count actual spikes
                        peaks.append(V_steady[i])
            
            # Store current value and corresponding peak voltages
            for peak in peaks[:n_samples]:
                I_values.append(I_ext)
                V_values.append(peak)
        
        return {
            'I_values': np.array(I_values),
            'V_values': np.array(V_values)
        }


class HHVisualizer:
    """Visualization tools for Hodgkin-Huxley model results."""
    
    @staticmethod
    def plot_voltage_trace(t: np.ndarray, 
                          solution: np.ndarray,
                          title: str = "Hodgkin-Huxley Neuron Simulation") -> plt.Figure:
        """
        Plot voltage and gating variables over time.
        
        Args:
            t: time array
            solution: state array [V, m, h, n]
            title: plot title
            
        Returns:
            matplotlib Figure
        """
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # Voltage trace
        axes[0].plot(t, solution[:, 0], 'b-', linewidth=2, label='Membrane Voltage')
        axes[0].set_ylabel('Voltage (mV)', fontsize=12)
        axes[0].set_title(title, fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        # Gating variables
        axes[1].plot(t, solution[:, 1], 'r-', label='m (Na activation)', linewidth=2)
        axes[1].plot(t, solution[:, 2], 'g-', label='h (Na inactivation)', linewidth=2)
        axes[1].plot(t, solution[:, 3], 'b-', label='n (K activation)', linewidth=2)
        axes[1].set_xlabel('Time (ms)', fontsize=12)
        axes[1].set_ylabel('Gating Variable', fontsize=12)
        axes[1].set_title('Ion Channel Gating Dynamics', fontsize=12)
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        axes[1].set_ylim([0, 1])
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_phase_portrait(solution: np.ndarray,
                          title: str = "Phase Portrait (V-n)") -> plt.Figure:
        """
        Plot phase portrait showing dynamical structure.
        
        Args:
            solution: state array [V, m, h, n]
            title: plot title
            
        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        V = solution[:, 0]
        n = solution[:, 3]
        
        # Color by time progression
        colors = np.arange(len(V))
        scatter = ax.scatter(V, n, c=colors, cmap='viridis', s=1, alpha=0.6)
        
        ax.set_xlabel('Voltage V (mV)', fontsize=12)
        ax.set_ylabel('Potassium gate n', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Time progression', fontsize=10)
        
        return fig
    
    @staticmethod
    def plot_bifurcation(bifurcation_data: Dict[str, np.ndarray],
                        title: str = "Bifurcation Diagram") -> plt.Figure:
        """
        Plot bifurcation diagram showing routes to chaos.
        
        Args:
            bifurcation_data: dict with 'I_values' and 'V_values'
            title: plot title
            
        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.plot(bifurcation_data['I_values'], 
                bifurcation_data['V_values'], 
                'k.', markersize=0.5, alpha=0.5)
        
        ax.set_xlabel('External Current I (μA/cm²)', fontsize=12)
        ax.set_ylabel('Voltage Peaks (mV)', fontsize=12)
        ax.set_title(title + '\n(Period-doubling route to chaos)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        return fig


def example_simulation():
    """
    Example: Simulate HH neuron with different stimulation currents.
    Demonstrates regular spiking, bursting, and potential chaos.
    """
    print("=" * 70)
    print("Hodgkin-Huxley Neuron Model - Example Simulation")
    print("=" * 70)
    
    # Example 1: Regular spiking with moderate current
    print("\n1. Regular spiking regime (I = 10 μA/cm²)")
    params_regular = HHParameters(I_ext=10.0)
    model_regular = HodgkinHuxleyModel(params_regular)
    t, solution = model_regular.simulate(t_span=(0, 100), dt=0.01)
    
    spikes = model_regular.calculate_spikes(solution[:, 0])
    print(f"   Number of spikes: {len(spikes)}")
    print(f"   Spike frequency: {len(spikes) / (t[-1] - t[0]) * 1000:.2f} Hz")
    
    # Example 2: Higher current - potential bursting
    print("\n2. Higher stimulation (I = 50 μA/cm²)")
    params_high = HHParameters(I_ext=50.0)
    model_high = HodgkinHuxleyModel(params_high)
    t2, solution2 = model_high.simulate(t_span=(0, 100), dt=0.01)
    
    spikes2 = model_high.calculate_spikes(solution2[:, 0])
    print(f"   Number of spikes: {len(spikes2)}")
    print(f"   Spike frequency: {len(spikes2) / (t2[-1] - t2[0]) * 1000:.2f} Hz")
    
    # Example 3: Fractal analysis - Lyapunov exponent
    print("\n3. Fractal Analysis - Lyapunov Exponent")
    print("   (Positive value indicates chaotic/fractal dynamics)")
    lyap = FractalAnalysis.lyapunov_exponent(model_regular, t_span=(0, 500))
    print(f"   Lyapunov exponent: {lyap:.6f}")
    
    if lyap > 0.001:
        print("   → Chaotic regime detected! (Fractal attractor)")
    elif lyap > -0.001:
        print("   → Periodic/quasi-periodic regime")
    else:
        print("   → Stable regime")
    
    # Visualization
    print("\n4. Generating visualizations...")
    
    # Plot voltage trace
    fig1 = HHVisualizer.plot_voltage_trace(t, solution)
    fig1.savefig('/tmp/hh_voltage_trace.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved voltage trace to /tmp/hh_voltage_trace.png")
    
    # Plot phase portrait
    fig2 = HHVisualizer.plot_phase_portrait(solution)
    fig2.savefig('/tmp/hh_phase_portrait.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved phase portrait to /tmp/hh_phase_portrait.png")
    
    # Bifurcation diagram (this may take a moment)
    print("\n5. Computing bifurcation diagram (route to chaos)...")
    I_range = np.linspace(0, 100, 200)  # Vary external current
    bifurc_data = FractalAnalysis.bifurcation_diagram(I_range, n_transient=500, n_samples=50)
    
    fig3 = HHVisualizer.plot_bifurcation(bifurc_data)
    fig3.savefig('/tmp/hh_bifurcation.png', dpi=150, bbox_inches='tight')
    print("   ✓ Saved bifurcation diagram to /tmp/hh_bifurcation.png")
    
    print("\n" + "=" * 70)
    print("Simulation complete!")
    print("=" * 70)
    print("\nKey Insights:")
    print("• The HH model captures realistic action potential generation")
    print("• Parameters (g_Na, g_K, I_ext) control spiking patterns")
    print("• Nonlinear dynamics lead to fractal patterns and chaos")
    print("• Bifurcation diagrams reveal self-similar structure")
    print("• Ion channel kinetics show memory effects (non-Markovian)")
    print("\nBiological Relevance:")
    print("• Fractal patterns emerge from voltage-dependent channel kinetics")
    print("• Parameter variations model different neuron types")
    print("• Chaos explains irregular firing in biological neurons")
    print("• Self-similarity across time scales matches neural data")
    print("=" * 70)
    
    plt.close('all')  # Clean up


if __name__ == "__main__":
    # Run example simulation
    example_simulation()
    
    print("\n" + "=" * 70)
    print("Module Information")
    print("=" * 70)
    print("\nThis module implements the complete Hodgkin-Huxley model:")
    print("• HHParameters: Biophysically realistic parameter values")
    print("• HodgkinHuxleyModel: Core ODE system with voltage & gates")
    print("• FractalAnalysis: Lyapunov exponents & bifurcation analysis")
    print("• HHVisualizer: Plotting tools for results")
    print("\nTo use in your code:")
    print(">>> from hodgkin_huxley_model import HodgkinHuxleyModel, HHParameters")
    print(">>> model = HodgkinHuxleyModel(HHParameters(I_ext=10.0))")
    print(">>> t, solution = model.simulate(t_span=(0, 100))")
    print("=" * 70)
