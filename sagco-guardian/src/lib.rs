use serde::{Deserialize, Serialize};

/// Uncertainty measurement in cognitive operations
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Uncertainty {
    pub entropy: f64,
    pub confidence: f64,
}

impl Uncertainty {
    pub fn new(entropy: f64, confidence: f64) -> Self {
        Self { entropy, confidence }
    }
}

/// Geometric point in cognitive space
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeometryPoint {
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl GeometryPoint {
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Self { x, y, z }
    }
}

/// Safety classification for operations
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SafetyClassification {
    Safe,
    Caution,
    Unsafe,
}

/// Core Guardian for cognitive safety monitoring
#[derive(Debug)]
pub struct Guardian {
    threshold_entropy: f64,
}

impl Guardian {
    pub fn new(threshold_entropy: f64) -> Self {
        Self { threshold_entropy }
    }

    pub fn map_uncertainty_to_geometry(&self, uncertainty: &Uncertainty) -> GeometryPoint {
        // Map high entropy to higher spatial coordinates (Q3 minute 35 reference)
        GeometryPoint::new(
            uncertainty.entropy,
            uncertainty.confidence,
            uncertainty.entropy * uncertainty.confidence,
        )
    }

    pub fn classify(&self, uncertainty: &Uncertainty) -> SafetyClassification {
        if uncertainty.entropy > self.threshold_entropy {
            SafetyClassification::Unsafe
        } else if uncertainty.entropy > self.threshold_entropy * 0.5 {
            SafetyClassification::Caution
        } else {
            SafetyClassification::Safe
        }
    }
}

/// FlameLang engine bindings module
pub mod flamelang_bindings {
    use super::*;

    /// Register Guardian functions with FlameLang engine
    /// This would be called by the engine to expose Guardian functionality
    pub fn register_guardian_functions<T>(engine: &mut T)
    where
        T: EngineRegistrar,
    {
        engine.register_fn("uncertainty_new", |entropy: f64, confidence: f64| {
            Uncertainty::new(entropy, confidence)
        });

        engine.register_fn("geometry_new", |x: f64, y: f64, z: f64| {
            GeometryPoint::new(x, y, z)
        });

        // More function registrations would go here
    }

    /// Trait for engine function registration
    pub trait EngineRegistrar {
        fn register_fn<F>(&mut self, name: &str, func: F)
        where
            F: 'static;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_guardian_classification() {
        let guardian = Guardian::new(0.7);
        
        let low_uncertainty = Uncertainty::new(0.2, 0.9);
        assert_eq!(guardian.classify(&low_uncertainty), SafetyClassification::Safe);

        let med_uncertainty = Uncertainty::new(0.5, 0.7);
        assert_eq!(guardian.classify(&med_uncertainty), SafetyClassification::Caution);

        let high_uncertainty = Uncertainty::new(0.9, 0.3);
        assert_eq!(guardian.classify(&high_uncertainty), SafetyClassification::Unsafe);
    }

    #[test]
    fn test_map_uncertainty_to_geometry() {
        let guardian = Guardian::new(0.7);
        let uncertainty = Uncertainty::new(0.5, 0.8);
        let point = guardian.map_uncertainty_to_geometry(&uncertainty);
        
        assert_eq!(point.x, 0.5);
        assert_eq!(point.y, 0.8);
        assert_eq!(point.z, 0.4); // 0.5 * 0.8
    }
}
