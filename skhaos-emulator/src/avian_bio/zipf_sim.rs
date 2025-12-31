// Zipf's Law Simulator for Bio-acoustic Patterns
// Generates frequency distributions following 1/rank pattern with slope ~-1.0

use std::collections::HashMap;

/// Zipf distribution simulator for bio-acoustic communication patterns
pub struct ZipfSimulator {
    slope: f64,
    vocabulary_size: usize,
}

impl ZipfSimulator {
    /// Create a new Zipf simulator with target slope
    pub fn new(slope: f64, vocabulary_size: usize) -> Self {
        Self {
            slope,
            vocabulary_size,
        }
    }
    
    /// Create simulator with default target slope of -1.0
    pub fn with_default_slope(vocabulary_size: usize) -> Self {
        Self::new(-1.0, vocabulary_size)
    }
    
    /// Generate Zipf distribution for given vocabulary size
    /// Returns HashMap of rank -> frequency
    pub fn generate_distribution(&self) -> HashMap<usize, f64> {
        let mut distribution = HashMap::new();
        let mut total = 0.0;
        
        // Calculate normalization constant (Zeta function approximation)
        for rank in 1..=self.vocabulary_size {
            total += (rank as f64).powf(self.slope);
        }
        
        // Generate normalized frequencies
        for rank in 1..=self.vocabulary_size {
            let frequency = (rank as f64).powf(self.slope) / total;
            distribution.insert(rank, frequency);
        }
        
        distribution
    }
    
    /// Calculate actual slope from distribution using log-log regression
    pub fn calculate_slope(&self, distribution: &HashMap<usize, f64>) -> f64 {
        let mut sum_x = 0.0;
        let mut sum_y = 0.0;
        let mut sum_xy = 0.0;
        let mut sum_x2 = 0.0;
        let n = distribution.len() as f64;
        
        for (rank, freq) in distribution.iter() {
            if *freq > 0.0 {
                let x = (*rank as f64).ln();
                let y = freq.ln();
                sum_x += x;
                sum_y += y;
                sum_xy += x * y;
                sum_x2 += x * x;
            }
        }
        
        // Linear regression slope: (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x^2)
        (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    }
    
    /// Generate synthetic bio-acoustic units with Zipf-ranked frequencies
    pub fn generate_units(&self, base_freq: f64, freq_range: (f64, f64)) -> Vec<crate::avian_bio::BioUnit> {
        use crate::avian_bio::{BioUnit, Species};
        
        let distribution = self.generate_distribution();
        let mut units = Vec::new();
        
        for rank in 1..=self.vocabulary_size {
            let frequency = distribution.get(&rank).unwrap_or(&0.0);
            
            // Map rank to frequency within species range
            let normalized_rank = (rank as f64) / (self.vocabulary_size as f64);
            let unit_freq = freq_range.0 + (freq_range.1 - freq_range.0) * (1.0 - normalized_rank);
            
            // Abbreviation effect: high-frequency units have shorter duration
            // Duration inversely proportional to frequency occurrence
            let duration = if *frequency > 0.0 {
                (1.0 / frequency).min(1000.0) // Cap at 1000ms
            } else {
                1000.0
            };
            
            units.push(BioUnit {
                frequency: unit_freq,
                duration,
                rank,
                species: Species::Dolphin, // Default, will be set by caller
            });
        }
        
        units
    }
    
    /// Simulate dolphin click patterns with Zipf distribution
    pub fn simulate_dolphin(&self) -> Vec<crate::avian_bio::BioUnit> {
        use crate::avian_bio::frequency_ranges;
        let mut units = self.generate_units(
            frequency_ranges::DOLPHIN_DOMINANT,
            (frequency_ranges::DOLPHIN_MIN, frequency_ranges::DOLPHIN_MAX)
        );
        
        // Set species for all units
        for unit in &mut units {
            unit.species = crate::avian_bio::Species::Dolphin;
        }
        
        units
    }
    
    /// Simulate orca call sequences with Zipf distribution
    pub fn simulate_orca(&self) -> Vec<crate::avian_bio::BioUnit> {
        use crate::avian_bio::frequency_ranges;
        let mut units = self.generate_units(
            frequency_ranges::ORCA_DOMINANT,
            (frequency_ranges::ORCA_MIN, frequency_ranges::ORCA_MAX)
        );
        
        for unit in &mut units {
            unit.species = crate::avian_bio::Species::Orca;
        }
        
        units
    }
    
    /// Simulate crow caw patterns with Zipf distribution
    pub fn simulate_crow(&self) -> Vec<crate::avian_bio::BioUnit> {
        use crate::avian_bio::frequency_ranges;
        let mut units = self.generate_units(
            frequency_ranges::CROW_DOMINANT,
            (frequency_ranges::CROW_MIN, frequency_ranges::CROW_MAX)
        );
        
        for unit in &mut units {
            unit.species = crate::avian_bio::Species::Crow;
        }
        
        units
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_zipf_distribution_generation() {
        let sim = ZipfSimulator::with_default_slope(100);
        let dist = sim.generate_distribution();
        
        assert_eq!(dist.len(), 100);
        
        // Rank 1 should have highest frequency
        let freq1 = dist.get(&1).unwrap();
        let freq10 = dist.get(&10).unwrap();
        assert!(freq1 > freq10);
    }
    
    #[test]
    fn test_slope_calculation() {
        let sim = ZipfSimulator::new(-1.0, 100);
        let dist = sim.generate_distribution();
        let calculated_slope = sim.calculate_slope(&dist);
        
        // Should be close to -1.0
        assert!((calculated_slope - (-1.0)).abs() < 0.1);
    }
    
    #[test]
    fn test_dolphin_simulation() {
        let sim = ZipfSimulator::with_default_slope(50);
        let units = sim.simulate_dolphin();
        
        assert_eq!(units.len(), 50);
        assert_eq!(units[0].species, crate::avian_bio::Species::Dolphin);
        
        // Check frequency range
        for unit in &units {
            assert!(unit.frequency >= crate::avian_bio::frequency_ranges::DOLPHIN_MIN);
            assert!(unit.frequency <= crate::avian_bio::frequency_ranges::DOLPHIN_MAX);
        }
    }
    
    #[test]
    fn test_abbreviation_effect() {
        let sim = ZipfSimulator::with_default_slope(10);
        let units = sim.simulate_crow();
        
        // High-rank (frequent) units should have shorter durations
        // Low-rank (rare) units should have longer durations
        assert!(units[0].duration < units[units.len() - 1].duration);
    }
}
