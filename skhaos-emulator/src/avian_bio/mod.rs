// Avian-Cetacean Hybrid Bioacoustics Simulator - Core Module
// INVENTION_075: Simulating Zipf's Law across Dolphin, Orca, and Crow patterns

pub mod zipf_sim;
pub mod crow_pattern;
pub mod hybrid_evolve;
pub mod udap_avian;

pub use zipf_sim::ZipfSimulator;
pub use crow_pattern::CrowPattern;
pub use hybrid_evolve::HybridEvolver;
pub use udap_avian::UdapAvianHandler;

/// Frequency ranges for different species (in Hz)
pub mod frequency_ranges {
    /// Crow vocalizations: 0.5-2 kHz (500-2000 Hz)
    pub const CROW_MIN: f64 = 500.0;
    pub const CROW_MAX: f64 = 2000.0;
    pub const CROW_DOMINANT: f64 = 1000.0;
    
    /// Orca (Killer Whale) calls: 1-25 kHz
    pub const ORCA_MIN: f64 = 1000.0;
    pub const ORCA_MAX: f64 = 25000.0;
    pub const ORCA_DOMINANT: f64 = 13000.0;
    
    /// Dolphin (Bottlenose) whistles and clicks: 25-200 kHz
    pub const DOLPHIN_MIN: f64 = 25000.0;
    pub const DOLPHIN_MAX: f64 = 200000.0;
    pub const DOLPHIN_DOMINANT: f64 = 50000.0;
    
    /// Hybrid ranges for evolved patterns
    pub const HYBRID_MIN: f64 = CROW_MIN;
    pub const HYBRID_MAX: f64 = DOLPHIN_MAX;
}

/// Zipf law constants
pub mod zipf_constants {
    /// Target Zipf slope for all species
    pub const TARGET_SLOPE: f64 = -1.0;
    
    /// Measured slopes from real data
    pub const DOLPHIN_SLOPE: f64 = -0.94;
    pub const ORCA_SLOPE: f64 = -0.95;
    pub const CROW_SLOPE: f64 = -1.0;
    
    /// Menzerath law coefficients
    pub const DOLPHIN_MENZERATH_BETA: f64 = -0.0001;
    pub const ORCA_MENZERATH_BETA: f64 = -0.043;
    pub const CROW_MENZERATH_BETA_MIN: f64 = -0.5;
    pub const CROW_MENZERATH_BETA_MAX: f64 = -0.2;
}

/// Bio-acoustic unit representing a vocalization element
#[derive(Debug, Clone)]
pub struct BioUnit {
    pub frequency: f64,    // Hz
    pub duration: f64,     // milliseconds
    pub rank: usize,       // Zipf rank
    pub species: Species,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Species {
    Crow,
    Orca,
    Dolphin,
    Hybrid(Box<Species>, Box<Species>),
}

impl Species {
    pub fn name(&self) -> String {
        match self {
            Species::Crow => "Crow".to_string(),
            Species::Orca => "Orca".to_string(),
            Species::Dolphin => "Dolphin".to_string(),
            Species::Hybrid(s1, s2) => format!("{}-{} Hybrid", s1.name(), s2.name()),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_frequency_ranges() {
        assert!(frequency_ranges::CROW_MIN < frequency_ranges::CROW_MAX);
        assert!(frequency_ranges::ORCA_MIN < frequency_ranges::ORCA_MAX);
        assert!(frequency_ranges::DOLPHIN_MIN < frequency_ranges::DOLPHIN_MAX);
    }
    
    #[test]
    fn test_species_names() {
        assert_eq!(Species::Crow.name(), "Crow");
        assert_eq!(Species::Orca.name(), "Orca");
        assert_eq!(Species::Dolphin.name(), "Dolphin");
        
        let hybrid = Species::Hybrid(
            Box::new(Species::Crow),
            Box::new(Species::Dolphin)
        );
        assert_eq!(hybrid.name(), "Crow-Dolphin Hybrid");
    }
}
