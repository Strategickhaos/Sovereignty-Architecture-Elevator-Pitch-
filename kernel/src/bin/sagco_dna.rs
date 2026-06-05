// SAGCO DNA - DNA Evolution Tool
// Reads guardian-uncertainty.json, analyzes compiler health, and mutates DNA strand

use sagco_guardian::bench_ingest::load_guardian_uncertainty;
use sagco_kernel::dna_mutation::*;
use serde_yaml;
use std::fs;
use std::path::Path;

fn main() -> anyhow::Result<()> {
    println!("╔═══════════════════════════════════════════════════════╗");
    println!("║              SAGCO DNA v1.0.0                         ║");
    println!("║         DNA Strand Evolution System                   ║");
    println!("╚═══════════════════════════════════════════════════════╝\n");

    // Try to find guardian-uncertainty.json
    let uncertainty_paths = vec![
        "guardian-uncertainty.json",
        "flamebench/guardian-uncertainty.json",
        "/tmp/guardian-uncertainty.json",
    ];

    let mut export = None;
    for path in &uncertainty_paths {
        if let Ok(e) = load_guardian_uncertainty(path) {
            println!("✅ Loaded Guardian export from: {}", path);
            export = Some(e);
            break;
        }
    }

    if export.is_none() {
        eprintln!("⚠️  Warning: No guardian-uncertainty.json found.");
        eprintln!("   Searched paths:");
        for path in &uncertainty_paths {
            eprintln!("     - {}", path);
        }
        eprintln!("\n   DNA strand will not be mutated.");
        eprintln!("   To enable mutation, run flamebench first to generate guardian-uncertainty.json");
        return Ok(());
    }

    let export = export.unwrap();

    // Display compiler health
    println!("\n📊 FLM2 Compiler Health (overall):");
    println!("   DNA Strand:  {}", export.dna_strand);
    println!("   p_success = {:.3}", export.overall.p_success);
    println!("   entropy   = {:.3}", export.overall.entropy);

    // Show concept-specific uncertainties
    if !export.uncertainties.is_empty() {
        println!("\n   Concept Analysis:");
        for u in &export.uncertainties {
            println!("   [{:12}] p={:.3} entropy={:.3} (α={:.1}, β={:.1}, n={})",
                     u.tag, u.p_correct, u.entropy, u.alpha, u.beta, u.sample_size);
        }
    }

    // Load DNA spec
    let spec_paths = vec![
        "sagco_unified_spec.yaml",
        "../sagco_unified_spec.yaml",
        "/opt/sagco-os/sagco_unified_spec.yaml",
    ];

    let mut spec_path = None;
    for path in &spec_paths {
        if Path::new(path).exists() {
            spec_path = Some(path);
            break;
        }
    }

    if spec_path.is_none() {
        eprintln!("\n❌ Error: sagco_unified_spec.yaml not found.");
        eprintln!("   Searched paths:");
        for path in &spec_paths {
            eprintln!("     - {}", path);
        }
        return Ok(());
    }

    let spec_path = spec_path.unwrap();
    println!("\n✅ Found DNA spec: {}", spec_path);

    let dna_txt = fs::read_to_string(spec_path)?;
    let mut dna_yaml: serde_yaml::Value = serde_yaml::from_str(&dna_txt)?;

    // Extract current DNA strand
    let current_strand = dna_yaml["DNA_Strand"]
        .as_str()
        .unwrap_or("FLM2-CMD1-MESH5-ORB1")
        .to_string();

    println!("   Current DNA Strand: {}", current_strand);

    // Check for mutations
    let mut mutations = Vec::new();
    let mut new_strand = current_strand.clone();

    // FLM2 mutation (p_success >= 0.95)
    if let Some(mutated) = suggest_flm_mutation(&new_strand, export.overall.p_success, 0.95) {
        mutations.push(format!("FLM2 → FLM2.1 (p_success={:.3} >= 0.95)", export.overall.p_success));
        new_strand = mutated;
    }

    // CMD mutation (example: check if we have 2+ commands)
    // In a real implementation, this would count actual commands
    // For now, we'll skip automatic CMD mutation

    // MESH mutation (example: would check actual node count)
    // Skipped for this demo

    // ORB mutation (example: would check oracle safety score)
    // Skipped for this demo

    if mutations.is_empty() {
        println!("\n✅ DNA Strand Health: STABLE");
        println!("   No mutations recommended at this time.");
        println!("   Thresholds:");
        println!("     - FLM2 → FLM2.1: p_success >= 0.95 (current: {:.3})", export.overall.p_success);
    } else {
        println!("\n🧬 DNA MUTATION RECOMMENDED:");
        for m in &mutations {
            println!("   ✓ {}", m);
        }
        println!("\n   Old Strand: {}", current_strand);
        println!("   New Strand: {}", new_strand);

        // Update the YAML
        dna_yaml["DNA_Strand"] = serde_yaml::Value::String(new_strand.clone());
        
        // Write back
        let new_yaml = serde_yaml::to_string(&dna_yaml)?;
        fs::write(spec_path, new_yaml)?;
        
        println!("\n✅ DNA Strand Updated in: {}", spec_path);
    }

    Ok(())
}
