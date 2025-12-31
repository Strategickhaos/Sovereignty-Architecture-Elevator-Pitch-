// Zipf's Law Analyzer for Whale/Dolphin Patterns
// Ranks units by frequency: frequent short units rank high (~1/f distribution)
// Based on Menzerath's brevity principle and cultural evolution

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Zipf analyzer for bio-communication patterns
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ZipfAnalyzer {
    /// Frequency distribution cache
    frequency_map: HashMap<Vec<u8>, usize>,
    /// Alpha parameter for Zipf distribution (typically ~1.0)
    alpha: f64,
}

impl ZipfAnalyzer {
    /// Create a new Zipf analyzer with default alpha=1.0
    pub fn new() -> Self {
        Self {
            frequency_map: HashMap::new(),
            alpha: 1.0,
        }
    }

    /// Create analyzer with custom alpha parameter
    pub fn with_alpha(alpha: f64) -> Self {
        Self {
            frequency_map: HashMap::new(),
            alpha,
        }
    }

    /// Rank units by Zipf distribution (1/f)
    /// Returns vector of (rank, unit) pairs sorted by frequency
    pub fn rank_units(&self, data: &[u8]) -> Vec<(usize, Vec<u8>)> {
        if data.is_empty() {
            return Vec::new();
        }

        // Extract units (simplified: fixed-length chunks)
        let unit_size = 4; // 4-byte units for dolphin/whale patterns
        let units: Vec<Vec<u8>> = data
            .chunks(unit_size)
            .map(|chunk| chunk.to_vec())
            .collect();

        // Count frequencies
        let mut freq_map: HashMap<Vec<u8>, usize> = HashMap::new();
        for unit in units.iter() {
            *freq_map.entry(unit.clone()).or_insert(0) += 1;
        }

        // Sort by frequency (descending)
        let mut ranked: Vec<(Vec<u8>, usize)> = freq_map.into_iter().collect();
        ranked.sort_by(|a, b| b.1.cmp(&a.1));

        // Return ranked units (rank starts at 1)
        ranked
            .into_iter()
            .enumerate()
            .map(|(idx, (unit, _freq))| (idx + 1, unit))
            .collect()
    }

    /// Calculate expected Zipf frequency for given rank
    /// f(r) = 1 / (r^alpha) where r is rank, alpha typically ~1.0
    pub fn zipf_frequency(&self, rank: usize) -> f64 {
        if rank == 0 {
            return 0.0;
        }
        1.0 / (rank as f64).powf(self.alpha)
    }

    /// Generate pattern based on Zipf distribution
    /// High-rank (frequent) patterns are shorter per Menzerath's law
    pub fn generate_pattern(&self, rank: usize, base_hz: f64) -> Vec<u8> {
        let freq = self.zipf_frequency(rank);
        let length = (8.0 / freq).ceil() as usize; // Inverse relationship: high freq = short
        
        // Generate pattern with frequency-modulated data
        let mut pattern = Vec::with_capacity(length);
        for i in 0..length {
            let phase = (i as f64 * base_hz * freq * 0.1) % 256.0;
            pattern.push(phase as u8);
        }
        
        pattern
    }

    /// Mutate pattern using Zipf law (frequent units mutate less)
    pub fn mutate_pattern(&self, pattern: &[u8], generation: usize) -> Vec<u8> {
        let ranks = self.rank_units(pattern);
        let mut mutated = pattern.to_vec();
        
        for (rank, unit) in ranks.iter() {
            // Mutation rate inversely proportional to rank (high rank = less mutation)
            let mutation_rate = 1.0 / (*rank as f64);
            let should_mutate = (generation as f64 * mutation_rate) % 1.0 > 0.5;
            
            if should_mutate {
                // Find and mutate this unit in the pattern
                for i in 0..mutated.len() {
                    if i + unit.len() <= mutated.len() {
                        let slice = &mutated[i..i + unit.len()];
                        if slice == unit.as_slice() {
                            // Apply mutation: bit flip based on generation
                            mutated[i] ^= (generation % 256) as u8;
                            break;
                        }
                    }
                }
            }
        }
        
        mutated
    }

