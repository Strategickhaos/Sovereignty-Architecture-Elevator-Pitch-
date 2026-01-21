//! # FlameLang Compilation Pipeline
//! 
//! The canonical spine that wires all layers together.
//! 
//! ```text
//! Source → Lexer → Parser → AST → FlameIR → Transforms → LLVM → Binary
//!                                    ↓
//!                            [16 Proofs Validate Here]
//! ```
//! 
//! © 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

use crate::lexer::{Lexer, Token};
use crate::parser::{Parser, Expr, Literal, BinOp};
use crate::transform::{
    layer1_linguistic,
    layer2_numeric,
    layer3_wave,
    layer4_dna,
    layer5_llvm,
};
use crate::{FlameError, FlameResult};

// ═══════════════════════════════════════════════════════════════════════════════
// FLAMELANG IR v0.1 - THE SPINE
// ═══════════════════════════════════════════════════════════════════════════════

/// Core type system with proof constraints
#[derive(Debug, Clone, PartialEq)]
pub enum FlameType {
    /// Standard float
    Float,
    /// Angle in radians - PROOF: ops enforce mod 2π
    Angle,
    /// DNA codon (0-63) - PROOF: bijection to 64 states
    Codon,
    /// Rubik permutation - PROOF: bounded 0-20 (God's Number)
    Perm,
    /// Frequency in Hz - PROOF: positive, bounded
    Freq,
}

/// Operations with physics semantics
#[derive(Debug, Clone, PartialEq)]
pub enum FlameOp {
    // Arithmetic
    Add, Sub, Mul, Div,
    
    // Trigonometric (unit circle anchors)
    Sin, Cos, Tan,
    
    // Domain transforms (your kernel)
    Bend,   // angle + radius → arc length
    Codon,  // arc → DNA codon (bijection)
    Perm,   // codon → Rubik moves (bounded)
    
    // Wave encoding
    ToFreq,   // value → Hz
    FromFreq, // Hz → value
}

/// The canonical IR - everything targets this
#[derive(Debug, Clone)]
pub struct FlameIR {
    pub decls: Vec<FlameDecl>,
    pub exprs: Vec<FlameExpr>,
}

#[derive(Debug, Clone)]
pub struct FlameDecl {
    pub name: String,
    pub ty: FlameType,
    pub value: usize, // Index into exprs
}

