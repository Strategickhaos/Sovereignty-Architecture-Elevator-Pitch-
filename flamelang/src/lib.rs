//! # FlameLang v2.0.0
//! 
//! ## Sovereign 5-Layer Transformation Pipeline
//! 
//! ```text
//! ┌─────────────────────────────────────────────────────────────────────────────┐
//! │  LAYER 1: LINGUISTIC    English → Hebrew → Glyph                            │
//! │  LAYER 2: NUMERIC       Unicode → Decimal → Hex                             │
//! │  LAYER 3: WAVE          Decimal → c=2πr → Hz/BPS                            │
//! │  LAYER 4: DNA           Freq → Codon → ACGT Sequence                        │
//! │  LAYER 5: LLVM          Codon → Opcode → Native Binary                      │
//! └─────────────────────────────────────────────────────────────────────────────┘
//! ```
//! 
//! ## Mathematical Foundations (16 Proofs)
//! 
//! - **Tier 1 (Kernel)**: Fixed-point convergence, grounding, genome, bijection
//! - **Tier 2 (Geometric)**: Pipe closure, Rubik bound, Fourier, setback identity
//! - **Tier 3 (Adversarial)**: Fallacy detection, jujitsu, RLHF, chess isomorphism
//! - **Tier 4 (Distribution)**: Torrent, hash chain, DNA durability, swarm immortality
//! 
//! © 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

#![warn(missing_docs)]
#![allow(dead_code)]

pub mod lexer;
pub mod parser;
pub mod transform;
pub mod pipeline;

use thiserror::Error;

/// FlameLang compilation errors
#[derive(Error, Debug)]
pub enum FlameError {
    /// Lexical analysis error
    #[error("Lexer error: {0}")]
    Lexer(String),
    
    /// Parsing error
    #[error("Parse error: {0}")]
    Parser(String),
    
    /// Transformation layer error
    #[error("Layer {layer} transform error: {message}")]
    Transform {
        /// Which layer failed (1-5)
        layer: u8,
        /// Error description
        message: String,
    },
    
    /// Type/dimensional mismatch
    #[error("Dimensional error: expected {expected}, got {actual}")]
    Dimensional {
        /// Expected type/dimension
        expected: String,
        /// Actual type/dimension
        actual: String,
    },
    
    /// Proof validation failure
    #[error("Proof {proof_id} failed: {message}")]
    ProofViolation {
        /// Which proof failed (1-16)
        proof_id: u8,
        /// Why it failed
        message: String,
    },
    
    /// Code generation error
    #[error("Codegen error: {0}")]
    Codegen(String),
    
    /// IO error
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

/// Result type for FlameLang operations
pub type FlameResult<T> = Result<T, FlameError>;

/// Compile FlameLang source to binary
/// 
/// # Example
/// 
/// ```ignore
/// use flamelang::compile;
/// 
/// let source = r#"
///     let r: float = 5.0;
///     let theta: angle = 90deg;
///     bend theta radius r;
/// "#;
/// 
/// let binary = compile(source)?;
/// ```
pub fn compile(source: &str) -> FlameResult<Vec<u8>> {
    pipeline::compile(source)
}

/// Compilation target
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Target {
    /// Stop after Layer 1 (Hebrew roots)
    Hebrew,
    /// Stop after Layer 2 (Numeric/Gematria)
    Numeric,
    /// Stop after Layer 3 (Wave/Frequency)
    Wave,
    /// Stop after Layer 4 (DNA/Codon)
    Dna,
    /// Emit LLVM IR
    LlvmIr,
    /// Full native binary
    Native,
}

/// Version information
pub const VERSION: &str = "2.0.0";
/// Build identifier
pub const BUILD_ID: &str = "ratio-ex-nihilo";
