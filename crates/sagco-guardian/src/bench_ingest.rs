//! Benchmark Ingestion Module
//!
//! Loads FlameBench results.json and converts to Guardian Uncertainty

use crate::Uncertainty;
use anyhow::Result;
use serde::Deserialize;
use std::fs;
use std::path::Path;

/// Benchmark summary from FlameBench results.json
#[derive(Debug, Clone, Deserialize)]
pub struct BenchSummary {
    pub test_id: String,
    pub concept_tags: Vec<String>,
    pub runs: u32,
    pub successes: u32,
    pub p_success: f64,
}

/// Load benchmark summaries from results.json
pub fn load_bench_summaries<P: AsRef<Path>>(path: P) -> Result<Vec<BenchSummary>> {
    let data = fs::read_to_string(path)?;
    let summaries: Vec<BenchSummary> = serde_json::from_str(&data)?;
    Ok(summaries)
}

/// Map a Bernoulli test (pass/fail) summary into an Uncertainty.
///
/// # Arguments
/// * `summary` - The benchmark summary with test results
/// * `alpha0` - Prior Beta distribution alpha parameter (default: 1.0 for uniform)
/// * `beta0` - Prior Beta distribution beta parameter (default: 1.0 for uniform)
///
/// # Returns
/// An Uncertainty with:
/// - p_correct: posterior mean probability
/// - entropy: Bernoulli entropy using posterior mean
/// - kl_div: approximate KL divergence from prior to posterior
pub fn bench_to_uncertainty(summary: &BenchSummary, alpha0: f64, beta0: f64) -> Uncertainty {
    // Posterior Beta parameters
    let alpha_post = alpha0 + summary.successes as f64;
    let beta_post = beta0 + (summary.runs - summary.successes) as f64;

    // Posterior mean
    let p_correct = alpha_post / (alpha_post + beta_post);

    // Bernoulli entropy (bits), using posterior mean as p
    let p = p_correct.clamp(1e-9, 1.0 - 1e-9);
    let entropy = -(p * p.log2() + (1.0 - p) * (1.0 - p).log2());

    // Simple KL from prior Beta to posterior Beta (approximate)
    // Using Euclidean distance in parameter space as a proxy
    let kl_div = ((alpha_post - alpha0).powi(2) + (beta_post - beta0).powi(2)).sqrt()
        / (alpha0 + beta0 + 1.0);

    Uncertainty::new(p_correct, entropy, kl_div)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bench_to_uncertainty() {
        let summary = BenchSummary {
            test_id: "test-1".to_string(),
            concept_tags: vec!["if-else".to_string()],
            runs: 4,
            successes: 4,
            p_success: 0.8333,
        };

        let u = bench_to_uncertainty(&summary, 1.0, 1.0);

        // With Beta(1,1) prior and 4/4 successes:
        // Posterior is Beta(5, 1), mean = 5/6 ≈ 0.833
        assert!((u.p_correct - 0.8333).abs() < 0.01);
        assert!(u.entropy > 0.0);
        assert!(u.kl_div > 0.0);
    }
}
