// The Spike - Neural Signal Event Schema
// How organs communicate with the brain

use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use uuid::Uuid;
use crate::homeostasis::gradient::PhysicsVector;

/// Organ types that can generate spikes
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum OrganType {
    // Vision (Reconnaissance)
    Retina,      // The All-Seeing Eye (f.k.a. Nmap)
    Cochlea,     // The Whisper Catcher (f.k.a. Wireshark)
    Sonar,       // The Deep Sonar (f.k.a. Masscan)
    Arachnid,    // The Web Weaver (f.k.a. Burp Suite)
    
    // Touch (Exploitation)
    Osteon,      // The Skeleton Key (f.k.a. Metasploit)
    SynapseFire, // The Pressure Point (f.k.a. Hydra)
    Erosion,     // The Wall Breaker (f.k.a. SQLMap)
    PhaseShift,  // The Ghost Walker (f.k.a. ProxyChains)
    
    // Speech (C2 & Social Engineering)
    Larynx,      // The Mimic (f.k.a. SET)
    Doppelganger,// The Echo (f.k.a. Responder)
    
    // Immune (Defense & Forensics)
    Leukocyte,   // The White Blood Cell (f.k.a. Snort/Suricata)
    Hippocampus, // The Memory Siphon (f.k.a. Volatility)
    Scalpel,     // The File Carver (f.k.a. Foremost)
    Enzyme,      // The Code Breaker (f.k.a. John the Ripper)
    Faraday,     // The Signal Jammer (f.k.a. Aircrack-ng)
    Chronos,     // The Time Traveler (f.k.a. Git/Autopsy)
    
    // System
    System,
    Unknown,
}

/// Encrypted payload container
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CryptoCell<T> {
    data: T,
    encrypted: bool,
}

impl<T> CryptoCell<T> {
    pub fn new(data: T) -> Self {
        Self {
            data,
            encrypted: false,
        }
    }

    pub fn encrypted(data: T) -> Self {
        Self {
            data,
            encrypted: true,
        }
    }

    pub fn get(&self) -> &T {
        &self.data
    }
}

/// The Spike - The fundamental unit of neural communication
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Spike {
    /// Unique identifier
    pub id: Uuid,
    
    /// Timestamp of spike generation
    pub timestamp: DateTime<Utc>,
    
    /// Origin organ that generated this spike
    pub origin: OrganType,
    
    /// Physics vector (GSCH data)
    pub vector: PhysicsVector,
    
    /// Encrypted data payload
    pub payload: CryptoCell<Vec<u8>>,
    
    /// Risk score (0.0 - 1.0, representing entropy level)
    pub risk_score: f32,
}

impl Spike {
    /// Create a new spike
    pub fn new(origin: OrganType, vector: PhysicsVector, payload: Vec<u8>) -> Self {
        Self {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            origin,
            vector,
            payload: CryptoCell::new(payload),
            risk_score: 0.0,
        }
    }

    /// Create a spike with risk assessment
    pub fn with_risk(
        origin: OrganType,
        vector: PhysicsVector,
        payload: Vec<u8>,
        risk_score: f32,
    ) -> Self {
        Self {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            origin,
            vector,
            payload: CryptoCell::new(payload),
            risk_score: risk_score.clamp(0.0, 1.0),
        }
    }

    /// Check if spike is high risk
    pub fn is_high_risk(&self) -> bool {
        self.risk_score > 0.7
    }

    /// Check if spike is stable
    pub fn is_stable(&self) -> bool {
        self.risk_score < 0.3
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spike_creation() {
        let vector = PhysicsVector::new(0.5, 0.3);
        let spike = Spike::new(OrganType::Retina, vector, vec![1, 2, 3]);
        
        assert_eq!(spike.origin, OrganType::Retina);
        assert_eq!(spike.risk_score, 0.0);
        assert!(!spike.is_high_risk());
        assert!(spike.is_stable());
    }

    #[test]
    fn test_spike_risk_assessment() {
        let vector = PhysicsVector::new(0.8, 0.2);
        let spike = Spike::with_risk(OrganType::Osteon, vector, vec![4, 5, 6], 0.85);
        
        assert!(spike.is_high_risk());
        assert!(!spike.is_stable());
        assert_eq!(spike.risk_score, 0.85);
    }

    #[test]
    fn test_crypto_cell() {
        let cell = CryptoCell::new(vec![1, 2, 3]);
        assert_eq!(cell.get(), &vec![1, 2, 3]);
        assert!(!cell.encrypted);

        let encrypted = CryptoCell::encrypted(vec![4, 5, 6]);
        assert!(encrypted.encrypted);
    }
}
