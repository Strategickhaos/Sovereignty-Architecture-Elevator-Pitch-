// SkhaOS Multi-Whale Quantum Emulator Library
// Bio-mimetic quantum computing via cetacean communication patterns

pub mod multi_whale;

// Re-export main types
pub use multi_whale::{
    WhaleSpecies,
    QuantumWhaleState,
    MultiWhaleOrchestrator,
};

pub use multi_whale::humpback_theme::{
    HumpbackTheme,
    SongLevel,
    HumpbackSimulator,
};

pub use multi_whale::sperm_coda::{
    SpermCoda,
    Rhythm,
    Tempo,
    VowelFormant,
    SpermPhoneticAlphabet,
};

pub use multi_whale::killer_dialect::{
    KillerDialectCall,
    CallType,
    Ecotype,
    PodIdentity,
    KillerDialectSystem,
};

/// Library version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Library description
pub const DESCRIPTION: &str = "Multi-whale quantum emulator: Bio-mimetic quantum computing";

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        assert!(!VERSION.is_empty());
    }

    #[test]
    fn test_whale_species() {
        let humpback = WhaleSpecies::Humpback;
        let sperm = WhaleSpecies::Sperm;
        let killer = WhaleSpecies::Killer;
        
        assert_ne!(humpback, sperm);
        assert_ne!(sperm, killer);
        assert_ne!(killer, humpback);
    }
}
