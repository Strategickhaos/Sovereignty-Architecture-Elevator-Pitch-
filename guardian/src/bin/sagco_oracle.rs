// SAGCO Oracle - Guardian Layer Analysis Tool
// Analyzes text inputs and compiler health using Guardian uncertainty mapping

use sagco_guardian::{Guardian, Uncertainty};
use sagco_guardian::bench_ingest::load_guardian_uncertainty;
use std::env;
use std::io::{self, Read};

fn main() -> anyhow::Result<()> {
    let guardian = Guardian::new();

    println!("╔═══════════════════════════════════════════════════════╗");
    println!("║              SAGCO ORACLE v1.0.0                      ║");
    println!("║         Guardian Layer Analysis System                ║");
    println!("╚═══════════════════════════════════════════════════════╝\n");

    // 1. Try to load compiler health from flamebench (optional)
    // Try multiple potential paths
    let potential_paths = vec![
        "guardian-uncertainty.json",
        "flamebench/guardian-uncertainty.json",
        "/tmp/guardian-uncertainty.json",
    ];

    for path in potential_paths {
        if let Ok(export) = load_guardian_uncertainty(path) {
            println!("📊 FLM2 Compiler Health (from {}):", path);
            println!("   DNA Strand: {}", export.dna_strand);
            println!("   p_success = {:.3}", export.overall.p_success);
            println!("   entropy   = {:.3}", export.overall.entropy);
            
            // Show individual concept uncertainties
            if !export.uncertainties.is_empty() {
                println!("\n   Concept Analysis:");
                for u in &export.uncertainties {
                    println!("   [{:12}] p={:.3} entropy={:.3} samples={}",
                             u.tag, u.p_correct, u.entropy, u.sample_size);
                }
            }
            println!();
            break;
        }
    }

    // 2. Get input text: arg1 or stdin
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 {
        args[1..].join(" ")
    } else {
        let mut buf = String::new();
        io::stdin().read_to_string(&mut buf)?;
        buf
    };

    if input.trim().is_empty() {
        eprintln!("Usage: sagco-oracle <text> OR echo 'text' | sagco-oracle");
        eprintln!("\nExample:");
        eprintln!("  sagco-oracle 'Test hallucination text'");
        eprintln!("  echo 'AI generated content' | sagco-oracle");
        std::process::exit(1);
    }

    println!("🔍 Analyzing Input:");
    println!("   Text: \"{}\"", input.trim());
    println!("   Length: {} characters\n", input.len());

    // 3. Simple heuristic → uncertainty
    // More text = higher confidence, but also higher potential entropy
    let len = input.chars().count() as f64;
    let p_correct = (1.0_f64 - (1.0 / (1.0 + len / 100.0))).clamp(0.1, 0.99);
    let entropy = (len / 400.0).min(2.0);
    let kl = (len / 600.0).min(3.0);
    let u = Uncertainty::new(p_correct, entropy, kl);

    println!("📐 Uncertainty Metrics:");
    println!("   p_correct:     {:.3}", u.p_correct);
    println!("   entropy:       {:.3}", u.entropy);
    println!("   kl_divergence: {:.3}\n", u.kl_divergence);

    // 4. Map to geometry
    let point = guardian.map_uncertainty_to_geometry(u.clone(), 1); // St element
    let safety = guardian.classify_safety(&point);

    sagco_guardian::print_geometry_point(&point, &guardian);
    println!();
    sagco_guardian::print_safety_classification(&safety);

    Ok(())
}
