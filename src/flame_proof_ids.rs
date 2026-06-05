//! Stable Kernel ABI for FlameLang Proofs
//!
//! This module defines stable identifiers for all proofs enforced by SAGCO.
//! These IDs form part of the kernel ABI and must not change between versions.

#[repr(u16)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProofId {
    // TIER 1 — KERNEL PROOFS (0x0100-0x01FF)
    FixedPointConvergence = 0x0101,
    GroundingCompleteness = 0x0102,
    GenomeClassification = 0x0103,
    CodonBijection = 0x0104,

    // TIER 2 — PHYSICS PROOFS (0x0200-0x02FF)
    AngleBoundedness = 0x0201,
    LipschitzContinuity = 0x0202,
    WaveConservation = 0x0203,
    FrequencyPositivity = 0x0204,

    // TIER 3 — TRANSFORM PROOFS (0x0300-0x03FF)
    HebrewRootValidity = 0x0301,
    GematriaBounds = 0x0302,
    DnaEncoding = 0x0303,
    RubikGodNumber = 0x0304,

    // TIER 4 — SYSTEM PROOFS (0x0400-0x04FF)
    IrAcyclicity = 0x0401,
    TypeSafety = 0x0402,
    ResourceBounds = 0x0403,
    Determinism = 0x0404,
}

impl ProofId {
    /// Get the tier (category) of this proof
    pub const fn tier(&self) -> u8 {
        (*self as u16 >> 8) as u8
    }

    /// Get the human-readable name of this proof
    pub const fn name(&self) -> &'static str {
        match self {
            // Tier 1
            ProofId::FixedPointConvergence => "fixed_point_convergence",
            ProofId::GroundingCompleteness => "grounding_completeness",
            ProofId::GenomeClassification => "genome_classification",
            ProofId::CodonBijection => "codon_bijection",
            
            // Tier 2
            ProofId::AngleBoundedness => "angle_boundedness",
            ProofId::LipschitzContinuity => "lipschitz_continuity",
            ProofId::WaveConservation => "wave_conservation",
            ProofId::FrequencyPositivity => "frequency_positivity",
            
            // Tier 3
            ProofId::HebrewRootValidity => "hebrew_root_validity",
            ProofId::GematriaBounds => "gematria_bounds",
            ProofId::DnaEncoding => "dna_encoding",
            ProofId::RubikGodNumber => "rubik_god_number",
            
            // Tier 4
            ProofId::IrAcyclicity => "ir_acyclicity",
            ProofId::TypeSafety => "type_safety",
            ProofId::ResourceBounds => "resource_bounds",
            ProofId::Determinism => "determinism",
        }
    }

    /// Get the tier name for this proof
    pub const fn tier_name(&self) -> &'static str {
        match self.tier() {
            1 => "KERNEL",
            2 => "PHYSICS",
            3 => "TRANSFORM",
            4 => "SYSTEM",
            _ => "UNKNOWN",
        }
    }
}

/// All proofs grouped by tier
pub const PROOF_TIERS: &[&[ProofId]] = &[
    // Tier 1 - Kernel
    &[
        ProofId::FixedPointConvergence,
        ProofId::GroundingCompleteness,
        ProofId::GenomeClassification,
        ProofId::CodonBijection,
    ],
    // Tier 2 - Physics
    &[
        ProofId::AngleBoundedness,
        ProofId::LipschitzContinuity,
        ProofId::WaveConservation,
        ProofId::FrequencyPositivity,
    ],
    // Tier 3 - Transform
    &[
        ProofId::HebrewRootValidity,
        ProofId::GematriaBounds,
        ProofId::DnaEncoding,
        ProofId::RubikGodNumber,
    ],
    // Tier 4 - System
    &[
        ProofId::IrAcyclicity,
        ProofId::TypeSafety,
        ProofId::ResourceBounds,
        ProofId::Determinism,
    ],
];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_proof_tiers() {
        assert_eq!(ProofId::FixedPointConvergence.tier(), 1);
        assert_eq!(ProofId::AngleBoundedness.tier(), 2);
        assert_eq!(ProofId::HebrewRootValidity.tier(), 3);
        assert_eq!(ProofId::IrAcyclicity.tier(), 4);
    }

    #[test]
    fn test_proof_names() {
        assert_eq!(ProofId::FixedPointConvergence.name(), "fixed_point_convergence");
        assert_eq!(ProofId::CodonBijection.name(), "codon_bijection");
    }

    #[test]
    fn test_tier_names() {
        assert_eq!(ProofId::FixedPointConvergence.tier_name(), "KERNEL");
        assert_eq!(ProofId::AngleBoundedness.tier_name(), "PHYSICS");
        assert_eq!(ProofId::HebrewRootValidity.tier_name(), "TRANSFORM");
        assert_eq!(ProofId::IrAcyclicity.tier_name(), "SYSTEM");
    }

    #[test]
    fn test_all_tiers_populated() {
        assert_eq!(PROOF_TIERS.len(), 4);
        assert_eq!(PROOF_TIERS[0].len(), 4); // Kernel
        assert_eq!(PROOF_TIERS[1].len(), 4); // Physics
        assert_eq!(PROOF_TIERS[2].len(), 4); // Transform
        assert_eq!(PROOF_TIERS[3].len(), 4); // System
    }
}
