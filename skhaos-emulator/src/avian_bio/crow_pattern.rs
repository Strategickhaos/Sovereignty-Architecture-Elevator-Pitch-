// Crow Communication Pattern Simulator
// Models territorial caws, social hierarchies, and Menzerath's Law adherence

use crate::avian_bio::{BioUnit, Species, frequency_ranges};

/// Crow communication pattern with hierarchical structure
#[derive(Debug, Clone)]
pub struct CrowPattern {
    pub caw_type: CawType,
    pub hierarchy_level: usize,
    pub menzerath_beta: f64,
    pub units: Vec<BioUnit>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum CawType {
    Territorial,     // Defending territory
    Begging,         // Food requests
    Assembly,        // Gathering calls
    Alarm,           // Danger warnings
    Contact,         // Flock coordination
}

impl CawType {
    /// Get base frequency for caw type
    pub fn base_frequency(&self) -> f64 {
        match self {
            CawType::Territorial => 1000.0,  // Dominant frequency
            CawType::Begging => 1500.0,      // Higher pitch
            CawType::Assembly => 800.0,       // Lower, carrying call
            CawType::Alarm => 1800.0,        // High, sharp
            CawType::Contact => 1200.0,      // Mid-range
        }
    }
    
    /// Get typical duration for caw type (milliseconds)
    pub fn typical_duration(&self) -> f64 {
        match self {
            CawType::Territorial => 200.0,   // Strong, sustained
            CawType::Begging => 150.0,       // Quick, repeated
            CawType::Assembly => 300.0,      // Long, carrying
            CawType::Alarm => 100.0,         // Sharp, urgent
            CawType::Contact => 180.0,       // Moderate
        }
    }
}

impl CrowPattern {
    /// Create a new crow pattern
    pub fn new(caw_type: CawType, hierarchy_level: usize) -> Self {
        // Menzerath adherence stronger in young (low hierarchy) and females
        // Beta ranges from -0.5 (strong) to -0.2 (weak)
        let menzerath_beta = -0.5 + (hierarchy_level as f64 * 0.1).min(0.3);
        
        Self {
            caw_type,
            hierarchy_level,
            menzerath_beta,
            units: Vec::new(),
        }
    }
    
    /// Generate caw sequence with Menzerath's Law
    /// Long sequences have shorter elements
    pub fn generate_sequence(&mut self, sequence_length: usize) {
        let base_freq = self.caw_type.base_frequency();
        let base_duration = self.caw_type.typical_duration();
        
        self.units.clear();
        
        for rank in 1..=sequence_length {
            // Apply Menzerath's Law: element duration decreases with sequence length
            // duration = base_duration * (sequence_length ^ beta)
            let menzerath_factor = (sequence_length as f64).powf(self.menzerath_beta);
            let duration = base_duration * menzerath_factor;
            
            // Add frequency variation within crow range
            let freq_variation = ((rank as f64 / sequence_length as f64) - 0.5) * 500.0;
            let frequency = (base_freq + freq_variation)
                .max(frequency_ranges::CROW_MIN)
                .min(frequency_ranges::CROW_MAX);
            
            self.units.push(BioUnit {
                frequency,
                duration,
                rank,
                species: Species::Crow,
            });
        }
    }
    
    /// Generate territorial caw hierarchy
    pub fn territorial_hierarchy(levels: usize) -> Vec<CrowPattern> {
        (1..=levels)
            .map(|level| {
                let mut pattern = CrowPattern::new(CawType::Territorial, level);
                pattern.generate_sequence(10 - level); // Higher hierarchy = shorter sequences
                pattern
            })
            .collect()
    }
    
    /// Calculate average element duration for this pattern
    pub fn average_duration(&self) -> f64 {
        if self.units.is_empty() {
            0.0
        } else {
            self.units.iter().map(|u| u.duration).sum::<f64>() / self.units.len() as f64
        }
    }
    
    /// Calculate frequency spread (Hz)
    pub fn frequency_spread(&self) -> f64 {
        if self.units.is_empty() {
            0.0
        } else {
            let freqs: Vec<f64> = self.units.iter().map(|u| u.frequency).collect();
            let min = freqs.iter().cloned().fold(f64::INFINITY, f64::min);
            let max = freqs.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            max - min
        }
    }
}

/// Crow learning and social transmission simulator
pub struct CrowLearning {
    pub young_patterns: Vec<CrowPattern>,
    pub adult_patterns: Vec<CrowPattern>,
}

impl CrowLearning {
    pub fn new() -> Self {
        Self {
            young_patterns: Vec::new(),
            adult_patterns: Vec::new(),
        }
    }
    
    /// Simulate young crows learning from adults
    /// Young show stronger Menzerath adherence
    pub fn simulate_learning(&mut self, num_young: usize, num_adult: usize) {
        // Young crows (hierarchy 1-2) have stronger Menzerath
        for i in 0..num_young {
            let mut pattern = CrowPattern::new(CawType::Contact, 1);
            pattern.generate_sequence(8);
            self.young_patterns.push(pattern);
        }
        
        // Adult crows (hierarchy 3-5) have weaker Menzerath
        for i in 0..num_adult {
            let mut pattern = CrowPattern::new(CawType::Contact, 3 + (i % 3));
            pattern.generate_sequence(5);
            self.adult_patterns.push(pattern);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_caw_type_frequencies() {
        assert_eq!(CawType::Territorial.base_frequency(), 1000.0);
        assert!(CawType::Alarm.base_frequency() > CawType::Assembly.base_frequency());
    }
    
    #[test]
    fn test_crow_pattern_generation() {
        let mut pattern = CrowPattern::new(CawType::Territorial, 1);
        pattern.generate_sequence(5);
        
        assert_eq!(pattern.units.len(), 5);
        assert_eq!(pattern.units[0].species, Species::Crow);
    }
    
    #[test]
    fn test_menzerath_law() {
        let mut short_pattern = CrowPattern::new(CawType::Contact, 1);
        short_pattern.generate_sequence(3);
        
        let mut long_pattern = CrowPattern::new(CawType::Contact, 1);
        long_pattern.generate_sequence(10);
        
        // Longer sequences should have shorter average element duration
        assert!(long_pattern.average_duration() < short_pattern.average_duration());
    }
    
    #[test]
    fn test_hierarchy_levels() {
        let hierarchy = CrowPattern::territorial_hierarchy(5);
        
        assert_eq!(hierarchy.len(), 5);
        
        // Higher hierarchy should have stronger Menzerath (more negative beta)
        assert!(hierarchy[0].menzerath_beta < hierarchy[4].menzerath_beta);
    }
    
    #[test]
    fn test_young_vs_adult_menzerath() {
        let young = CrowPattern::new(CawType::Contact, 1);
        let adult = CrowPattern::new(CawType::Contact, 4);
        
        // Young should have stronger (more negative) Menzerath beta
        assert!(young.menzerath_beta < adult.menzerath_beta);
    }
}
