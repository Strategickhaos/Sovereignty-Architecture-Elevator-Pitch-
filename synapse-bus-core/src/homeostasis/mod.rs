// Homeostasis Module
// GSCH Physics Engine - Maintains system equilibrium

pub mod gradient;
pub mod feedback;
pub mod dissolve;

/// System homeostasis state
#[derive(Debug, Clone)]
pub struct HomeostasisState {
    pub temperature: f32,
    pub entropy: f32,
    pub stability: f32,
}

impl HomeostasisState {
    /// Create a new homeostasis state
    pub fn new() -> Self {
        Self {
            temperature: 37.0, // "Normal" body temperature
            entropy: 0.0,
            stability: 1.0,
        }
    }

    /// Check if system is stable
    pub fn is_stable(&self) -> bool {
        self.temperature < 100.0 && self.entropy < 0.8 && self.stability > 0.3
    }

    /// Check if system is critical
    pub fn is_critical(&self) -> bool {
        self.temperature > 150.0 || self.entropy > 0.9 || self.stability < 0.1
    }
}

impl Default for HomeostasisState {
    fn default() -> Self {
        Self::new()
    }
}
