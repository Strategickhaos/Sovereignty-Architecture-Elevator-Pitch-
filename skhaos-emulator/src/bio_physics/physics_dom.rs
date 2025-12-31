// Physics Domain Ontology Model (DOM)
// Laws: Entropy (swarm decay), Uncertainty (superposition), Conservation (energy balance), Relativity (spacetime coords)

use serde::{Deserialize, Serialize};

/// Physics Domain Ontology Model
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PhysicsDOM {
    /// Entropy parameter for swarm decay
    entropy_factor: f64,
    /// Uncertainty parameter for quantum branching
    uncertainty_factor: f64,
    /// Conservation enforcement flag
    enforce_conservation: bool,
}

/// Physics laws applicable to bio-patterns
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub enum PhysicsLaw {
    /// Thermodynamic entropy - disorder increases over time
    Entropy,
    /// Quantum uncertainty - superposition and measurement
    Uncertainty,
    /// Energy conservation - total energy remains constant
    Conservation,
    /// Relativistic spacetime - coordinate transformations
    Relativity,
}

impl PhysicsLaw {
    /// Parse law from string
    pub fn from_str(s: &str) -> Result<Self, String> {
        match s.to_lowercase().as_str() {
            "entropy" => Ok(PhysicsLaw::Entropy),
            "uncertainty" => Ok(PhysicsLaw::Uncertainty),
            "conservation" => Ok(PhysicsLaw::Conservation),
            "relativity" => Ok(PhysicsLaw::Relativity),
            _ => Err(format!("Unknown physics law: {}", s)),
        }
    }

    /// Get law name
    pub fn name(&self) -> &str {
        match self {
            PhysicsLaw::Entropy => "entropy",
            PhysicsLaw::Uncertainty => "uncertainty",
            PhysicsLaw::Conservation => "conservation",
            PhysicsLaw::Relativity => "relativity",
        }
    }
}

impl PhysicsDOM {
    /// Create a new Physics DOM with default parameters
    pub fn new() -> Self {
        Self {
            entropy_factor: 1.07, // 7% eternal loop from genesis
            uncertainty_factor: 0.5,
            enforce_conservation: true,
        }
    }

    /// Apply physics law to pattern
    pub fn apply_law(&self, law_name: &str, frequency_hz: f64) -> Result<Vec<u8>, String> {
        let law = PhysicsLaw::from_str(law_name)?;
        
        match law {
            PhysicsLaw::Entropy => Ok(self.generate_entropy_pattern(frequency_hz)),
            PhysicsLaw::Uncertainty => Ok(self.generate_uncertainty_pattern(frequency_hz)),
            PhysicsLaw::Conservation => Ok(self.generate_conservation_pattern(frequency_hz)),
            PhysicsLaw::Relativity => Ok(self.generate_relativity_pattern(frequency_hz)),
        }
    }

    /// Generate entropy-constrained pattern (disorder increases)
    fn generate_entropy_pattern(&self, frequency_hz: f64) -> Vec<u8> {
        let length = 64;
        let mut pattern = Vec::with_capacity(length);
        
        for i in 0..length {
            // Entropy increases over time
            let disorder = (i as f64 * self.entropy_factor) % 256.0;
            let phase = (i as f64 * frequency_hz * 0.1) % 256.0;
            let value = ((disorder + phase) / 2.0) as u8;
            pattern.push(value);
        }
        
        pattern
    }

    /// Generate uncertainty-constrained pattern (superposition)
    fn generate_uncertainty_pattern(&self, frequency_hz: f64) -> Vec<u8> {
        let length = 64;
        let mut pattern = Vec::with_capacity(length);
        
        for i in 0..length {
            // Superposition of states
            let state_a = ((i as f64 * frequency_hz * 0.1).sin() * 127.0 + 128.0) as u8;
            let state_b = ((i as f64 * frequency_hz * 0.2).cos() * 127.0 + 128.0) as u8;
            
            // Uncertain superposition
            let superposed = ((state_a as f64 * self.uncertainty_factor + 
                             state_b as f64 * (1.0 - self.uncertainty_factor)) as u8);
            pattern.push(superposed);
        }
        
        pattern
    }

    /// Generate conservation-constrained pattern (energy balance)
    fn generate_conservation_pattern(&self, frequency_hz: f64) -> Vec<u8> {
        let length = 64;
        let mut pattern = Vec::with_capacity(length);
        let mut total_energy = 0u64;
        
        for i in 0..length {
            let phase = (i as f64 * frequency_hz * 0.1) % 256.0;
            let mut value = phase as u8;
            
            // Enforce energy conservation
            if self.enforce_conservation {
                let current_energy = value as u64;
                if total_energy + current_energy > 8192 { // Energy limit
                    value = ((8192 - total_energy) % 256) as u8;
                }
                total_energy += value as u64;
            }
            
            pattern.push(value);
        }
        
        pattern
    }

    /// Generate relativity-constrained pattern (spacetime coords)
    fn generate_relativity_pattern(&self, frequency_hz: f64) -> Vec<u8> {
        let length = 64;
        let mut pattern = Vec::with_capacity(length);
        let c = 299792458.0; // Speed of light (symbolic)
        
        for i in 0..length {
            // Lorentz transformation (simplified)
            let t = i as f64;
            let v = frequency_hz / c; // Relative velocity (symbolic)
            let gamma = 1.0 / (1.0 - v * v).sqrt().max(0.1);
            
            let spacetime_coord = (t * gamma) % 256.0;
            pattern.push(spacetime_coord as u8);
        }
        
        pattern
    }

