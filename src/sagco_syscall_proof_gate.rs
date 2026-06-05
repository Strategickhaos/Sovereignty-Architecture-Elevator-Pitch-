//! SAGCO Syscall Proof Gate
//!
//! This module provides the syscall boundary integration point.
//! It wraps the proof enforcer and provides task scheduling integration.

use crate::sagco_proof_enforcer::{FlameIR, ProofError, enforce_all};

/// Task identifier returned by the SAGCO scheduler
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct TaskId(pub u64);

impl TaskId {
    pub fn new(id: u64) -> Self {
        TaskId(id)
    }
}

/// Submit FlameIR to SAGCO for execution
///
/// This is the kernel syscall entrypoint. It enforces all proofs
/// and admits the IR to the scheduler only if validation passes.
///
/// # Arguments
/// * `ir` - The FlameIR to validate and schedule
///
/// # Returns
/// * `Ok(TaskId)` - Task was admitted and scheduled
/// * `Err(ProofError)` - IR failed validation and was rejected
///
/// # Example
/// ```rust
/// use sagco_proof_enforcer::{FlameIR, FlameExpr, FlameType, FlameOp, sagco_submit_ir};
///
/// let ir = FlameIR {
///     decls: vec![],
///     exprs: vec![
///         FlameExpr::Lit { value: 1.0, ty: FlameType::Float },
///         FlameExpr::Op { kind: FlameOp::Add, args: vec![0] },
///     ],
/// };
///
/// match sagco_submit_ir(ir) {
///     Ok(task_id) => println!("Task {} scheduled", task_id.0),
///     Err(e) => println!("Rejected: {}", e),
/// }
/// ```
pub fn sagco_submit_ir(ir: FlameIR) -> Result<TaskId, ProofError> {
    // Enforce all 16 proofs at the syscall boundary
    enforce_all(&ir)?;
    
    // IR passed validation - admit to scheduler
    // In a real implementation, this would call into the scheduler
    let task_id = scheduler_admit(ir);
    
    Ok(task_id)
}

/// Mock scheduler admission (replace with real scheduler in production)
fn scheduler_admit(_ir: FlameIR) -> TaskId {
    // In production, this would:
    // 1. Allocate task resources
    // 2. Insert into execution queue
    // 3. Return real task ID
    
    // For now, return a mock ID
    TaskId::new(42)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{FlameExpr, FlameType, FlameOp};

    #[test]
    fn test_valid_ir_admitted() {
        let ir = FlameIR {
            decls: vec![],
            exprs: vec![
                FlameExpr::Lit { value: 1.0, ty: FlameType::Float },
                FlameExpr::Op { kind: FlameOp::Add, args: vec![0] },
            ],
        };
        
        let result = sagco_submit_ir(ir);
        assert!(result.is_ok());
    }

    #[test]
    fn test_invalid_ir_rejected() {
        let ir = FlameIR {
            decls: vec![],
            exprs: vec![],
        };
        
        let result = sagco_submit_ir(ir);
        assert!(result.is_err());
    }

    #[test]
    fn test_codon_violation_rejected() {
        let ir = FlameIR {
            decls: vec![],
            exprs: vec![
                FlameExpr::Lit { value: 100.0, ty: FlameType::Codon },
                FlameExpr::Op { kind: FlameOp::Codon, args: vec![0] },
            ],
        };
        
        let result = sagco_submit_ir(ir);
        assert!(result.is_err());
    }
}
