// Humpback Whale Theme Module
// Hierarchical song structure: units → phrases → themes
// Frequency range: 20-4000 Hz
// Cultural transmission with Zipf-distributed evolution

use std::collections::HashMap;

/// Hierarchical level in humpback song structure
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SongLevel {
    Unit,       // Basic grunt, moan, cry (1-3 sec)
    Phrase,     // String of units (10-15 sec)
    Theme,      // Repeated phrase pattern (2-4 min)
    Song,       // Full composition (6-30 min)
}

/// Humpback song theme with hierarchical structure
#[derive(Debug, Clone)]
pub struct HumpbackTheme {
    pub level: SongLevel,
    pub frequency_range: (f64, f64), // Hz min, max
    pub duration_sec: f64,
    pub units: Vec<String>,
    pub cultural_variant: String, // Population-specific variant
    pub zipf_rank: usize,         // Rank in popularity distribution
}

impl HumpbackTheme {
    /// Create a new humpback theme
    pub fn new(level: SongLevel, freq_min: f64, freq_max: f64, duration: f64) -> Self {
        Self {
            level,
            frequency_range: (freq_min, freq_max),
            duration_sec: duration,
            units: Vec::new(),
            cultural_variant: "atlantic".to_string(),
            zipf_rank: 1,
        }
    }

    /// Add a unit to the theme
    pub fn add_unit(&mut self, unit: String) {
        self.units.push(unit);
    }

    /// Validate frequency range (20-4000 Hz for humpback)
    pub fn validate_frequency(&self) -> Result<(), String> {
        if self.frequency_range.0 < 20.0 || self.frequency_range.1 > 4000.0 {
            return Err(format!(
                "Humpback frequency range {:?} exceeds [20-4000 Hz]",
                self.frequency_range
            ));
        }
        Ok(())
    }

    /// Calculate Zipf probability for cultural transmission
    pub fn zipf_probability(&self) -> f64 {
        1.0 / (self.zipf_rank as f64).powf(1.0)
    }

    /// Evolve theme via cultural transmission
    pub fn evolve_cultural(&mut self, mutation_rate: f64) -> Result<(), String> {
        if mutation_rate < 0.0 || mutation_rate > 1.0 {
            return Err("Mutation rate must be in [0.0, 1.0]".to_string());
        }

        // Simulate cultural evolution: higher Zipf rank = more mutation
        let evolution_factor = mutation_rate * self.zipf_probability();
        
        // Adjust frequency range slightly (within bounds)
        let freq_shift = evolution_factor * 50.0; // Max 50 Hz shift
        self.frequency_range.0 = (self.frequency_range.0 + freq_shift).max(20.0);
        self.frequency_range.1 = (self.frequency_range.1 + freq_shift).min(4000.0);

        Ok(())
    }

    /// Generate recursive superposition (quantum analog)
    pub fn recursive_superposition(&self, depth: usize) -> Vec<HumpbackTheme> {
        let mut themes = Vec::new();
        
        for i in 0..depth {
            let mut variant = self.clone();
            variant.zipf_rank = i + 1;
            
            // Frequency shift based on recursion depth
            let shift = (i as f64) * 100.0;
            variant.frequency_range.0 = (variant.frequency_range.0 + shift).min(3900.0);
            variant.frequency_range.1 = (variant.frequency_range.1 + shift).min(4000.0);
            
            themes.push(variant);
        }
        
        themes
    }

    /// Downsweep moan simulation (characteristic humpback pattern)
    pub fn simulate_downsweep(&self) -> Vec<f64> {
        let mut frequencies = Vec::new();
        let steps = 100;
        
        // Exponential downsweep from high to low frequency
        for i in 0..steps {
            let t = i as f64 / steps as f64;
            let freq = self.frequency_range.1 * (1.0 - t) + self.frequency_range.0 * t;
            frequencies.push(freq);
        }
        
        frequencies
    }
}

/// Humpback song simulator for full compositions
pub struct HumpbackSimulator {
    themes: Vec<HumpbackTheme>,
    population: String,
}

