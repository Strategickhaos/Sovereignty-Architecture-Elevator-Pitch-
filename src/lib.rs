//! SAGCO-OS: Sovereignty Architecture with Geometric Computing and Ontology
//! 
//! This library provides the core components for the SAGCO operating system,
//! including hypervisor simulation, probability inference (VI), geometric
//! guardian mapping, and trigonometric lookup tables.

pub mod sagco_tables;
pub mod probability;
pub mod sagco_guardian;

// Re-export common types
pub use sagco_tables::*;
pub use probability::*;
pub use sagco_guardian::*;
