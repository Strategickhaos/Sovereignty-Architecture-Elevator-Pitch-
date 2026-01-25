// Example: Variational Inference for mesh optimization
use sagco_pipecalc_vi::{Gaussian, optimal_mesh_route, HasLatency};

// Simple struct that implements HasLatency
struct TestNode {
    latency: Gaussian,
}

impl HasLatency for TestNode {
    fn latency(&self) -> &Gaussian {
        &self.latency
    }
}

fn main() {
    println!("🧮 SAGCO Variational Inference Example\n");

    // Create test mesh with different latencies
    let mesh = vec![
        TestNode { latency: Gaussian::new(5.0, 1.0) },   // Node 0: 5ms ± 1ms
        TestNode { latency: Gaussian::new(10.0, 2.0) },  // Node 1: 10ms ± 1.4ms
        TestNode { latency: Gaussian::new(15.0, 4.0) },  // Node 2: 15ms ± 2ms
        TestNode { latency: Gaussian::new(8.0, 0.5) },   // Node 3: 8ms ± 0.7ms
    ];

    println!("Mesh nodes:");
    for (i, node) in mesh.iter().enumerate() {
        println!("  Node {}: {:.1}ms ± {:.1}ms", 
                 i, node.latency.mean, node.latency.stddev());
    }

    // Calculate optimal route from node 0 to node 1
    println!("\nCalculating optimal route from 0 to 1...");
    let alpha = 1.0;  // Weight for mean latency
    let beta = 0.5;   // Weight for variance (uncertainty)
    let gamma = 0.7;  // Weight for hop count

    match optimal_mesh_route(&mesh, 0, 1, alpha, beta, gamma) {
        Some(route) => {
            println!("  Path: {:?}", route.path);
            println!("  Total latency: {:.2}ms", route.total_latency);
            println!("  ✅ Route calculated successfully");
        }
        None => {
            println!("  ❌ No route found");
        }
    }

    // Test different weight configurations
    println!("\nTesting different VI weights:");
    let weight_configs = vec![
        (1.0, 0.0, 0.0, "Only mean latency"),
        (0.0, 1.0, 0.0, "Only variance"),
        (1.0, 1.0, 0.0, "Mean + variance"),
        (1.0, 0.5, 0.7, "Balanced (default)"),
    ];

    for (alpha, beta, gamma, desc) in weight_configs {
        if let Some(route) = optimal_mesh_route(&mesh, 0, 1, alpha, beta, gamma) {
            println!("  {}: cost={:.2}ms", desc, route.total_latency);
        }
    }
}
