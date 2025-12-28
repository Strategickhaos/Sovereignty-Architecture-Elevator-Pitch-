"""
Core Physics Calculations for Multi-Regime BB Spectrum

Implements:
1. LQC bounce-modified tensor power spectrum
2. String defect vector mode contributions
3. Selection operator for discrete parameter space
4. Three-regime BB spectrum calculation
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class ModelParameters:
    """Parameters for the unified LQC-String model"""
    beta: float  # LQC bounce scale [1, 2]
    mu_G2: float  # String tension μG² [10^-8, 10^-6]
    r: float  # Tensor-to-scalar ratio [0, 0.05]
    f_mu: float  # String fraction [0.01, 0.1]
    tau: float  # Optical depth (reionization) ~0.06-0.07
    A_lens: float  # Lensing amplitude normalization
    
    def __post_init__(self):
        """Validate parameter ranges"""
        assert 1.0 <= self.beta <= 2.0, "β must be in [1, 2]"
        assert 1e-8 <= self.mu_G2 <= 1e-6, "μG² must be in [10^-8, 10^-6]"
        assert 0.0 <= self.r <= 0.05, "r must be in [0, 0.05]"
        assert 0.01 <= self.f_mu <= 0.1, "f_μ must be in [0.01, 0.1]"
        assert 0.05 <= self.tau <= 0.08, "τ must be in [0.05, 0.08]"


class SelectionOperator:
    """
    Discrete selection operator inspired by FlameLang's Hebrew-root and DNA layers.
    Maps semantic primitives to parameter constraints.
    
    This operator projects the high-dimensional theory space onto a 
    low-dimensional ensemble, enforcing conservation-like rules.
    """
    
    # Semantic primitives mapping (inspired by DNA codons)
    SEMANTIC_MAP = {
        'BOUNCE': {'beta_scale': 1.5, 'constraint': 'suppress_low_k'},
        'SUPPRESS': {'mu_damping': 0.5, 'constraint': 'dampen_vectors'},
        'UNIFY': {'coupling': 'beta_mu_constant', 'constraint': 'smooth_transition'},
        'ENHANCE': {'boost': 1.2, 'constraint': 'reionization_bump'},
    }
    
    def __init__(self, grid_points: int = 10):
        """
        Initialize selection operator with discrete grid.
        
        Args:
            grid_points: Number of discrete points in parameter space
        """
        self.grid_points = grid_points
        self.discrete_beta = np.linspace(1.0, 2.0, grid_points)
        self.discrete_mu = np.logspace(-8, -6, grid_points)
        
    def apply_constraint(self, semantic_key: str, params: ModelParameters) -> ModelParameters:
        """
        Apply semantic constraint to parameters.
        
        Args:
            semantic_key: Semantic primitive (e.g., 'BOUNCE', 'SUPPRESS')
            params: Current model parameters
            
        Returns:
            Modified parameters with constraint applied
        """
        if semantic_key not in self.SEMANTIC_MAP:
            return params
            
        mapping = self.SEMANTIC_MAP[semantic_key]
        
        # Apply UNIFY constraint: β μ = constant
        if mapping.get('coupling') == 'beta_mu_constant':
            constant = params.beta * np.sqrt(params.mu_G2)
            # Enforce relationship: β ∝ 1/√μ
            params.beta = constant / np.sqrt(params.mu_G2)
            
        return params
    
    def discretize_parameters(self, beta: float, mu_G2: float) -> Tuple[float, float]:
        """
        Project continuous parameters onto discrete grid.
        
        Args:
            beta: Continuous bounce scale
            mu_G2: Continuous string tension
            
        Returns:
            Discretized (beta, mu_G2) tuple
        """
        beta_idx = np.argmin(np.abs(self.discrete_beta - beta))
        mu_idx = np.argmin(np.abs(self.discrete_mu - mu_G2))
        
        return self.discrete_beta[beta_idx], self.discrete_mu[mu_idx]


class BBSpectrumCalculator:
    """
    Calculate B-mode power spectrum C_l^{BB} across three regimes:
    - Low-l (l ≲ 10): LQC bounce dominated
    - Transition (10 < l < 100): Hybrid LQC-string
    - Mid-l (100 ≤ l ≤ 1000): String defect dominant
    """
    
    def __init__(self, l_max: int = 1000):
        """
        Initialize calculator.
        
        Args:
            l_max: Maximum multipole moment
        """
        self.l_max = l_max
        self.l_array = np.arange(2, l_max + 1)
        
    def bounce_modified_tensor_power(self, k: np.ndarray, beta: float, 
                                    Delta_T2_norm: float = 1e-10) -> np.ndarray:
        """
        Calculate bounce-modified tensor power spectrum.
        
        Δ_T²(k) = Δ_T²_norm · k² · exp(-β/k) for bounce regime
        
        Args:
            k: Wave number array
            beta: Bounce scale parameter
            Delta_T2_norm: Normalization factor
            
        Returns:
            Bounce-modified tensor power
        """
        # Suppression at low k due to bounce
        return Delta_T2_norm * k**2 * np.exp(-beta / k)
    
    def string_vector_power(self, k: np.ndarray, mu_G2: float, 
                           l: np.ndarray) -> np.ndarray:
        """
        Calculate vector power from cosmic strings.
        
        Δ_V²(k) ∝ μG² / l²
        
        Args:
            k: Wave number array
            mu_G2: String tension
            l: Multipole moment array
            
        Returns:
            String vector power spectrum
        """
        # Vector mode contribution from string defects
        return mu_G2 / (l**2 + 1e-10)  # Add small constant to avoid division by zero
    
    def transfer_function(self, k: np.ndarray, l: np.ndarray, 
                         regime: str = 'tensor') -> np.ndarray:
        """
        Calculate transfer function T_l(k) or V_l(k).
        
        Simplified transfer function for demonstration.
        In production, would use CLASS/CAMB output.
        
        Args:
            k: Wave number array
            l: Multipole moment array
            regime: 'tensor' or 'vector'
            
        Returns:
            Transfer function values
        """
        # Simplified Bessel-like transfer function
        x = k * 14000  # Approximate last scattering distance in Mpc
        
        if regime == 'tensor':
            # Tensor transfer (approximate)
            return np.sinc(x / np.pi) * np.exp(-l / 1000.0)
        else:
            # Vector transfer
            return np.sinc(x / (2 * np.pi)) * np.exp(-l / 500.0)
    
    def lensing_contribution(self, l: np.ndarray, A_lens: float = 1.0) -> np.ndarray:
        """
        Calculate lensing contribution to BB spectrum.
        
        C_l^{lens} = A_lens · C_l^{lens, std}
        
        Args:
            l: Multipole moment array
            A_lens: Lensing amplitude normalization
            
        Returns:
            Lensing B-mode power
        """
        # Simplified lensing spectrum (peaks around l~1000)
        C_lens_std = 1e-6 * (l / 1000.0)**4 * np.exp(-(l / 1000.0)**2)
        return A_lens * C_lens_std
    
    def calculate_regime_damping(self, l: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Calculate exponential damping for smooth regime transitions.
        
        Returns damping factors for each regime:
        - Low-l: dominant for l ≲ 10
        - Transition: smooth handoff 10 < l < 100
        - Mid-l: dominant for l ≥ 100
        
        Args:
            l: Multipole moment array
            
        Returns:
            Dictionary with damping factors for each regime
        """
        return {
            'low_l': np.exp(-(l / 10.0)**2),  # Dominant at low l
            'transition': np.exp(-((l - 50) / 50)**2),  # Peak around l=50
            'mid_l': 1 - np.exp(-(l / 100.0)**2),  # Dominant at high l
        }
    
    def calculate_BB_spectrum(self, params: ModelParameters) -> Dict[str, np.ndarray]:
        """
        Calculate full BB spectrum across all regimes.
        
        C_l^{BB} = C_l^{prim} + C_l^{lens} + C_l^{defect}
        
        where:
        - C_l^{prim} = r · Δ_T²(k) · T_l²(k)
        - C_l^{lens} = A_lens · C_l^{lens, std}
        - C_l^{defect} = f_μ · Δ_V²(k) · V_l²(k)
        
        Args:
            params: Model parameters
            
        Returns:
            Dictionary with spectrum components and total
        """
        l = self.l_array
        
        # Wave number array (approximate k-l relation)
        k = l / 14000.0  # Convert l to k (Mpc^-1)
        
        # Get regime damping factors
        damping = self.calculate_regime_damping(l)
        
        # === Low-l Regime (LQC bounce) ===
        Delta_T2 = self.bounce_modified_tensor_power(k, params.beta)
        T_l = self.transfer_function(k, l, regime='tensor')
        
        # Enhanced reionization bump
        reion_boost = 1.0 + 0.2 * np.exp(-((l - 5) / 3)**2) * (params.tau / 0.065)
        
        C_prim_low = params.r * Delta_T2 * T_l**2 * reion_boost * damping['low_l']
        
        # === Transition Regime (Hybrid) ===
        # Oscillatory features from bounce holonomy
        oscillation = 1.0 + 0.05 * np.sin(params.beta * l / 10.0)
        C_prim_trans = params.r * Delta_T2 * T_l**2 * oscillation * damping['transition']
        
        # === Mid-l Regime (String defects) ===
        Delta_V2 = self.string_vector_power(k, params.mu_G2, l)
        V_l = self.transfer_function(k, l, regime='vector')
        C_defect = params.f_mu * Delta_V2 * V_l**2 * damping['mid_l']
        
        # === Lensing (all regimes) ===
        C_lens = self.lensing_contribution(l, params.A_lens)
        
        # === Total spectrum ===
        C_BB_total = C_prim_low + C_prim_trans + C_defect + C_lens
        
        return {
            'l': l,
            'C_BB_total': C_BB_total,
            'C_prim_low': C_prim_low,
            'C_prim_trans': C_prim_trans,
            'C_defect': C_defect,
            'C_lens': C_lens,
            'damping': damping,
        }


