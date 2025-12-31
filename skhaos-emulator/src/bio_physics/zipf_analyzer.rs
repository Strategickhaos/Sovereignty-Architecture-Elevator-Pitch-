// Zipf's Law Analyzer for Whale/Dolphin Communication Patterns
// Implements 1/f rank-frequency distribution (Zipf-Mandelbrot law)
// Applies Menzerath's brevity principle: frequent units are shorter

use std::collections::HashMap;

/// Zipf distribution analyzer for bio-communication units
pub struct ZipfAnalyzer {
    pub units: Vec<ZipfUnit>,
    pub distribution_exponent: f64, // s in Zipf's law: f(r) = 1/(r^s)
}

#[derive(Debug, Clone)]
pub struct ZipfUnit {
    pub rank: u32,              // Position in frequency ranking (1 = most frequent)
    pub frequency_hz: f64,      // Base frequency in Hz
    pub pattern: String,        // Phonetic pattern (e.g., "ahh-OOO-ahh")
    pub duration_ms: f64,       // Duration in milliseconds
    pub occurrence_count: u32,  // How many times observed
    pub species: BioSpecies,
    pub brevity_score: f64,     // Menzerath: high freq = short duration
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum BioSpecies {
    HumpbackWhale,
    SpermWhale,
    KillerWhale,
    Dolphin,
}

impl ZipfAnalyzer {
    /// Create new Zipf analyzer with standard exponent (s ≈ 1.0)
    pub fn new() -> Self {
        Self {
            units: Vec::new(),
            distribution_exponent: 1.0,
        }
    }

    /// Create with custom exponent for different distribution shapes
    pub fn with_exponent(exponent: f64) -> Self {
        Self {
            units: Vec::new(),
            distribution_exponent: exponent,
        }
    }

    /// Add a bio-communication unit to analyze
    pub fn add_unit(&mut self, unit: ZipfUnit) {
        self.units.push(unit);
    }

    /// Calculate Zipf frequency for a given rank: f(r) = C / (r^s)
    /// where C is normalization constant, r is rank, s is exponent
    pub fn zipf_frequency(&self, rank: u32, normalization: f64) -> f64 {
        if rank == 0 {
            return 0.0;
        }
        normalization / (rank as f64).powf(self.distribution_exponent)
    }

    /// Rank units by occurrence count (Zipf ranking)
    pub fn rank_units(&mut self) {
        // Sort by occurrence count (descending)
        self.units.sort_by(|a, b| b.occurrence_count.cmp(&a.occurrence_count));
        
        // Assign ranks
        for (idx, unit) in self.units.iter_mut().enumerate() {
            unit.rank = (idx + 1) as u32;
            // Calculate brevity score: high rank (low number) = high brevity
            unit.brevity_score = 1.0 / unit.rank as f64;
        }
    }

    /// Calculate Menzerath brevity principle: frequent units are shorter
    pub fn verify_menzerath(&self) -> MenzerathAnalysis {
        if self.units.is_empty() {
            return MenzerathAnalysis {
                correlation: 0.0,
                high_freq_avg_duration: 0.0,
                low_freq_avg_duration: 0.0,
                validates_principle: false,
            };
        }

        let top_quartile = self.units.len() / 4;
        let high_freq_units = &self.units[0..top_quartile.max(1)];
        let low_freq_units = &self.units[top_quartile.max(1)..];

        let high_avg = high_freq_units.iter()
            .map(|u| u.duration_ms)
            .sum::<f64>() / high_freq_units.len() as f64;
        
        let low_avg = if low_freq_units.is_empty() {
            high_avg
        } else {
            low_freq_units.iter()
                .map(|u| u.duration_ms)
                .sum::<f64>() / low_freq_units.len() as f64
        };

        // Menzerath principle: high frequency should have shorter duration
        let validates = high_avg < low_avg;
        let correlation = if validates { 
            1.0 - (high_avg / low_avg) 
        } else { 
            0.0 
        };

        MenzerathAnalysis {
            correlation,
            high_freq_avg_duration: high_avg,
            low_freq_avg_duration: low_avg,
            validates_principle: validates,
        }
    }

    /// Get top N most frequent units (highest Zipf rank)
    pub fn top_units(&self, n: usize) -> Vec<&ZipfUnit> {
        self.units.iter().take(n).collect()
    }

    /// Calculate distribution statistics
    pub fn distribution_stats(&self) -> DistributionStats {
        if self.units.is_empty() {
            return DistributionStats::default();
        }

        let total_occurrences: u32 = self.units.iter()
            .map(|u| u.occurrence_count)
            .sum();

        let avg_frequency: f64 = self.units.iter()
            .map(|u| u.frequency_hz)
            .sum::<f64>() / self.units.len() as f64;

        let species_distribution = self.count_by_species();

        DistributionStats {
            total_units: self.units.len(),
            total_occurrences,
            avg_frequency_hz: avg_frequency,
            exponent: self.distribution_exponent,
            species_distribution,
        }
    }

