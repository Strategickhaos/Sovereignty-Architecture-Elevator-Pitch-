//! SAGCO DOM0 Daemon
//!
//! Example integration of FlameBench results with Guardian uncertainty system.
//! This daemon loads benchmark results and classifies compiler reliability.

use anyhow::Result;
use sagco_guardian::bench_ingest::{bench_to_uncertainty, load_bench_summaries};
use sagco_guardian::{Guardian, RiskLevel};

fn main() -> Result<()> {
    println!("🔥 SAGCO DOM0 Daemon - Guardian Uncertainty Analysis");
    println!("{}", "=".repeat(60));

    // Initialize Guardian
    let guardian = Guardian::new();

    // Load FlameBench summaries from results.json
    // Default path for demonstration - can be configured via args or env
    let results_path = std::env::var("FLAMEBENCH_RESULTS")
        .unwrap_or_else(|_| "bench_cache/results.json".to_string());

    println!("\n📊 Loading benchmark results from: {}", results_path);

    let summaries = match load_bench_summaries(&results_path) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("❌ Error loading benchmark results: {}", e);
            eprintln!("   Make sure to run flamebench.py first to generate results.json");
            std::process::exit(1);
        }
    };

    println!("✓ Loaded {} test summaries\n", summaries.len());

    // Process each benchmark summary
    println!("🔍 Analyzing compiler reliability:\n");

    for summary in &summaries {
        // Convert benchmark to uncertainty with Beta(1,1) uniform prior
        let uncertainty = bench_to_uncertainty(summary, 1.0, 1.0);

        // Map to geometry (using element_id 4 for branching constructs)
        // In a real system, element_id would be determined by concept_tags
        let element_id = if summary.concept_tags.contains(&"if-else".to_string()) {
            4 // Branching element
        } else {
            0 // Generic element
        };

        let point = guardian.map_uncertainty_to_geometry(uncertainty.clone(), element_id);

        // Classify safety
        let safety = guardian.classify_safety(&point);

        // Print results
        let status_icon = match safety {
            RiskLevel::Safe => "✅",
            RiskLevel::Caution => "⚠️ ",
            RiskLevel::Warning => "⚠️ ",
            RiskLevel::Critical => "❌",
        };

        println!(
            "{} {} [{:?}]",
            status_icon, summary.test_id, safety
        );
        println!(
            "   Successes: {}/{} (p_correct={:.4})",
            summary.successes, summary.runs, uncertainty.p_correct
        );
        println!(
            "   Entropy: {:.4} bits, KL-div: {:.4}",
            uncertainty.entropy, uncertainty.kl_div
        );
        println!(
            "   Concepts: {}",
            summary.concept_tags.join(", ")
        );
        println!();
    }

    // Aggregate analysis by concept
    println!("{}", "=".repeat(60));
    println!("📈 Concept-level Risk Analysis:\n");

    // Group by concept tags
    let mut concept_summaries: std::collections::HashMap<String, Vec<&_>> =
        std::collections::HashMap::new();

    for summary in &summaries {
        for tag in &summary.concept_tags {
            concept_summaries
                .entry(tag.clone())
                .or_default()
                .push(summary);
        }
    }

    // Analyze each concept
    for (concept, tests) in concept_summaries.iter() {
        let total_runs: u32 = tests.iter().map(|t| t.runs).sum();
        let total_successes: u32 = tests.iter().map(|t| t.successes).sum();

        // Create aggregate summary
        let agg_p_success = (total_successes as f64 + 1.0) / (total_runs as f64 + 2.0);

        // Create temporary summary for uncertainty calculation
        let agg_summary = sagco_guardian::bench_ingest::BenchSummary {
            test_id: format!("aggregate-{}", concept),
            concept_tags: vec![concept.clone()],
            runs: total_runs,
            successes: total_successes,
            p_success: agg_p_success,
        };

        let uncertainty = bench_to_uncertainty(&agg_summary, 1.0, 1.0);
        let point = guardian.map_uncertainty_to_geometry(uncertainty.clone(), 4);
        let safety = guardian.classify_safety(&point);

        let status_icon = match safety {
            RiskLevel::Safe => "✅",
            RiskLevel::Caution => "⚠️ ",
            RiskLevel::Warning => "⚠️ ",
            RiskLevel::Critical => "❌",
        };

        println!(
            "{} Concept: \"{}\" [{:?}]",
            status_icon, concept, safety
        );
        println!(
            "   Tests: {}, Total runs: {}/{} (p_correct={:.4})",
            tests.len(),
            total_successes,
            total_runs,
            uncertainty.p_correct
        );
        println!();
    }

    println!("{}", "=".repeat(60));
    println!("✅ Guardian analysis complete");

    Ok(())
}
