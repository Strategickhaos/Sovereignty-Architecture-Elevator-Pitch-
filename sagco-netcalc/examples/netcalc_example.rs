// Example: Network latency measurement with TCP probing
use sagco_netcalc::{TcpPinger, Pinger, MeshNode};
use sagco_pipecalc_vi::Gaussian;
use std::net::Ipv4Addr;

#[tokio::main]
async fn main() {
    println!("📡 SAGCO Network Calculation Example\n");

    // Create TCP pinger
    let pinger = TcpPinger::new(80, 5000);

    // Test localhost
    let target = Ipv4Addr::new(127, 0, 0, 1);
    println!("Pinging {} on port 80...", target);

    // Single ping
    match pinger.ping(target).await {
        Some(latency) => println!("  Single ping: {:.2}ms", latency),
        None => println!("  Single ping: timeout"),
    }

    // Multiple pings
    let stats = pinger.ping_multiple(target, 5).await;
    println!("\nMultiple pings (n=5):");
    println!("  Average: {:.2}ms", stats.avg_ms);
    println!("  Std Dev: {:.2}ms", stats.stddev_ms);
    println!("  Min: {:.2}ms", stats.min_ms);
    println!("  Max: {:.2}ms", stats.max_ms);
    println!("  Success: {}/{}", stats.success_count, stats.total_count);

    // Create mesh node
    let node = MeshNode {
        name: target.to_string(),
        latency: Gaussian::new(stats.avg_ms, stats.stddev_ms.powi(2)),
        bandwidth: Gaussian::new(1000.0, 100.0),
    };

    println!("\nMesh Node:");
    println!("  Name: {}", node.name);
    println!("  Latency: {:.2}ms ± {:.2}ms", 
             node.latency.mean, node.latency.stddev());
    println!("  Bandwidth: {:.2} Mbps ± {:.2} Mbps", 
             node.bandwidth.mean, node.bandwidth.stddev());
}
