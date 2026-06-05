//! # CryptoCell: Encrypted Data Container
//!
//! Wraps data in a cryptographic envelope using BLAKE3 for hashing.

use serde::{Deserialize, Serialize};
use blake3;

/// An encrypted cell containing data
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CryptoCell<T> {
    /// The actual data (in a real implementation, this would be encrypted)
    data: T,
    
    /// BLAKE3 hash of the data for integrity
    #[serde(skip)]
    hash: Option<blake3::Hash>,
}

impl<T> CryptoCell<T>
where
    T: Serialize,
{
    /// Create a new CryptoCell
    pub fn new(data: T) -> Self {
        // In a full implementation, encrypt the data here
        let hash = Self::compute_hash(&data);
        Self {
            data,
            hash: Some(hash),
        }
    }
    
    /// Compute BLAKE3 hash of the data
    fn compute_hash(data: &T) -> blake3::Hash {
        let bytes = serde_json::to_vec(data).unwrap_or_default();
        blake3::hash(&bytes)
    }
    
    /// Get a reference to the data
    pub fn get(&self) -> &T {
        &self.data
    }
    
    /// Verify the integrity of the data
    pub fn verify(&self) -> bool {
        match &self.hash {
            Some(stored_hash) => {
                let computed_hash = Self::compute_hash(&self.data);
                stored_hash == &computed_hash
            }
            None => false,
        }
    }
}

impl<T> CryptoCell<T>
where
    T: Serialize + Clone,
{
    /// Extract the data (consuming the cell)
    pub fn extract(self) -> T {
        self.data
    }
    
    /// Clone the data
    pub fn clone_data(&self) -> T {
        self.data.clone()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_crypto_cell_creation() {
        let cell = CryptoCell::new(vec![1, 2, 3, 4]);
        assert_eq!(cell.get(), &vec![1, 2, 3, 4]);
    }

    #[test]
    fn test_crypto_cell_verify() {
        let cell = CryptoCell::new(String::from("test data"));
        assert!(cell.verify());
    }

    #[test]
    fn test_crypto_cell_extract() {
        let cell = CryptoCell::new(42);
        let value = cell.extract();
        assert_eq!(value, 42);
    }
}
