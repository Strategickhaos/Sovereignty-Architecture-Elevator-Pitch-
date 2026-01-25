use serde::{Deserialize, Serialize};

/// Gaussian distribution for Variational Inference
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct Gaussian {
    /// Mean value
    pub mean: f64,
    /// Variance
    pub variance: f64,
}

impl Gaussian {
    /// Create a new Gaussian distribution
    pub fn new(mean: f64, variance: f64) -> Self {
        Self { mean, variance }
    }

    /// Get standard deviation
    pub fn stddev(&self) -> f64 {
        self.variance.sqrt()
    }
}

/// Route information for mesh networking
#[derive(Debug, Clone)]
pub struct Route {
    pub path: Vec<usize>,
    pub total_latency: f64,
}

/// Calculate optimal mesh route using VI
/// 
/// # Arguments
/// * `mesh` - Slice of mesh nodes with latency distributions
/// * `start` - Starting node index
/// * `end` - Ending node index
/// * `alpha` - Weight for mean latency
/// * `beta` - Weight for variance (uncertainty)
/// * `gamma` - Weight for hop count
pub fn optimal_mesh_route<T>(
    mesh: &[T],
    start: usize,
    end: usize,
    alpha: f64,
    beta: f64,
    gamma: f64,
) -> Option<Route>
where
    T: HasLatency,
{
    // Simple direct route for now (stub for full routing algorithm)
    if start >= mesh.len() || end >= mesh.len() {
        return None;
    }

    let path = vec![start, end];
    let latency = mesh.get(end)?.latency();
    let total_latency = latency.mean * alpha + latency.stddev() * beta + gamma * (path.len() as f64);

    Some(Route {
        path,
        total_latency,
    })
}

/// Trait for types that have latency measurements
pub trait HasLatency {
    fn latency(&self) -> &Gaussian;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gaussian_creation() {
        let g = Gaussian::new(5.0, 2.0);
        assert_eq!(g.mean, 5.0);
        assert_eq!(g.variance, 2.0);
        assert!((g.stddev() - 1.414).abs() < 0.01);
    }

    #[test]
    fn test_gaussian_stddev() {
        let g = Gaussian::new(10.0, 4.0);
        assert_eq!(g.stddev(), 2.0);
    }
}
