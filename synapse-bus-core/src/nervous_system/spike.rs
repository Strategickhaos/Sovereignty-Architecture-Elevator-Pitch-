//! # Spike: The Signal
//!
//! A Spike is the fundamental unit of communication in the Synapse-Bus system.
//! It carries encrypted data along with physics metadata.

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use super::{OrganType, PhysicsVector};
use crate::primitives::CryptoCell;

/// A Spike is how organs communicate with the brain
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Spike {
    /// Unique identifier for this spike
    pub id: Uuid,
    
    /// When this spike was generated
    pub timestamp: DateTime<Utc>,
    
    /// Which organ generated this spike
    pub origin: OrganType,
    
    /// Physics data (GSCH)
    pub vector: PhysicsVector,
    
    /// Encrypted payload
    pub payload: CryptoCell<Vec<u8>>,
    
    /// Risk score (0.0 - 1.0) representing entropy level
    pub risk_score: f32,
}

impl Spike {
    /// Create a new Spike
    pub fn new(
        origin: OrganType,
        vector: PhysicsVector,
        payload: Vec<u8>,
        risk_score: f32,
    ) -> Self {
        Self {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            origin,
            vector,
            payload: CryptoCell::new(payload),
            risk_score: risk_score.clamp(0.0, 1.0),
        }
    }
    
    /// Check if this spike should be gated (blocked)
    pub fn should_gate(&self) -> bool {
        // Gate if entropy is too high
        if self.vector.heat > 0.8 {
            return true;
        }
        
        // Gate if target has negative gravity
        if self.vector.gravity < -5.0 {
            return true;
        }
        
        // Gate if risk score is critical
        if self.risk_score > 0.9 {
            return true;
        }
        
        false
    }
    
    /// Get the age of this spike in seconds
    pub fn age_seconds(&self) -> i64 {
        let now = Utc::now();
        (now - self.timestamp).num_seconds()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::nervous_system::VisionOrgan;

    #[test]
    fn test_spike_creation() {
        let spike = Spike::new(
            OrganType::Vision(VisionOrgan::Retina),
            PhysicsVector {
                heat: 0.5,
                gravity: 1.0,
            },
            vec![1, 2, 3, 4],
            0.3,
        );
        
        assert!(spike.id != Uuid::nil());
        assert_eq!(spike.risk_score, 0.3);
        assert!(!spike.should_gate());
    }

    #[test]
    fn test_spike_gating_heat() {
        let spike = Spike::new(
            OrganType::System,
            PhysicsVector {
                heat: 0.9,
                gravity: 0.0,
            },
            vec![],
            0.0,
        );
        
        assert!(spike.should_gate());
    }

    #[test]
    fn test_spike_gating_gravity() {
        let spike = Spike::new(
            OrganType::System,
            PhysicsVector {
                heat: 0.0,
                gravity: -6.0,
            },
            vec![],
            0.0,
        );
        
        assert!(spike.should_gate());
    }

    #[test]
    fn test_spike_gating_risk() {
        let spike = Spike::new(
            OrganType::System,
            PhysicsVector::default(),
            vec![],
            0.95,
        );
        
        assert!(spike.should_gate());
    }
}
