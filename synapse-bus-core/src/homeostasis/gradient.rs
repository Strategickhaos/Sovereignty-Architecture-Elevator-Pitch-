//! # Gradient: Proton (Push) / Electron (Pull) Logic
//!
//! Implements the gradient-driven homeostasis mechanism.

use nalgebra as na;
use crate::error::Result;

/// The gradient engine state
pub struct GradientEngine {
    /// Current system gradient vector
    gradient: na::Vector3<f64>,
}

impl GradientEngine {
    /// Create a new gradient engine
    pub fn new() -> Self {
        Self {
            gradient: na::Vector3::zeros(),
        }
    }
    
    /// Calculate push force (protons)
    pub fn calculate_push(&self, position: na::Vector3<f64>) -> na::Vector3<f64> {
        // Simple repulsive force calculation
        let distance = position.norm();
        if distance < 1e-6 {
            return na::Vector3::zeros();
        }
        
        let force_magnitude = 1.0 / (distance * distance);
        position.normalize() * force_magnitude
    }
    
    /// Calculate pull force (electrons)
    pub fn calculate_pull(&self, position: na::Vector3<f64>) -> na::Vector3<f64> {
        // Simple attractive force calculation
        let distance = position.norm();
        if distance < 1e-6 {
            return na::Vector3::zeros();
        }
        
        let force_magnitude = -1.0 / (distance * distance);
        position.normalize() * force_magnitude
    }
    
    /// Update the system gradient
    pub fn update_gradient(&mut self, delta: na::Vector3<f64>) {
        self.gradient += delta;
    }
    
    /// Get the current gradient
    pub fn get_gradient(&self) -> na::Vector3<f64> {
        self.gradient
    }
}

impl Default for GradientEngine {
    fn default() -> Self {
        Self::new()
    }
}

static ENGINE: once_cell::sync::OnceCell<std::sync::Mutex<GradientEngine>> = 
    once_cell::sync::OnceCell::new();

/// Initialize the global gradient engine
pub fn initialize() -> Result<()> {
    let engine = std::sync::Mutex::new(GradientEngine::new());
    ENGINE
        .set(engine)
        .map_err(|_| crate::error::SynapseError::General("Gradient engine already initialized".to_string()))?;
    Ok(())
}

/// Get access to the gradient engine
pub fn with_engine<F, R>(f: F) -> Result<R>
where
    F: FnOnce(&mut GradientEngine) -> R,
{
    let engine = ENGINE
        .get()
        .ok_or_else(|| crate::error::SynapseError::General("Gradient engine not initialized".to_string()))?;
    
    let mut guard = engine.lock().unwrap();
    Ok(f(&mut *guard))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gradient_engine_creation() {
        let engine = GradientEngine::new();
        assert_eq!(engine.get_gradient(), na::Vector3::zeros());
    }

    #[test]
    fn test_push_force() {
        let engine = GradientEngine::new();
        let position = na::Vector3::new(1.0, 0.0, 0.0);
        let force = engine.calculate_push(position);
        
        // Force should be in the same direction as position (repulsive)
        assert!(force.x > 0.0);
    }

    #[test]
    fn test_pull_force() {
        let engine = GradientEngine::new();
        let position = na::Vector3::new(1.0, 0.0, 0.0);
        let force = engine.calculate_pull(position);
        
        // Force should be opposite to position (attractive)
        assert!(force.x < 0.0);
    }

    #[test]
    fn test_update_gradient() {
        let mut engine = GradientEngine::new();
        let delta = na::Vector3::new(1.0, 2.0, 3.0);
        
        engine.update_gradient(delta);
        assert_eq!(engine.get_gradient(), delta);
    }
}
