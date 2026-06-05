//! SAGCO Guardian - Uncertainty Quantification and Risk Classification System
//!
//! This module provides the core Guardian system for tracking compiler reliability
//! through Bayesian probability analysis and geometric uncertainty mapping.

use serde::{Deserialize, Serialize};

pub mod bench_ingest;

/// Uncertainty representation with probability, entropy, and KL divergence
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Uncertainty {
    /// Probability that the compiler is correct (0.0 to 1.0)
    pub p_correct: f64,
    /// Shannon entropy in bits (higher = more uncertain)
    pub entropy: f64,
    /// KL divergence from prior (measures information gain)
    pub kl_div: f64,
}

impl Uncertainty {
    /// Create a new Uncertainty with validation
    pub fn new(p_correct: f64, entropy: f64, kl_div: f64) -> Self {
        Self {
            p_correct: p_correct.clamp(0.0, 1.0),
            entropy: entropy.max(0.0),
            kl_div: kl_div.max(0.0),
        }
    }
}

/// Geometric point in uncertainty space
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeometryPoint {
    /// Element ID (e.g., 4 for Ty, or a dedicated Br element)
    pub element_id: u32,
    /// Uncertainty coordinates
    pub uncertainty: Uncertainty,
    /// Timestamp of measurement
    pub timestamp: u64,
}

/// Risk classification levels
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum RiskLevel {
    Safe,
    Caution,
    Warning,
    Critical,
}

/// Guardian system for uncertainty tracking and risk assessment
#[derive(Debug, Clone)]
pub struct Guardian {
    // Configuration parameters can be added here
}

impl Guardian {
    /// Create a new Guardian instance
    pub fn new() -> Self {
        Self {}
    }

    /// Map uncertainty to geometry point
    ///
    /// # Arguments
    /// * `uncertainty` - The uncertainty measurement
    /// * `element_id` - Semantic element identifier (e.g., 4 for Ty/branching)
    pub fn map_uncertainty_to_geometry(
        &self,
        uncertainty: Uncertainty,
        element_id: u32,
    ) -> GeometryPoint {
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs();

        GeometryPoint {
            element_id,
            uncertainty,
            timestamp,
        }
    }

    /// Classify safety level based on geometry point
    ///
    /// Classification rules:
    /// - Safe: p_correct > 0.95, entropy < 0.2
    /// - Caution: p_correct > 0.85, entropy < 0.5
    /// - Warning: p_correct > 0.70, entropy < 0.8
    /// - Critical: below Warning thresholds
    pub fn classify_safety(&self, point: &GeometryPoint) -> RiskLevel {
        let p = point.uncertainty.p_correct;
        let entropy = point.uncertainty.entropy;

        if p > 0.95 && entropy < 0.2 {
            RiskLevel::Safe
        } else if p > 0.85 && entropy < 0.5 {
            RiskLevel::Caution
        } else if p > 0.70 && entropy < 0.8 {
            RiskLevel::Warning
        } else {
            RiskLevel::Critical
        }
    }
}

impl Default for Guardian {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_uncertainty_clamping() {
        let u = Uncertainty::new(1.5, -1.0, -2.0);
        assert_eq!(u.p_correct, 1.0);
        assert_eq!(u.entropy, 0.0);
        assert_eq!(u.kl_div, 0.0);
    }

    #[test]
    fn test_risk_classification() {
        let guardian = Guardian::new();

        // Safe case
        let safe_point = guardian.map_uncertainty_to_geometry(
            Uncertainty::new(0.98, 0.1, 0.01),
            4,
        );
        assert_eq!(guardian.classify_safety(&safe_point), RiskLevel::Safe);

        // Critical case
        let critical_point = guardian.map_uncertainty_to_geometry(
            Uncertainty::new(0.60, 0.9, 0.5),
            4,
        );
        assert_eq!(guardian.classify_safety(&critical_point), RiskLevel::Critical);
    }
}
