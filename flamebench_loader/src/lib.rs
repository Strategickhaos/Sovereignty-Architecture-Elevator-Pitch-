// FLAMEBENCH LOADER — Library module
// DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::BufReader;

// === FLAMEBENCH RESULT STRUCTURES ===

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlameBenchResults {
    pub version: String,
    pub dna_strand: String,
    pub overall: OverallMetrics,
    pub compiler: String,
    pub capsules: Vec<CapsuleResult>,
    pub concepts: Vec<ConceptAggregate>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OverallMetrics {
    pub p_success: f64,
    pub entropy: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CapsuleResult {
    pub id: String,
    pub name: String,
    pub tags: Vec<String>,
    pub passed: u32,
    pub total: u32,
    pub p_success: f64,
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConceptAggregate {
    pub tag: String,
    pub atoms: u32,
    pub passed: u32,
    pub total: u32,
    pub p_success: f64,
    pub entropy: f64,
}

// === GUARDIAN UNCERTAINTY STRUCTURES ===

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GuardianUncertainty {
    pub source: String,
    pub dna_strand: String,
    pub uncertainties: Vec<UncertaintyEntry>,
    pub overall: OverallMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UncertaintyEntry {
    pub quadrant: String,
    pub tag: String,
    pub p_correct: f64,
    pub entropy: f64,
    pub alpha: u32,
    pub beta: u32,
    pub sample_size: u32,
}

// === MAPPED UNCERTAINTY STRUCTURES ===

#[derive(Debug, Clone)]
pub struct Uncertainty {
    pub tag: String,
    pub quadrant: Quadrant,
    pub p_correct: f64,
    pub entropy: f64,
    pub kl_divergence: f64,
    pub alpha: u32,
    pub beta: u32,
    pub sample_size: u32,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Quadrant {
    Linguistic,   // Language/Text domain (zyBooks)
    Numerical,    // Math/Computation domain
    Visual,       // Graphics/Rendering domain
    Temporal,     // Time-series/Sequential domain
}

impl Quadrant {
    pub fn from_str(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            "linguistic" => Quadrant::Linguistic,
            "numerical" => Quadrant::Numerical,
            "visual" => Quadrant::Visual,
            "temporal" => Quadrant::Temporal,
            _ => Quadrant::Linguistic,
        }
    }
}

// === LOADER IMPLEMENTATION ===

pub struct FlameBenchLoader {
    results_path: String,
    guardian_path: String,
}

impl FlameBenchLoader {
    pub fn new(results_dir: &str) -> Self {
        Self {
            results_path: format!("{}/flamebench-results.json", results_dir),
            guardian_path: format!("{}/guardian-uncertainty.json", results_dir),
        }
    }

    pub fn load_results(&self) -> Result<FlameBenchResults, Box<dyn std::error::Error>> {
        let file = File::open(&self.results_path)?;
        let reader = BufReader::new(file);
        let results: FlameBenchResults = serde_json::from_reader(reader)?;
        Ok(results)
    }

    pub fn load_guardian(&self) -> Result<GuardianUncertainty, Box<dyn std::error::Error>> {
        let file = File::open(&self.guardian_path)?;
        let reader = BufReader::new(file);
        let guardian: GuardianUncertainty = serde_json::from_reader(reader)?;
        Ok(guardian)
    }

    pub fn load_uncertainties(&self) -> Result<Vec<Uncertainty>, Box<dyn std::error::Error>> {
        let guardian = self.load_guardian()?;
        let results = self.load_results()?;

        let mut uncertainties = Vec::new();

        // Calculate average KL divergence from concept entropies
        let avg_entropy: f64 = if results.concepts.is_empty() {
            0.0
        } else {
            results.concepts.iter()
                .map(|c| c.entropy)
                .sum::<f64>() / results.concepts.len() as f64
        };

        for entry in guardian.uncertainties {
            // KL divergence estimation: how far concept entropy is from average
            let kl_divergence = (entry.entropy - avg_entropy).abs();

            uncertainties.push(Uncertainty {
                tag: entry.tag,
                quadrant: Quadrant::from_str(&entry.quadrant),
                p_correct: entry.p_correct,
                entropy: entry.entropy,
                kl_divergence,
                alpha: entry.alpha,
                beta: entry.beta,
                sample_size: entry.sample_size,
            });
        }

        Ok(uncertainties)
    }

    pub fn get_overall_metrics(&self) -> Result<(f64, f64), Box<dyn std::error::Error>> {
        let results = self.load_results()?;
        Ok((results.overall.p_success, results.overall.entropy))
    }

    pub fn filter_high_uncertainty(&self, threshold: f64) -> Result<Vec<Uncertainty>, Box<dyn std::error::Error>> {
        let uncertainties = self.load_uncertainties()?;
        Ok(uncertainties.into_iter()
            .filter(|u| u.entropy > threshold)
            .collect())
    }

    pub fn filter_low_success(&self, threshold: f64) -> Result<Vec<Uncertainty>, Box<dyn std::error::Error>> {
        let uncertainties = self.load_uncertainties()?;
        Ok(uncertainties.into_iter()
            .filter(|u| u.p_correct < threshold)
            .collect())
    }

    pub fn get_concept_summary(&self) -> Result<HashMap<String, (f64, f64)>, Box<dyn std::error::Error>> {
        let uncertainties = self.load_uncertainties()?;
        let mut summary = HashMap::new();

        for u in uncertainties {
            summary.insert(u.tag, (u.p_correct, u.entropy));
        }

        Ok(summary)
    }
}

// === INTEGRATION WITH GUARDIAN SYSTEM ===

pub struct GuardianIntegration {
    loader: FlameBenchLoader,
}

impl GuardianIntegration {
    pub fn new(results_dir: &str) -> Self {
        Self {
            loader: FlameBenchLoader::new(results_dir),
        }
    }

    /// Determine if compiler should be rejected based on benchmark results
    /// Q3 minute 35 reject rule: high entropy or low p_correct → reject
    pub fn should_reject_compiler(&self, entropy_threshold: f64, p_threshold: f64) 
        -> Result<(bool, String), Box<dyn std::error::Error>> {
        let (overall_p, overall_entropy) = self.loader.get_overall_metrics()?;

        if overall_entropy > entropy_threshold {
            return Ok((true, format!(
                "REJECT: High entropy {:.3} > threshold {:.3}",
                overall_entropy, entropy_threshold
            )));
        }

        if overall_p < p_threshold {
            return Ok((true, format!(
                "REJECT: Low p_success {:.3} < threshold {:.3}",
                overall_p, p_threshold
            )));
        }

        Ok((false, format!(
            "ACCEPT: p_success={:.3}, entropy={:.3}",
            overall_p, overall_entropy
        )))
    }

    /// Calculate fitness score for DNA mutation decisions
    /// Higher p_success and lower entropy = higher fitness
    pub fn calculate_fitness(&self) -> Result<f64, Box<dyn std::error::Error>> {
        let (p_success, entropy) = self.loader.get_overall_metrics()?;
        
        // Fitness = p_success * (1 - normalized_entropy)
        // Entropy is in range [0, 1] for binary probability
        let fitness = p_success * (1.0 - entropy);
        
        Ok(fitness)
    }

    /// Get tags that need improvement (low p_correct or high entropy)
    pub fn get_weak_concepts(&self, p_threshold: f64, entropy_threshold: f64)
        -> Result<Vec<String>, Box<dyn std::error::Error>> {
        let uncertainties = self.loader.load_uncertainties()?;
        
        let weak: Vec<String> = uncertainties.into_iter()
            .filter(|u| u.p_correct < p_threshold || u.entropy > entropy_threshold)
            .map(|u| u.tag)
            .collect();
        
        Ok(weak)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_loader_creation() {
        let loader = FlameBenchLoader::new("results");
        assert_eq!(loader.results_path, "results/flamebench-results.json");
        assert_eq!(loader.guardian_path, "results/guardian-uncertainty.json");
    }

    #[test]
    fn test_quadrant_from_str() {
        assert_eq!(Quadrant::from_str("linguistic"), Quadrant::Linguistic);
        assert_eq!(Quadrant::from_str("NUMERICAL"), Quadrant::Numerical);
        assert_eq!(Quadrant::from_str("visual"), Quadrant::Visual);
        assert_eq!(Quadrant::from_str("temporal"), Quadrant::Temporal);
        assert_eq!(Quadrant::from_str("unknown"), Quadrant::Linguistic);
    }
}
