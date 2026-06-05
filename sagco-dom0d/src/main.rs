use anyhow::Result;
use flamelang_engine::Engine;
use sagco_guardian::{Guardian, Uncertainty};
use sagco_netcalc::{probe_all_nodes, best_control_peer};

#[tokio::main]
async fn main() -> Result<()> {
    println!("🔥 SAGCO Dom0 Daemon Starting...");
    
    // Initialize Guardian
    let guardian = Guardian::new(0.7);
    println!("✓ Guardian initialized with threshold 0.7");
    
    // Initialize FlameLang Engine
    let mut engine = Engine::new();
    flamelang_engine::register_all(&mut engine);
    println!("✓ FlameLang engine registered with Guardian bindings");
    
    // Probe mesh network
    println!("\n📡 Probing mesh network...");
    let mesh = probe_all_nodes().await?;
    
    for node in &mesh {
        println!(
            "  Node: {} | Latency: {:.2}ms ± {:.2}ms",
            node.name,
            node.latency.mean,
            node.latency.stddev()
        );
        
        // Classify node safety based on latency uncertainty
        let uncertainty = Uncertainty::new(
            node.latency.stddev() / node.latency.mean.max(1.0),  // Coefficient of variation
            1.0 - (node.latency.stddev() / 100.0).min(1.0),      // Confidence inversely proportional to stddev
        );
        
        let classification = guardian.classify(&uncertainty);
        let geometry = guardian.map_uncertainty_to_geometry(&uncertainty);
        
        println!(
            "    Classification: {:?} | Geometry: ({:.2}, {:.2}, {:.2})",
            classification, geometry.x, geometry.y, geometry.z
        );
    }
    
    // Select best control peer
    let best_peer = best_control_peer(&mesh);
    println!("\n🎯 Best control peer: index {}", best_peer);
    
    println!("\n✅ Dom0 daemon initialized successfully");
    println!("   - Guardian: ACTIVE");
    println!("   - FlameLang Engine: REGISTERED");
    println!("   - Mesh Network: {} nodes", mesh.len());
    
    Ok(())
}
