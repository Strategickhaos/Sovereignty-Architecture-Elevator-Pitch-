//! Error types for FlameLang compiler

use thiserror::Error;

#[derive(Error, Debug, Clone)]
pub enum FlameError {
    #[error("Lexer error at line {line}, column {col}: {message}")]
    LexerError {
        line: usize,
        col: usize,
        message: String,
    },
    
    #[error("Parser error at line {line}: {message}")]
    ParserError {
        line: usize,
        message: String,
    },
    
    #[error("Transform error in layer {layer}: {message}")]
    TransformError {
        layer: String,
        message: String,
    },
    
    #[error("LLVM backend error: {0}")]
    BackendError(String),
    
    #[error("Proof validation failed: {proof_name}: {message}")]
    ProofError {
        proof_name: String,
        message: String,
    },
    
    #[error("IO error: {0}")]
    IoError(String),
    
    #[error("{0}")]
    Other(String),
}

impl From<std::io::Error> for FlameError {
    fn from(err: std::io::Error) -> Self {
        FlameError::IoError(err.to_string())
    }
}

pub type FlameResult<T> = Result<T, FlameError>;
