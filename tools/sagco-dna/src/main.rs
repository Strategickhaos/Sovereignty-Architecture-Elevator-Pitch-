use sagco_guardian::bench_ingest::load_guardian_uncertainty;
use sagco_kernel::dna_mutation::suggest_flm_mutation;
use std::fs;
use std::path::Path;
use anyhow::Context;

fn main() -> anyhow::Result<()> {
    println!("\n╔════════════════════════════════════════╗");
    println!("║  SAGCO-DNA v1.0                        ║");
    println!("║  DNA Strand Evolution Manager          ║");
    println!("╚════════════════════════════════════════╝\n");

    // Paths to check
    let guardian_paths = vec![
        "guardian-uncertainty.json",
        "E:\\FlameBench\\guardian-uncertainty.json",
        "/opt/flamebench/guardian-uncertainty.json",
    ];

    let spec_paths = vec![
        "sagco_unified_spec.yaml",
        "E:\\Strategickhaos\\sagco-os\\sagco_unified_spec.yaml",
        "/opt/sagco-os/sagco_unified_spec.yaml",
    ];

    // Find Guardian export
    let mut guardian_path = None;
    for path in &guardian_paths {
        if Path::new(path).exists() {
            guardian_path = Some(path.to_string());
            break;
        }
    }

    let guardian_path = guardian_path
        .context("Guardian uncertainty export not found. Run FlameBench first.")?;

    // Find spec file
    let mut spec_path = None;
    for path in &spec_paths {
        if Path::new(path).exists() {
            spec_path = Some(path.to_string());
            break;
        }
    }

    let spec_path = spec_path
        .context("sagco_unified_spec.yaml not found")?;

    // Load Guardian export
    println!("Loading Guardian metrics from: {}", guardian_path);
    let export = load_guardian_uncertainty(&guardian_path)?;
    
    println!("\nCurrent DNA Strand: {}", export.dna_strand);
    println!("FLM2 Compiler Health:");
    println!("  p_success = {:.3}", export.overall.p_success);
    println!("  entropy   = {:.3}", export.overall.entropy);
    println!();

    // Check if mutation is suggested
    let suggested = suggest_flm_mutation(
        &export.dna_strand,
        export.overall.p_success,
        export.overall.entropy,
    );

    match suggested {
        Some(new_strand) => {
            println!("✓ Mutation suggested: {} → {}", export.dna_strand, new_strand);
            println!("  Reason: p_success >= 0.95 and entropy < 0.3");
            println!();

            // Update the spec file
            println!("Updating {}...", spec_path);
            let spec_txt = fs::read_to_string(&spec_path)?;
            let mut new_txt = String::new();

            for line in spec_txt.lines() {
                if line.starts_with("DNA Strand:") {
                    new_txt.push_str(&format!("DNA Strand: {}\n", new_strand));
                } else {
                    new_txt.push_str(line);
                    new_txt.push('\n');
                }
            }

            fs::write(&spec_path, new_txt)?;
            println!("✓ DNA strand updated successfully!");
        }
        None => {
            println!("✗ No mutation suggested");
            println!("  Thresholds not met:");
            println!("    - p_success: {:.3} (need >= 0.95)", export.overall.p_success);
            println!("    - entropy: {:.3} (need < 0.30)", export.overall.entropy);
        }
    }

    println!();
    Ok(())
}
