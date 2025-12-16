// [Q12] Garbage Collection as Energy Return
// Dissolve - Resource reclamation and entropy reduction

use std::sync::Arc;
use parking_lot::RwLock;

/// Dissolved resource - ready for reclamation
#[derive(Debug)]
pub struct DissolvedResource {
    pub id: String,
    pub size: usize,
    pub energy: f32,
}

/// The Dissolve system - garbage collection with energy accounting
pub struct Dissolve {
    reclaimed: Arc<RwLock<Vec<DissolvedResource>>>,
    total_energy_returned: Arc<RwLock<f32>>,
}

impl Dissolve {
    /// Create a new dissolve system
    pub fn new() -> Self {
        Self {
            reclaimed: Arc::new(RwLock::new(Vec::new())),
            total_energy_returned: Arc::new(RwLock::new(0.0)),
        }
    }

    /// Dissolve a resource and return its energy
    pub fn dissolve<T>(&self, resource: T, size: usize) -> f32
    where
        T: std::fmt::Debug,
    {
        let energy = (size as f32) * 0.001; // Energy = size * efficiency factor

        let dissolved = DissolvedResource {
            id: format!("{:?}", resource),
            size,
            energy,
        };

        self.reclaimed.write().push(dissolved);
        *self.total_energy_returned.write() += energy;

        energy
    }

    /// Get total energy returned to the system
    pub fn total_energy_returned(&self) -> f32 {
        *self.total_energy_returned.read()
    }

    /// Get count of reclaimed resources
    pub fn reclaimed_count(&self) -> usize {
        self.reclaimed.read().len()
    }

    /// Compact and clear reclaimed resources
    pub fn compact(&self) -> usize {
        let mut reclaimed = self.reclaimed.write();
        let count = reclaimed.len();
        reclaimed.clear();
        count
    }

    /// Calculate entropy reduction from dissolution
    pub fn entropy_reduction(&self) -> f32 {
        let energy = self.total_energy_returned();
        // Entropy reduction is proportional to energy returned
        (energy * 0.1).min(1.0)
    }
}

impl Default for Dissolve {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dissolve_resource() {
        let dissolve = Dissolve::new();
        
        let energy = dissolve.dissolve("test_resource", 1000);
        assert_eq!(energy, 1.0);
        assert_eq!(dissolve.reclaimed_count(), 1);
    }

    #[test]
    fn test_total_energy_returned() {
        let dissolve = Dissolve::new();
        
        dissolve.dissolve("resource1", 500);
        dissolve.dissolve("resource2", 500);
        
        assert_eq!(dissolve.total_energy_returned(), 1.0);
    }

    #[test]
    fn test_compact() {
        let dissolve = Dissolve::new();
        
        dissolve.dissolve("resource1", 100);
        dissolve.dissolve("resource2", 200);
        dissolve.dissolve("resource3", 300);
        
        assert_eq!(dissolve.reclaimed_count(), 3);
        
        let count = dissolve.compact();
        assert_eq!(count, 3);
        assert_eq!(dissolve.reclaimed_count(), 0);
    }

    #[test]
    fn test_entropy_reduction() {
        let dissolve = Dissolve::new();
        
        dissolve.dissolve("large_resource", 5000);
        
        let reduction = dissolve.entropy_reduction();
        assert!(reduction > 0.0);
        assert!(reduction <= 1.0);
    }
}
