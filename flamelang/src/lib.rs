//! # FlameLang Compiler Library
//! 
//! Core compiler functionality for the FlameLang sovereign programming language.
//! 
//! ## Architecture
//! 
//! FlameLang compiles through 5 transformation layers with 16 proof validations:
//! 
//! ```text
//! Source → Lexer → Parser → FlameIR → 5-Layer Transform → Proof Validation → Binary
//! ```

use std::fmt;

pub mod lexer;
pub mod parser;
pub mod transform;

/// FlameLang error types
#[derive(Debug, Clone)]
pub enum FlameError {
    /// Lexical analysis error
    LexError(String),
    /// Parsing error
    ParseError(String),
    /// Transform error
    TransformError(String),
    /// Proof violation - illegal physics detected
    ProofViolation(String),
    /// LLVM code generation error
    CodeGenError(String),
}

impl fmt::Display for FlameError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FlameError::LexError(msg) => write!(f, "Lexical Error: {}", msg),
            FlameError::ParseError(msg) => write!(f, "Parse Error: {}", msg),
            FlameError::TransformError(msg) => write!(f, "Transform Error: {}", msg),
            FlameError::ProofViolation(msg) => write!(f, "⚠️  PROOF VIOLATION: {}", msg),
            FlameError::CodeGenError(msg) => write!(f, "Code Generation Error: {}", msg),
        }
    }
}

impl std::error::Error for FlameError {}

pub type Result<T> = std::result::Result<T, FlameError>;
