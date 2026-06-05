//! # Nervous System: The SynapseBus Core
//!
//! The nervous system connects all organs through signal propagation.
//! Spikes carry information, dendrites route them, and reflexes respond automatically.

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::error::{Result, SynapseError};
use crate::primitives::CryptoCell;

/// Re-export submodules
pub mod dendrite;
pub mod reflex;
pub mod spike;

pub use spike::Spike;

/// Types of organs in the system
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum OrganType {
    /// Vision organs (reconnaissance)
    Vision(VisionOrgan),
    /// Touch organs (exploitation)
    Touch(TouchOrgan),
    /// Speech organs (C2)
    Speech(SpeechOrgan),
    /// Immune organs (defense)
    Immune(ImmuneOrgan),
    /// System organ (internal)
    System,
}

/// Vision organs for reconnaissance
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum VisionOrgan {
    /// The All-Seeing Eye (f.k.a. Nmap)
    Retina,
    /// The Whisper Catcher (f.k.a. Wireshark)
    Cochlea,
    /// The Deep Sonar (f.k.a. Masscan)
    Sonar,
    /// The Web Weaver (f.k.a. Burp Suite)
    Arachnid,
}

/// Touch organs for exploitation
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum TouchOrgan {
    /// The Skeleton Key (f.k.a. Metasploit)
    Osteon,
    /// The Pressure Point (f.k.a. Hydra)
    SynapseFire,
    /// The Wall Breaker (f.k.a. SQLMap)
    Erosion,
    /// The Ghost Walker (f.k.a. ProxyChains)
    PhaseShift,
}

/// Speech organs for C2
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SpeechOrgan {
    /// The Mimic (f.k.a. SET)
    Larynx,
    /// The Echo (f.k.a. Responder)
    Doppelganger,
}

/// Immune organs for defense
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ImmuneOrgan {
    /// The White Blood Cell (f.k.a. Snort/Suricata)
    Leukocyte,
    /// The Memory Siphon (f.k.a. Volatility)
    Hippocampus,
    /// The File Carver (f.k.a. Foremost)
    Scalpel,
    /// The Code Breaker (f.k.a. John the Ripper)
    Enzyme,
    /// The Signal Jammer (f.k.a. Aircrack-ng)
    Faraday,
    /// The Time Traveler (f.k.a. Git/Autopsy)
    Chronos,
}

/// Physics vector for GSCH calculations
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct PhysicsVector {
    /// Heat level (0.0 - 1.0): System stress/entropy
    pub heat: f32,
    /// Gravity level (-10.0 to 10.0): Attraction/repulsion
    pub gravity: f32,
}

impl Default for PhysicsVector {
    fn default() -> Self {
        Self {
            heat: 0.0,
            gravity: 0.0,
        }
    }
}

/// Initialize and start the SynapseBus
pub async fn start_synapse_bus() -> Result<()> {
    tracing::info!("Starting SynapseBus");
    
    // Initialize the dendrite network
    dendrite::initialize_network().await?;
    
    // Start reflex system
    reflex::start_autonomic_system().await?;
    
    Ok(())
}

/// Stop the SynapseBus gracefully
pub async fn stop_synapse_bus() -> Result<()> {
    tracing::info!("Stopping SynapseBus");
    
    // Stop reflex system
    reflex::stop_autonomic_system().await?;
    
    // Shutdown dendrite network
    dendrite::shutdown_network().await?;
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_organ_type_serialization() {
        let organ = OrganType::Vision(VisionOrgan::Retina);
        let json = serde_json::to_string(&organ).unwrap();
        let deserialized: OrganType = serde_json::from_str(&json).unwrap();
        assert_eq!(organ, deserialized);
    }

    #[test]
    fn test_physics_vector_default() {
        let vec = PhysicsVector::default();
        assert_eq!(vec.heat, 0.0);
        assert_eq!(vec.gravity, 0.0);
    }
}
