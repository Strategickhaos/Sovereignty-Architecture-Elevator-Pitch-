// FlameLang Compiler Library
// 
// This library provides the intermediate representation (IR) and compiler
// infrastructure for FlameLang v0.1.0

pub mod ir;

// Re-export main types for convenience
pub use ir::{
    FlameIR, FlameType, BinaryOperator,
    Module, FnDef, Param, Block, Let, Const, Call, Return, Extern, Var, BinOp,
    TransformPass, ValidatePass, PassError, Diagnostic, DiagnosticLevel, Location,
    InvariantChecker, PassTRIG6Lowering, PassTRIG6Validate,
    IR_VERSION, IR_VERSION_MAJOR, IR_VERSION_MINOR, IR_VERSION_PATCH,
};

pub mod builder {
    pub use crate::ir::builder::*;
}
