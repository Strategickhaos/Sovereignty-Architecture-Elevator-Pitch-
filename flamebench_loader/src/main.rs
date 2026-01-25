// FLAMEBENCH LOADER — Main executable
// DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1

use flamebench_loader::{FlameBenchLoader, GuardianIntegration};

fn main() {
    println!("═══════════════════════════════════════════════════════════");
    println!("  FLAMEBENCH LOADER — Rust Uncertainty Integration");
    println!("  DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD27-ISO103-MESH5-ORB1-BENCH1");
    println!("═══════════════════════════════════════════════════════════\n");

    // Get results directory from args or use default
    let args: Vec<String> = std::env::args().collect();
    let results_dir = if args.len() > 1 {
        &args[1]
    } else {
        "results"
    };

    println!("📂 Loading from: {}\n", results_dir);

    let loader = FlameBenchLoader::new(results_dir);

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
            let guardian = GuardianIntegration::new(results_dir);

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
            println!("   python3 flamebench.py --output-dir {}", results_dir);
        }
    }

    println!("\n═══════════════════════════════════════════════════════════");
}
