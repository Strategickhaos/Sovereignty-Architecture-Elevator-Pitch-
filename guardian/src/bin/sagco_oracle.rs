use sagco_guardian::{Guardian, Uncertainty};
use sagco_guardian::bench_ingest::load_guardian_uncertainty;
use std::env;
use std::io::{self, Read};
use std::path::Path;

fn main() -> anyhow::Result<()> {
    let guardian = Guardian::new();

    // Print header
    println!("\n╔════════════════════════════════════════╗");
    println!("║  SAGCO-ORACLE v1.0                     ║");
    println!("║  Guardian Layer Analysis               ║");
    println!("╚════════════════════════════════════════╝\n");

    // 1. Try to load compiler health from flamebench (optional)
    let guardian_paths = vec![
        "guardian-uncertainty.json",
        "E:\\FlameBench\\guardian-uncertainty.json",
        "/opt/flamebench/guardian-uncertainty.json",
    ];

    let mut loaded = false;
    for path in &guardian_paths {
        if Path::new(path).exists() {
            match load_guardian_uncertainty(path) {
                Ok(export) => {
                    println!("FLM2 Compiler Health Report:");
                    println!("  Source: {}", export.source);
                    println!("  DNA Strand: {}", export.dna_strand);
                    println!("  Overall Success: {:.1}%", export.overall.p_success * 100.0);
                    println!("  Entropy: {:.3}", export.overall.entropy);
                    
                    // Print top uncertainties
                    if !export.uncertainties.is_empty() {
                        println!("\n  Concept Uncertainties:");
                        for (idx, u) in export.uncertainties.iter().take(5).enumerate() {
                            println!("    {}. [{}] p={:.3}, H={:.3}", 
                                idx + 1, u.tag, u.p_correct, u.entropy);
                        }
                    }
                    println!();
                    loaded = true;
                    break;
                }
                Err(e) => {
                    eprintln!("Warning: Failed to load {}: {}", path, e);
                }
            }
        }
    }

    if !loaded {
        println!("Note: No Guardian benchmark data found. Skipping health report.");
        println!("Expected locations:");
        for path in &guardian_paths {
            println!("  - {}", path);
        }
        println!();
    }

    // 2. Get input text: arg1 or stdin
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 {
        args[1..].join(" ")
    } else {
        let mut buf = String::new();
        match io::stdin().read_to_string(&mut buf) {
            Ok(_) => buf,
            Err(_) => {
                // If stdin is not available, show usage
                println!("Usage:");
                println!("  sagco-oracle \"text to analyze\"");
                println!("  echo \"text\" | sagco-oracle");
                println!();
                println!("The oracle will:");
                println!("  1. Display FLM2 compiler health (if available)");
                println!("  2. Analyze input text for uncertainty");
                println!("  3. Map to Guardian geometry");
                println!("  4. Classify safety risk");
                return Ok(());
            }
        }
    };

    if input.trim().is_empty() {
        println!("No input provided. Exiting.");
        return Ok(());
    }

    // 3. Simple heuristic → uncertainty
    println!("Analyzing input: \"{}\"", input.trim());
    println!();

    let len = input.chars().count() as f64;
    
    // Simple heuristic: longer text = higher confidence, but with diminishing returns
    let p_correct = (1.0 - (1.0 / (1.0 + len / 100.0))).clamp(0.1, 0.99);
    let entropy = (len / 400.0).min(2.0);
    let kl = (len / 600.0).min(3.0);
    
    let u = Uncertainty::new(p_correct, entropy, kl);

    // 4. Map to geometry (using S1 element for this example)
    let point = guardian.map_uncertainty_to_geometry(u.clone(), 0);
    let safety = guardian.classify_safety(&point);

    // Print results
    sagco_guardian::print_geometry_point(&point, &guardian);
    sagco_guardian::print_safety_classification(&safety);

    Ok(())
}
