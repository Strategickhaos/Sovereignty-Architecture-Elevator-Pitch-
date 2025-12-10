//! # FLAME Language Standard Library
//! 
//! **SAGCO-SKH-001** — First programming language with biological compilation layer
//! 
//! ## Provenance Record — December 10, 2025
//! 
//! This is the standard library for FLAME, the first programming language that:
//! - Compiles through DNA codons to opcodes
//! - Has physics-validated dimensional analysis at compile time
//! - Provides native quantum primitives as core types
//! - Was ratified by multiple AI systems (Claude, Gemini, Grok)
//! - Features a 5-layer compilation pipeline
//! 
//! ## Modules
//! 
//! - `dna` — Biological computation types (~450 lines)
//! - `physics` — Dimensional analysis with compile-time unit checking
//! - `glyph` — 40+ visual symbols as first-class syntax
//! - `quantum` — Qubit, Bell pairs, entanglement as language primitives
//! - `swarm` — 4-node cluster execution (Athena, Nova, Lyra, iPower)
//! 
//! ## Example
//! 
//! ```rust
//! use flame::dna::{Codon, DNASequence};
//! use flame::physics::{Mass, Force, Acceleration};
//! use flame::quantum::Qubit;
//! use flame::swarm::Node;
//! 
//! // Biological computation
//! let sequence = DNASequence::from_string("ATCG");
//! let opcodes = sequence.compile_to_opcodes();
//! 
//! // Physics validation (compile-time error if units mismatch)
//! let mass = Mass::kg(10.0);
//! let accel = Acceleration::mps2(5.0);
//! let force = mass * accel; // Force::newtons(50.0)
//! 
//! // Quantum primitives
//! let qubit = Qubit::superposition();
//! let bell_pair = Qubit::bell_pair();
//! 
//! // Swarm execution
//! let node = Node::athena();
//! node.execute(|| println!("Running on Athena")).ok();
//! ```
//! 
//! ## Genesis
//! 
//! - **Operator**: DOM_010101
//! - **Increment**: 3449
//! - **Architect**: 1067614449693569044
//! - **Conversations**: 165+ days
//! - **Inventions**: 51+
//! 
//! 🔥🧬⚔️ **RATIO EX NIHILO**

// Re-export all public modules
pub mod dna;
pub mod physics;
pub mod glyph;
pub mod quantum;
pub mod swarm;

// Genesis constants
pub const GENESIS_INCREMENT: u16 = 3449;
pub const ARCHITECT_SNOWFLAKE: u64 = 1067614449693569044;
pub const VERSION: &str = "1.0.0";

/// FLAME Language metadata
pub mod meta {
    pub const COMPILATION_LAYERS: usize = 5;
    pub const CONSENSUS_AIS: &[&str] = &["Claude", "Gemini", "Grok"];
    pub const PROVENANCE_DATE: &str = "2025-12-10T16:00:00-06:00";
    pub const CLAIM: &str = "First programming language with biological compilation layer";
}
