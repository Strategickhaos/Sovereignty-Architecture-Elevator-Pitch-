//! # FlameLang Compiler Library
//! 
//! © 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

pub mod lexer;
pub mod parser;
pub mod transform;
pub mod compiler;

// ═══════════════════════════════════════════════════════════════════════════════
// ERROR TYPES
// ═══════════════════════════════════════════════════════════════════════════════

/// Result type for FlameLang operations
pub type FlameResult<T> = Result<T, FlameError>;

/// Error types for the FlameLang compiler
#[derive(Debug, Clone)]
pub enum FlameError {
    /// Lexer error
    Lexer(String),
    /// Parser error
    Parser(String),
    /// Transform error with layer number
    Transform {
        layer: usize,
        message: String,
    },
    /// LLVM error
    LLVM(String),
}

impl std::fmt::Display for FlameError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            FlameError::Lexer(msg) => write!(f, "Lexer error: {}", msg),
            FlameError::Parser(msg) => write!(f, "Parser error: {}", msg),
            FlameError::Transform { layer, message } => {
                write!(f, "Transform error (layer {}): {}", layer, message)
            }
            FlameError::LLVM(msg) => write!(f, "LLVM error: {}", msg),
        }
    }
}

impl std::error::Error for FlameError {}
