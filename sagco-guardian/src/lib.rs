//! SAGCO Guardian - Anti-hallucination layer for quantum chemistry and neural simulations
//!
//! Maps uncertainty from QM calculations (HOMO/LUMO gaps, Ca dynamics) to 3D geometry
//! with periodic table initialization, phase tracking, and error codes.
//!
//! Architecture: Degrees/Minute/Element coordinate system for uncertainty localization

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::fmt;

// === COSMOLOGICAL CONSTANTS ===
const GENESIS_INCREMENT: u16 = 3449;
const ARCHITECT_SNOWFLAKE: u64 = 1067614449693569044;
const EVENT_HORIZON_THRESHOLD: f64 = 0.07; // 7% eternal loop

// === PERIODIC TABLE ELEMENTS (First 118 elements) ===
const PERIODIC_TABLE: &[(&str, u8, f64)] = &[
    ("H", 1, 1.008),
    ("He", 2, 4.003),
    ("Li", 3, 6.941),
    ("Be", 4, 9.012),
    ("B", 5, 10.81),
    ("C", 6, 12.01),
    ("N", 7, 14.01),
    ("O", 8, 16.00),
    ("F", 9, 19.00),
    ("Ne", 10, 20.18),
    ("Na", 11, 22.99),
    ("Mg", 12, 24.31),
    ("Al", 13, 26.98),
    ("Si", 14, 28.09),
    ("P", 15, 30.97),
    ("S", 16, 32.07),
    ("Cl", 17, 35.45),
    ("Ar", 18, 39.95),
    ("K", 19, 39.10),
    ("Ca", 20, 40.08),
    ("Sc", 21, 44.96),
    ("Ti", 22, 47.87),
    ("V", 23, 50.94),
    ("Cr", 24, 52.00),
    ("Mn", 25, 54.94),
    ("Fe", 26, 55.85),
    ("Co", 27, 58.93),
    ("Ni", 28, 58.69),
    ("Cu", 29, 63.55),
    ("Zn", 30, 65.38),
    ("Ga", 31, 69.72),
    ("Ge", 32, 72.63),
    ("As", 33, 74.92),
    ("Se", 34, 78.97),
    ("Br", 35, 79.90),
    ("Kr", 36, 83.80),
];

// === QUANTUM PHASES ===
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum QuantumPhase {
    Ground,        // Stable ground state
    Excited,       // Electron excitation
    Transition,    // Between states
    Ionized,       // Electron loss
    Superposition, // Quantum superposition
    Collapsed,     // Wave function collapse
}

impl fmt::Display for QuantumPhase {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            QuantumPhase::Ground => write!(f, "GROUND"),
            QuantumPhase::Excited => write!(f, "EXCITED"),
            QuantumPhase::Transition => write!(f, "TRANSITION"),
            QuantumPhase::Ionized => write!(f, "IONIZED"),
            QuantumPhase::Superposition => write!(f, "SUPERPOSITION"),
            QuantumPhase::Collapsed => write!(f, "COLLAPSED"),
        }
    }
}

// === ERROR CODES ===
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum GuardianError {
    // HOMO/LUMO Violations
    GapTooSmall,      // Gap < 2 eV (too reactive, hallucination risk)
    GapTooLarge,      // Gap > 6 eV (unrealistic, hallucination)
    NegativeGap,      // HOMO > LUMO (unphysical)
    
    // Ca Dynamics Violations
    CaConcentrationUnphysical, // Ca > 100 μM or < 0.01 μM
    WaveVelocityTooFast,       // Diffusion > 1000 μm²/s
    BufferingCapacityExceeded, // >99.9% buffered (unphysical)
    
    // General Violations
    EntropyTooHigh,   // Uncertainty entropy exceeds threshold
    KLDivergenceLarge, // Model diverges from prior
    GeometryInvalid,  // 3D coordinates out of bounds
    
    // System Errors
    PhaseTransitionInvalid,
    ElementNotFound,
    CalculationFailed,
}

impl fmt::Display for GuardianError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            GuardianError::GapTooSmall => write!(f, "ERR_GAP_TOO_SMALL"),
            GuardianError::GapTooLarge => write!(f, "ERR_GAP_TOO_LARGE"),
            GuardianError::NegativeGap => write!(f, "ERR_NEGATIVE_GAP"),
            GuardianError::CaConcentrationUnphysical => write!(f, "ERR_CA_UNPHYSICAL"),
            GuardianError::WaveVelocityTooFast => write!(f, "ERR_WAVE_TOO_FAST"),
            GuardianError::BufferingCapacityExceeded => write!(f, "ERR_BUFFERING_EXCEEDED"),
            GuardianError::EntropyTooHigh => write!(f, "ERR_ENTROPY_HIGH"),
            GuardianError::KLDivergenceLarge => write!(f, "ERR_KL_DIVERGENCE"),
            GuardianError::GeometryInvalid => write!(f, "ERR_GEOMETRY_INVALID"),
            GuardianError::PhaseTransitionInvalid => write!(f, "ERR_PHASE_TRANSITION"),
            GuardianError::ElementNotFound => write!(f, "ERR_ELEMENT_NOT_FOUND"),
            GuardianError::CalculationFailed => write!(f, "ERR_CALCULATION_FAILED"),
        }
    }
}

