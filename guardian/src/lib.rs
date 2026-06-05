/// SAGCO Guardian - Uncertainty tracking and safety layer
///
/// The Guardian module provides:
/// - Benchmark data ingestion from FlameBench
/// - Uncertainty quantification for compilation concepts
/// - Safety classification for AI outputs
/// - Geometry mapping for neural states

pub mod bench_ingest;

use serde::{Deserialize, Serialize};

/// Core uncertainty measurement structure
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

/// Geometric point in Guardian's safety space
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeometryPoint {
    pub element: String,
    pub coordinates: Vec<f64>,
    pub uncertainty: Uncertainty,
}

/// Risk classification levels
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum RiskLevel {
    Safe,
    Caution,
    Warning,
    Critical,
}

/// Safety classification result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SafetyClassification {
    pub risk_level: RiskLevel,
    pub confidence: f64,
    pub reasoning: String,
}

/// Main Guardian structure for uncertainty mapping
pub struct Guardian {
    pub name: String,
}

impl Guardian {
    pub fn new() -> Self {
        Self {
            name: "SAGCO Guardian v1.0".to_string(),
        }
    }

    /// Map uncertainty metrics to geometric point
    pub fn map_uncertainty_to_geometry(&self, u: Uncertainty, element_idx: usize) -> GeometryPoint {
        let elements = ["S1", "S2", "Cl", "Ne", "Ar"];
        let element = elements.get(element_idx).unwrap_or(&"Unknown").to_string();
        
        // Simple mapping: uncertainty → coordinates
        let coordinates = vec![
            u.p_correct,
            1.0 - u.entropy / 2.0,
            1.0 - u.kl_divergence / 3.0,
        ];

        GeometryPoint {
            element,
            coordinates,
            uncertainty: u,
        }
    }

    /// Classify safety based on geometry point
    pub fn classify_safety(&self, point: &GeometryPoint) -> SafetyClassification {
        let avg_coord = point.coordinates.iter().sum::<f64>() / point.coordinates.len() as f64;
        
        let (risk_level, reasoning) = if avg_coord > 0.9 {
            (RiskLevel::Safe, "High confidence, low uncertainty".to_string())
        } else if avg_coord > 0.7 {
            (RiskLevel::Caution, "Moderate confidence, manageable uncertainty".to_string())
        } else if avg_coord > 0.5 {
            (RiskLevel::Warning, "Low confidence, elevated uncertainty".to_string())
        } else {
            (RiskLevel::Critical, "Very low confidence, critical uncertainty".to_string())
        };

        SafetyClassification {
            risk_level,
            confidence: avg_coord,
            reasoning,
        }
    }
}

impl Default for Guardian {
    fn default() -> Self {
        Self::new()
    }
}

/// Print geometry point in a formatted box
pub fn print_geometry_point(point: &GeometryPoint, guardian: &Guardian) {
    println!("\n╔════════════════════════════════════════╗");
    println!("║  {} ", guardian.name);
    println!("╠════════════════════════════════════════╣");
    println!("║  Element: {:<28} ║", point.element);
    println!("║  Coordinates: [{:.3}, {:.3}, {:.3}]   ║", 
             point.coordinates[0], 
             point.coordinates.get(1).unwrap_or(&0.0),
             point.coordinates.get(2).unwrap_or(&0.0));
    println!("║  Uncertainty:                          ║");
    println!("║    p_correct: {:<24.3} ║", point.uncertainty.p_correct);
    println!("║    entropy:   {:<24.3} ║", point.uncertainty.entropy);
    println!("║    kl_div:    {:<24.3} ║", point.uncertainty.kl_divergence);
    println!("╚════════════════════════════════════════╝");
}

/// Print safety classification
pub fn print_safety_classification(safety: &SafetyClassification) {
    let risk_symbol = match safety.risk_level {
        RiskLevel::Safe => "✓",
        RiskLevel::Caution => "⚠",
        RiskLevel::Warning => "⚠⚠",
        RiskLevel::Critical => "✗",
    };

    println!("\n╔════════════════════════════════════════╗");
    println!("║  Safety Classification                 ║");
    println!("╠════════════════════════════════════════╣");
    println!("║  Risk Level: {:?} {}               ", safety.risk_level, risk_symbol);
    println!("║  Confidence: {:.1}%                     ", safety.confidence * 100.0);
    println!("║  Reasoning: {:<26} ║", safety.reasoning);
    println!("╚════════════════════════════════════════╝\n");
}
