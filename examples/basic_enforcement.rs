//! Basic SAGCO Proof Enforcement Example
//!
//! This example demonstrates how to use the SAGCO proof enforcer
//! to validate FlameIR before execution.

use sagco_proof_enforcer::{
    FlameIR, FlameExpr, FlameType, FlameOp, FlameDecl,
    enforce_all, sagco_submit_ir,
};

fn main() {
    println!("═══════════════════════════════════════════════════════════");
    println!("  SAGCO PROOF ENFORCER — KERNEL ADMISSION GATE");
    println!("  Enforcing 16 proofs across 4 tiers");
    println!("═══════════════════════════════════════════════════════════\n");

    // Example 1: Valid IR that passes all proofs
    println!("🔬 Example 1: Valid FlameIR");
    let valid_ir = FlameIR {
        decls: vec![
            FlameDecl {
                name: "x".to_string(),
                ty: FlameType::Float,
                value: 0,
            },
        ],
        exprs: vec![
            FlameExpr::Lit { value: 1.5, ty: FlameType::Float },
            FlameExpr::Lit { value: 2.5, ty: FlameType::Float },
            FlameExpr::Op { 
                kind: FlameOp::Add, 
                args: vec![0, 1] 
            },
            FlameExpr::Return(2),
        ],
    };

    match enforce_all(&valid_ir) {
        Ok(()) => println!("✅ IR passed all 16 proofs - ADMITTED\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    // Example 2: Submit to scheduler
    println!("🔬 Example 2: Submit to SAGCO Scheduler");
    let ir_for_scheduling = FlameIR {
        decls: vec![],
        exprs: vec![
            FlameExpr::Lit { value: 3.14159, ty: FlameType::Angle },
            FlameExpr::Op { kind: FlameOp::Sin, args: vec![0] },
        ],
    };

    match sagco_submit_ir(ir_for_scheduling) {
        Ok(task_id) => println!("✅ Task {} scheduled for execution\n", task_id.0),
        Err(e) => println!("❌ Task rejected: {}\n", e),
    }

    // Example 3: Empty IR (fails fixed_point_convergence)
    println!("🔬 Example 3: Empty IR (should fail)");
    let empty_ir = FlameIR {
        decls: vec![],
        exprs: vec![],
    };

    match enforce_all(&empty_ir) {
        Ok(()) => println!("✅ IR admitted\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    // Example 4: Only literals (fails grounding_completeness)
    println!("🔬 Example 4: Only literals (should fail)");
    let literals_only = FlameIR {
        decls: vec![],
        exprs: vec![
            FlameExpr::Lit { value: 1.0, ty: FlameType::Float },
            FlameExpr::Lit { value: 2.0, ty: FlameType::Float },
        ],
    };

    match enforce_all(&literals_only) {
        Ok(()) => println!("✅ IR admitted\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    // Example 5: Codon out of range (fails codon_bijection)
    println!("🔬 Example 5: Invalid codon (should fail)");
    let invalid_codon = FlameIR {
        decls: vec![],
        exprs: vec![
            FlameExpr::Lit { value: 65.0, ty: FlameType::Codon },
            FlameExpr::Op { kind: FlameOp::Codon, args: vec![0] },
        ],
    };

    match enforce_all(&invalid_codon) {
        Ok(()) => println!("✅ IR admitted\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    // Example 6: Non-finite angle (fails angle_boundedness)
    println!("🔬 Example 6: Infinite angle (should fail)");
    let infinite_angle = FlameIR {
        decls: vec![],
        exprs: vec![
            FlameExpr::Lit { value: f64::INFINITY, ty: FlameType::Angle },
            FlameExpr::Op { kind: FlameOp::Sin, args: vec![0] },
        ],
    };

    match enforce_all(&infinite_angle) {
        Ok(()) => println!("✅ IR admitted\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    // Example 7: Negative frequency (fails frequency_positivity)
    println!("🔬 Example 7: Negative frequency (should fail)");
    let negative_freq = FlameIR {
        decls: vec![],
        exprs: vec![
            FlameExpr::Lit { value: -440.0, ty: FlameType::Freq },
            FlameExpr::Op { kind: FlameOp::ToFreq, args: vec![0] },
        ],
    };

    match enforce_all(&negative_freq) {
        Ok(()) => println!("✅ IR admitted\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    // Example 8: Permutation exceeds God's number (fails rubik_god_number)
    println!("🔬 Example 8: Permutation > 20 (should fail)");
    let invalid_perm = FlameIR {
        decls: vec![],
        exprs: vec![
            FlameExpr::Lit { value: 25.0, ty: FlameType::Perm },
            FlameExpr::Op { kind: FlameOp::Perm, args: vec![0] },
        ],
    };

    match enforce_all(&invalid_perm) {
        Ok(()) => println!("✅ IR admitted\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    // Example 9: Cyclic reference (fails ir_acyclicity)
    println!("🔬 Example 9: Forward reference (should fail)");
    let cyclic_ir = FlameIR {
        decls: vec![],
        exprs: vec![
            FlameExpr::Lit { value: 1.0, ty: FlameType::Float },
            FlameExpr::Op { kind: FlameOp::Add, args: vec![0, 2] }, // Forward ref
            FlameExpr::Op { kind: FlameOp::Mul, args: vec![1] },
        ],
    };

    match enforce_all(&cyclic_ir) {
        Ok(()) => println!("✅ IR admitted\n"),
        Err(e) => println!("❌ IR rejected: {}\n", e),
    }

    println!("═══════════════════════════════════════════════════════════");
    println!("  ENFORCEMENT COMPLETE");
    println!("  Kernel remains uncontaminated");
    println!("═══════════════════════════════════════════════════════════\n");
}