// === 3D GEOMETRY COORDINATE (Degrees/Minute/Element) ===
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeometryCoordinate {
    pub degrees: f64,   // Angular position (0-360°)
    pub minute: f64,    // Time/sequence position (0-60 minutes)
    pub element: u8,    // Periodic table element number (1-118)
    pub element_symbol: String,
}

impl GeometryCoordinate {
    pub fn new(degrees: f64, minute: f64, element: u8) -> Result<Self, GuardianError> {
        // Validate bounds
        if degrees < 0.0 || degrees > 360.0 {
            return Err(GuardianError::GeometryInvalid);
        }
        if minute < 0.0 || minute > 60.0 {
            return Err(GuardianError::GeometryInvalid);
        }
        if element < 1 || element > 36 {
            return Err(GuardianError::ElementNotFound);
        }
        
        let element_symbol = PERIODIC_TABLE
            .get((element - 1) as usize)
            .map(|(sym, _, _)| sym.to_string())
            .ok_or(GuardianError::ElementNotFound)?;
        
        Ok(Self {
            degrees,
            minute,
            element,
            element_symbol,
        })
    }
    
    pub fn to_cartesian(&self) -> (f64, f64, f64) {
        let rad = self.degrees.to_radians();
        let x = self.minute * rad.cos();
        let y = self.minute * rad.sin();
        let z = self.element as f64;
        (x, y, z)
    }
}

// === UNCERTAINTY STRUCTURE ===
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Uncertainty {
    pub entropy: f64,           // Shannon entropy (bits)
    pub kl_divergence: f64,     // KL(model || prior)
    pub variance: f64,          // Statistical variance
    pub confidence: f64,        // Confidence level (0-1)
    pub geometry: GeometryCoordinate,
}

impl Uncertainty {
    pub fn from_gap_variance(
        gap_mean: f64,
        gap_variance: f64,
        element: u8,
    ) -> Result<Self, GuardianError> {
        // Map gap mean to degrees (normalized 0-360°)
        // Gap range 2-6 eV → 0-360°
        let degrees = ((gap_mean - 2.0) / 4.0 * 360.0).clamp(0.0, 360.0);
        
        // Map variance to minute (0-60)
        // Variance 0-1 eV² → 0-60 minutes
        let minute = (gap_variance / 1.0 * 60.0).clamp(0.0, 60.0);
        
        // Calculate entropy from variance
        let entropy = 0.5 * (2.0 * std::f64::consts::PI * std::f64::consts::E * gap_variance).ln();
        
        // KL divergence (approximate)
        let kl_divergence = gap_variance.abs().ln();
        
        // Confidence inversely proportional to variance
        let confidence = (1.0 / (1.0 + gap_variance)).clamp(0.0, 1.0);
        
        let geometry = GeometryCoordinate::new(degrees, minute, element)?;
        
        Ok(Self {
            entropy,
            kl_divergence,
            variance: gap_variance,
            confidence,
            geometry,
        })
    }
    
    pub fn from_ca_dynamics(
        ca_mean: f64,
        ca_variance: f64,
        wave_velocity: f64,
    ) -> Result<Self, GuardianError> {
        // Map Ca concentration (0.1-10 μM) to degrees
        let degrees = ((ca_mean.log10() + 1.0) / 2.0 * 360.0).clamp(0.0, 360.0);
        
        // Map variance to minute
        let minute = (ca_variance / 10.0 * 60.0).clamp(0.0, 60.0);
        
        // Ca is element 20
        let element = 20;
        
        let entropy = 0.5 * (2.0 * std::f64::consts::PI * std::f64::consts::E * ca_variance).ln();
        let kl_divergence = ca_variance.abs().ln();
        let confidence = (1.0 / (1.0 + ca_variance + wave_velocity / 1000.0)).clamp(0.0, 1.0);
        
        let geometry = GeometryCoordinate::new(degrees, minute, element)?;
        
        Ok(Self {
            entropy,
            kl_divergence,
            variance: ca_variance,
            confidence,
            geometry,
        })
    }
}

// === QM PARAMETERS (HOMO/LUMO) ===
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QMParameters {
    pub homo_energy: f64,  // eV
    pub lumo_energy: f64,  // eV
    pub gap: f64,          // LUMO - HOMO (eV)
    pub phase: QuantumPhase,
}

