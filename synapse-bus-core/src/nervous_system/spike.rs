// Nervous System: Spike routing structure
use std::fmt;

/// Physics vector for spike propagation
#[derive(Debug, Clone, Copy)]
pub struct PhysicsVector {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

/// Spike: Neural event in the Synapse-Bus nervous system
#[derive(Debug, Clone)]
pub struct Spike {
    /// Direction and magnitude of spike propagation
    pub vector: PhysicsVector,
    
    /// Risk factor (0.0 = safe, 1.0 = critical)
    pub risk: f32,
    
    /// Timestamp of spike generation
    pub timestamp: u64,
}

impl Spike {
    pub fn new(vector: PhysicsVector, risk: f32) -> Self {
        Self {
            vector,
            risk,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        }
    }
    
    /// Calculate spike magnitude
    pub fn magnitude(&self) -> f32 {
        (self.vector.x.powi(2) + 
         self.vector.y.powi(2) + 
         self.vector.z.powi(2)).sqrt()
    }
}
