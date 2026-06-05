// SkhaOS Emulator - Library Entry Point
// Bio-Physics Entanglement Compiler (BPEC) - INVENTION_074

pub mod bio_physics;

// Re-export main types
pub use bio_physics::{
    BPECCompiler,
    ZipfAnalyzer,
    DolphinComm,
    PhysicsDOM,
    UDAPBioParser,
    BioURI,
};

/// SkhaOS Emulator version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Genesis constants from Strategickhaos architecture
pub mod genesis {
    pub const GENESIS_TIMESTAMP: u64 = 1674852049000; // 2023-01-27 21:00:49.000 UTC
    pub const GENESIS_WORKER: u8 = 0;
    pub const GENESIS_PROCESS: u8 = 1;
    pub const GENESIS_INCREMENT: u16 = 3449;
    pub const ARCHITECT_SNOWFLAKE: u64 = 1067614449693569044;
    pub const EVENT_HORIZON_THRESHOLD: f64 = 0.07; // 7% eternal loop
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_library_version() {
        assert!(!VERSION.is_empty());
    }

    #[test]
    fn test_genesis_constants() {
        assert_eq!(genesis::GENESIS_INCREMENT, 3449);
        assert_eq!(genesis::ARCHITECT_SNOWFLAKE, 1067614449693569044);
    }
}
