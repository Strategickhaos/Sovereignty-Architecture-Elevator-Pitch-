//! # Reflex: Autonomic Response
//!
//! Reflexes are automatic responses to spikes based on local policy.
//! They operate without conscious thought, like biological reflexes.

use crate::error::{Result, SynapseError};
use super::{Spike, dendrite};

/// Start the autonomic reflex system
pub async fn start_autonomic_system() -> Result<()> {
    tracing::info!("Starting autonomic reflex system");
    
    // Spawn a task to monitor spikes and respond automatically
    tokio::spawn(async move {
        if let Err(e) = reflex_loop().await {
            tracing::error!("Reflex loop error: {}", e);
        }
    });
    
    Ok(())
}

/// Stop the autonomic system
pub async fn stop_autonomic_system() -> Result<()> {
    tracing::info!("Stopping autonomic reflex system");
    Ok(())
}

/// Main reflex loop
async fn reflex_loop() -> Result<()> {
    let network = dendrite::get_network()?;
    let mut receiver = network.subscribe();
    
    loop {
        match receiver.recv().await {
            Ok(spike) => {
                // Process spike reflexively
                if let Err(e) = process_reflex(&spike).await {
                    tracing::warn!("Reflex processing error: {}", e);
                }
            }
            Err(e) => {
                tracing::error!("Receiver error: {}", e);
                break;
            }
        }
    }
    
    Ok(())
}

/// Process a spike reflexively
async fn process_reflex(spike: &Spike) -> Result<()> {
    // Check if spike should be gated
    if spike.should_gate() {
        tracing::warn!(
            "Spike {} gated - heat: {}, gravity: {}, risk: {}",
            spike.id,
            spike.vector.heat,
            spike.vector.gravity,
            spike.risk_score
        );
        return Err(SynapseError::PhysicsGate(format!(
            "Spike {} blocked by physics gate",
            spike.id
        )));
    }
    
    // Log spike passage
    tracing::debug!("Spike {} processed - origin: {:?}", spike.id, spike.origin);
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::nervous_system::{OrganType, PhysicsVector};

    #[tokio::test]
    async fn test_process_reflex_normal() {
        let spike = Spike::new(
            OrganType::System,
            PhysicsVector::default(),
            vec![],
            0.0,
        );
        
        let result = process_reflex(&spike).await;
        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_process_reflex_gated() {
        let spike = Spike::new(
            OrganType::System,
            PhysicsVector {
                heat: 0.9,
                gravity: 0.0,
            },
            vec![],
            0.0,
        );
        
        let result = process_reflex(&spike).await;
        assert!(result.is_err());
    }
}
