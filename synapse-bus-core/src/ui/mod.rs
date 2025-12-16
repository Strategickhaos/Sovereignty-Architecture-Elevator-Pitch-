//! # UI: Event Horizon v0
//!
//! Visualization and user interface layer.

pub mod holodeck;
pub mod narrative;

/// Initialize UI
pub async fn initialize() -> crate::error::Result<()> {
    tracing::info!("Initializing Event Horizon UI");
    Ok(())
}
