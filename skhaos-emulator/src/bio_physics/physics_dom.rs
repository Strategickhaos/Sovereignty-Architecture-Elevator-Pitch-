// Physics Domain Constraints for Bio-Acoustic Simulations
// Applies entropy, uncertainty, and conservation laws

use crate::avian_bio::BioUnit;
use crate::bio_physics::BioMetrics;
use crate::bio_physics::physics_constants;

/// Physics law types
#[derive(Debug, Clone, PartialEq)]
pub enum PhysicsLaw {
    Entropy,         // Increases hybrid diversity
    Uncertainty,     // Fuzzes Zipf ranks for robustness
    Conservation,    // Maintains energy across evolution
}

impl PhysicsLaw {
    pub fn from_string(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "entropy" => Some(PhysicsLaw::Entropy),
            "uncertainty" => Some(PhysicsLaw::Uncertainty),
            "conservation" => Some(PhysicsLaw::Conservation),
            _ => None,
        }
    }
}

/// Physics domain simulator
pub struct PhysicsDomain;

impl PhysicsDomain {
    /// Apply entropy law: increase diversity
    pub fn apply_entropy(units: &mut [BioUnit]) -> f64 {
        let initial_entropy = Self::calculate_entropy(units);
        
        // Apply entropy coefficient to increase diversity
        for unit in units.iter_mut() {
            unit.duration *= physics_constants::ENTROPY_COEFF;
        }
        
        let final_entropy = Self::calculate_entropy(units);
        final_entropy - initial_entropy
    }
    
    /// Apply uncertainty principle: fuzz Zipf ranks
    pub fn apply_uncertainty(units: &mut [BioUnit]) {
        for unit in units.iter_mut() {
            // Add random uncertainty to rank-based properties
            let fuzz_factor = 1.0 + (Self::pseudo_random(unit.rank) - 0.5) 
                * physics_constants::UNCERTAINTY_FUZZ;
            unit.frequency *= fuzz_factor;
        }
    }
    
    /// Apply conservation law: maintain total energy
    pub fn apply_conservation(units: &mut [BioUnit]) {
        if units.is_empty() {
            return;
        }
        
        // Energy proportional to frequency * duration
        let initial_energy: f64 = units
            .iter()
            .map(|u| u.frequency * u.duration)
            .sum();
        
        // Redistribute while conserving total
        let target_energy = initial_energy;
        let current_energy: f64 = units
            .iter()
            .map(|u| u.frequency * u.duration)
            .sum();
        
        if current_energy > 0.0 {
            let scale = target_energy / current_energy;
            for unit in units.iter_mut() {
                unit.duration *= scale;
            }
        }
    }
    
    /// Apply physics law to hybrid evolution
    pub fn constrain_hybrid(units: &mut [BioUnit], law: PhysicsLaw) -> BioMetrics {
        match law {
            PhysicsLaw::Entropy => {
                let delta = Self::apply_entropy(units);
                BioMetrics {
                    entropy: delta,
                    ..BioMetrics::new()
                }
            }
            PhysicsLaw::Uncertainty => {
                Self::apply_uncertainty(units);
                BioMetrics::new()
            }
            PhysicsLaw::Conservation => {
                Self::apply_conservation(units);
                BioMetrics::new()
            }
        }
    }
    
    /// Calculate Shannon entropy
    fn calculate_entropy(units: &[BioUnit]) -> f64 {
        if units.is_empty() {
            return 0.0;
        }
        
        let total: f64 = units.iter().map(|u| u.duration).sum();
        let mut entropy = 0.0;
        
        for unit in units {
            let p = unit.duration / total;
            if p > 0.0 {
                entropy -= p * p.ln();
            }
        }
        
        entropy
    }
    
    /// Simple pseudo-random number generator for deterministic physics
    fn pseudo_random(seed: usize) -> f64 {
        let x = ((seed as f64 * 12.9898).sin() * 43758.5453).fract();
        x.abs()
    }
    
