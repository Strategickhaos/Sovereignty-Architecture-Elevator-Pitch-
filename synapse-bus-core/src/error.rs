//! Error types for Synapse-Bus-Core

use thiserror::Error;

/// Result type alias for Synapse operations
pub type Result<T> = std::result::Result<T, SynapseError>;

/// Main error type for the Synapse-Bus system
#[derive(Error, Debug)]
pub enum SynapseError {
    /// Physics gate violation (system too hot, gradient imbalance)
    #[error("Physics gate violation: {0}")]
    PhysicsGate(String),
    
    /// Homeostasis failure (system out of balance)
    #[error("Homeostasis failure: {0}")]
    Homeostasis(String),
    
    /// Spike transmission error
    #[error("Spike transmission failed: {0}")]
    SpikeTransmission(String),
    
    /// Organ failure
    #[error("Organ {organ} failure: {reason}")]
    OrganFailure {
        /// Which organ failed
        organ: String,
        /// Why it failed
        reason: String,
    },
    
    /// Council ratification failed
    #[error("Council ratification failed: {0}")]
    RatificationFailed(String),
    
    /// Immune system alert
    #[error("Immune system alert: {0}")]
    ImmuneAlert(String),
    
    /// Cryptographic operation failed
    #[error("Cryptographic operation failed: {0}")]
    Crypto(String),
    
    /// IO error
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    /// Serialization error
    #[error("Serialization error: {0}")]
    Serialization(String),
    
    /// Configuration error
    #[error("Configuration error: {0}")]
    Config(String),
    
    /// General error
    #[error("Error: {0}")]
    General(String),
}

impl From<serde_json::Error> for SynapseError {
    fn from(err: serde_json::Error) -> Self {
        SynapseError::Serialization(err.to_string())
    }
}

impl From<serde_yaml::Error> for SynapseError {
    fn from(err: serde_yaml::Error) -> Self {
        SynapseError::Serialization(err.to_string())
    }
}
