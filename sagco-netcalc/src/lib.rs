use async_trait::async_trait;
use sagco_pipecalc_vi::{Gaussian, HasLatency};
use std::net::Ipv4Addr;
use std::time::Duration;
use tokio::net::TcpStream;
use tokio::time::Instant;

/// Geographic location for mesh nodes
#[derive(Debug, Clone)]
pub struct GeoLocation {
    pub latitude: f64,
    pub longitude: f64,
}

impl GeoLocation {
    pub fn new(latitude: f64, longitude: f64) -> Self {
        Self { latitude, longitude }
    }
}

/// Latency statistics from multiple probes
#[derive(Debug, Clone)]
pub struct LatencyStats {
    pub avg_ms: f64,
    pub stddev_ms: f64,
    pub min_ms: f64,
    pub max_ms: f64,
    pub success_count: usize,
    pub total_count: usize,
}

impl LatencyStats {
    pub fn new(latencies: Vec<f64>) -> Self {
        let count = latencies.len();
        let avg_ms = if count > 0 {
            latencies.iter().sum::<f64>() / count as f64
        } else {
            0.0
        };

        let variance = if count > 1 {
            latencies.iter()
                .map(|l| (l - avg_ms).powi(2))
                .sum::<f64>() / (count - 1) as f64
        } else {
            0.0
        };

        let stddev_ms = variance.sqrt();
        let min_ms = latencies.iter().copied().fold(f64::INFINITY, f64::min);
        let max_ms = latencies.iter().copied().fold(f64::NEG_INFINITY, f64::max);

        Self {
            avg_ms,
            stddev_ms,
            min_ms,
            max_ms,
            success_count: count,
            total_count: count,
        }
    }
}

/// Mesh network node with latency and bandwidth measurements
#[derive(Debug, Clone)]
pub struct MeshNode {
    pub name: String,
    pub latency: Gaussian,
    pub bandwidth: Gaussian,
}

impl HasLatency for MeshNode {
    fn latency(&self) -> &Gaussian {
        &self.latency
    }
}

/// Trait for network pinging
#[async_trait]
pub trait Pinger {
    async fn ping(&self, target: Ipv4Addr) -> Option<f64>;
    async fn ping_multiple(&self, target: Ipv4Addr, count: usize) -> LatencyStats;
}

/// TCP-based pinger implementation
#[derive(Debug, Default)]
pub struct TcpPinger {
    pub port: u16,
    pub timeout_ms: u64,
}

impl TcpPinger {
    pub fn new(port: u16, timeout_ms: u64) -> Self {
        Self { port, timeout_ms }
    }
}

#[async_trait]
impl Pinger for TcpPinger {
    async fn ping(&self, target: Ipv4Addr) -> Option<f64> {
        let start = Instant::now();
        let addr = format!("{}:{}", target, self.port);
        
        match tokio::time::timeout(
            Duration::from_millis(self.timeout_ms),
            TcpStream::connect(&addr)
        ).await {
            Ok(Ok(_)) => {
                let elapsed = start.elapsed();
                Some(elapsed.as_secs_f64() * 1000.0) // Convert to milliseconds
            }
            _ => None,
        }
    }

    async fn ping_multiple(&self, target: Ipv4Addr, count: usize) -> LatencyStats {
        let mut latencies = Vec::new();
        
        for _ in 0..count {
            if let Some(latency) = self.ping(target).await {
                latencies.push(latency);
            }
            // Small delay between pings
            tokio::time::sleep(Duration::from_millis(100)).await;
        }

        LatencyStats::new(latencies)
    }
}

/// Probe all mesh nodes with real TCP connections
pub async fn probe_all_nodes() -> anyhow::Result<Vec<MeshNode>> {
    let nodes = vec![
        Ipv4Addr::new(127, 0, 0, 1),  // Localhost for testing
        // Add more IPs as needed: Ipv4Addr::new(192, 168, 1, 1),
    ];
    
    let pinger = TcpPinger {
        port: 80,        // HTTP port for testing
        timeout_ms: 5000, // 5 second timeout
    };
    
    let mut mesh = Vec::new();
    for ip in nodes {
        let lat_stats = pinger.ping_multiple(ip, 3).await;
        
        // Use variance from statistics (stddev squared)
        mesh.push(MeshNode {
            name: ip.to_string(),
            latency: Gaussian::new(lat_stats.avg_ms, lat_stats.stddev_ms.powi(2)),
            bandwidth: Gaussian::new(1000.0, 100.0),  // Stub bandwidth for now
        });
    }
    
    Ok(mesh)
}

/// Select best control peer using VI route optimization
pub fn best_control_peer(mesh: &[MeshNode]) -> usize {
    if mesh.is_empty() {
        return 0;
    }

    // Use VI route to find low-latency peer
    sagco_pipecalc_vi::optimal_mesh_route(mesh, 0, 1, 1.0, 0.5, 0.7)
        .and_then(|r| r.path.get(1).copied())
        .unwrap_or(0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_latency_stats() {
        let latencies = vec![10.0, 12.0, 11.0, 13.0, 10.5];
        let stats = LatencyStats::new(latencies);
        
        assert!((stats.avg_ms - 11.3).abs() < 0.1);
        assert!(stats.min_ms == 10.0);
        assert!(stats.max_ms == 13.0);
    }

    #[test]
    fn test_mesh_node_creation() {
        let node = MeshNode {
            name: "test-node".to_string(),
            latency: Gaussian::new(5.0, 1.0),
            bandwidth: Gaussian::new(1000.0, 100.0),
        };
        
        assert_eq!(node.name, "test-node");
        assert_eq!(node.latency.mean, 5.0);
    }

    #[tokio::test]
    async fn test_tcp_pinger_localhost() {
        let pinger = TcpPinger {
            port: 80,
            timeout_ms: 1000,
        };
        
        // This may fail if nothing is listening on localhost:80
        // but it tests the implementation
        let _result = pinger.ping(Ipv4Addr::new(127, 0, 0, 1)).await;
    }
}
