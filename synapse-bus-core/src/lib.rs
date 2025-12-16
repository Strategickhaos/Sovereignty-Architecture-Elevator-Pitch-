// Synapse-Bus-Core Library Root
// Bio-Mimetic Sovereign OS with GSCH Physics Engine

pub mod claims;
pub mod primitives;
pub mod homeostasis;
pub mod nervous_system;
pub mod council;
pub mod immune_system;
pub mod organs;
pub mod infra;
pub mod ui;

// Re-export core types
pub use nervous_system::spike::Spike;
pub use primitives::membrane::Membrane;
pub use homeostasis::gradient::PhysicsVector;

/// Version information
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const VERSION_TAG: &str = "0.1.0-alpha (Event Horizon)";

/// The Axiom of Sovereignty
/// "All code is local until proven necessary to be remote"
pub mod axioms {
    /// Q1: The Axiom of Sovereignty
    pub const SOVEREIGNTY: &str = "All 3rd party dependencies live in quarantine until purified";
    
    /// Q2: True First Ledger
    pub const TRUE_FIRST: &str = "Patent timestamping ensures proof of invention";
    
    /// Q3: Bio-Digital Interface
    pub const BIO_MIMETIC: &str = "Systems mirror biological processes for resilience";
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        assert_eq!(VERSION, "0.1.0-alpha");
    }

    #[test]
    fn test_axioms() {
        assert!(!axioms::SOVEREIGNTY.is_empty());
        assert!(!axioms::TRUE_FIRST.is_empty());
        assert!(!axioms::BIO_MIMETIC.is_empty());
    }
}
