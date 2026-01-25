// Example: Using SAGCO Guardian for uncertainty classification
use sagco_guardian::{Guardian, Uncertainty, SafetyClassification};

fn main() {
    println!("🛡️ SAGCO Guardian Example\n");

    // Create Guardian with entropy threshold 0.7
    let guardian = Guardian::new(0.7);

    // Test different uncertainty levels
    let test_cases = vec![
        ("Low uncertainty", Uncertainty::new(0.2, 0.95)),
        ("Medium uncertainty", Uncertainty::new(0.5, 0.7)),
        ("High uncertainty", Uncertainty::new(0.9, 0.3)),
    ];

    for (name, uncertainty) in test_cases {
        let classification = guardian.classify(&uncertainty);
        let geometry = guardian.map_uncertainty_to_geometry(&uncertainty);

        println!("Test: {}", name);
        println!("  Uncertainty: entropy={:.2}, confidence={:.2}", 
                 uncertainty.entropy, uncertainty.confidence);
        println!("  Classification: {:?}", classification);
        println!("  Geometry: ({:.2}, {:.2}, {:.2})", 
                 geometry.x, geometry.y, geometry.z);

        match classification {
            SafetyClassification::Safe => println!("  ✅ Operation is safe to proceed"),
            SafetyClassification::Caution => println!("  ⚠️  Proceed with caution"),
            SafetyClassification::Unsafe => println!("  ❌ Operation should be halted"),
        }
        println!();
    }
}
