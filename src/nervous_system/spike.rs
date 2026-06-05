use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum OrganType {
    Retina,
    Cochlea,
    Sonar,
    Arachnid,
    Osteon,
    SynapseFire,
    Erosion,
    PhaseShift,
    Larynx,
    Doppelganger,
    Leukocyte,
    Hippocampus,
    Scalpel,
    Enzyme,
    Faraday,
    Chronos,
    IntrinsicCurl,
    Unknown(String),
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct PhysicsVector {
    pub heat: f32,
    pub gravity: f32,
    pub entropy: f32,
    pub trust: f32,
}

/// CryptoCell is a placeholder for an audited encrypted container.
/// v0 uses bytes; later replace with an AEAD envelope + provenance binding.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CryptoCell<T> {
    pub bytes: T,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Spike {
    pub id: Uuid,
    pub timestamp: DateTime<Utc>,
    pub origin: OrganType,
    pub vector: PhysicsVector,
    pub payload: CryptoCell<Vec<u8>>,
    pub risk_score: f32,
}

impl Spike {
    pub fn new(origin: OrganType, vector: PhysicsVector, payload: Vec<u8>, risk_score: f32) -> Self {
        Self {
            id: Uuid::new_v4(),
            timestamp: Utc::now(),
            origin,
            vector,
            payload: CryptoCell { bytes: payload },
            risk_score,
        }
    }
}