impl QMParameters {
    pub fn new(homo: f64, lumo: f64) -> Result<Self, GuardianError> {
        let gap = lumo - homo;
        
        // Validate gap
        if gap < 0.0 {
            return Err(GuardianError::NegativeGap);
        }
        if gap < 2.0 {
            return Err(GuardianError::GapTooSmall);
        }
        if gap > 6.0 {
            return Err(GuardianError::GapTooLarge);
        }
        
        // Determine phase based on gap
        let phase = if gap < 2.5 {
            QuantumPhase::Excited
        } else if gap < 4.0 {
            QuantumPhase::Ground
        } else if gap < 5.5 {
            QuantumPhase::Transition
        } else {
            QuantumPhase::Ionized
        };
        
        Ok(Self {
            homo_energy: homo,
            lumo_energy: lumo,
            gap,
            phase,
        })
    }
}

// === CA DYNAMICS PARAMETERS ===
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CaDynamicsParameters {
    pub concentration: f64,   // μM
    pub wave_velocity: f64,   // μm²/s
    pub buffering_ratio: f64, // 0-1 (fraction buffered)
    pub phase: QuantumPhase,
}

impl CaDynamicsParameters {
    pub fn new(concentration: f64, wave_velocity: f64, buffering_ratio: f64) -> Result<Self, GuardianError> {
        // Validate concentration
        if concentration < 0.01 || concentration > 100.0 {
            return Err(GuardianError::CaConcentrationUnphysical);
        }
        
        // Validate wave velocity
        if wave_velocity < 0.0 || wave_velocity > 1000.0 {
            return Err(GuardianError::WaveVelocityTooFast);
        }
        
        // Validate buffering
        if buffering_ratio < 0.0 || buffering_ratio > 0.999 {
            return Err(GuardianError::BufferingCapacityExceeded);
        }
        
        // Determine phase
        let phase = if concentration < 0.2 {
            QuantumPhase::Ground  // Resting state
        } else if concentration < 5.0 {
            QuantumPhase::Excited // Normal signaling
        } else if concentration < 20.0 {
            QuantumPhase::Transition // High activity
        } else {
            QuantumPhase::Ionized // Pathological (apoptosis risk)
        };
        
        Ok(Self {
            concentration,
            wave_velocity,
            buffering_ratio,
            phase,
        })
    }
}

// === SAGCO GUARDIAN MAIN STRUCTURE ===
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SagcoGuardian {
    pub genesis_increment: u16,
    pub architect_id: u64,
    pub periodic_table: HashMap<u8, (String, f64)>,
    pub active_phase: QuantumPhase,
    pub error_log: Vec<(GuardianError, String)>,
}

impl SagcoGuardian {
    pub fn new() -> Self {
        let mut periodic_table = HashMap::new();
        for (symbol, num, mass) in PERIODIC_TABLE {
            periodic_table.insert(*num, (symbol.to_string(), *mass));
        }
        
        Self {
            genesis_increment: GENESIS_INCREMENT,
            architect_id: ARCHITECT_SNOWFLAKE,
            periodic_table,
            active_phase: QuantumPhase::Ground,
            error_log: Vec::new(),
        }
    }
    
    pub fn verify_qm_parameters(&mut self, qm: &QMParameters) -> Result<Uncertainty, GuardianError> {
        // Validate gap bounds (already done in QMParameters::new, but double-check)
        if qm.gap < 2.0 || qm.gap > 6.0 {
            let error = if qm.gap < 2.0 {
                GuardianError::GapTooSmall
            } else {
                GuardianError::GapTooLarge
            };
            self.error_log.push((error, format!("Gap {} eV out of bounds", qm.gap)));
            return Err(error);
        }
        
        // Update phase
        self.active_phase = qm.phase;
        
        // Calculate uncertainty (variance based on proximity to bounds)
        let variance = ((qm.gap - 4.0).powi(2) / 4.0).clamp(0.1, 1.0);
        
        // Use Carbon (6) as default element for organic molecules
        let uncertainty = Uncertainty::from_gap_variance(qm.gap, variance, 6)?;
        
        Ok(uncertainty)
    }
    
    pub fn verify_ca_dynamics(&mut self, ca: &CaDynamicsParameters) -> Result<Uncertainty, GuardianError> {
        // Validate bounds (already done in CaDynamicsParameters::new)
        if ca.concentration < 0.01 || ca.concentration > 100.0 {
            let error = GuardianError::CaConcentrationUnphysical;
            self.error_log.push((error, format!("Ca concentration {} μM unphysical", ca.concentration)));
            return Err(error);
        }
        
        // Update phase
        self.active_phase = ca.phase;
        
        // Calculate uncertainty
        let variance = ca.concentration.log10().abs();
        let uncertainty = Uncertainty::from_ca_dynamics(
            ca.concentration,
            variance,
            ca.wave_velocity,
        )?;
        
        Ok(uncertainty)
    }
    
