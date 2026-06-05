/// SAGCO Kernel - Core DNA mutation and evolution logic
///
/// The kernel module provides:
/// - DNA strand parsing and manipulation
/// - Mutation suggestion based on Guardian metrics
/// - Evolution rules for compiler, mesh, and orbit layers

pub mod dna_mutation;

pub use dna_mutation::{
    DnaComponents, DnaSpec, suggest_flm_mutation, 
    suggest_mesh_mutation, suggest_orbit_mutation
};
