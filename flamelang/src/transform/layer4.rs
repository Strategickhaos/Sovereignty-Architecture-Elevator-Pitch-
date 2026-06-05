//! Layer 4: DNA Transform
//! Frequency → 64-codon bijection → FlameIR

use crate::FlameResult;
use crate::transform::layer3::WaveData;
use crate::ir::*;
use crate::ast::{Statement, Expr, Literal, BinOp as AstBinOp};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct DNAData {
    pub wave_data: WaveData,
    pub codon_mappings: HashMap<String, [u8; 3]>,
}

/// 64 DNA codons (simplified mapping)
const DNA_BASES: [u8; 4] = [b'A', b'C', b'G', b'T'];

/// Map frequency to 64-codon space
fn frequency_to_codon(frequency: f64) -> [u8; 3] {
    let normalized = (frequency.abs() * 100.0) as usize % 64;
    let i = normalized / 16;
    let j = (normalized / 4) % 4;
    let k = normalized % 4;
    [DNA_BASES[i % 4], DNA_BASES[j], DNA_BASES[k]]
}

/// Transform wave data to FlameIR via DNA encoding
pub fn transform(wave_data: &WaveData, module_name: &str) -> FlameResult<FlameIR> {
    let mut ir = FlameIR::new(module_name);
    let mut codon_mappings = HashMap::new();
    
    // Map frequencies to codons
    for (name, freq) in &wave_data.frequencies {
        let codon = frequency_to_codon(*freq);
        codon_mappings.insert(name.clone(), codon);
    }
    
    // Convert AST to FlameIR
    for statement in &wave_data.numeric_data.hebrew_ast.program.statements {
        match statement {
            Statement::FunctionDef { name, params, return_type, body } => {
                let flame_func = convert_function(
                    name,
                    params,
                    return_type,
                    body,
                    &wave_data.numeric_data.hebrew_ast.root_mappings,
                    &wave_data.numeric_data.gematria_values,
                    &wave_data.frequencies,
                    &codon_mappings,
                )?;
                ir.add_function(flame_func);
            }
            _ => {
                // Handle top-level statements as part of implicit main
            }
        }
    }
    
    Ok(ir)
}

fn convert_function(
    name: &str,
    params: &[(String, crate::ast::Type)],
    return_type: &crate::ast::Type,
    body: &[Statement],
    hebrew_roots: &HashMap<String, String>,
    gematria: &HashMap<String, u64>,
    frequencies: &HashMap<String, f64>,
    codons: &HashMap<String, [u8; 3]>,
) -> FlameResult<FlameFunction> {
    let flame_params: Vec<FlameParam> = params.iter()
        .map(|(n, t)| FlameParam {
            name: n.clone(),
            param_type: convert_type(t),
        })
        .collect();
    
    let mut flame_body = Vec::new();
    for stmt in body {
        if let Statement::Return(Some(expr)) = stmt {
            flame_body.push(FlameExpr::Return(Box::new(convert_expr(expr)?)));
        } else if let Statement::Return(None) = stmt {
            flame_body.push(FlameExpr::Return(Box::new(FlameExpr::Constant(FlameValue::Integer(0)))));
        } else {
            // Convert other statements to expressions
            if let Statement::Expression(expr) = stmt {
                flame_body.push(convert_expr(expr)?);
            }
        }
    }
    
    Ok(FlameFunction {
        name: name.to_string(),
        params: flame_params,
        return_type: convert_type(return_type),
        body: flame_body,
        hebrew_root: hebrew_roots.get(name).cloned(),
        gematria_value: gematria.get(name).copied(),
        frequency: frequencies.get(name).copied(),
        codon: codons.get(name).map(|c| format!("{}{}{}", c[0] as char, c[1] as char, c[2] as char)),
    })
}

fn convert_type(t: &crate::ast::Type) -> FlameType {
    match t {
        crate::ast::Type::I32 => FlameType::I32,
        crate::ast::Type::I64 => FlameType::I64,
        crate::ast::Type::F64 => FlameType::F64,
        crate::ast::Type::Bool => FlameType::Bool,
        crate::ast::Type::String => FlameType::String,
        crate::ast::Type::Array(inner, size) => {
            FlameType::Array(Box::new(convert_type(inner)), size.unwrap_or(0))
        }
        crate::ast::Type::Void => FlameType::Void,
    }
}

fn convert_expr(expr: &Expr) -> FlameResult<FlameExpr> {
    match expr {
        Expr::Literal(lit) => Ok(FlameExpr::Constant(convert_literal(lit))),
        Expr::BinOp { left, op, right } => {
            Ok(FlameExpr::BinaryOp {
                op: convert_binop(op),
                left: Box::new(convert_expr(left)?),
                right: Box::new(convert_expr(right)?),
            })
        }
        Expr::UnaryOp { op: _, expr } => {
            Ok(FlameExpr::UnaryOp {
                op: FlameOp::Sub, // Simplified
                operand: Box::new(convert_expr(expr)?),
            })
        }
        Expr::Variable(name) => Ok(FlameExpr::Variable(name.clone())),
        Expr::FunctionCall { name, args } => {
            let flame_args: Result<Vec<_>, _> = args.iter()
                .map(convert_expr)
                .collect();
            Ok(FlameExpr::Call {
                function: name.clone(),
                args: flame_args?,
            })
        }
        Expr::Array(elements) => {
            // Simplified: return first element or default
            if let Some(first) = elements.first() {
                convert_expr(first)
            } else {
                Ok(FlameExpr::Constant(FlameValue::Integer(0)))
            }
        }
    }
}

fn convert_literal(lit: &Literal) -> FlameValue {
    match lit {
        Literal::Integer(n) => FlameValue::Integer(*n),
        Literal::Float(f) => FlameValue::Float(*f),
        Literal::String(s) => FlameValue::String(s.clone()),
        Literal::Boolean(b) => FlameValue::Boolean(*b),
        Literal::Hebrew(h) => FlameValue::String(h.clone()),
    }
}

fn convert_binop(op: &AstBinOp) -> FlameOp {
    match op {
        AstBinOp::Add => FlameOp::Add,
        AstBinOp::Sub => FlameOp::Sub,
        AstBinOp::Mul => FlameOp::Mul,
        AstBinOp::Div => FlameOp::Div,
        AstBinOp::Mod => FlameOp::Mod,
        _ => FlameOp::Add, // Simplified
    }
}