impl HumpbackSimulator {
    /// Create new simulator for a whale population
    pub fn new(population: String) -> Self {
        Self {
            themes: Vec::new(),
            population,
        }
    }

    /// Add theme to repertoire
    pub fn add_theme(&mut self, theme: HumpbackTheme) -> Result<(), String> {
        theme.validate_frequency()?;
        self.themes.push(theme);
        Ok(())
    }

    /// Simulate cultural transmission across population
    pub fn simulate_transmission(&mut self, generations: usize) -> Result<(), String> {
        for _ in 0..generations {
            for theme in self.themes.iter_mut() {
                theme.evolve_cultural(0.1)?; // 10% mutation rate
            }
        }
        Ok(())
    }

    /// Get most popular themes (Zipf-ranked)
    pub fn get_popular_themes(&self, count: usize) -> Vec<&HumpbackTheme> {
        let mut sorted = self.themes.iter().collect::<Vec<_>>();
        sorted.sort_by_key(|t| t.zipf_rank);
        sorted.into_iter().take(count).collect()
    }

    /// Generate statistics for population
    pub fn get_stats(&self) -> HashMap<String, f64> {
        let mut stats = HashMap::new();
        
        let avg_freq = self.themes.iter()
            .map(|t| (t.frequency_range.0 + t.frequency_range.1) / 2.0)
            .sum::<f64>() / self.themes.len() as f64;
        
        let avg_duration = self.themes.iter()
            .map(|t| t.duration_sec)
            .sum::<f64>() / self.themes.len() as f64;
        
        stats.insert("avg_frequency_hz".to_string(), avg_freq);
        stats.insert("avg_duration_sec".to_string(), avg_duration);
        stats.insert("theme_count".to_string(), self.themes.len() as f64);
        
        stats
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_humpback_theme_creation() {
        let theme = HumpbackTheme::new(SongLevel::Phrase, 100.0, 500.0, 12.0);
        assert_eq!(theme.level, SongLevel::Phrase);
        assert!(theme.validate_frequency().is_ok());
    }

    #[test]
    fn test_zipf_probability() {
        let mut theme = HumpbackTheme::new(SongLevel::Theme, 200.0, 1000.0, 180.0);
        theme.zipf_rank = 1;
        assert!((theme.zipf_probability() - 1.0).abs() < 0.001);
        
        theme.zipf_rank = 2;
        assert!((theme.zipf_probability() - 0.5).abs() < 0.001);
    }

    #[test]
    fn test_cultural_evolution() {
        let mut theme = HumpbackTheme::new(SongLevel::Unit, 100.0, 300.0, 2.0);
        let original_freq = theme.frequency_range.0;
        
        assert!(theme.evolve_cultural(0.1).is_ok());
        // Frequency should have shifted slightly
        assert!(theme.frequency_range.0 != original_freq);
    }

    #[test]
    fn test_recursive_superposition() {
        let theme = HumpbackTheme::new(SongLevel::Phrase, 200.0, 800.0, 12.0);
        let variants = theme.recursive_superposition(3);
        
        assert_eq!(variants.len(), 3);
        assert_eq!(variants[0].zipf_rank, 1);
        assert_eq!(variants[2].zipf_rank, 3);
    }

    #[test]
    fn test_downsweep_simulation() {
        let theme = HumpbackTheme::new(SongLevel::Unit, 500.0, 1000.0, 3.0);
        let sweep = theme.simulate_downsweep();
        
        assert_eq!(sweep.len(), 100);
        assert!(sweep[0] > sweep[99]); // Should decrease over time
    }

    #[test]
    fn test_simulator() {
        let mut sim = HumpbackSimulator::new("atlantic_population".to_string());
        
        let theme1 = HumpbackTheme::new(SongLevel::Theme, 200.0, 1000.0, 180.0);
        let theme2 = HumpbackTheme::new(SongLevel::Theme, 300.0, 1200.0, 200.0);
        
        assert!(sim.add_theme(theme1).is_ok());
        assert!(sim.add_theme(theme2).is_ok());
        
        assert!(sim.simulate_transmission(10).is_ok());
        
        let stats = sim.get_stats();
        assert_eq!(stats["theme_count"], 2.0);
    }
}
