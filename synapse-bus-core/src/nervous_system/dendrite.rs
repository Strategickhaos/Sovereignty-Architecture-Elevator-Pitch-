// Dendrite - The Channel (Tokio Async Pub/Sub)
// Communication pathways between organs

use tokio::sync::broadcast;
use crate::nervous_system::spike::Spike;

/// Channel capacity for spike transmission
const CHANNEL_CAPACITY: usize = 1000;

/// Dendrite - Asynchronous message channel
pub struct Dendrite {
    sender: broadcast::Sender<Spike>,
}

impl Dendrite {
    /// Create a new dendrite channel
    pub fn new() -> Self {
        let (sender, _) = broadcast::channel(CHANNEL_CAPACITY);
        Self { sender }
    }

    /// Emit a spike into the nervous system
    pub fn emit(&self, spike: Spike) -> Result<usize, broadcast::error::SendError<Spike>> {
        self.sender.send(spike)
    }

    /// Subscribe to receive spikes
    pub fn subscribe(&self) -> broadcast::Receiver<Spike> {
        self.sender.subscribe()
    }

    /// Get the number of active receivers
    pub fn receiver_count(&self) -> usize {
        self.sender.receiver_count()
    }
}

impl Default for Dendrite {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::nervous_system::spike::OrganType;
    use crate::homeostasis::gradient::PhysicsVector;

    #[tokio::test]
    async fn test_dendrite_emit_receive() {
        let dendrite = Dendrite::new();
        let mut receiver = dendrite.subscribe();

        let vector = PhysicsVector::new(0.5, 0.5);
        let spike = Spike::new(OrganType::Retina, vector, vec![1, 2, 3]);
        let spike_id = spike.id;

        dendrite.emit(spike).unwrap();

        let received = receiver.recv().await.unwrap();
        assert_eq!(received.id, spike_id);
    }

    #[test]
    fn test_dendrite_receiver_count() {
        let dendrite = Dendrite::new();
        assert_eq!(dendrite.receiver_count(), 0);

        let _receiver1 = dendrite.subscribe();
        assert_eq!(dendrite.receiver_count(), 1);

        let _receiver2 = dendrite.subscribe();
        assert_eq!(dendrite.receiver_count(), 2);
    }
}
