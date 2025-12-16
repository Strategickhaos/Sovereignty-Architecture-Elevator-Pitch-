// Gradient - Proton (Push) / Electron (Pull) Logic
// GSCH Physics Vector Implementation

use serde::{Deserialize, Serialize};

/// Physics vector representing GSCH (Gradient, Charge, Heat) data
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct PhysicsVector {
    /// Heat: System temperature / entropy (0.0 - 1.0)
    pub heat: f32,
    
    /// Gravity: Attraction/repulsion force (-inf to +inf)
    /// Positive = attractive, Negative = repulsive
    pub gravity: f32,
}

impl PhysicsVector {
    /// Create a new physics vector
    pub fn new(heat: f32, gravity: f32) -> Self {
        Self {
            heat: heat.clamp(0.0, 1.0),
            gravity,
        }
    }

    /// Create a zero vector
    pub fn zero() -> Self {
        Self {
            heat: 0.0,
            gravity: 0.0,
        }
    }

    /// Create a stable vector (low heat, neutral gravity)
    pub fn stable() -> Self {
        Self {
            heat: 0.2,
            gravity: 0.0,
        }
    }

    /// Create a critical vector (high heat, negative gravity)
    pub fn critical() -> Self {
        Self {
            heat: 0.9,
            gravity: -10.0,
        }
    }

    /// Calculate total energy
    pub fn energy(&self) -> f32 {
        self.heat.abs() + (self.gravity.abs() / 10.0).min(1.0)
    }

    /// Check if vector is stable
    pub fn is_stable(&self) -> bool {
        self.heat < 0.3 && self.gravity.abs() < 5.0
    }

    /// Check if vector is critical
    pub fn is_critical(&self) -> bool {
        self.heat > 0.8 || self.gravity < -5.0
    }

    /// Apply proton push (increase heat)
    pub fn push(&mut self, amount: f32) {
        self.heat = (self.heat + amount).clamp(0.0, 1.0);
    }

    /// Apply electron pull (decrease heat)
    pub fn pull(&mut self, amount: f32) {
        self.heat = (self.heat - amount).clamp(0.0, 1.0);
    }

    /// Add gravitational force
    pub fn attract(&mut self, force: f32) {
        self.gravity += force;
    }

    /// Subtract gravitational force
    pub fn repel(&mut self, force: f32) {
        self.gravity -= force;
    }

    /// Combine two vectors
    pub fn combine(&self, other: &PhysicsVector) -> PhysicsVector {
        PhysicsVector {
            heat: ((self.heat + other.heat) / 2.0).clamp(0.0, 1.0),
            gravity: (self.gravity + other.gravity) / 2.0,
        }
    }
}

impl Default for PhysicsVector {
    fn default() -> Self {
        Self::stable()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_physics_vector_creation() {
        let vec = PhysicsVector::new(0.5, 2.0);
        assert_eq!(vec.heat, 0.5);
        assert_eq!(vec.gravity, 2.0);
    }

    #[test]
    fn test_heat_clamping() {
        let vec = PhysicsVector::new(1.5, 0.0);
        assert_eq!(vec.heat, 1.0);

        let vec2 = PhysicsVector::new(-0.5, 0.0);
        assert_eq!(vec2.heat, 0.0);
    }

    #[test]
    fn test_stability_checks() {
        let stable = PhysicsVector::stable();
        assert!(stable.is_stable());
        assert!(!stable.is_critical());

        let critical = PhysicsVector::critical();
        assert!(!critical.is_stable());
        assert!(critical.is_critical());
    }

    #[test]
    fn test_push_pull() {
        let mut vec = PhysicsVector::new(0.5, 0.0);
        
        vec.push(0.2);
        assert!((vec.heat - 0.7).abs() < 0.001);

        vec.pull(0.4);
        assert!((vec.heat - 0.3).abs() < 0.001);
    }

    #[test]
    fn test_attract_repel() {
        let mut vec = PhysicsVector::new(0.5, 0.0);
        
        vec.attract(5.0);
        assert_eq!(vec.gravity, 5.0);

        vec.repel(10.0);
        assert_eq!(vec.gravity, -5.0);
    }

    #[test]
    fn test_combine() {
        let vec1 = PhysicsVector::new(0.6, 4.0);
        let vec2 = PhysicsVector::new(0.4, 2.0);
        
        let combined = vec1.combine(&vec2);
        assert_eq!(combined.heat, 0.5);
        assert_eq!(combined.gravity, 3.0);
    }

    #[test]
    fn test_energy_calculation() {
        let vec = PhysicsVector::new(0.5, 10.0);
        let energy = vec.energy();
        assert!(energy > 0.0);
        assert!(energy <= 2.0);
    }
}
