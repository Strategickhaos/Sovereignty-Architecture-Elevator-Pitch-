use tokio::sync::broadcast;

/// Dendrite = async pub/sub channel for spikes.
/// v0 uses broadcast for simplicity; later upgrade to routing tables + backpressure.
pub struct Dendrite<T: Clone> {
    tx: broadcast::Sender<T>,
}

impl<T: Clone> Dendrite<T> {
    pub fn new(capacity: usize) -> Self {
        let (tx, _) = broadcast::channel(capacity);
        Self { tx }
    }

    pub fn emit(&self, msg: T) {
        let _ = self.tx.send(msg);
    }

    pub fn subscribe(&self) -> broadcast::Receiver<T> {
        self.tx.subscribe()
    }
}
