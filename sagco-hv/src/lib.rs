//! SAGCO-HYDRA Type-1 Hypervisor
//! 
//! A distributed organism hypervisor with no single point of failure.
//! DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD23-ISO102-MESH5
//!
//! Core Features:
//! - KVM-based virtualization
//! - CRDT distributed state
//! - FlameLang DSL integration
//! - TPM attestation
//! - 5-node neural mesh

use tracing::info;

pub mod kvm;
pub mod vm;
pub mod config;
pub mod mesh;
pub mod crdt_state;
pub mod flamelang;

/// Initialize the hypervisor logging system
pub fn init_logging() {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::from_default_env()
                .add_directive(tracing::Level::INFO.into())
        )
        .with_target(false)
        .with_thread_ids(true)
        .init();
    
    info!("SAGCO-HYDRA hypervisor logging initialized");
    info!("DNA: SAGCO-ATG-FLM2-MSMC2-P16-CMD23-ISO102-MESH5");
}

/// Hypervisor version information
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const DNA_STRAND: &str = "SAGCO-ATG-FLM2-MSMC2-P16-CMD23-ISO102-MESH5";

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        assert!(!VERSION.is_empty());
    }
}
