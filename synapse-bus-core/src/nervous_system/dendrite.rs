//! # Dendrite: The Channel
//!
//! Dendrites are async pub/sub channels using Tokio for signal propagation.

use tokio::sync::broadcast;
use std::sync::Arc;
use parking_lot::RwLock;

use crate::error::{Result, SynapseError};
use super::Spike;

/// The dendrite network for spike propagation
pub struct DendriteNetwork {
    /// Broadcast channel for spikes
    sender: broadcast::Sender<Spike>,
}

impl DendriteNetwork {
    /// Create a new dendrite network
    pub fn new(capacity: usize) -> Self {
        let (sender, _) = broadcast::channel(capacity);
        Self { sender }
    }
    
    /// Emit a spike into the network
    pub fn emit(&self, spike: Spike) -> Result<()> {
        self.sender
            .send(spike)
            .map_err(|e| SynapseError::SpikeTransmission(e.to_string()))?;
        Ok(())
    }
    
    /// Subscribe to receive spikes
    pub fn subscribe(&self) -> broadcast::Receiver<Spike> {
        self.sender.subscribe()
    }
}

static NETWORK: once_cell::sync::OnceCell<Arc<DendriteNetwork>> = once_cell::sync::OnceCell::new();

/// Initialize the global dendrite network
pub async fn initialize_network() -> Result<()> {
    let network = Arc::new(DendriteNetwork::new(1000));
    NETWORK
        .set(network)
        .map_err(|_| SynapseError::General("Network already initialized".to_string()))?;
    Ok(())
}

/// Get the global dendrite network
pub fn get_network() -> Result<Arc<DendriteNetwork>> {
    NETWORK
        .get()
        .cloned()
        .ok_or_else(|| SynapseError::General("Network not initialized".to_string()))
}

/// Shutdown the dendrite network
pub async fn shutdown_network() -> Result<()> {
    // Network will be dropped when Arc refcount reaches 0
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::nervous_system::{OrganType, PhysicsVector};

    #[test]
    fn test_dendrite_network_creation() {
        let network = DendriteNetwork::new(10);
        let _receiver = network.subscribe();
    }

    #[tokio::test]
    async fn test_spike_emission() {
        let network = DendriteNetwork::new(10);
        let mut receiver = network.subscribe();
        
        let spike = Spike::new(
            OrganType::System,
            PhysicsVector::default(),
            vec![1, 2, 3],
            0.0,
        );
        
        network.emit(spike.clone()).unwrap();
        
        let received = receiver.recv().await.unwrap();
        assert_eq!(received.id, spike.id);
    }
}
