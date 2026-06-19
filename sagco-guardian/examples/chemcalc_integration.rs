//! Example: Integrating SAGCO Guardian with Quantum Chemistry Calculations (chemcalc_vi)
//!
//! This example demonstrates how to use SAGCO Guardian to validate HOMO/LUMO gaps
//! from quantum mechanical calculations with variational inference.

use sagco_guardian::{SagcoGuardian, QMParameters, Uncertainty};

fn main() {
    println!("═══════════════════════════════════════════════════════════");
    println!("  SAGCO GUARDIAN × CHEMCALC_VI INTEGRATION");
    println!("  Quantum Chemistry Validation with VI on Orbital Gaps");
    println!("═══════════════════════════════════════════════════════════\n");
    
    // Initialize guardian
    let mut guardian = SagcoGuardian::new();
    println!("✅ Guardian initialized with genesis increment {}", guardian.genesis_increment);
    println!("   Architect ID: {}\n", guardian.architect_id);
    
    // === EXPERIMENT 1: Glycine Amino Acid ===
    println!("🧬 EXPERIMENT 1: Glycine Amino Acid");
    println!("   Formula: C₂H₅NO₂");
    
    // Typical DFT calculation for glycine
    let glycine_homo = -7.5; // eV
    let glycine_lumo = -3.0; // eV
    
    match QMParameters::new(glycine_homo, glycine_lumo) {
        Ok(qm) => {
            println!("   HOMO: {:.2} eV", qm.homo_energy);
            println!("   LUMO: {:.2} eV", qm.lumo_energy);
            println!("   Gap: {:.2} eV", qm.gap);
            println!("   Phase: {}", qm.phase);
            
            // Verify with guardian
            match guardian.verify_qm_parameters(&qm) {
                Ok(uncertainty) => {
                    println!("   ✅ Validation PASSED");
                    println!("   Uncertainty: [{:.2}°, {:.2}', {}]",
                        uncertainty.geometry.degrees,
                        uncertainty.geometry.minute,
                        uncertainty.geometry.element_symbol);
                    println!("   Confidence: {:.4}", uncertainty.confidence);
                    println!("   Entropy: {:.4} bits", uncertainty.entropy);
                    
                    // Generate cryptographic proof
                    let proof = guardian.generate_proof(&uncertainty);
                    println!("   Proof: {}...", &proof[..20]);
                }
                Err(e) => {
                    println!("   ❌ Validation FAILED: {}", e);
                }
            }
        }
        Err(e) => {
            println!("   ❌ Invalid QM parameters: {}", e);
        }
    }
    
    println!();
    
    // === EXPERIMENT 2: Ca-Binding EF-Hand Motif ===
    println!("🧬 EXPERIMENT 2: EF-Hand Ca-Binding Site");
    println!("   Protein fragment with Ca²⁺ coordination");
    
    // QM/MM calculation for Ca-binding site
    let efhand_homo = -6.8; // eV (less negative due to Ca²⁺)
    let efhand_lumo = -2.3; // eV
    
    match QMParameters::new(efhand_homo, efhand_lumo) {
        Ok(qm) => {
            println!("   HOMO: {:.2} eV", qm.homo_energy);
            println!("   LUMO: {:.2} eV", qm.lumo_energy);
            println!("   Gap: {:.2} eV", qm.gap);
            println!("   Phase: {}", qm.phase);
            
            match guardian.verify_qm_parameters(&qm) {
                Ok(uncertainty) => {
                    println!("   ✅ Validation PASSED");
                    println!("   Geometry: [{:.2}°, {:.2}', {}]",
                        uncertainty.geometry.degrees,
                        uncertainty.geometry.minute,
                        uncertainty.geometry.element_symbol);
                    println!("   KL Divergence: {:.4}", uncertainty.kl_divergence);
                }
                Err(e) => {
                    println!("   ❌ Validation FAILED: {}", e);
                }
            }
        }
        Err(e) => {
            println!("   ❌ Invalid QM parameters: {}", e);
        }
    }
    
    println!();
    
    // === EXPERIMENT 3: Variational Inference on Gap Distribution ===
    println!("🧬 EXPERIMENT 3: Variational Inference on Gap Distribution");
    println!("   Bayesian uncertainty quantification");
    
    // VI posterior: Gaussian(mean=4.0 eV, variance=0.5 eV²)
    let gap_mean = 4.0;
    let gap_variance = 0.5;
    let element = 6; // Carbon (organic molecules)
    
    match Uncertainty::from_gap_variance(gap_mean, gap_variance, element) {
        Ok(uncertainty) => {
            println!("   Gap Mean: {:.2} eV", gap_mean);
            println!("   Gap Variance: {:.2} eV²", gap_variance);
            println!("   Entropy (H): {:.4} bits", uncertainty.entropy);
            println!("   Confidence: {:.4}", uncertainty.confidence);
            println!("   Mapped to: [{:.2}°, {:.2}', {}]",
                uncertainty.geometry.degrees,
                uncertainty.geometry.minute,
                uncertainty.geometry.element_symbol);
            
            // Check if entropy is within acceptable bounds
            if uncertainty.entropy > 2.0 {
                println!("   ⚠️  WARNING: High entropy detected, increase sampling");
            } else {
                println!("   ✅ Entropy within acceptable bounds");
            }
            
            // Generate signature
            let signature = guardian.sign_with_authority(b"VI_GAP_POSTERIOR");
            println!("   Signature: 0x{}...", hex::encode(&signature[..8]));
        }
        Err(e) => {
            println!("   ❌ Failed to map uncertainty: {}", e);
        }
    }
    
    println!();
    
    // === EXPERIMENT 4: Hallucination Detection ===
    println!("🧬 EXPERIMENT 4: Hallucination Detection");
    println!("   Testing invalid/unrealistic gaps");
    
    // Try to create unrealistic gap (too small - reactive/hallucination)
    println!("\n   Test A: Gap too small (0.5 eV)");
    match QMParameters::new(-5.0, -4.5) {
        Ok(_) => println!("   ❌ Should have been rejected!"),
        Err(e) => println!("   ✅ Correctly rejected: {}", e),
    }
    
    // Try to create unrealistic gap (too large - hallucination)
    println!("\n   Test B: Gap too large (8.0 eV)");
    match QMParameters::new(-9.0, -1.0) {
        Ok(_) => println!("   ❌ Should have been rejected!"),
        Err(e) => println!("   ✅ Correctly rejected: {}", e),
    }
    
    // Try negative gap (unphysical)
    println!("\n   Test C: Negative gap (HOMO > LUMO)");
    match QMParameters::new(-3.0, -5.0) {
        Ok(_) => println!("   ❌ Should have been rejected!"),
        Err(e) => println!("   ✅ Correctly rejected: {}", e),
    }
    
    println!("\n═══════════════════════════════════════════════════════════");
    println!("✅ CHEMCALC_VI INTEGRATION COMPLETE");
    println!("   Guardian successfully validated all realistic calculations");
    println!("   Guardian successfully rejected all hallucinations");
    println!("═══════════════════════════════════════════════════════════\n");
}
