// Bio-Physics Entanglement Core (BPEC)
// Simulates Zipf/Menzerath laws with physics domain constraints

pub mod zipf_analyzer;
pub mod dolphin_comm;
pub mod physics_dom;
pub mod udap_bio;

pub use zipf_analyzer::ZipfAnalyzer;
pub use dolphin_comm::DolphinComm;
pub use physics_dom::PhysicsDomain;
pub use udap_bio::UdapBioHandler;

/// Physical constants for bio-acoustic simulations
pub mod physics_constants {
    /// Speed of sound in water (m/s) - for cetacean calculations
    pub const SOUND_SPEED_WATER: f64 = 1500.0;
    
    /// Speed of sound in air (m/s) - for crow calculations
    pub const SOUND_SPEED_AIR: f64 = 343.0;
    
    /// Entropy coefficient for diversity increase
    pub const ENTROPY_COEFF: f64 = 1.07;
    
    /// Uncertainty fuzz factor for Zipf ranks
    pub const UNCERTAINTY_FUZZ: f64 = 0.1;
}

/// Bio-acoustic metrics
#[derive(Debug, Clone)]
pub struct BioMetrics {
    pub zipf_slope: f64,
    pub menzerath_beta: f64,
    pub entropy: f64,
    pub frequency_spread: f64,
    pub duration_avg: f64,
}

impl BioMetrics {
    pub fn new() -> Self {
        Self {
            zipf_slope: 0.0,
            menzerath_beta: 0.0,
            entropy: 0.0,
            frequency_spread: 0.0,
            duration_avg: 0.0,
        }
    }
}
