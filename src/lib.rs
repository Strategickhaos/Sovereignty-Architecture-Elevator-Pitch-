//! SAGCO Proof Enforcer Library
//! 
//! This library provides kernel-side proof enforcement for FlameIR,
//! ensuring that all code admitted to the SAGCO execution environment
//! satisfies 16 fundamental proofs across 4 tiers.
//! 
//! # Architecture
//! 
//! The enforcer sits at the syscall boundary and validates FlameIR
//! before it enters the execution domain.
//! 
//! # Example
//! 
//! ```rust
//! use sagco_proof_enforcer::{FlameIR, FlameExpr, FlameType, FlameOp, enforce_all};
//! 
//! let ir = FlameIR {
//!     decls: vec![],
//!     exprs: vec![
//!         FlameExpr::Lit { value: 1.0, ty: FlameType::Float },
//!         FlameExpr::Op { kind: FlameOp::Add, args: vec![0] },
//!     ],
//! };
//! 
//! match enforce_all(&ir) {
//!     Ok(()) => println!("IR admitted to execution"),
//!     Err(e) => println!("IR rejected: {}", e),
//! }
//! ```

pub mod sagco_proof_enforcer;
pub mod flame_proof_ids;
pub mod sagco_syscall_proof_gate;

// Re-export main types for convenience
pub use sagco_proof_enforcer::{
    FlameIR, FlameType, FlameOp, FlameDecl, FlameExpr,
    ProofError, ProofErrorKind, ProofResult,
    enforce_all,
};

pub use flame_proof_ids::{ProofId, PROOF_TIERS};
pub use sagco_syscall_proof_gate::{sagco_submit_ir, TaskId};
