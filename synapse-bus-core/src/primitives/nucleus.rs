// Nucleus - State Management (Mutex/Arc)
// The cellular nucleus contains the state and coordinates activities

use parking_lot::RwLock;
use std::sync::Arc;
use std::collections::HashMap;

/// The Nucleus - Central state manager
#[derive(Clone)]
pub struct Nucleus<T> {
    state: Arc<RwLock<T>>,
    metadata: Arc<RwLock<HashMap<String, String>>>,
}

impl<T> Nucleus<T> {
    /// Create a new nucleus with initial state
    pub fn new(initial_state: T) -> Self {
        Self {
            state: Arc::new(RwLock::new(initial_state)),
            metadata: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Read the current state
    pub fn read<F, R>(&self, f: F) -> R
    where
        F: FnOnce(&T) -> R,
    {
        let state = self.state.read();
        f(&state)
    }

    /// Write to the state
    pub fn write<F, R>(&self, f: F) -> R
    where
        F: FnOnce(&mut T) -> R,
    {
        let mut state = self.state.write();
        f(&mut state)
    }

    /// Set metadata
    pub fn set_metadata(&self, key: String, value: String) {
        self.metadata.write().insert(key, value);
    }

    /// Get metadata
    pub fn get_metadata(&self, key: &str) -> Option<String> {
        self.metadata.read().get(key).cloned()
    }

    /// Clear all metadata
    pub fn clear_metadata(&self) {
        self.metadata.write().clear();
    }
}

/// System nucleus - global system state
#[derive(Debug, Clone)]
pub struct SystemState {
    pub temperature: f32,
    pub entropy: f32,
    pub uptime: u64,
    pub spike_count: u64,
}

impl SystemState {
    pub fn new() -> Self {
        Self {
            temperature: 37.0,
            entropy: 0.0,
            uptime: 0,
            spike_count: 0,
        }
    }

    pub fn increment_spike_count(&mut self) {
        self.spike_count += 1;
    }

    pub fn update_temperature(&mut self, temp: f32) {
        self.temperature = temp;
    }

    pub fn update_entropy(&mut self, entropy: f32) {
        self.entropy = entropy.clamp(0.0, 1.0);
    }
}

impl Default for SystemState {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_nucleus_creation() {
        let nucleus = Nucleus::new(42);
        let value = nucleus.read(|state| *state);
        assert_eq!(value, 42);
    }

    #[test]
    fn test_nucleus_write() {
        let nucleus = Nucleus::new(0);
        nucleus.write(|state| *state = 100);
        let value = nucleus.read(|state| *state);
        assert_eq!(value, 100);
    }

    #[test]
    fn test_nucleus_metadata() {
        let nucleus = Nucleus::new(());
        nucleus.set_metadata("key1".to_string(), "value1".to_string());
        
        let value = nucleus.get_metadata("key1");
        assert_eq!(value, Some("value1".to_string()));
    }

    #[test]
    fn test_system_state() {
        let mut state = SystemState::new();
        assert_eq!(state.spike_count, 0);
        
        state.increment_spike_count();
        assert_eq!(state.spike_count, 1);
        
        state.update_entropy(0.5);
        assert_eq!(state.entropy, 0.5);
    }

    #[test]
    fn test_system_state_clamping() {
        let mut state = SystemState::new();
        state.update_entropy(1.5);
        assert_eq!(state.entropy, 1.0);
        
        state.update_entropy(-0.5);
        assert_eq!(state.entropy, 0.0);
    }
}
