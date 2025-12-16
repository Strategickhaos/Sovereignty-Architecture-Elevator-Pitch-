//! # Nodes: Personality Injection
//!
//! Each Kubernetes node gets a personality (Nova, Lyra, Athena).

use serde::{Deserialize, Serialize};

/// Node personality types
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum NodePersonality {
    Nova,
    Lyra,
    Athena,
}

/// A node with personality
pub struct PersonalityNode {
    pub id: String,
    pub personality: NodePersonality,
}
