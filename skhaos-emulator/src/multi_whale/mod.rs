// Multi-Whale Cross-Species Integration Hub
// Symbolic quantum computing via cetacean communication patterns

pub mod humpback_theme;
pub mod sperm_coda;
pub mod killer_dialect;

use std::collections::HashMap;

/// Whale species enum for pattern dispatch
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum WhaleSpecies {
    Humpback,
    Sperm,
    Killer,
    Hybrid(Vec<WhaleSpecies>),
}

/// Quantum state representation for whale patterns
#[derive(Debug, Clone)]
pub struct QuantumWhaleState {
    pub species: WhaleSpecies,
    pub frequency_hz: f64,
    pub pattern_type: String,
    pub entanglement_depth: usize,
    pub cultural_transmission: f64, // 0.0-1.0 probability
    pub parameters: HashMap<String, String>,
}

impl QuantumWhaleState {
    /// Create a new quantum whale state
    pub fn new(species: WhaleSpecies, frequency_hz: f64, pattern_type: String) -> Self {
        Self {
            species,
            frequency_hz,
            pattern_type,
            entanglement_depth: 0,
            cultural_transmission: 0.0,
            parameters: HashMap::new(),
        }
    }

    /// Entangle with another whale state (superposition)
    pub fn entangle(&mut self, other: &QuantumWhaleState) -> Result<(), String> {
        self.entanglement_depth += 1;
        
        // Cross-species entanglement creates hybrid
        if self.species != other.species {
            let species_vec = vec![self.species.clone(), other.species.clone()];
            self.species = WhaleSpecies::Hybrid(species_vec);
        }
        
        // Frequency averaging for hybrid resonance
        self.frequency_hz = (self.frequency_hz + other.frequency_hz) / 2.0;
        
        // Cultural transmission probability increases with entanglement
        self.cultural_transmission = (self.cultural_transmission + other.cultural_transmission) / 2.0;
        self.cultural_transmission = self.cultural_transmission.min(1.0);
        
        Ok(())
    }

    /// Evolve pattern via cultural transmission (Zipf-distributed)
    pub fn evolve_cultural(&mut self, zipf_rank: usize) -> Result<(), String> {
        if zipf_rank == 0 {
            return Err("Zipf rank must be > 0".to_string());
        }
        
        // Zipf law: frequency ∝ 1/rank^s where s ≈ 1.0
        let zipf_probability = 1.0 / (zipf_rank as f64).powf(1.0);
        self.cultural_transmission = zipf_probability;
        
        Ok(())
    }

    /// Validate frequency range for species
    pub fn validate_frequency(&self) -> Result<(), String> {
        match &self.species {
            WhaleSpecies::Humpback => {
                if self.frequency_hz >= 20.0 && self.frequency_hz <= 4000.0 {
                    Ok(())
                } else {
                    Err(format!("Humpback frequency {} Hz out of range [20-4000 Hz]", self.frequency_hz))
                }
            }
            WhaleSpecies::Sperm => {
                if self.frequency_hz >= 1.0 && self.frequency_hz <= 30000.0 {
                    Ok(())
                } else {
                    Err(format!("Sperm frequency {} Hz out of range [1-30000 Hz]", self.frequency_hz))
                }
            }
            WhaleSpecies::Killer => {
                if self.frequency_hz >= 1.0 && self.frequency_hz <= 25000.0 {
                    Ok(())
                } else {
                    Err(format!("Killer frequency {} Hz out of range [1-25000 Hz]", self.frequency_hz))
                }
            }
            WhaleSpecies::Hybrid(_) => {
                // Hybrid can span full range
                if self.frequency_hz >= 1.0 && self.frequency_hz <= 40000.0 {
                    Ok(())
                } else {
                    Err(format!("Hybrid frequency {} Hz out of range [1-40000 Hz]", self.frequency_hz))
                }
            }
        }
    }
}

/// Multi-whale pattern orchestrator
pub struct MultiWhaleOrchestrator {
    states: Vec<QuantumWhaleState>,
    swarm_size: usize,
}

impl MultiWhaleOrchestrator {
    /// Create new orchestrator with swarm size
    pub fn new(swarm_size: usize) -> Self {
        Self {
            states: Vec::with_capacity(swarm_size),
            swarm_size,
        }
    }

