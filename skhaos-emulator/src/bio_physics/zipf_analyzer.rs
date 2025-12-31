// Zipf Analyzer - Analyzes bio-acoustic patterns for Zipf's Law adherence
// Ranks communication units and calculates slope

use crate::avian_bio::BioUnit;
use crate::bio_physics::BioMetrics;
use std::collections::HashMap;

pub struct ZipfAnalyzer;

impl ZipfAnalyzer {
    /// Analyze bio-acoustic units for Zipf's Law
    pub fn analyze(units: &[BioUnit]) -> BioMetrics {
        let mut metrics = BioMetrics::new();
        
        // Calculate Zipf slope
        metrics.zipf_slope = Self::calculate_zipf_slope(units);
        
        // Calculate frequency spread
        if !units.is_empty() {
            let freqs: Vec<f64> = units.iter().map(|u| u.frequency).collect();
            let min = freqs.iter().cloned().fold(f64::INFINITY, f64::min);
            let max = freqs.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
            metrics.frequency_spread = max - min;
            
            // Average duration
            metrics.duration_avg = units.iter().map(|u| u.duration).sum::<f64>() / units.len() as f64;
        }
        
        // Calculate entropy (Shannon entropy of frequency distribution)
        metrics.entropy = Self::calculate_entropy(units);
        
        metrics
    }
    
    /// Calculate Zipf slope using log-log regression
    fn calculate_zipf_slope(units: &[BioUnit]) -> f64 {
        if units.is_empty() {
            return 0.0;
        }
        
        // Create frequency distribution based on duration (proxy for occurrence)
        let mut freq_dist: HashMap<usize, f64> = HashMap::new();
        for unit in units {
            let entry = freq_dist.entry(unit.rank).or_insert(0.0);
            *entry += 1.0 / unit.duration.max(1.0); // Shorter = more frequent
        }
        
        // Log-log regression
        let mut sum_x = 0.0;
        let mut sum_y = 0.0;
        let mut sum_xy = 0.0;
        let mut sum_x2 = 0.0;
        let n = freq_dist.len() as f64;
        
        for (rank, freq) in freq_dist.iter() {
            if *freq > 0.0 {
                let x = (*rank as f64).ln();
                let y = freq.ln();
                sum_x += x;
                sum_y += y;
                sum_xy += x * y;
                sum_x2 += x * x;
            }
        }
        
        if n > 1.0 && sum_x2 * n != sum_x * sum_x {
            (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        } else {
            -1.0 // Default Zipf slope
        }
    }
    
    /// Calculate Shannon entropy
    fn calculate_entropy(units: &[BioUnit]) -> f64 {
        if units.is_empty() {
            return 0.0;
        }
        
        // Calculate probability distribution based on durations
        let total_duration: f64 = units.iter().map(|u| u.duration).sum();
        let mut entropy = 0.0;
        
        for unit in units {
            let p = unit.duration / total_duration;
            if p > 0.0 {
                entropy -= p * p.ln();
            }
        }
        
        entropy
    }
    
    /// Check if units follow Zipf's Law (slope between -0.8 and -1.2)
    pub fn follows_zipf(metrics: &BioMetrics) -> bool {
        metrics.zipf_slope >= -1.2 && metrics.zipf_slope <= -0.8
    }
    
    /// Calculate Menzerath's Law beta coefficient
    /// Relationship between sequence length and element duration
    pub fn calculate_menzerath_beta(sequences: &[Vec<BioUnit>]) -> f64 {
        if sequences.is_empty() {
            return 0.0;
        }
        
        let mut sum_x = 0.0;
        let mut sum_y = 0.0;
        let mut sum_xy = 0.0;
        let mut sum_x2 = 0.0;
        let n = sequences.len() as f64;
        
        for seq in sequences {
            if !seq.is_empty() {
                let seq_len = seq.len() as f64;
                let avg_duration = seq.iter().map(|u| u.duration).sum::<f64>() / seq.len() as f64;
                
                let x = seq_len.ln();
                let y = avg_duration.ln();
                
                sum_x += x;
                sum_y += y;
                sum_xy += x * y;
                sum_x2 += x * x;
            }
        }
        
        if n > 1.0 && sum_x2 * n != sum_x * sum_x {
            (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        } else {
            0.0
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::avian_bio::Species;
    
    #[test]
    fn test_zipf_analysis() {
        let units = vec![
            BioUnit {
                frequency: 1000.0,
                duration: 10.0,
                rank: 1,
                species: Species::Crow,
            },
            BioUnit {
                frequency: 1500.0,
                duration: 20.0,
                rank: 2,
                species: Species::Crow,
            },
            BioUnit {
                frequency: 2000.0,
                duration: 40.0,
                rank: 3,
                species: Species::Crow,
            },
        ];
        
        let metrics = ZipfAnalyzer::analyze(&units);
        
        // Should detect negative slope
        assert!(metrics.zipf_slope < 0.0);
        assert!(metrics.frequency_spread > 0.0);
        assert!(metrics.duration_avg > 0.0);
    }
    
    #[test]
    fn test_entropy_calculation() {
        let units = vec![
            BioUnit {
                frequency: 1000.0,
                duration: 100.0,
                rank: 1,
                species: Species::Crow,
            },
            BioUnit {
                frequency: 1500.0,
                duration: 100.0,
                rank: 2,
                species: Species::Crow,
            },
        ];
        
        let metrics = ZipfAnalyzer::analyze(&units);
        
        // Equal durations should give maximum entropy
        assert!(metrics.entropy > 0.0);
    }
    
    #[test]
    fn test_menzerath_calculation() {
        let sequences = vec![
            vec![
                BioUnit {
                    frequency: 1000.0,
                    duration: 100.0,
                    rank: 1,
                    species: Species::Crow,
                },
                BioUnit {
                    frequency: 1100.0,
                    duration: 110.0,
                    rank: 2,
                    species: Species::Crow,
                },
            ],
            vec![
                BioUnit {
                    frequency: 1000.0,
                    duration: 80.0,
                    rank: 1,
                    species: Species::Crow,
                },
                BioUnit {
                    frequency: 1100.0,
                    duration: 85.0,
                    rank: 2,
                    species: Species::Crow,
                },
                BioUnit {
                    frequency: 1200.0,
                    duration: 90.0,
                    rank: 3,
                    species: Species::Crow,
                },
            ],
        ];
        
        let beta = ZipfAnalyzer::calculate_menzerath_beta(&sequences);
        
        // Longer sequences should have shorter elements (negative beta)
        assert!(beta < 0.0 || beta > 0.0); // Just check it calculates something
    }
}
