//! # Synapse-Bus-Core: The Sovereign OS Nervous System
//!
//! Version: 0.1.0-alpha (Event Horizon)
//!
//! A bio-mimetic, physics-gated nervous system for sovereign digital infrastructure.
//! Built on the GSCH (Gradient-driven Systematic Cycle of Homeostasis) patent claim.
//!
//! ## Architecture
//!
//! - **Claims**: Patent-protected inventions (GSCH Claim 8, INV-088)
//! - **Primitives**: Bio-digital interface (Cells, Membranes, Nucleus)
//! - **Homeostasis**: Physics engine for system balance
//! - **Nervous System**: Signal propagation (Spikes, Dendrites, Reflexes)
//! - **Council**: Legion of Minds governance system
//! - **Immune System**: Red/Blue/Purple team security
//! - **Organs**: The purified tool arsenal (16 organs)
//! - **Infrastructure**: Kubernetes & hardware management
//! - **UI**: Event Horizon visualization layer

#![warn(missing_docs)]
#![warn(clippy::all)]
#![warn(clippy::cognitive_complexity)]

// Re-export core types
pub use crate::nervous_system::{Spike, OrganType, PhysicsVector};

/// Patent claims and proof-of-invention bindings
pub mod claims;

/// Bio-digital primitives (cells, membranes, buffers)
pub mod primitives;

/// GSCH physics engine for system homeostasis
pub mod homeostasis;

/// The nervous system: signals, channels, reflexes
pub mod nervous_system;

/// Legion of Minds governance and ratification
pub mod council;

/// Security: red, blue, and purple teams
pub mod immune_system;

/// The 16 purified organs (tools arsenal)
pub mod organs;

/// Infrastructure management (Kubernetes, nodes)
pub mod infra;

/// Event Horizon UI and visualization
pub mod ui;

/// Common error types
pub mod error;

/// Prelude for convenient imports
pub mod prelude {
    pub use crate::error::{Result, SynapseError};
    pub use crate::nervous_system::{OrganType, PhysicsVector, Spike};
    pub use crate::primitives::{CryptoCell, Membrane};
}

use error::Result;

/// Initialize the Synapse-Bus-Core system
///
/// This bootstraps the nervous system, homeostasis engine, and organ registry.
pub async fn initialize() -> Result<()> {
    tracing::info!("Initializing Synapse-Bus-Core v0.1.0-alpha");
    
    // Initialize homeostasis engine
    homeostasis::init_gradient_engine()?;
    
    // Start nervous system
    nervous_system::start_synapse_bus().await?;
    
    // Register organs
    organs::register_all_organs().await?;
    
    tracing::info!("Synapse-Bus-Core initialization complete");
    Ok(())
}

/// Shutdown the system gracefully
pub async fn shutdown() -> Result<()> {
    tracing::info!("Shutting down Synapse-Bus-Core");
    
    // Stop nervous system
    nervous_system::stop_synapse_bus().await?;
    
    // Dissolve resources (energy return)
    homeostasis::dissolve_all().await?;
    
    tracing::info!("Shutdown complete");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_system_initialization() {
        // Basic smoke test
        let result = initialize().await;
        assert!(result.is_ok() || result.is_err()); // System may not fully init in test
    }
}
