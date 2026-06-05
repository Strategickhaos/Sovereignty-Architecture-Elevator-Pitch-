// Dolphin Communication Simulator
// Bottlenose dolphin whistles and clicks with pod-specific signatures

use crate::avian_bio::{BioUnit, Species, frequency_ranges};

/// Dolphin communication types
#[derive(Debug, Clone, PartialEq)]
pub enum DolphinCommType {
    Whistle,        // Signature whistles (pod identification)
    Click,          // Echolocation clicks
    BurstPulse,     // Social communication
}

impl DolphinCommType {
    pub fn frequency_range(&self) -> (f64, f64) {
        match self {
            DolphinCommType::Whistle => (25000.0, 50000.0),    // Lower end of dolphin range
            DolphinCommType::Click => (50000.0, 200000.0),      // High frequency clicks
            DolphinCommType::BurstPulse => (30000.0, 80000.0),  // Mid-range
        }
    }
    
    pub fn typical_duration(&self) -> f64 {
        match self {
            DolphinCommType::Whistle => 500.0,      // 500ms whistles
            DolphinCommType::Click => 0.05,         // 50 microseconds
            DolphinCommType::BurstPulse => 100.0,   // 100ms bursts
        }
    }
}

/// Dolphin communication pattern
pub struct DolphinComm {
    pub comm_type: DolphinCommType,
    pub pod_signature: String,
    pub units: Vec<BioUnit>,
}

impl DolphinComm {
    pub fn new(comm_type: DolphinCommType, pod_signature: String) -> Self {
        Self {
            comm_type,
            pod_signature,
            units: Vec::new(),
        }
    }
    
    /// Generate dolphin communication sequence
    pub fn generate_sequence(&mut self, num_units: usize) {
        let (min_freq, max_freq) = self.comm_type.frequency_range();
        let base_duration = self.comm_type.typical_duration();
        
        self.units.clear();
        
        for rank in 1..=num_units {
            // Frequency varies within type range
            let freq_factor = (rank as f64) / (num_units as f64);
            let frequency = min_freq + (max_freq - min_freq) * freq_factor;
            
            // Apply abbreviation: high-frequency (common) units are shorter
            let duration = base_duration * (1.0 / (rank as f64).sqrt());
            
            self.units.push(BioUnit {
                frequency,
                duration,
                rank,
                species: Species::Dolphin,
            });
        }
    }
    
    /// Generate signature whistle (pod-specific)
    pub fn signature_whistle(pod_id: usize) -> DolphinComm {
        let mut comm = DolphinComm::new(
            DolphinCommType::Whistle,
            format!("Pod-{}", pod_id),
        );
        
        // Each pod has unique whistle pattern
        let num_elements = 5 + (pod_id % 5);
        comm.generate_sequence(num_elements);
        
        comm
    }
    
    /// Generate echolocation click train
    pub fn echolocation_clicks(num_clicks: usize) -> DolphinComm {
        let mut comm = DolphinComm::new(
            DolphinCommType::Click,
            "Echolocation".to_string(),
        );
        
        comm.generate_sequence(num_clicks);
        comm
    }
    
    /// Calculate click interval (for echolocation)
    pub fn click_interval(&self) -> f64 {
        if self.units.len() < 2 {
            0.0
        } else {
            // Average time between clicks
            self.units[0].duration
        }
    }
}

/// Dolphin pod dialect
pub struct DolphinPod {
    pub pod_id: usize,
    pub members: usize,
    pub dialect: Vec<DolphinComm>,
}

impl DolphinPod {
    pub fn new(pod_id: usize, members: usize) -> Self {
        let mut dialect = Vec::new();
        
        // Each pod has signature whistles
        for i in 0..members {
            dialect.push(DolphinComm::signature_whistle(pod_id * 100 + i));
        }
        
        Self {
            pod_id,
            members,
            dialect,
        }
    }
    
    /// Get all communication units from pod
    pub fn all_units(&self) -> Vec<BioUnit> {
        self.dialect
            .iter()
            .flat_map(|comm| comm.units.clone())
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_dolphin_comm_types() {
        assert_eq!(
            DolphinCommType::Whistle.frequency_range(),
            (25000.0, 50000.0)
        );
        assert_eq!(
            DolphinCommType::Click.frequency_range(),
            (50000.0, 200000.0)
        );
    }
    
    #[test]
    fn test_signature_whistle() {
        let comm = DolphinComm::signature_whistle(1);
        
        assert_eq!(comm.comm_type, DolphinCommType::Whistle);
        assert_eq!(comm.pod_signature, "Pod-1");
        assert!(!comm.units.is_empty());
    }
    
    #[test]
    fn test_echolocation_clicks() {
        let comm = DolphinComm::echolocation_clicks(10);
        
        assert_eq!(comm.comm_type, DolphinCommType::Click);
        assert_eq!(comm.units.len(), 10);
        
        // All units should be dolphin species
        for unit in &comm.units {
            assert_eq!(unit.species, Species::Dolphin);
        }
    }
    
    #[test]
    fn test_dolphin_pod() {
        let pod = DolphinPod::new(1, 3);
        
        assert_eq!(pod.pod_id, 1);
        assert_eq!(pod.members, 3);
        assert_eq!(pod.dialect.len(), 3);
        
        let units = pod.all_units();
        assert!(!units.is_empty());
    }
    
    #[test]
    fn test_frequency_ranges() {
        let mut comm = DolphinComm::new(DolphinCommType::Click, "Test".to_string());
        comm.generate_sequence(5);
        
        for unit in &comm.units {
            let (min, max) = DolphinCommType::Click.frequency_range();
            assert!(unit.frequency >= min && unit.frequency <= max);
        }
    }
}
