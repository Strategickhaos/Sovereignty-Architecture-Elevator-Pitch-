//! FlameLang Compiler
//! 5-Layer Transformation Pipeline: Linguistic → Numeric → Wave → DNA → LLVM
//! 
//! Copyright (c) 2025 Strategickhaos DAO LLC (EIN: 39-2900295)
//! Inventor: Domenic Gabriel Garza

pub mod lexer;
pub mod parser;
pub mod ast;
pub mod transform;
pub mod backend;
pub mod pipeline;
pub mod proofs;
pub mod ir;
pub mod error;

pub use error::{FlameError, FlameResult};
pub use pipeline::compile;

/// Version info
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const COMPILER_NAME: &str = "flamec";
