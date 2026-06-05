// SAGCO Guardian Library
// Uncertainty quantification and safety classification for AI outputs

pub mod bench_ingest;

use serde::{Deserialize, Serialize};

/// Uncertainty measurement for a concept or prediction
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Uncertainty {
    pub p_correct: f64,
    pub entropy: f64,
    pub kl_divergence: f64,
}

impl Uncertainty {
    pub fn new(p_correct: f64, entropy: f64, kl_divergence: f64) -> Self {
        Self {
            p_correct,
            entropy,
            kl_divergence,
        }
    }
}

/// Geometric point in the Guardian manifold
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeometryPoint {
    pub s_value: f64,      // Symplectic element
    pub u_value: f64,      // Uncertainty measure
    pub o_value: f64,      // Observable
    pub risk_level: String,
}

/// Safety classification result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SafetyClassification {
    pub level: RiskLevel,
    pub confidence: f64,
    pub recommendations: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum RiskLevel {
    Safe,
    Caution,
    Warning,
    Critical,
}

/// Guardian layer - maps uncertainties to geometric manifold
pub struct Guardian {
    threshold_safe: f64,
    threshold_caution: f64,
    threshold_warning: f64,
}

impl Guardian {
    pub fn new() -> Self {
        Self {
            threshold_safe: 0.8,
            threshold_caution: 0.6,
            threshold_warning: 0.4,
        }
    }

    /// Map uncertainty to geometry point
    pub fn map_uncertainty_to_geometry(
        &self,
        uncertainty: Uncertainty,
        s_element: u32,
    ) -> GeometryPoint {
        // Simple mapping: s_value from element, u from uncertainty, o from p_correct
        let s_value = s_element as f64;
        let u_value = uncertainty.entropy + uncertainty.kl_divergence;
        let o_value = uncertainty.p_correct;
        
        let risk_level = if o_value >= self.threshold_safe {
            "Safe".to_string()
        } else if o_value >= self.threshold_caution {
            "Caution".to_string()
        } else if o_value >= self.threshold_warning {
            "Warning".to_string()
        } else {
            "Critical".to_string()
        };

        GeometryPoint {
            s_value,
            u_value,
            o_value,
            risk_level,
        }
    }

    /// Classify safety based on geometry point
    pub fn classify_safety(&self, point: &GeometryPoint) -> SafetyClassification {
        let level = if point.o_value >= self.threshold_safe {
            RiskLevel::Safe
        } else if point.o_value >= self.threshold_caution {
            RiskLevel::Caution
        } else if point.o_value >= self.threshold_warning {
            RiskLevel::Warning
        } else {
            RiskLevel::Critical
        };

        let confidence = point.o_value;
        
        let recommendations = match level {
            RiskLevel::Safe => vec!["Output appears safe for production use.".to_string()],
            RiskLevel::Caution => vec![
                "Review output before deployment.".to_string(),
                "Consider additional validation.".to_string(),
            ],
            RiskLevel::Warning => vec![
                "High uncertainty detected.".to_string(),
                "Manual review required.".to_string(),
                "Consider retraining or refinement.".to_string(),
            ],
            RiskLevel::Critical => vec![
                "Critical risk level - do not use in production.".to_string(),
                "Requires immediate attention.".to_string(),
                "Implement additional safeguards.".to_string(),
            ],
        };

        SafetyClassification {
            level,
            confidence,
            recommendations,
        }
    }
}

impl Default for Guardian {
    fn default() -> Self {
        Self::new()
    }
}

/// Pretty-print geometry point
pub fn print_geometry_point(point: &GeometryPoint, _guardian: &Guardian) {
    println!("╔═══════════════════════════════════════════════════════╗");
    println!("║         GUARDIAN GEOMETRY POINT ANALYSIS             ║");
    println!("╠═══════════════════════════════════════════════════════╣");
    println!("║ S-value (Symplectic):  {:<30.3} ║", point.s_value);
    println!("║ U-value (Uncertainty): {:<30.3} ║", point.u_value);
    println!("║ O-value (Observable):  {:<30.3} ║", point.o_value);
    println!("║ Risk Level:            {:<30} ║", point.risk_level);
    println!("╚═══════════════════════════════════════════════════════╝");
}

/// Pretty-print safety classification
pub fn print_safety_classification(classification: &SafetyClassification) {
    println!("\n╔═══════════════════════════════════════════════════════╗");
    println!("║         SAFETY CLASSIFICATION RESULT                 ║");
    println!("╠═══════════════════════════════════════════════════════╣");
    println!("║ Level:      {:<42?} ║", classification.level);
    println!("║ Confidence: {:<42.2} ║", classification.confidence);
    println!("╠═══════════════════════════════════════════════════════╣");
    println!("║ Recommendations:                                      ║");
    for rec in &classification.recommendations {
        println!("║  • {:<49} ║", rec);
    }
    println!("╚═══════════════════════════════════════════════════════╝");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_uncertainty_creation() {
        let u = Uncertainty::new(0.95, 0.25, 0.1);
        assert_eq!(u.p_correct, 0.95);
        assert_eq!(u.entropy, 0.25);
    }

    #[test]
    fn test_guardian_safe_classification() {
        let guardian = Guardian::new();
        let uncertainty = Uncertainty::new(0.95, 0.2, 0.05);
        let point = guardian.map_uncertainty_to_geometry(uncertainty, 1);
        let safety = guardian.classify_safety(&point);
        assert_eq!(safety.level, RiskLevel::Safe);
    }
}