    /// Apply entropy decay to pattern (mutations increase disorder)
    pub fn apply_entropy_decay(&self, pattern: &[u8], generation: usize) -> Vec<u8> {
        pattern
            .iter()
            .enumerate()
            .map(|(i, &byte)| {
                let decay = (generation as f64 * self.entropy_factor * i as f64 / pattern.len() as f64) as u8;
                byte.wrapping_add(decay)
            })
            .collect()
    }

    /// Apply conservation law to pattern (maintain energy balance)
    pub fn apply_conservation(&self, pattern: &[u8]) -> Vec<u8> {
        if !self.enforce_conservation {
            return pattern.to_vec();
        }

        let total_energy: u64 = pattern.iter().map(|&b| b as u64).sum();
        let target_energy = total_energy;
        let mut conserved = pattern.to_vec();
        
        // Normalize to maintain total energy
        let current_energy: u64 = conserved.iter().map(|&b| b as u64).sum();
        if current_energy != target_energy && current_energy > 0 {
            let scale = target_energy as f64 / current_energy as f64;
            conserved = conserved
                .iter()
                .map(|&b| ((b as f64 * scale) as u8).min(255))
                .collect();
        }
        
        conserved
    }

    /// Apply uncertainty principle (measurement affects state)
    pub fn apply_uncertainty(&self, pattern: &[u8], measurement_strength: f64) -> Vec<u8> {
        pattern
            .iter()
            .enumerate()
            .map(|(i, &byte)| {
                // Measurement collapses superposition
                let collapse_factor = (measurement_strength * (i as f64 % 8.0) / 8.0) as u8;
                byte.wrapping_add(collapse_factor)
            })
            .collect()
    }

    /// Apply relativistic time dilation
    pub fn apply_time_dilation(&self, pattern: &[u8], velocity_factor: f64) -> Vec<u8> {
        let gamma = 1.0 / (1.0 - velocity_factor * velocity_factor).sqrt().max(0.1);
        
        // Dilate pattern in time dimension
        let dilated_length = (pattern.len() as f64 * gamma) as usize;
        let mut dilated = Vec::with_capacity(dilated_length);
        
        for i in 0..dilated_length {
            let original_index = ((i as f64 / gamma) as usize).min(pattern.len() - 1);
            dilated.push(pattern[original_index]);
        }
        
        dilated
    }

    /// Calculate system entropy (Shannon entropy)
    pub fn calculate_entropy(&self, pattern: &[u8]) -> f64 {
        let mut freq = [0u64; 256];
        for &byte in pattern {
            freq[byte as usize] += 1;
        }
        
        let total = pattern.len() as f64;
        let mut entropy = 0.0;
        
        for &count in &freq {
            if count > 0 {
                let p = count as f64 / total;
                entropy -= p * p.log2();
            }
        }
        
        entropy
    }

    /// Enforce thermodynamic constraints (entropy increases)
    pub fn enforce_thermodynamics(&self, pattern: &[u8], initial_entropy: f64) -> Vec<u8> {
        let current_entropy = self.calculate_entropy(pattern);
        
        // If entropy decreased (violates 2nd law), add noise
        if current_entropy < initial_entropy {
            let mut corrected = pattern.to_vec();
            let noise_level = ((initial_entropy - current_entropy) * 10.0) as u8;
            
            for byte in corrected.iter_mut() {
                *byte = byte.wrapping_add(noise_level);
            }
            
            corrected
        } else {
            pattern.to_vec()
        }
    }
}

impl Default for PhysicsDOM {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_physics_dom_creation() {
        let physics = PhysicsDOM::new();
        assert_eq!(physics.entropy_factor, 1.07);
        assert!(physics.enforce_conservation);
    }

    #[test]
    fn test_physics_law_parsing() {
        assert_eq!(PhysicsLaw::from_str("entropy").unwrap(), PhysicsLaw::Entropy);
        assert_eq!(PhysicsLaw::from_str("uncertainty").unwrap(), PhysicsLaw::Uncertainty);
        assert_eq!(PhysicsLaw::from_str("conservation").unwrap(), PhysicsLaw::Conservation);
        assert_eq!(PhysicsLaw::from_str("relativity").unwrap(), PhysicsLaw::Relativity);
    }

    #[test]
    fn test_entropy_pattern() {
        let physics = PhysicsDOM::new();
        let pattern = physics.generate_entropy_pattern(20.0);
        assert_eq!(pattern.len(), 64);
    }

    #[test]
    fn test_conservation_pattern() {
        let physics = PhysicsDOM::new();
        let pattern = physics.generate_conservation_pattern(20.0);
        assert_eq!(pattern.len(), 64);
    }

    #[test]
    fn test_entropy_calculation() {
        let physics = PhysicsDOM::new();
        let pattern = vec![1, 2, 3, 4, 5, 6, 7, 8];
        let entropy = physics.calculate_entropy(&pattern);
        assert!(entropy > 0.0);
    }

    #[test]
    fn test_apply_conservation() {
        let physics = PhysicsDOM::new();
        let pattern = vec![10, 20, 30, 40];
        let conserved = physics.apply_conservation(&pattern);
        assert_eq!(conserved.len(), pattern.len());
    }
}
