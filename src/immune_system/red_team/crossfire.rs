/// Crossfire harness stub (SAFE).
/// Focus: fuzz schemas + parsers + gates (no exploitation tooling).
pub fn generate_vectors(count: usize) -> Vec<Vec<u8>> {
    (0..count).map(|i| format!("VECTOR::{i}").into_bytes()).collect()
}
