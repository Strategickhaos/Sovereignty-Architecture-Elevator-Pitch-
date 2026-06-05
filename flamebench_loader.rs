// FLAMEBENCH LOADER — Load benchmark results into Uncertainty structures
// DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1
// Reads flamebench-results.json and guardian-uncertainty.json
// Maps probabilistic metrics into quantum uncertainty structures

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

// === FLAMEBENCH RESULT STRUCTURES ===

#[derive(Debug, Clone, Serialize, Deserialize)]
struct FlameBenchResults {
    version: String,
    dna_strand: String,
    overall: OverallMetrics,
    compiler: String,
    capsules: Vec<CapsuleResult>,
    concepts: Vec<ConceptAggregate>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct OverallMetrics {
    p_success: f64,
    entropy: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CapsuleResult {
    id: String,
    name: String,
    tags: Vec<String>,
    passed: u32,
    total: u32,
    p_success: f64,
    status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ConceptAggregate {
    tag: String,
    atoms: u32,
    passed: u32,
    total: u32,
    p_success: f64,
    entropy: f64,
}

// === GUARDIAN UNCERTAINTY STRUCTURES ===

#[derive(Debug, Clone, Serialize, Deserialize)]
struct GuardianUncertainty {
    source: String,
    dna_strand: String,
    uncertainties: Vec<UncertaintyEntry>,
    overall: OverallMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct UncertaintyEntry {
    quadrant: String,
    tag: String,
    p_correct: f64,
    entropy: f64,
    alpha: u32,
    beta: u32,
    sample_size: u32,
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
    fn from_str(s: &str) -> Self {
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
        let avg_entropy: f64 = results.concepts.iter()
            .map(|c| c.entropy)
            .sum::<f64>() / results.concepts.len() as f64;

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

// === EXAMPLE USAGE ===

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

// === MAIN DEMO ===

fn main() {
    println!("═══════════════════════════════════════════════════════════");
    println!("  FLAMEBENCH LOADER — Rust Uncertainty Integration");
    println!("  DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1");
    println!("═══════════════════════════════════════════════════════════\n");

    let loader = FlameBenchLoader::new("results");

    match loader.load_uncertainties() {
        Ok(uncertainties) => {
            println!("✅ Loaded {} uncertainty entries\n", uncertainties.len());

            println!("📊 UNCERTAINTY ANALYSIS:");
            println!("{:<25} {:<12} {:<10} {:<10}", "Tag", "p_correct", "Entropy", "KL Div");
            println!("{}", "-".repeat(60));

            for u in &uncertainties {
                println!("{:<25} {:<12.4} {:<10.4} {:<10.4}",
                    u.tag, u.p_correct, u.entropy, u.kl_divergence);
            }
            println!();

            // Guardian integration
            let guardian = GuardianIntegration::new("results");

            match guardian.calculate_fitness() {
                Ok(fitness) => {
                    println!("🧬 Compiler Fitness Score: {:.4}", fitness);
                }
                Err(e) => println!("⚠️  Could not calculate fitness: {}", e),
            }

            match guardian.should_reject_compiler(0.65, 0.80) {
                Ok((should_reject, reason)) => {
                    let emoji = if should_reject { "❌" } else { "✅" };
                    println!("{} Guardian Decision: {}", emoji, reason);
                }
                Err(e) => println!("⚠️  Could not evaluate rejection: {}", e),
            }

            match guardian.get_weak_concepts(0.85, 0.50) {
                Ok(weak) => {
                    if !weak.is_empty() {
                        println!("\n⚠️  Weak Concepts Requiring Improvement:");
                        for tag in weak {
                            println!("   - {}", tag);
                        }
                    } else {
                        println!("\n✅ All concepts meet quality thresholds");
                    }
                }
                Err(e) => println!("⚠️  Could not analyze weak concepts: {}", e),
            }
        }
        Err(e) => {
            println!("❌ Failed to load uncertainties: {}", e);
            println!("\n💡 Run flamebench.py first to generate results:");
            println!("   python3 flamebench.py --output-dir results");
        }
    }

    println!("\n═══════════════════════════════════════════════════════════");
}

// Dependencies for Cargo.toml:
// [dependencies]
// serde = { version = "1.0", features = ["derive"] }
// serde_json = "1.0"