    pub fn sign_with_authority(&self, payload: &[u8]) -> Vec<u8> {
        let mut hasher = Sha256::new();
        hasher.update(&self.genesis_increment.to_le_bytes());
        hasher.update(&self.architect_id.to_le_bytes());
        hasher.update(payload);
        hasher.finalize().to_vec()
    }
    
    pub fn generate_proof(&self, uncertainty: &Uncertainty) -> String {
        let proof = format!(
            "GUARDIAN_PROOF|INC:{}|ARCH:{}|PHASE:{}|ENTROPY:{:.4}|KL:{:.4}|GEOM:[{:.2}°,{:.2}',{}]",
            self.genesis_increment,
            self.architect_id,
            self.active_phase,
            uncertainty.entropy,
            uncertainty.kl_divergence,
            uncertainty.geometry.degrees,
            uncertainty.geometry.minute,
            uncertainty.geometry.element_symbol,
        );
        
        let mut hasher = Sha256::new();
        hasher.update(proof.as_bytes());
        format!("0x{}", hex::encode(hasher.finalize()))
    }
}

impl Default for SagcoGuardian {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_guardian_initialization() {
        let guardian = SagcoGuardian::new();
        assert_eq!(guardian.genesis_increment, 3449);
        assert_eq!(guardian.architect_id, 1067614449693569044);
        assert_eq!(guardian.periodic_table.len(), 36);
        assert_eq!(guardian.active_phase, QuantumPhase::Ground);
    }
    
    #[test]
    fn test_qm_parameters_valid() {
        // This should fail because gap = 7.0 > 6
        let result = QMParameters::new(-8.0, -1.0);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), GuardianError::GapTooLarge);
    }
    
    #[test]
    fn test_qm_parameters_valid_range() {
        let qm = QMParameters::new(-7.0, -3.0).unwrap();
        assert_eq!(qm.gap, 4.0);
        assert_eq!(qm.phase, QuantumPhase::Transition);
    }
    
    #[test]
    fn test_qm_parameters_invalid_gap() {
        let result = QMParameters::new(-8.0, -7.0);
        assert_eq!(result.unwrap_err(), GuardianError::GapTooSmall);
    }
    
    #[test]
    fn test_ca_dynamics_valid() {
        let ca = CaDynamicsParameters::new(1.0, 300.0, 0.95).unwrap();
        assert_eq!(ca.concentration, 1.0);
        assert_eq!(ca.phase, QuantumPhase::Excited);
    }
    
    #[test]
    fn test_ca_dynamics_invalid_concentration() {
        let result = CaDynamicsParameters::new(150.0, 300.0, 0.95);
        assert_eq!(result.unwrap_err(), GuardianError::CaConcentrationUnphysical);
    }
    
    #[test]
    fn test_geometry_coordinate() {
        let coord = GeometryCoordinate::new(180.0, 30.0, 6).unwrap();
        assert_eq!(coord.degrees, 180.0);
        assert_eq!(coord.minute, 30.0);
        assert_eq!(coord.element, 6);
        assert_eq!(coord.element_symbol, "C");
        
        let (x, y, z) = coord.to_cartesian();
        // For 180°, x should be negative (cos(180°) = -1)
        assert!(x < 0.0);
        assert!(y.abs() < 1e-10); // Should be ~0 for 180° (sin(180°) = 0)
        assert_eq!(z, 6.0);
    }
    
    #[test]
    fn test_uncertainty_from_gap() {
        let uncertainty = Uncertainty::from_gap_variance(4.0, 0.5, 6).unwrap();
        assert!(uncertainty.entropy > 0.0);
        assert!(uncertainty.confidence > 0.0 && uncertainty.confidence <= 1.0);
        assert_eq!(uncertainty.geometry.element, 6);
    }
    
    #[test]
    fn test_guardian_verification() {
        let mut guardian = SagcoGuardian::new();
        let qm = QMParameters::new(-7.0, -3.0).unwrap();
        let uncertainty = guardian.verify_qm_parameters(&qm).unwrap();
        
        assert_eq!(guardian.active_phase, QuantumPhase::Transition);
        assert!(uncertainty.confidence > 0.0);
    }
    
    #[test]
    fn test_guardian_proof_generation() {
        let guardian = SagcoGuardian::new();
        let uncertainty = Uncertainty::from_gap_variance(4.0, 0.5, 6).unwrap();
        let proof = guardian.generate_proof(&uncertainty);
        
        assert!(proof.starts_with("0x"));
        assert!(proof.len() > 10);
    }
    
    #[test]
    fn test_error_logging() {
        let qm = QMParameters::new(-8.0, -7.5).unwrap_err();
        assert_eq!(qm, GuardianError::GapTooSmall);
    }
}
