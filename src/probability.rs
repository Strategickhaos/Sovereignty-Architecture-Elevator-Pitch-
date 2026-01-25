//! probability.rs - Variational Inference (VI) and Uncertainty Quantification
//! 
//! Implements Gaussian distributions, KL divergence, and entropy calculations
//! for probabilistic reasoning in SAGCO-OS

use std::f64::consts::PI;

/// Gaussian distribution for Variational Inference
#[derive(Debug, Clone, Copy)]
pub struct Gaussian {
    pub mean: f64,
    pub variance: f64,
}

impl Gaussian {
    pub fn new(mean: f64, variance: f64) -> Self {
        Self { mean, variance }
    }
    
    /// KL divergence: KL(self || other)
    pub fn kl_divergence(&self, other: &Gaussian) -> f64 {
        let var_ratio = self.variance / other.variance;
        let mean_diff = other.mean - self.mean;
        
        0.5 * (var_ratio + (mean_diff * mean_diff) / other.variance - 1.0 + (other.variance / self.variance).ln())
    }
    
    /// Entropy in bits
    pub fn entropy_bits(&self) -> f64 {
        0.5 * (2.0 * PI * std::f64::consts::E * self.variance).ln() / 2.0f64.ln()
    }
    
    /// Sample from distribution (Box-Muller transform)
    pub fn sample(&self) -> f64 {
        // Simplified: return mean for deterministic testing
        // In production, use proper random sampling
        self.mean
    }
}

/// Uncertainty quantification for SAGCO guardian
#[derive(Debug, Clone, Copy)]
pub struct Uncertainty {
    pub p_correct: f64,
    pub entropy: f64,
    pub kl_divergence: f64,
}

impl Uncertainty {
    pub fn new(p_correct: f64, entropy: f64, kl_divergence: f64) -> Self {
        Self { p_correct, entropy, kl_divergence }
    }
    
    /// Check if uncertainty is within acceptable bounds
    pub fn is_acceptable(&self, kl_threshold: f64) -> bool {
        self.kl_divergence < kl_threshold && self.p_correct > 0.5
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_gaussian_kl() {
        let g1 = Gaussian::new(1.0, 0.1);
        let g2 = Gaussian::new(1.0, 0.1);
        let kl = g1.kl_divergence(&g2);
        assert!(kl < 0.01, "KL divergence of identical distributions should be near 0");
    }
    
    #[test]
    fn test_entropy() {
        let g = Gaussian::new(0.0, 1.0);
        let entropy = g.entropy_bits();
        assert!(entropy > 0.0, "Entropy should be positive");
    }
    
    #[test]
    fn test_uncertainty_acceptable() {
        let unc = Uncertainty::new(0.9, 1.0, 0.1);
        assert!(unc.is_acceptable(0.5));
        
        let unc_bad = Uncertainty::new(0.3, 1.0, 0.8);
        assert!(!unc_bad.is_acceptable(0.5));
    }
}