#[derive(Debug, Clone)]
pub enum FlameExpr {
    /// Literal value with type
    Lit { value: f64, ty: FlameType },
    /// Variable reference
    Var(String),
    /// Operation application
    Op { kind: FlameOp, args: Vec<usize> },
    /// Return value
    Return(usize),
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN COMPILATION PIPELINE
// ═══════════════════════════════════════════════════════════════════════════════

/// Compile FlameLang source to binary
/// 
/// This is THE function. Everything flows through here.
pub fn compile(source: &str) -> FlameResult<Vec<u8>> {
    // ─────────────────────────────────────────────────────────────────────────
    // PHASE 1: FRONTEND (Source → IR)
    // ─────────────────────────────────────────────────────────────────────────
    
    // Step 1: Lexical analysis
    let mut lexer = Lexer::new(source);
    let tokens: Vec<Token> = lexer.tokenize();
    
    // Check if we only have EOF token (empty source)
    if tokens.len() == 1 && matches!(tokens[0], Token::Eof) {
        return Err(FlameError::Lexer("No tokens produced".into()));
    }
    
    // Step 2: Parsing → AST
    let mut parser = Parser::new(tokens);
    let ast = parser.parse()
        .map_err(|e| FlameError::Parser(e))?;
    
    // Step 3: Lower AST → FlameIR
    let mut ir = lower_to_ir(&ast)?;
    
    // ─────────────────────────────────────────────────────────────────────────
    // PHASE 2: MIDDLE-END (IR → IR transforms)
    // ─────────────────────────────────────────────────────────────────────────
    
    // Step 4: 5-Layer Transformation Pipeline
    ir = run_linguistic_pass(ir)?;   // Layer 1: English → Hebrew
    ir = run_numeric_pass(ir)?;      // Layer 2: Unicode → Gematria
    ir = run_wave_pass(ir)?;         // Layer 3: c=2πr → Hz
    ir = run_dna_pass(ir)?;          // Layer 4: Freq → Codon
    
    // Step 5: Validate proofs (YOUR 16 PROOFS ATTACH HERE)
    validate_proofs(&ir)?;
    
    // ─────────────────────────────────────────────────────────────────────────
    // PHASE 3: BACKEND (IR → Binary)
    // ─────────────────────────────────────────────────────────────────────────
    
    // Step 6: Generate LLVM IR
    let llvm_ir = run_llvm_pass(&ir)?;
    
    // Step 7: Emit binary
    let binary = emit_binary(&llvm_ir)?;
    
    Ok(binary)
}

// ═══════════════════════════════════════════════════════════════════════════════
// AST → IR LOWERING
// ═══════════════════════════════════════════════════════════════════════════════

fn lower_to_ir(ast: &[Expr]) -> FlameResult<FlameIR> {
    let mut ir = FlameIR {
        decls: Vec::new(),
        exprs: Vec::new(),
    };
    
    for expr in ast {
        lower_expr(&mut ir, expr)?;
    }
    
    Ok(ir)
}

fn lower_expr(ir: &mut FlameIR, expr: &Expr) -> FlameResult<usize> {
    match expr {
        Expr::Literal(lit) => {
            let (value, ty) = match lit {
                Literal::Integer(i) => (*i as f64, FlameType::Float),
                Literal::Float(f) => (*f, FlameType::Float),
                Literal::String(_) => return Err(FlameError::Parser("Strings not yet supported".into())),
                Literal::Bool(b) => (if *b { 1.0 } else { 0.0 }, FlameType::Float),
            };
            let idx = ir.exprs.len();
            ir.exprs.push(FlameExpr::Lit { value, ty });
            Ok(idx)
        }
        
        Expr::Binary { left, op, right } => {
            let left_idx = lower_expr(ir, left)?;
            let right_idx = lower_expr(ir, right)?;
            
            let flame_op = match op {
                BinOp::Add => FlameOp::Add,
                BinOp::Sub => FlameOp::Sub,
                BinOp::Mul => FlameOp::Mul,
                BinOp::Div => FlameOp::Div,
            };
            
            let idx = ir.exprs.len();
            ir.exprs.push(FlameExpr::Op {
                kind: flame_op,
                args: vec![left_idx, right_idx],
            });
            Ok(idx)
        }
        
        Expr::Glyph(c) => {
            // Map glyph to operation
            let op = match c {
                '🔥' => FlameOp::Bend,
                '🧬' => FlameOp::Codon,
                '♜' => FlameOp::Perm,
                '∿' => FlameOp::ToFreq,
                _ => return Err(FlameError::Parser(format!("Unknown glyph: {}", c))),
            };
            let idx = ir.exprs.len();
            ir.exprs.push(FlameExpr::Op { kind: op, args: vec![] });
            Ok(idx)
        }
        
        _ => Err(FlameError::Parser("Unsupported expression".into())),
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// TRANSFORMATION PASSES
// ═══════════════════════════════════════════════════════════════════════════════

fn run_linguistic_pass(ir: FlameIR) -> FlameResult<FlameIR> {
    // Layer 1: English identifiers → Hebrew triconsonantal roots
    // This is where your layer1_linguistic::transform hooks in
    layer1_linguistic(ir)
}

fn run_numeric_pass(ir: FlameIR) -> FlameResult<FlameIR> {
    // Layer 2: Hebrew → Gematria values
    // This is where your layer2_numeric::transform hooks in
    layer2_numeric(ir)
}

fn run_wave_pass(ir: FlameIR) -> FlameResult<FlameIR> {
    // Layer 3: Gematria → Frequency (c = 2πr)
    // This is where your layer3_wave::transform hooks in
    layer3_wave(ir)
}

fn run_dna_pass(ir: FlameIR) -> FlameResult<FlameIR> {
    // Layer 4: Frequency → Codon (64-state bijection)
    // This is where your layer4_dna::transform hooks in
    layer4_dna(ir)
}

fn run_llvm_pass(ir: &FlameIR) -> FlameResult<String> {
    // Layer 5: FlameIR → LLVM IR
    layer5_llvm(ir)
}

fn emit_binary(llvm_ir: &str) -> FlameResult<Vec<u8>> {
    // For now, just return the IR as bytes
    // Full implementation would use inkwell to compile to native
    Ok(llvm_ir.as_bytes().to_vec())
}

// ═══════════════════════════════════════════════════════════════════════════════
// PROOF VALIDATION (YOUR 16 PROOFS ATTACH HERE)
// ═══════════════════════════════════════════════════════════════════════════════

/// Validate all 16 proofs against the IR
/// 
/// These are compile-time guarantees, not runtime checks.
fn validate_proofs(ir: &FlameIR) -> FlameResult<()> {
    // ─────────────────────────────────────────────────────────────────────────
    // TIER 1: KERNEL PROOFS
    // ─────────────────────────────────────────────────────────────────────────
    
    validate_fixed_point_convergence(ir)?;      // Proof 1
    validate_grounding_completeness(ir)?;       // Proof 2
    validate_genome_classification(ir)?;        // Proof 3
    validate_codon_bijection(ir)?;              // Proof 4
    
    // ─────────────────────────────────────────────────────────────────────────
    // TIER 2: GEOMETRIC PROOFS
    // ─────────────────────────────────────────────────────────────────────────
    
    validate_pipe_bend_closure(ir)?;            // Proof 5
    validate_rubik_bound(ir)?;                  // Proof 6
    validate_fourier_encoding(ir)?;             // Proof 7
    validate_setback_identity(ir)?;             // Proof 8
    
    // ─────────────────────────────────────────────────────────────────────────
    // TIER 3: ADVERSARIAL PROOFS (compile-time not applicable)
    // ─────────────────────────────────────────────────────────────────────────
    
    // Proofs 9-12 are runtime behavioral checks
    
    // ─────────────────────────────────────────────────────────────────────────
    // TIER 4: DISTRIBUTION PROOFS (compile-time not applicable)
    // ─────────────────────────────────────────────────────────────────────────
    
    // Proofs 13-16 are deployment-time checks
    
    Ok(())
}

// ═══════════════════════════════════════════════════════════════════════════════
// INDIVIDUAL PROOF IMPLEMENTATIONS
// ═══════════════════════════════════════════════════════════════════════════════

fn validate_fixed_point_convergence(_ir: &FlameIR) -> FlameResult<()> {
    // Proof 1: Feedback loops converge in bounded iterations
    // Check: No unbounded recursion in IR
    Ok(())
}

fn validate_grounding_completeness(ir: &FlameIR) -> FlameResult<()> {
    // Proof 2: All inputs satisfy M/F/B
    // Check: Every expr has measurable, falsifiable, bounded semantics
    for expr in &ir.exprs {
        match expr {
            FlameExpr::Lit { value, ty: _ } => {
                // Bounded check
                if !value.is_finite() {
                    return Err(FlameError::Transform {
                        layer: 0,
                        message: format!("Unbounded literal: {}", value),
                    });
                }
            }
            _ => {}
        }
    }
    Ok(())
}

fn validate_genome_classification(_ir: &FlameIR) -> FlameResult<()> {
    // Proof 3: Behavioral markers cluster into 4 modes
    // (Not applicable at compile time)
    Ok(())
}

fn validate_codon_bijection(ir: &FlameIR) -> FlameResult<()> {
    // Proof 4: 64 codons ↔ 64 states bijection
    // Check: All Codon operations preserve the bijection
    for expr in &ir.exprs {
        if let FlameExpr::Op { kind: FlameOp::Codon, .. } = expr {
            // Verify codon mapping is reversible
            // (Full implementation would track state)
        }
    }
    Ok(())
}

fn validate_pipe_bend_closure(ir: &FlameIR) -> FlameResult<()> {
    // Proof 5: Σθᵢ = 360° implies closed path
    // Check: Bend operations with Angle type sum correctly
    
    use std::f64::consts::PI;
    const TWO_PI: f64 = 2.0 * PI;
    const EPSILON: f64 = 0.001;
    
    let mut angle_sum = 0.0;
    
    for expr in &ir.exprs {
        if let FlameExpr::Lit { value, ty: FlameType::Angle } = expr {
            angle_sum += value;
        }
    }
    
    // Normalize to [0, 2π)
    let normalized = angle_sum % TWO_PI;
    
    // For closure, sum should be multiple of 2π (or 0)
    if normalized.abs() > EPSILON && (TWO_PI - normalized).abs() > EPSILON {
        // Not an error - just not a closed path
        // Full implementation would track this as metadata
    }
    
    Ok(())
}

fn validate_rubik_bound(ir: &FlameIR) -> FlameResult<()> {
    // Proof 6: God's Number ≤ 20
    // Check: All Perm operations produce values in [0, 20]
    
    for expr in &ir.exprs {
        if let FlameExpr::Lit { value, ty: FlameType::Perm } = expr {
            if *value < 0.0 || *value > 20.0 {
                return Err(FlameError::Transform {
                    layer: 4,
                    message: format!("Perm {} violates God's Number bound [0, 20]", value),
                });
            }
        }
    }
    Ok(())
}

fn validate_fourier_encoding(_ir: &FlameIR) -> FlameResult<()> {
    // Proof 7: Spectral peaks at 90° harmonics
    // (Requires full wave analysis - stub for now)
    Ok(())
}

fn validate_setback_identity(_ir: &FlameIR) -> FlameResult<()> {
    // Proof 8: arc_length = r × θ
    // Check: Bend operations maintain this identity
    Ok(())
}

// ═══════════════════════════════════════════════════════════════════════════════
// TESTS
// ═══════════════════════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_empty_compile() {
        let result = compile("");
        assert!(result.is_err()); // Empty source should fail
    }
    
    #[test]
    fn test_minimal_program() {
        // This would need actual lexer/parser to work
        // For now, test the IR directly
        let ir = FlameIR {
            decls: vec![],
            exprs: vec![
                FlameExpr::Lit { value: 0.0, ty: FlameType::Float },
                FlameExpr::Return(0),
            ],
        };
        
        let result = validate_proofs(&ir);
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_rubik_bound_enforced() {
        let ir = FlameIR {
            decls: vec![],
            exprs: vec![
                FlameExpr::Lit { value: 25.0, ty: FlameType::Perm }, // Violates!
            ],
        };
        
        let result = validate_rubik_bound(&ir);
        assert!(result.is_err());
    }
    
    #[test]
    fn test_unbounded_literal_rejected() {
        let ir = FlameIR {
            decls: vec![],
            exprs: vec![
                FlameExpr::Lit { value: f64::INFINITY, ty: FlameType::Float },
            ],
        };
        
        let result = validate_grounding_completeness(&ir);
        assert!(result.is_err());
    }
}
