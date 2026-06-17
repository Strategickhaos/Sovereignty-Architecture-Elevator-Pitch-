// Membrane - API Boundary Traits
// The cellular membrane controls what enters and exits

use async_trait::async_trait;
use anyhow::Result;

/// Membrane trait - defines the boundary interface
#[async_trait]
pub trait Membrane {
    /// Check if a request can pass through the membrane
    fn can_pass(&self, request: &[u8]) -> bool;

    /// Process incoming data
    async fn ingest(&mut self, data: Vec<u8>) -> Result<Vec<u8>>;

    /// Process outgoing data
    async fn excrete(&mut self, data: Vec<u8>) -> Result<Vec<u8>>;

    /// Get membrane permeability (0.0 = closed, 1.0 = fully open)
    fn permeability(&self) -> f32;
}

/// Basic membrane implementation
pub struct BasicMembrane {
    permeability: f32,
    max_size: usize,
}

impl BasicMembrane {
    pub fn new(permeability: f32, max_size: usize) -> Self {
        Self {
            permeability: permeability.clamp(0.0, 1.0),
            max_size,
        }
    }

    pub fn set_permeability(&mut self, permeability: f32) {
        self.permeability = permeability.clamp(0.0, 1.0);
    }
}

#[async_trait]
impl Membrane for BasicMembrane {
    fn can_pass(&self, request: &[u8]) -> bool {
        request.len() <= self.max_size && self.permeability > 0.0
    }

    async fn ingest(&mut self, data: Vec<u8>) -> Result<Vec<u8>> {
        if !self.can_pass(&data) {
            anyhow::bail!("Data too large or membrane closed");
        }
        Ok(data)
    }

    async fn excrete(&mut self, data: Vec<u8>) -> Result<Vec<u8>> {
        if !self.can_pass(&data) {
            anyhow::bail!("Data too large or membrane closed");
        }
        Ok(data)
    }

    fn permeability(&self) -> f32 {
        self.permeability
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_membrane_creation() {
        let membrane = BasicMembrane::new(0.5, 1000);
        assert_eq!(membrane.permeability(), 0.5);
    }

    #[tokio::test]
    async fn test_membrane_ingest() {
        let mut membrane = BasicMembrane::new(1.0, 1000);
        let data = vec![1, 2, 3, 4, 5];
        let result = membrane.ingest(data.clone()).await;
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), data);
    }

    #[tokio::test]
    async fn test_membrane_size_limit() {
        let mut membrane = BasicMembrane::new(1.0, 10);
        let large_data = vec![0u8; 100];
        let result = membrane.ingest(large_data).await;
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_membrane_closed() {
        let mut membrane = BasicMembrane::new(0.0, 1000);
        let data = vec![1, 2, 3];
        let result = membrane.ingest(data).await;
        assert!(result.is_err());
    }
}
