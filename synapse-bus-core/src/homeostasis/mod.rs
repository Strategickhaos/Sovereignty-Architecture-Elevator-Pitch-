//! # Homeostasis: GSCH Physics Engine
//!
//! The physics engine maintains system balance using gradient-driven homeostasis.

pub mod gradient;
pub mod feedback;
pub mod dissolve;

use crate::error::{Result, SynapseError};

/// Initialize the gradient engine
pub fn init_gradient_engine() -> Result<()> {
    tracing::info!("Initializing GSCH gradient engine");
    gradient::initialize()?;
    Ok(())
}

/// Dissolve all resources (energy return during shutdown)
pub async fn dissolve_all() -> Result<()> {
    tracing::info!("Dissolving resources - returning energy to system");
    dissolve::dissolve_resources().await?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_init_gradient_engine() {
        let result = init_gradient_engine();
        assert!(result.is_ok());
    }
}
