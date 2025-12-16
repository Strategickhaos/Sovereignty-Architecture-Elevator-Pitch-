use std::sync::{Arc, Mutex};

/// Nucleus = local state (intentionally small, auditable).
#[derive(Clone, Default)]
pub struct Nucleus<T> {
    inner: Arc<Mutex<T>>,
}

impl<T> Nucleus<T> {
    pub fn new(v: T) -> Self { Self { inner: Arc::new(Mutex::new(v)) } }
    pub fn lock(&self) -> std::sync::MutexGuard<'_, T> {
        self.inner.lock().expect("nucleus poisoned")
    }
}