    /// Analyze cultural evolution of units over time
    /// Returns evolution trajectory showing rank changes
    pub fn analyze_cultural_evolution(&self, generations: &[Vec<u8>]) -> Vec<HashMap<usize, Vec<u8>>> {
        generations
            .iter()
            .map(|gen| {
                let ranks = self.rank_units(gen);
                ranks.into_iter().map(|(rank, unit)| (rank, unit)).collect()
            })
            .collect()
    }

    /// Calculate Zipf coefficient for given data (how well it fits Zipf's law)
    /// Returns value close to 1.0 if distribution follows Zipf
    pub fn zipf_coefficient(&self, data: &[u8]) -> f64 {
        let ranks = self.rank_units(data);
        if ranks.is_empty() {
            return 0.0;
        }

        // Calculate frequencies
        let mut freq_map: HashMap<Vec<u8>, usize> = HashMap::new();
        let unit_size = 4;
        for chunk in data.chunks(unit_size) {
            *freq_map.entry(chunk.to_vec()).or_insert(0) += 1;
        }

        // Compare actual vs expected frequencies
        let mut sum_squared_error = 0.0;
        let mut count = 0;
        
        for (rank, unit) in ranks.iter() {
            if let Some(&actual_freq) = freq_map.get(unit) {
                let expected_freq = self.zipf_frequency(*rank);
                let normalized_actual = actual_freq as f64 / data.len() as f64;
                let error = (normalized_actual - expected_freq).powi(2);
                sum_squared_error += error;
                count += 1;
            }
        }

        if count == 0 {
            return 0.0;
        }

        // Return R-squared-like coefficient (1.0 = perfect fit)
        let mse = sum_squared_error / count as f64;
        1.0 - mse.min(1.0)
    }

    /// Rank whale song units (humpback: 20-4kHz range)
    pub fn rank_whale_units(&self, song_data: &[u8]) -> Vec<(usize, Vec<u8>, f64)> {
        let ranks = self.rank_units(song_data);
        
        ranks
            .into_iter()
            .map(|(rank, unit)| {
                let freq_hz = 20.0 + (rank as f64 * 20.0); // Map to whale range
                (rank, unit, freq_hz)
            })
            .collect()
    }

    /// Apply Menzerath's brevity principle: shorter units are more frequent
    pub fn apply_menzerath_brevity(&self, units: &[(usize, Vec<u8>)]) -> Vec<(usize, Vec<u8>, usize)> {
        units
            .iter()
            .map(|(rank, unit)| {
                let brevity_score = unit.len(); // Length as inverse brevity
                (*rank, unit.clone(), brevity_score)
            })
            .collect()
    }
}

impl Default for ZipfAnalyzer {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zipf_analyzer_creation() {
        let analyzer = ZipfAnalyzer::new();
        assert_eq!(analyzer.alpha, 1.0);
    }

    #[test]
    fn test_zipf_frequency_calculation() {
        let analyzer = ZipfAnalyzer::new();
        assert!((analyzer.zipf_frequency(1) - 1.0).abs() < 0.001);
        assert!((analyzer.zipf_frequency(2) - 0.5).abs() < 0.001);
        assert!((analyzer.zipf_frequency(4) - 0.25).abs() < 0.001);
    }

    #[test]
    fn test_rank_units() {
        let analyzer = ZipfAnalyzer::new();
        let data = vec![1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 7, 8];
        let ranks = analyzer.rank_units(&data);
        assert!(!ranks.is_empty());
        assert_eq!(ranks[0].0, 1); // First rank
    }

    #[test]
    fn test_generate_pattern() {
        let analyzer = ZipfAnalyzer::new();
        let pattern = analyzer.generate_pattern(1, 20.0);
        assert!(!pattern.is_empty());
        assert!(pattern.len() >= 8); // High rank = longer pattern
    }

    #[test]
    fn test_mutate_pattern() {
        let analyzer = ZipfAnalyzer::new();
        let original = vec![1, 2, 3, 4, 5, 6, 7, 8];
        let mutated = analyzer.mutate_pattern(&original, 1);
        assert_eq!(mutated.len(), original.len());
    }
}