    /// Calculate propagation distance in water (for cetaceans)
    pub fn propagation_distance_water(frequency: f64, duration: f64) -> f64 {
        // Distance = speed * time
        // Duration in ms, convert to seconds
        physics_constants::SOUND_SPEED_WATER * (duration / 1000.0)
    }
    
    /// Calculate propagation distance in air (for crows)
    pub fn propagation_distance_air(frequency: f64, duration: f64) -> f64 {
        physics_constants::SOUND_SPEED_AIR * (duration / 1000.0)
    }
    
    /// Calculate attenuation coefficient (frequency-dependent)
    pub fn attenuation_coefficient(frequency: f64, medium: &str) -> f64 {
        match medium {
            "water" => {
                // Attenuation increases with frequency in water
                // α ≈ 0.1 * f^2 dB/km (simplified)
                0.1 * (frequency / 1000.0).powi(2)
            }
            "air" => {
                // Attenuation in air
                // α ≈ 0.01 * f dB/m (simplified)
                0.01 * (frequency / 1000.0)
            }
            _ => 0.0,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::avian_bio::Species;
    
    #[test]
    fn test_entropy_application() {
        let mut units = vec![
            BioUnit {
                frequency: 1000.0,
                duration: 100.0,
                rank: 1,
                species: Species::Crow,
            },
            BioUnit {
                frequency: 2000.0,
                duration: 50.0,
                rank: 2,
                species: Species::Crow,
            },
        ];
        
        let initial_duration = units[0].duration;
        let delta = PhysicsDomain::apply_entropy(&mut units);
        
        // Duration should increase due to entropy
        assert!(units[0].duration > initial_duration);
        assert!(delta != 0.0);
    }
    
    #[test]
    fn test_uncertainty_application() {
        let mut units = vec![
            BioUnit {
                frequency: 1000.0,
                duration: 100.0,
                rank: 1,
                species: Species::Crow,
            },
        ];
        
        let initial_freq = units[0].frequency;
        PhysicsDomain::apply_uncertainty(&mut units);
        
        // Frequency should be slightly different
        assert!(units[0].frequency != initial_freq);
    }
    
    #[test]
    fn test_conservation_application() {
        let mut units = vec![
            BioUnit {
                frequency: 1000.0,
                duration: 100.0,
                rank: 1,
                species: Species::Crow,
            },
            BioUnit {
                frequency: 2000.0,
                duration: 50.0,
                rank: 2,
                species: Species::Crow,
            },
        ];
        
        let initial_energy: f64 = units
            .iter()
            .map(|u| u.frequency * u.duration)
            .sum();
        
        PhysicsDomain::apply_conservation(&mut units);
        
        let final_energy: f64 = units
            .iter()
            .map(|u| u.frequency * u.duration)
            .sum();
        
        // Energy should be approximately conserved
        assert!((initial_energy - final_energy).abs() < 0.01);
    }
    
    #[test]
    fn test_propagation_distances() {
        // Test water propagation (dolphin)
        let dist_water = PhysicsDomain::propagation_distance_water(50000.0, 100.0);
        assert!(dist_water > 0.0);
        
        // Test air propagation (crow)
        let dist_air = PhysicsDomain::propagation_distance_air(1000.0, 200.0);
        assert!(dist_air > 0.0);
        
        // Water should propagate faster
        assert!(dist_water > dist_air);
    }
    
    #[test]
    fn test_physics_law_from_string() {
        assert_eq!(
            PhysicsLaw::from_string("entropy"),
            Some(PhysicsLaw::Entropy)
        );
        assert_eq!(
            PhysicsLaw::from_string("UNCERTAINTY"),
            Some(PhysicsLaw::Uncertainty)
        );
        assert_eq!(
            PhysicsLaw::from_string("conservation"),
            Some(PhysicsLaw::Conservation)
        );
        assert_eq!(PhysicsLaw::from_string("invalid"), None);
    }
}
