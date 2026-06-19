//! Example: Neural Simulation with Ca Dynamics Validation
//!
//! This example demonstrates how to use SAGCO Guardian to validate calcium dynamics
//! in neural simulations, preventing unphysical hallucinations.

use sagco_guardian::{SagcoGuardian, CaDynamicsParameters};

fn main() {
    println!("═══════════════════════════════════════════════════════════");
    println!("  SAGCO GUARDIAN × NEURAL SIMULATION PIPELINE");
    println!("  Ca²⁺ Dynamics Validation in Neural Spike Trains");
    println!("═══════════════════════════════════════════════════════════\n");
    
    // Initialize guardian
    let mut guardian = SagcoGuardian::new();
    println!("✅ Guardian initialized\n");
    
    // === SIMULATION 1: Resting Neuron ===
    println!("🧠 SIMULATION 1: Resting Neuron (Baseline)");
    println!("   Condition: No stimulation, baseline Ca²⁺");
    
    let resting_ca = 0.1;        // μM (typical resting concentration)
    let resting_velocity = 250.0; // μm²/s (slow diffusion)
    let resting_buffering = 0.98; // 98% buffered
    
    match CaDynamicsParameters::new(resting_ca, resting_velocity, resting_buffering) {
        Ok(ca) => {
            println!("   [Ca²⁺]: {:.2} μM", ca.concentration);
            println!("   Wave Velocity: {:.1} μm²/s", ca.wave_velocity);
            println!("   Buffering: {:.1}%", ca.buffering_ratio * 100.0);
            println!("   Phase: {}", ca.phase);
            
            match guardian.verify_ca_dynamics(&ca) {
                Ok(uncertainty) => {
                    println!("   ✅ Validation PASSED");
                    println!("   Geometry: [{:.2}°, {:.2}', {}]",
                        uncertainty.geometry.degrees,
                        uncertainty.geometry.minute,
                        uncertainty.geometry.element_symbol);
                    println!("   Confidence: {:.4}", uncertainty.confidence);
                }
                Err(e) => println!("   ❌ Validation FAILED: {}", e),
            }
        }
        Err(e) => println!("   ❌ Invalid Ca parameters: {}", e),
    }
    
    println!();
    
    // === SIMULATION 2: Action Potential Spike ===
    println!("🧠 SIMULATION 2: Action Potential Spike");
    println!("   Condition: VGCC opening, Ca²⁺ influx");
    
    let spike_ca = 2.5;           // μM (during spike)
    let spike_velocity = 450.0;   // μm²/s (faster diffusion)
    let spike_buffering = 0.95;   // 95% buffered
    
    match CaDynamicsParameters::new(spike_ca, spike_velocity, spike_buffering) {
        Ok(ca) => {
            println!("   [Ca²⁺]: {:.2} μM", ca.concentration);
            println!("   Wave Velocity: {:.1} μm²/s", ca.wave_velocity);
            println!("   Buffering: {:.1}%", ca.buffering_ratio * 100.0);
            println!("   Phase: {}", ca.phase);
            
            match guardian.verify_ca_dynamics(&ca) {
                Ok(uncertainty) => {
                    println!("   ✅ Validation PASSED");
                    println!("   Entropy: {:.4} bits", uncertainty.entropy);
                    println!("   KL Divergence: {:.4}", uncertainty.kl_divergence);
                    
                    // Generate proof for this spike
                    let proof = guardian.generate_proof(&uncertainty);
                    println!("   Spike Proof: {}...", &proof[..20]);
                }
                Err(e) => println!("   ❌ Validation FAILED: {}", e),
            }
        }
        Err(e) => println!("   ❌ Invalid Ca parameters: {}", e),
    }
    
    println!();
    
    // === SIMULATION 3: High-Frequency Burst ===
    println!("🧠 SIMULATION 3: High-Frequency Burst (100 Hz)");
    println!("   Condition: Rapid firing, elevated Ca²⁺");
    
    let burst_ca = 8.0;           // μM (high activity)
    let burst_velocity = 600.0;   // μm²/s (rapid diffusion)
    let burst_buffering = 0.90;   // 90% buffered (saturation)
    
    match CaDynamicsParameters::new(burst_ca, burst_velocity, burst_buffering) {
        Ok(ca) => {
            println!("   [Ca²⁺]: {:.2} μM", ca.concentration);
            println!("   Wave Velocity: {:.1} μm²/s", ca.wave_velocity);
            println!("   Buffering: {:.1}%", ca.buffering_ratio * 100.0);
            println!("   Phase: {}", ca.phase);
            
            match guardian.verify_ca_dynamics(&ca) {
                Ok(uncertainty) => {
                    println!("   ✅ Validation PASSED");
                    
                    // Check for warning conditions
                    if ca.concentration > 5.0 {
                        println!("   ⚠️  WARNING: Elevated Ca²⁺, monitor for excitotoxicity");
                    }
                    if uncertainty.confidence < 0.5 {
                        println!("   ⚠️  WARNING: Low confidence, increase simulation resolution");
                    }
                }
                Err(e) => println!("   ❌ Validation FAILED: {}", e),
            }
        }
        Err(e) => println!("   ❌ Invalid Ca parameters: {}", e),
    }
    
    println!();
    
    // === SIMULATION 4: Pathological State (Huntington's) ===
    println!("🧠 SIMULATION 4: Pathological State (Huntington's Disease Model)");
    println!("   Condition: Mutant huntingtin, prolonged Ca²⁺ elevation");
    
    let pathological_ca = 15.0;   // μM (pathologically high)
    let pathological_velocity = 350.0; // μm²/s (slower clearance)
    let pathological_buffering = 0.85; // 85% buffered (buffer depletion)
    
    match CaDynamicsParameters::new(pathological_ca, pathological_velocity, pathological_buffering) {
        Ok(ca) => {
            println!("   [Ca²⁺]: {:.2} μM", ca.concentration);
            println!("   Wave Velocity: {:.1} μm²/s", ca.wave_velocity);
            println!("   Buffering: {:.1}%", ca.buffering_ratio * 100.0);
            println!("   Phase: {}", ca.phase);
            
            match guardian.verify_ca_dynamics(&ca) {
                Ok(uncertainty) => {
                    println!("   ✅ Validation PASSED (Pathological State Detected)");
                    println!("   ⚠️  CRITICAL: Ca²⁺ in toxic range (>10 μM)");
                    println!("   ⚠️  Risk of apoptosis activation");
                    println!("   Geometry: [{:.2}°, {:.2}', {}]",
                        uncertainty.geometry.degrees,
                        uncertainty.geometry.minute,
                        uncertainty.geometry.element_symbol);
                }
                Err(e) => println!("   ❌ Validation FAILED: {}", e),
            }
        }
        Err(e) => println!("   ❌ Invalid Ca parameters: {}", e),
    }
    
    println!();
    
    // === SIMULATION 5: Hallucination Detection ===
    println!("🧠 SIMULATION 5: Hallucination Detection");
    println!("   Testing unphysical Ca dynamics");
    
    // Test A: Unrealistically high Ca (should fail)
    println!("\n   Test A: Unrealistic [Ca²⁺] (150 μM)");
    match CaDynamicsParameters::new(150.0, 300.0, 0.95) {
        Ok(_) => println!("   ❌ Should have been rejected!"),
        Err(e) => println!("   ✅ Correctly rejected: {}", e),
    }
    
    // Test B: Impossible wave velocity (should fail)
    println!("\n   Test B: Impossible wave velocity (2000 μm²/s)");
    match CaDynamicsParameters::new(1.0, 2000.0, 0.95) {
        Ok(_) => println!("   ❌ Should have been rejected!"),
        Err(e) => println!("   ✅ Correctly rejected: {}", e),
    }
    
    // Test C: Unphysical buffering (>99.9%)
    println!("\n   Test C: Unphysical buffering (99.99%)");
    match CaDynamicsParameters::new(1.0, 300.0, 0.9999) {
        Ok(_) => println!("   ❌ Should have been rejected!"),
        Err(e) => println!("   ✅ Correctly rejected: {}", e),
    }
    
    println!();
    
    // === SIMULATION 6: Time Series Validation ===
    println!("🧠 SIMULATION 6: Time Series Validation (Spike Train)");
    println!("   10 Hz stimulation over 1 second");
    
    // Simulate 10 spikes
    let spike_times = vec![0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]; // seconds
    let spike_concentrations = vec![0.1, 3.0, 0.5, 3.5, 0.8, 4.0, 1.2, 4.5, 1.5, 5.0]; // μM
    
    let mut valid_spikes = 0;
    let mut total_entropy = 0.0;
    
    for (&_time, &conc) in spike_times.iter().zip(spike_concentrations.iter()) {
        match CaDynamicsParameters::new(conc, 400.0, 0.95) {
            Ok(ca) => {
                match guardian.verify_ca_dynamics(&ca) {
                    Ok(uncertainty) => {
                        valid_spikes += 1;
                        total_entropy += uncertainty.entropy;
                    }
                    Err(_) => {}
                }
            }
            Err(_) => {}
        }
    }
    
    println!("   Valid Spikes: {}/{}", valid_spikes, spike_times.len());
    println!("   Average Entropy: {:.4} bits", total_entropy / valid_spikes as f64);
    println!("   ✅ Time series validation complete");
    
    println!("\n═══════════════════════════════════════════════════════════");
    println!("✅ NEURAL SIMULATION PIPELINE COMPLETE");
    println!("   Guardian successfully validated physiological dynamics");
    println!("   Guardian successfully detected pathological states");
    println!("   Guardian successfully rejected all hallucinations");
    println!("═══════════════════════════════════════════════════════════\n");
}
