#!/usr/bin/env python3
"""
TRIG6 Theorem Simulations
Visualizations and empirical validation of TRIG6 theorems

Strategickhaos DAO LLC — Sovereignty Architecture
Author: Dom (Dominic Denicola)
Date: 2026-01-25
License: Proprietary — Patent Pending
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from trig6_core import TRIG6Core, MultiAgentOrchestrator
from typing import List, Tuple


class TRIG6TheoremSimulator:
    """Simulations and visualizations for TRIG6 theorems."""
    
    def __init__(self, output_dir: str = "./trig6_outputs"):
        """
        Initialize simulator.
        
        Args:
            output_dir: Directory for saving outputs
        """
        self.trig6 = TRIG6Core(alpha=0.1)
        self.output_dir = output_dir
        
        # Create output directory
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def theorem1_resonance_maximization(self, n_agents: int = 5,
                                       n_steps: int = 360) -> Tuple[float, np.ndarray]:
        """
        Simulate Theorem 1: Resonance Maximization.
        
        Demonstrates that optimal theta maximizes resonance across agents.
        
        Args:
            n_agents: Number of agents in the system
            n_steps: Number of theta values to evaluate
            
        Returns:
            (theta_opt, resonance_curve)
        """
        print("=" * 60)
        print("Theorem 1: Resonance Maximization Simulation")
        print("=" * 60)
        
        # Generate random agent affinities
        np.random.seed(42)
        agent_affinities = [np.random.randn(6) for _ in range(n_agents)]
        
        # Evaluate resonance across theta values
        theta_values = np.linspace(0, 2 * np.pi, n_steps)
        resonance_values = np.zeros(n_steps)
        
        for i, theta in enumerate(theta_values):
            proj = self.trig6.compute_projection(theta)
            
            # Skip danger zones
            if self.trig6.is_in_danger_zone(proj):
                resonance_values[i] = -np.inf
                continue
            
            # Compute weighted affinity score
            proj_array = proj.to_array()
            score = 0.0
            for affinity in agent_affinities:
                affinity_finite = np.where(np.isfinite(affinity), affinity, 0)
                proj_finite = np.where(np.isfinite(proj_array), proj_array, 0)
                min_len = min(len(affinity_finite), len(proj_finite))
                score += np.dot(affinity_finite[:min_len], proj_finite[:min_len])
            
            resonance_values[i] = score
        
        # Find optimal theta
        valid_indices = np.isfinite(resonance_values)
        theta_opt = theta_values[valid_indices][np.argmax(resonance_values[valid_indices])]
        max_resonance = np.max(resonance_values[valid_indices])
        
        print(f"Optimal θ: {theta_opt:.4f} rad ({np.degrees(theta_opt):.2f}°)")
        print(f"Maximum Resonance: {max_resonance:.4f}")
        
        # Visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Resonance vs Theta
        ax1.plot(np.degrees(theta_values), resonance_values, 
                linewidth=2, label='Resonance Score')
        ax1.axvline(np.degrees(theta_opt), color='red', linestyle='--',
                   label=f'Optimal θ = {np.degrees(theta_opt):.1f}°')
        ax1.axhline(max_resonance, color='green', linestyle=':', alpha=0.5,
                   label=f'Max Resonance = {max_resonance:.2f}')
        ax1.set_xlabel('θ (degrees)', fontsize=12)
        ax1.set_ylabel('Resonance Score', fontsize=12)
        ax1.set_title('Theorem 1: Resonance Maximization', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Polar representation
        ax2 = plt.subplot(2, 1, 2, projection='polar')
        valid_r = np.where(np.isfinite(resonance_values), 
                          resonance_values - resonance_values[valid_indices].min(), 0)
        ax2.plot(theta_values, valid_r, linewidth=2)
        ax2.plot([theta_opt, theta_opt], [0, max_resonance - resonance_values[valid_indices].min()],
                'r--', linewidth=2, label=f'θ_opt = {np.degrees(theta_opt):.1f}°')
        ax2.set_title('Resonance Manifold (Polar)', fontsize=12, fontweight='bold')
        ax2.legend()
        
        plt.tight_layout()
        output_path = f"{self.output_dir}/theorem1_resonance_maximization.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_path}")
        plt.close(fig)
        
        return theta_opt, resonance_values
    
    def theorem2_drift_correction(self, theta_init: float = 0.5,
                                  theta_opt: float = np.pi/3,
                                  n_iterations: int = 50) -> List[float]:
        """
        Simulate Theorem 2: Drift Correction Bound.
        
        Demonstrates exponential convergence of drift correction.
        
        Args:
            theta_init: Initial state angle
            theta_opt: Optimal state angle
            n_iterations: Number of correction iterations
            
        Returns:
            List of theta values during correction
        """
        print("\n" + "=" * 60)
        print("Theorem 2: Drift Correction Bound Simulation")
        print("=" * 60)
        
        theta_history = [theta_init]
        drift_history = []
        noise = 0.3  # Initial noise level
        
        theta_current = theta_init
        
        for i in range(n_iterations):
            # Compute drift
            drift = self.trig6.compute_drift(theta_current, theta_opt)
            drift_history.append(drift)
            
            # Perform correction step
            theta_current = self.trig6.drift_correction_step(
                theta_current, theta_opt, noise
            )
            theta_history.append(theta_current)
            
            # Decay noise (convergence improves)
            noise *= 0.95
        
        print(f"Initial drift: {drift_history[0]:.4f} rad")
        print(f"Final drift: {drift_history[-1]:.4f} rad")
        print(f"Convergence: {(1 - drift_history[-1]/drift_history[0]) * 100:.2f}%")
        
        # Theoretical bound: |D_n| ≤ tanh(α)^n * |D_0|
        alpha_values = np.linspace(0.1, 0.9, 5)
        
        # Visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot 1: Drift convergence
        iterations = np.arange(len(drift_history))
        ax1.semilogy(iterations, drift_history, 'b-', linewidth=2, 
                    marker='o', markersize=4, label='Actual Drift')
        
        # Theoretical bounds
        for alpha in alpha_values:
            bound = drift_history[0] * (np.tanh(alpha) ** iterations)
            ax1.semilogy(iterations, bound, '--', alpha=0.5,
                       label=f'Bound (α={alpha:.1f})')
        
        ax1.set_xlabel('Iteration', fontsize=12)
        ax1.set_ylabel('Drift |D| (log scale)', fontsize=12)
        ax1.set_title('Theorem 2: Drift Correction Convergence', 
                     fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Theta trajectory
        theta_iter = np.arange(len(theta_history))
        ax2.plot(theta_iter, np.degrees(theta_history), 
                'b-', linewidth=2, marker='o', markersize=4, label='θ(t)')
        ax2.axhline(np.degrees(theta_opt), color='red', linestyle='--',
                   label=f'θ_opt = {np.degrees(theta_opt):.1f}°')
        ax2.set_xlabel('Iteration', fontsize=12)
        ax2.set_ylabel('θ (degrees)', fontsize=12)
        ax2.set_title('State Angle Convergence', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = f"{self.output_dir}/theorem2_drift_correction.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_path}")
        plt.close(fig)
        
        return theta_history
    
    def theorem3_emergent_coherence(self, n_agents: int = 10,
                                   n_timesteps: int = 100) -> np.ndarray:
        """
        Simulate Theorem 3: Emergent Coherence.
        
        Demonstrates how decreasing noise leads to coherent swarm behavior.
        
        Args:
            n_agents: Number of agents in the swarm
            n_timesteps: Number of simulation timesteps
            
        Returns:
            Agent theta trajectories (n_agents x n_timesteps)
        """
        print("\n" + "=" * 60)
        print("Theorem 3: Emergent Coherence Simulation")
        print("=" * 60)
        
        # Initialize orchestrator
        theta_opt = np.pi / 4
        orchestrator = MultiAgentOrchestrator(theta_opt=theta_opt, alpha=0.2)
        
        # Register agents with random initial positions
        np.random.seed(42)
        for i in range(n_agents):
            affinity = np.random.randn(6)
            theta_init = np.random.uniform(0, 2 * np.pi)
            orchestrator.register_agent(f"agent_{i}", affinity, theta_init)
        
        # Track metrics over time
        theta_trajectories = np.zeros((n_agents, n_timesteps))
        resonance_history = []
        noise_history = []
        
        for t in range(n_timesteps):
            # Update each agent (random walk with drift towards optimal)
            for i, agent_id in enumerate(orchestrator.agents.keys()):
                agent = orchestrator.agents[agent_id]
                
                # Noise decreases over time (key to emergent coherence)
                noise_level = 1.0 * np.exp(-t / 20.0)
                
                # Random perturbation + drift towards optimal
                x = np.cos(agent['theta']) + np.random.normal(0, noise_level)
                y = np.sin(agent['theta']) + np.random.normal(0, noise_level)
                
                # Bias towards optimal angle
                x_opt = np.cos(theta_opt)
                y_opt = np.sin(theta_opt)
                x = 0.9 * x + 0.1 * x_opt
                y = 0.9 * y + 0.1 * y_opt
                
                orchestrator.update_agent_state(agent_id, x, y)
                theta_trajectories[i, t] = agent['theta']
            
            # Compute system metrics
            metrics = orchestrator.compute_system_metrics()
            resonance_history.append(metrics.resonance)
            noise_history.append(noise_level)
        
        print(f"Initial resonance: {resonance_history[0]:.4f}")
        print(f"Final resonance: {resonance_history[-1]:.4f}")
        print(f"Coherence achieved: {resonance_history[-1] > 0.5}")
        
        # Visualization
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(3, 2, figure=fig)
        
        # Plot 1: Agent trajectories over time
        ax1 = fig.add_subplot(gs[0, :])
        for i in range(n_agents):
            ax1.plot(np.degrees(theta_trajectories[i, :]), 
                    alpha=0.6, linewidth=1.5)
        ax1.axhline(np.degrees(theta_opt), color='red', linestyle='--',
                   linewidth=2, label=f'θ_opt = {np.degrees(theta_opt):.1f}°')
        ax1.set_xlabel('Time Step', fontsize=12)
        ax1.set_ylabel('θ (degrees)', fontsize=12)
        ax1.set_title('Theorem 3: Agent Theta Trajectories', 
                     fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Resonance over time
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(resonance_history, linewidth=2, color='blue')
        ax2.axhline(0.5, color='green', linestyle='--', 
                   label='Coherence Threshold')
        ax2.set_xlabel('Time Step', fontsize=12)
        ax2.set_ylabel('System Resonance', fontsize=12)
        ax2.set_title('Resonance Evolution', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Noise decay
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(noise_history, linewidth=2, color='orange')
        ax3.set_xlabel('Time Step', fontsize=12)
        ax3.set_ylabel('Noise Level', fontsize=12)
        ax3.set_title('Noise Decay (N → 0)', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Initial polar distribution
        ax4 = fig.add_subplot(gs[2, 0], projection='polar')
        initial_theta = theta_trajectories[:, 0]
        ax4.scatter(initial_theta, np.ones_like(initial_theta), 
                   s=100, alpha=0.6, label='Agents')
        ax4.plot([theta_opt, theta_opt], [0, 1], 'r--', 
                linewidth=2, label='θ_opt')
        ax4.set_title('Initial Distribution', fontsize=12, fontweight='bold')
        ax4.legend()
        
        # Plot 5: Final polar distribution (coherence)
        ax5 = fig.add_subplot(gs[2, 1], projection='polar')
        final_theta = theta_trajectories[:, -1]
        ax5.scatter(final_theta, np.ones_like(final_theta), 
                   s=100, alpha=0.6, color='green', label='Agents')
        ax5.plot([theta_opt, theta_opt], [0, 1], 'r--', 
                linewidth=2, label='θ_opt')
        ax5.set_title('Final Distribution (Coherent)', fontsize=12, fontweight='bold')
        ax5.legend()
        
        plt.tight_layout()
        output_path = f"{self.output_dir}/theorem3_emergent_coherence.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_path}")
        plt.close(fig)
        
        return theta_trajectories
    
    def visualize_trig6_manifold(self, n_points: int = 100):
        """
        Visualize the TRIG6 projection manifold.
        
        Args:
            n_points: Number of points to sample
        """
        print("\n" + "=" * 60)
        print("TRIG6 Manifold Visualization")
        print("=" * 60)
        
        theta_values = np.linspace(0, 2 * np.pi, n_points)
        
        # Compute all six projections
        sin_vals = np.sin(theta_values)
        cos_vals = np.cos(theta_values)
        tan_vals = np.tan(theta_values)
        
        # Clip unbounded functions for visualization
        tan_clipped = np.clip(tan_vals, -10, 10)
        
        # Create visualization
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('TRIG6 Projection Manifold', fontsize=16, fontweight='bold')
        
        # Plot each component
        components = [
            (sin_vals, 'sin(θ)', 'blue'),
            (cos_vals, 'cos(θ)', 'red'),
            (tan_clipped, 'tan(θ) [clipped]', 'green'),
        ]
        
        for idx, (vals, name, color) in enumerate(components):
            ax = axes[0, idx]
            ax.plot(np.degrees(theta_values), vals, linewidth=2, color=color)
            ax.set_xlabel('θ (degrees)', fontsize=10)
            ax.set_ylabel(name, fontsize=10)
            ax.set_title(f'Component: {name}', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.axhline(0, color='black', linewidth=0.5)
        
        # Plot hyperbolic blending effects
        alpha_values = [0.1, 0.5, 1.0]
        for idx, alpha in enumerate(alpha_values):
            ax = axes[1, idx]
            
            # Blend sin component at various alpha
            blended = [np.tanh(np.sin(theta) + np.sinh(alpha)) 
                      for theta in theta_values]
            
            ax.plot(np.degrees(theta_values), np.sin(theta_values), 
                   'b-', linewidth=1.5, alpha=0.5, label='Original sin(θ)')
            ax.plot(np.degrees(theta_values), blended, 
                   'r-', linewidth=2, label=f'Blended (α={alpha})')
            ax.set_xlabel('θ (degrees)', fontsize=10)
            ax.set_ylabel('Value', fontsize=10)
            ax.set_title(f'Hyperbolic Blend α={alpha}', fontsize=11, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = f"{self.output_dir}/trig6_manifold.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Visualization saved: {output_path}")
        plt.close(fig)


def run_all_simulations():
    """Run all TRIG6 theorem simulations."""
    print("🔥" * 30)
    print("TRIG6 THEOREM SIMULATION SUITE")
    print("🔥" * 30)
    print()
    
    simulator = TRIG6TheoremSimulator()
    
    # Run all simulations
    simulator.theorem1_resonance_maximization(n_agents=8)
    simulator.theorem2_drift_correction()
    simulator.theorem3_emergent_coherence(n_agents=12, n_timesteps=80)
    simulator.visualize_trig6_manifold()
    
    print("\n" + "🔥" * 30)
    print("✅ ALL SIMULATIONS COMPLETE")
    print(f"📊 Outputs saved to: {simulator.output_dir}")
    print("🔥" * 30)


if __name__ == '__main__':
    run_all_simulations()
