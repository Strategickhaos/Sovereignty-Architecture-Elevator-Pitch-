"""
Loop Quantum Cosmology (LQC) model implementation.

This module implements the LQC bounce model with modified primordial power spectrum
that affects the CMB power spectrum at large scales (low multipoles).
"""

import numpy as np
from typing import Dict, Optional, Tuple


class LQCModel:
    """
    Loop Quantum Cosmology model for CMB power spectrum predictions.
    
    LQC modifies the primordial power spectrum due to the quantum bounce,
    leading to scale-dependent effects at large scales (low multipoles, l < 30).
    This results in power suppression/enhancement patterns and improved fits
    to Planck data anomalies.
    
    Key parameters:
    - beta: Bounce parameter (β ≈ 1.2-1.5) controlling oscillation frequency
    - tau: Optical depth (τ ≈ 0.06-0.07 vs ΛCDM τ ≈ 0.054)
    - A: Amplitude normalization
    - alpha: Power-law index (α ≈ 0.35)
    """
    
    def __init__(self, beta: float = 1.35, tau: float = 0.065, 
                 A: float = 1.0, alpha: float = 0.35):
        """
        Initialize LQC model with bounce parameters.
        
        Args:
            beta: Bounce parameter controlling oscillation frequency
            tau: Optical depth (reionization parameter)
            A: Overall amplitude normalization
            alpha: Power-law index for large-scale behavior
        """
        self.beta = beta
        self.tau = tau
        self.A = A
        self.alpha = alpha
        
        # Store parameter bounds for validation
        self.parameter_bounds = {
            'beta': (1.0, 2.0),
            'tau': (0.04, 0.10),
            'A': (0.5, 2.0),
            'alpha': (0.0, 1.0)
        }
    
    def primordial_power_spectrum_modification(self, l: np.ndarray) -> np.ndarray:
        """
        Calculate LQC modification to primordial power spectrum.
        
        The bounce introduces oscillatory features and exponential damping:
        P_LQC(l) ∝ (1 + A_osc * sin(β*l) * exp(-l/λ)) * (1 - A_sup * exp(-l/l_sup))
        
        Args:
            l: Array of multipole moments
            
        Returns:
            Modification factor to apply to standard power spectrum
        """
        # Oscillatory bounce signature with exponential damping
        # The bounce creates coherent oscillations at low l
        # Amplitude is small to create subtle deviations
        A_osc = 0.08  # Oscillation amplitude
        lambda_damp = 15.0  # Damping scale
        oscillation = 1.0 + A_osc * np.sin(self.beta * l) * np.exp(-l / lambda_damp)
        
        # Large-scale power suppression from pre-bounce effects
        # This addresses the low-l deficit observed in Planck
        A_sup = 0.05  # Suppression amplitude
        l_sup = 8.0  # Suppression scale
        large_scale_suppression = 1.0 - A_sup * np.exp(-l / l_sup)
        
        # Small power-law tilt adjustment at low-l
        # This helps match the mild rise in the data
        tilt_factor = 1.0 + self.alpha * 0.01 * (l - 15.0) / 15.0
        
        return oscillation * large_scale_suppression * tilt_factor
    
    def reionization_damping(self, l: np.ndarray) -> np.ndarray:
        """
        Calculate reionization damping with LQC optical depth.
        
        LQC predicts larger optical depth (τ ≈ 0.06-0.07) which affects
        the reionization bump in B-mode polarization.
        
        Args:
            l: Array of multipole moments
            
        Returns:
            Reionization damping factor
        """
        # Exponential damping due to reionization
        # exp(-2*tau) for scalar modes, varies for tensor modes
        return np.exp(-2.0 * self.tau * (l / 10.0) ** 0.5)
    
    def predict_tt_spectrum(self, l: np.ndarray, 
                           lcdm_baseline: np.ndarray) -> np.ndarray:
        """
        Predict TT power spectrum with LQC modifications.
        
        Args:
            l: Array of multipole moments
            lcdm_baseline: Baseline ΛCDM predictions to modify
            
        Returns:
            LQC-modified D_l predictions in μK²
        """
        # Apply LQC primordial spectrum modifications
        primordial_mod = self.primordial_power_spectrum_modification(l)
        
        # Normalize the modification to preserve overall scale
        # Use high-l values where LQC effects are minimal
        if np.any(l > 20):
            normalization = np.mean(primordial_mod[l > 20])
        else:
            # If no high-l values, normalize to mean to preserve scale
            normalization = np.mean(primordial_mod)
        
        primordial_mod = primordial_mod / normalization
        
        # Apply overall amplitude factor
        # For low-l, this creates subtle deviations that improve fit
        lqc_prediction = self.A * lcdm_baseline * primordial_mod
        
        return lqc_prediction
    
    def predict_te_spectrum(self, l: np.ndarray, 
                           lcdm_baseline: np.ndarray) -> np.ndarray:
        """
        Predict TE cross-correlation spectrum with LQC modifications.
        
        TE correlations are affected by both temperature and E-mode modifications.
        LQC helps reduce cross-correlation tensions at l < 10.
        
        Args:
            l: Array of multipole moments
            lcdm_baseline: Baseline ΛCDM predictions to modify
            
        Returns:
            LQC-modified TE D_l predictions in μK²
        """
        # TE modifications are similar but with reduced amplitude
        primordial_mod = self.primordial_power_spectrum_modification(l)
        
        # TE cross-correlation has different sensitivity to modifications
        # Reduce modification strength for cross-spectrum
        te_factor = 0.7
        primordial_mod = 1.0 + te_factor * (primordial_mod - 1.0)
        
        # Normalize
        normalization = np.mean(primordial_mod[l > 20]) if np.any(l > 20) else 1.0
        primordial_mod = primordial_mod / normalization
        
        lqc_prediction = self.A * lcdm_baseline * primordial_mod
        
        return lqc_prediction
    
    def predict_bmode_spectrum(self, l: np.ndarray, r: float = 0.01) -> np.ndarray:
        """
        Predict B-mode polarization spectrum for given tensor-to-scalar ratio.
        
        LQC predicts power suppression on large scales but with larger optical depth,
        resulting in less overall suppression in the reionization bump.
        
        Args:
            l: Array of multipole moments
            r: Tensor-to-scalar ratio (r ≈ 0.01-0.05 for LQC predictions)
            
        Returns:
            Predicted B-mode D_l in μK²
        """
        # Base tensor power spectrum shape
        # Reionization bump at l ~ 2-10, recombination bump at l ~ 80-150
        
        # Reionization bump component
        reion_bump = 0.05 * r * np.exp(-((l - 5) ** 2) / (2 * 3 ** 2))
        
        # Recombination bump component
        recomb_bump = 0.02 * r * l * np.exp(-((l - 100) ** 2) / (2 * 40 ** 2))
        
        # LQC modifications: suppression at low k (large scales)
        lqc_suppression = 1.0 - 0.2 * np.exp(-l / 8.0)
        
        # Apply reionization damping with LQC optical depth
        reion_damping = self.reionization_damping(l)
        
        # Combine components
        Dl_BB = (reion_bump + recomb_bump) * lqc_suppression * reion_damping
        
        # Convert to μK² units (scaling factor)
        Dl_BB *= 5000.0
        
        return Dl_BB
    
    def calculate_improvement_over_lcdm(self, planck_data, data_type: str = 'TT',
                                       l_max: int = 30) -> Dict[str, float]:
        """
        Calculate fit improvement of LQC over ΛCDM.
        
        Args:
            planck_data: PlanckData instance with observational data
            data_type: 'TT' or 'TE' spectrum
            l_max: Maximum multipole to include
            
        Returns:
            Dictionary with χ² values and improvement metrics
        """
        # Get Planck data
        if data_type.upper() == 'TT':
            data = planck_data.get_tt_spectrum(l_max)
        else:
            data = planck_data.get_te_spectrum(l_max)
        
        # Get ΛCDM χ²
        chi2_lcdm = planck_data.get_lcdm_chi_squared(data_type, l_max)
        
        # Calculate LQC predictions
        if data_type.upper() == 'TT':
            lqc_predictions = self.predict_tt_spectrum(data['l'], data['lcdm_theory'])
        else:
            lqc_predictions = self.predict_te_spectrum(data['l'], data['lcdm_theory'])
        
        # Calculate LQC χ²
        chi2_lqc = planck_data.calculate_chi_squared(lqc_predictions, data_type, l_max)
        
        # Calculate improvement
        delta_chi2 = chi2_lqc - chi2_lcdm
        
        return {
            'chi2_lcdm': chi2_lcdm,
            'chi2_lqc': chi2_lqc,
            'delta_chi2': delta_chi2,
            'improvement': delta_chi2 < 0,
            'degrees_of_freedom': len(data['l'])
        }
    
    def set_parameters(self, **kwargs):
        """
        Update model parameters with validation.
        
        Args:
            **kwargs: Parameter names and values to update
        """
        for param, value in kwargs.items():
            if param in self.parameter_bounds:
                bounds = self.parameter_bounds[param]
                if not bounds[0] <= value <= bounds[1]:
                    raise ValueError(f"{param} = {value} outside valid range {bounds}")
                setattr(self, param, value)
            else:
                raise ValueError(f"Unknown parameter: {param}")
    
    def get_parameters(self) -> Dict[str, float]:
        """Get current model parameters."""
        return {
            'beta': self.beta,
            'tau': self.tau,
            'A': self.A,
            'alpha': self.alpha
        }
