"""
Bridge 10: Neural ↔ Weight Collapse (Energy Minimization)

This is the psychological glue - math-backed.

Formulas:
    E = Σ wᵢxᵢ
    w_{t+1} = w_t - η∇E

This is why:
- You feel "collapse"
- You prune paths
- Singularities matter
"""

import numpy as np
from typing import Callable, List, Tuple, Optional


class EnergyMinimization:
    """Bridges cognitive processes and energy-based optimization."""
    
    @staticmethod
    def energy(weights: np.ndarray, inputs: np.ndarray) -> float:
        """
        Compute energy of a state.
        
        Formula: E = Σ wᵢxᵢ
        
        Args:
            weights: Weight vector
            inputs: Input vector
            
        Returns:
            Energy scalar
        """
        if weights.shape != inputs.shape:
            raise ValueError(f"Weights {weights.shape} and inputs {inputs.shape} must match")
        
        return np.dot(weights, inputs)
    
    @staticmethod
    def gradient_descent_step(weights: np.ndarray, gradient: np.ndarray, 
                               learning_rate: float) -> np.ndarray:
        """
        Perform one gradient descent step.
        
        Formula: w_{t+1} = w_t - η∇E
        
        Args:
            weights: Current weights
            gradient: Gradient of energy function
            learning_rate: Learning rate η
            
        Returns:
            Updated weights
        """
        return weights - learning_rate * gradient
    
    @staticmethod
    def gradient_energy(weights: np.ndarray, inputs: np.ndarray) -> np.ndarray:
        """
        Compute gradient of energy function.
        
        For E = w^T x, ∇E = x
        
        Args:
            weights: Weight vector
            inputs: Input vector
            
        Returns:
            Gradient vector
        """
        return inputs
    
    @staticmethod
    def optimize_weights(initial_weights: np.ndarray, inputs: np.ndarray,
                         learning_rate: float = 0.01, iterations: int = 100,
                         target_energy: Optional[float] = None) -> Tuple[np.ndarray, List[float]]:
        """
        Optimize weights to minimize energy.
        
        Args:
            initial_weights: Starting weights
            inputs: Input vector
            learning_rate: Step size
            iterations: Number of iterations
            target_energy: Optional target energy (stops early if reached)
            
        Returns:
            (final_weights, energy_history)
        """
        weights = initial_weights.copy()
        energy_history = []
        
        for i in range(iterations):
            # Compute current energy
            E = EnergyMinimization.energy(weights, inputs)
            energy_history.append(E)
            
            # Check if target reached
            if target_energy is not None and abs(E - target_energy) < 1e-6:
                break
            
            # Compute gradient
            grad = EnergyMinimization.gradient_energy(weights, inputs)
            
            # Update weights
            weights = EnergyMinimization.gradient_descent_step(weights, grad, learning_rate)
        
        return weights, energy_history
    
    @staticmethod
    def collapse_singularity(weights: np.ndarray, threshold: float = 0.01) -> np.ndarray:
        """
        Prune weights below threshold (simulate collapse).
        
        Args:
            weights: Weight vector
            threshold: Pruning threshold
            
        Returns:
            Pruned weight vector
        """
        collapsed = weights.copy()
        collapsed[np.abs(collapsed) < threshold] = 0
        return collapsed
    
    @staticmethod
    def weight_entropy(weights: np.ndarray) -> float:
        """
        Compute entropy of weight distribution.
        
        Args:
            weights: Weight vector
            
        Returns:
            Shannon entropy
        """
        # Normalize to probabilities
        abs_weights = np.abs(weights)
        total = np.sum(abs_weights)
        
        if total == 0:
            return 0.0
        
        probs = abs_weights / total
        
        # Compute entropy
        entropy = 0
        for p in probs:
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy
    
    @staticmethod
    def energy_landscape_1d(weight_range: Tuple[float, float], 
                             input_value: float, num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Sample 1D energy landscape.
        
        Args:
            weight_range: (min, max) range for weight
            input_value: Fixed input value
            num_points: Number of sample points
            
        Returns:
            (weights, energies): Arrays of weight values and corresponding energies
        """
        weights = np.linspace(weight_range[0], weight_range[1], num_points)
        energies = weights * input_value
        
        return weights, energies
    
    @staticmethod
    def cognitive_load(weights: np.ndarray) -> float:
        """
        Compute cognitive load as L2 norm of weights.
        
        Args:
            weights: Weight vector
            
        Returns:
            Cognitive load
        """
        return np.linalg.norm(weights)
    
    @staticmethod
    def path_pruning_probability(weight: float, temperature: float = 1.0) -> float:
        """
        Compute probability of pruning a path based on weight.
        
        Uses softmax-like function.
        
        Args:
            weight: Weight value
            temperature: Temperature parameter (higher = less aggressive pruning)
            
        Returns:
            Probability of keeping the path (0-1)
        """
        return 1.0 / (1.0 + np.exp(-weight / temperature))
    
    @staticmethod
    def convergence_rate(energy_history: List[float]) -> float:
        """
        Compute convergence rate from energy history.
        
        Args:
            energy_history: List of energy values over iterations
            
        Returns:
            Convergence rate (average change per iteration)
        """
        if len(energy_history) < 2:
            return 0.0
        
        differences = np.diff(energy_history)
        return np.mean(np.abs(differences))
    
    @staticmethod
    def attention_weights(input_features: np.ndarray, 
                          query: np.ndarray) -> np.ndarray:
        """
        Compute attention weights using energy-based approach.
        
        Args:
            input_features: Matrix of input features (n_features x dim)
            query: Query vector (dim,)
            
        Returns:
            Attention weights (n_features,)
        """
        # Compute energies (scores)
        energies = np.dot(input_features, query)
        
        # Softmax to get probabilities
        exp_energies = np.exp(energies - np.max(energies))  # Numerical stability
        weights = exp_energies / np.sum(exp_energies)
        
        return weights
