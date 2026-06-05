//! # Nucleus: State Management
//!
//! The nucleus manages state using thread-safe primitives (Mutex/Arc).

use parking_lot::RwLock;
use std::sync::Arc;

/// Thread-safe state container
pub struct Nucleus<T> {
    state: Arc<RwLock<T>>,
}

impl<T> Nucleus<T> {
    /// Create a new nucleus with initial state
    pub fn new(initial: T) -> Self {
        Self {
            state: Arc::new(RwLock::new(initial)),
        }
    }
    
    /// Read the state
    pub fn read<F, R>(&self, f: F) -> R
    where
        F: FnOnce(&T) -> R,
    {
        let guard = self.state.read();
        f(&*guard)
    }
    
    /// Write to the state
    pub fn write<F, R>(&self, f: F) -> R
    where
        F: FnOnce(&mut T) -> R,
    {
        let mut guard = self.state.write();
        f(&mut *guard)
    }
    
    /// Clone the nucleus (shares the same state)
    pub fn clone_nucleus(&self) -> Self {
        Self {
            state: Arc::clone(&self.state),
        }
    }
}

impl<T: Clone> Nucleus<T> {
    /// Get a clone of the current state
    pub fn get(&self) -> T {
        self.read(|s| s.clone())
    }
    
    /// Set the state to a new value
    pub fn set(&self, value: T) {
        self.write(|s| *s = value);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_nucleus_read_write() {
        let nucleus = Nucleus::new(42);
        
        let value = nucleus.read(|v| *v);
        assert_eq!(value, 42);
        
        nucleus.write(|v| *v = 100);
        
        let value = nucleus.read(|v| *v);
        assert_eq!(value, 100);
    }

    #[test]
    fn test_nucleus_clone() {
        let nucleus1 = Nucleus::new(42);
        let nucleus2 = nucleus1.clone_nucleus();
        
        nucleus2.write(|v| *v = 100);
        
        let value = nucleus1.read(|v| *v);
        assert_eq!(value, 100); // Same state!
    }

    #[test]
    fn test_nucleus_get_set() {
        let nucleus = Nucleus::new(String::from("hello"));
        
        assert_eq!(nucleus.get(), "hello");
        
        nucleus.set(String::from("world"));
        assert_eq!(nucleus.get(), "world");
    }
}
