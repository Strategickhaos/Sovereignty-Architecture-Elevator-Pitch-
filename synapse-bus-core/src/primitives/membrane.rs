//! # Membrane: API Boundary Traits
//!
//! The membrane defines the interface between the internal system and external world.

use async_trait::async_trait;
use crate::error::Result;

/// Trait for objects that can pass through the membrane
#[async_trait]
pub trait Membrane: Send + Sync {
    /// Check if this object can enter the system
    async fn can_enter(&self) -> Result<bool>;
    
    /// Check if this object can exit the system
    async fn can_exit(&self) -> Result<bool>;
    
    /// Get the permeability score (0.0 = blocked, 1.0 = free flow)
    fn permeability(&self) -> f32;
}

/// A basic membrane implementation
pub struct BasicMembrane {
    permeability: f32,
}

impl BasicMembrane {
    /// Create a new membrane with given permeability
    pub fn new(permeability: f32) -> Self {
        Self {
            permeability: permeability.clamp(0.0, 1.0),
        }
    }
}

#[async_trait]
impl Membrane for BasicMembrane {
    async fn can_enter(&self) -> Result<bool> {
        Ok(self.permeability > 0.5)
    }
    
    async fn can_exit(&self) -> Result<bool> {
        Ok(self.permeability > 0.3)
    }
    
    fn permeability(&self) -> f32 {
        self.permeability
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_membrane_permeability() {
        let membrane = BasicMembrane::new(0.8);
        assert_eq!(membrane.permeability(), 0.8);
        assert!(membrane.can_enter().await.unwrap());
        assert!(membrane.can_exit().await.unwrap());
    }

    #[tokio::test]
    async fn test_membrane_low_permeability() {
        let membrane = BasicMembrane::new(0.2);
        assert_eq!(membrane.permeability(), 0.2);
        assert!(!membrane.can_enter().await.unwrap());
        assert!(!membrane.can_exit().await.unwrap());
    }
}