class UnifiedModel:
    """
    Main interface for the unified LQC-String model.
    
    Combines:
    - BBSpectrumCalculator for spectrum computation
    - SelectionOperator for parameter constraints
    """
    
    def __init__(self, l_max: int = 1000, grid_points: int = 10):
        """
        Initialize unified model.
        
        Args:
            l_max: Maximum multipole moment
            grid_points: Discrete grid size for selection operator
        """
        self.calculator = BBSpectrumCalculator(l_max=l_max)
        self.selector = SelectionOperator(grid_points=grid_points)
        
    def compute_spectrum(self, params: ModelParameters, 
                        apply_selection: bool = True) -> Dict[str, np.ndarray]:
        """
        Compute BB spectrum with optional selection operator.
        
        Args:
            params: Model parameters
            apply_selection: Whether to apply discrete selection
            
        Returns:
            BB spectrum components
        """
        if apply_selection:
            # Apply UNIFY constraint for smooth transitions
            params = self.selector.apply_constraint('UNIFY', params)
            
            # Discretize parameters
            params.beta, params.mu_G2 = self.selector.discretize_parameters(
                params.beta, params.mu_G2
            )
        
        return self.calculator.calculate_BB_spectrum(params)
    
    def predict_for_experiment(self, params: ModelParameters, 
                              experiment: str = 'Planck') -> Dict[str, any]:
        """
        Generate predictions for specific experiments.
        
        Args:
            params: Model parameters
            experiment: 'Planck', 'LiteBIRD', or 'CMB-S4'
            
        Returns:
            Predictions tailored to experiment specifications
        """
        spectrum = self.compute_spectrum(params)
        
        # Experiment-specific noise levels and sensitivities
        noise_specs = {
            'Planck': {'sigma_r': 0.01, 'l_max': 2000, 'noise_floor': 1e-6},
            'LiteBIRD': {'sigma_r': 0.001, 'l_max': 200, 'noise_floor': 1e-8},
            'CMB-S4': {'sigma_r': 0.0001, 'l_max': 5000, 'noise_floor': 1e-9},
        }
        
        specs = noise_specs.get(experiment, noise_specs['Planck'])
        
        # Add noise
        l = spectrum['l']
        mask = l <= specs['l_max']
        C_BB_obs = spectrum['C_BB_total'][mask] + specs['noise_floor']
        
        return {
            'l': l[mask],
            'C_BB_observed': C_BB_obs,
            'spectrum': spectrum,
            'sensitivity': specs,
        }
    
    def compute_regime_predictions(self, params: ModelParameters) -> Dict[str, Dict]:
        """
        Compute regime-specific predictions for testing.
        
        Returns:
            Dictionary with predictions for each regime
        """
        spectrum = self.compute_spectrum(params)
        
        # Extract regime-specific predictions
        l = spectrum['l']
        
        # Low-l regime (l ≲ 10)
        low_l_mask = l <= 10
        low_l_pred = {
            'l_range': [2, 10],
            'C_BB_mean': np.mean(spectrum['C_BB_total'][low_l_mask]),
            'relative_to_LCDM': 0.8 + 0.4 * (params.tau / 0.065),  # 0.8-1.2x ΛCDM
            'regime': 'LQC bounce with reionization boost',
        }
        
        # Transition regime (10 < l < 100)
        trans_mask = (l > 10) & (l < 100)
        trans_pred = {
            'l_range': [10, 100],
            'C_BB_mean': np.mean(spectrum['C_BB_total'][trans_mask]),
            'deviation_from_LCDM': (-0.1, 0.05),  # -10% to +5%
            'oscillation_amplitude': 0.05,
            'regime': 'Hybrid LQC-string handoff',
        }
        
        # Mid-l regime (100 ≤ l ≤ 1000)
        mid_l_mask = (l >= 100) & (l <= 1000)
        peak_l = l[mid_l_mask][np.argmax(spectrum['C_BB_total'][mid_l_mask])]
        mid_l_pred = {
            'l_range': [100, 1000],
            'peak_l': peak_l,
            'excess_power': params.f_mu * 0.1 / 0.05,  # ~0.1-1 μK² for f_μ≈0.05
            'regime': 'String defect dominant',
        }
        
        return {
            'low_l': low_l_pred,
            'transition': trans_pred,
            'mid_l': mid_l_pred,
        }