    /// Add whale state to swarm
    pub fn add_state(&mut self, state: QuantumWhaleState) -> Result<(), String> {
        state.validate_frequency()?;
        
        if self.states.len() >= self.swarm_size {
            return Err("Swarm size limit reached".to_string());
        }
        
        self.states.push(state);
        Ok(())
    }

    /// Entangle all states in swarm (recursive superposition)
    pub fn entangle_swarm(&mut self) -> Result<(), String> {
        if self.states.len() < 2 {
            return Err("Need at least 2 states to entangle".to_string());
        }

        // Create pairwise entanglements
        for i in 0..self.states.len() - 1 {
            let other_state = self.states[i + 1].clone();
            self.states[i].entangle(&other_state)?;
        }

        Ok(())
    }

    /// Evolve swarm via cultural transmission
    pub fn evolve_swarm(&mut self) -> Result<(), String> {
        for (rank, state) in self.states.iter_mut().enumerate() {
            state.evolve_cultural(rank + 1)?; // Zipf rank starts at 1
        }
        Ok(())
    }

    /// Get swarm statistics
    pub fn get_stats(&self) -> HashMap<String, f64> {
        let mut stats = HashMap::new();
        
        let avg_freq = self.states.iter()
            .map(|s| s.frequency_hz)
            .sum::<f64>() / self.states.len() as f64;
        
        let avg_entanglement = self.states.iter()
            .map(|s| s.entanglement_depth as f64)
            .sum::<f64>() / self.states.len() as f64;
        
        let avg_transmission = self.states.iter()
            .map(|s| s.cultural_transmission)
            .sum::<f64>() / self.states.len() as f64;
        
        stats.insert("avg_frequency_hz".to_string(), avg_freq);
        stats.insert("avg_entanglement_depth".to_string(), avg_entanglement);
        stats.insert("avg_cultural_transmission".to_string(), avg_transmission);
        stats.insert("swarm_size".to_string(), self.states.len() as f64);
        
        stats
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_humpback_frequency_validation() {
        let state = QuantumWhaleState::new(
            WhaleSpecies::Humpback,
            500.0,
            "phrase".to_string(),
        );
        assert!(state.validate_frequency().is_ok());
    }

    #[test]
    fn test_sperm_frequency_validation() {
        let state = QuantumWhaleState::new(
            WhaleSpecies::Sperm,
            5000.0,
            "coda".to_string(),
        );
        assert!(state.validate_frequency().is_ok());
    }

    #[test]
    fn test_entanglement() {
        let mut state1 = QuantumWhaleState::new(
            WhaleSpecies::Humpback,
            500.0,
            "phrase".to_string(),
        );
        let state2 = QuantumWhaleState::new(
            WhaleSpecies::Sperm,
            5000.0,
            "coda".to_string(),
        );
        
        assert!(state1.entangle(&state2).is_ok());
        assert!(matches!(state1.species, WhaleSpecies::Hybrid(_)));
        assert_eq!(state1.entanglement_depth, 1);
    }

    #[test]
    fn test_zipf_evolution() {
        let mut state = QuantumWhaleState::new(
            WhaleSpecies::Humpback,
            500.0,
            "phrase".to_string(),
        );
        
        assert!(state.evolve_cultural(1).is_ok());
        assert!((state.cultural_transmission - 1.0).abs() < 0.001);
        
        assert!(state.evolve_cultural(2).is_ok());
        assert!((state.cultural_transmission - 0.5).abs() < 0.001);
    }

    #[test]
    fn test_orchestrator() {
        let mut orch = MultiWhaleOrchestrator::new(3);
        
        let state1 = QuantumWhaleState::new(WhaleSpecies::Humpback, 500.0, "phrase".to_string());
        let state2 = QuantumWhaleState::new(WhaleSpecies::Sperm, 5000.0, "coda".to_string());
        let state3 = QuantumWhaleState::new(WhaleSpecies::Killer, 10000.0, "whistle".to_string());
        
        assert!(orch.add_state(state1).is_ok());
        assert!(orch.add_state(state2).is_ok());
        assert!(orch.add_state(state3).is_ok());
        
        assert!(orch.entangle_swarm().is_ok());
        assert!(orch.evolve_swarm().is_ok());
        
        let stats = orch.get_stats();
        assert_eq!(stats["swarm_size"], 3.0);
    }
}