    /// Count units by species
    fn count_by_species(&self) -> HashMap<String, usize> {
        let mut counts = HashMap::new();
        for unit in &self.units {
            let species_name = format!("{:?}", unit.species);
            *counts.entry(species_name).or_insert(0) += 1;
        }
        counts
    }

    /// Convert Zipf unit to quantum priority (rank 1 = highest priority)
    pub fn to_quantum_priority(&self, rank: u32) -> f64 {
        if rank == 0 {
            return 0.0;
        }
        // Priority inversely proportional to rank
        1.0 / rank as f64
    }
}

#[derive(Debug, Clone)]
pub struct MenzerathAnalysis {
    pub correlation: f64,              // 0.0-1.0, how well it fits
    pub high_freq_avg_duration: f64,   // Average duration of frequent units
    pub low_freq_avg_duration: f64,    // Average duration of rare units
    pub validates_principle: bool,      // True if high_freq < low_freq
}

#[derive(Debug, Clone, Default)]
pub struct DistributionStats {
    pub total_units: usize,
    pub total_occurrences: u32,
    pub avg_frequency_hz: f64,
    pub exponent: f64,
    pub species_distribution: HashMap<String, usize>,
}

impl Default for ZipfAnalyzer {
    fn default() -> Self {
        Self::new()
    }
}

/// Helper function to generate sample humpback whale song units
pub fn sample_humpback_units() -> Vec<ZipfUnit> {
    vec![
        ZipfUnit {
            rank: 0,
            frequency_hz: 20.0,
            pattern: "ahh-OOO".to_string(),
            duration_ms: 500.0,
            occurrence_count: 150,
            species: BioSpecies::HumpbackWhale,
            brevity_score: 0.0,
        },
        ZipfUnit {
            rank: 0,
            frequency_hz: 200.0,
            pattern: "WOO-ahh-WOO".to_string(),
            duration_ms: 800.0,
            occurrence_count: 75,
            species: BioSpecies::HumpbackWhale,
            brevity_score: 0.0,
        },
        ZipfUnit {
            rank: 0,
            frequency_hz: 500.0,
            pattern: "chirp-MOAN-chirp".to_string(),
            duration_ms: 1200.0,
            occurrence_count: 38,
            species: BioSpecies::HumpbackWhale,
            brevity_score: 0.0,
        },
        ZipfUnit {
            rank: 0,
            frequency_hz: 1000.0,
            pattern: "GROAN-whistle-GROAN-whistle".to_string(),
            duration_ms: 2000.0,
            occurrence_count: 20,
            species: BioSpecies::HumpbackWhale,
            brevity_score: 0.0,
        },
    ]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zipf_frequency_calculation() {
        let analyzer = ZipfAnalyzer::new();
        let freq = analyzer.zipf_frequency(1, 100.0);
        assert_eq!(freq, 100.0); // rank 1: 100/1^1 = 100
        
        let freq2 = analyzer.zipf_frequency(2, 100.0);
        assert_eq!(freq2, 50.0); // rank 2: 100/2^1 = 50
    }

    #[test]
    fn test_unit_ranking() {
        let mut analyzer = ZipfAnalyzer::new();
        let units = sample_humpback_units();
        
        for unit in units {
            analyzer.add_unit(unit);
        }
        
        analyzer.rank_units();
        
        assert_eq!(analyzer.units[0].rank, 1);
        assert_eq!(analyzer.units[0].occurrence_count, 150);
        assert!(analyzer.units[0].brevity_score > 0.0);
    }

    #[test]
    fn test_menzerath_principle() {
        let mut analyzer = ZipfAnalyzer::new();
        let units = sample_humpback_units();
        
        for unit in units {
            analyzer.add_unit(unit);
        }
        
        analyzer.rank_units();
        let menzerath = analyzer.verify_menzerath();
        
        // High frequency units should be shorter
        assert!(menzerath.validates_principle);
        assert!(menzerath.high_freq_avg_duration < menzerath.low_freq_avg_duration);
    }

    #[test]
    fn test_quantum_priority() {
        let analyzer = ZipfAnalyzer::new();
        let priority1 = analyzer.to_quantum_priority(1);
        let priority2 = analyzer.to_quantum_priority(2);
        
        assert_eq!(priority1, 1.0);
        assert_eq!(priority2, 0.5);
        assert!(priority1 > priority2);
    }
}
