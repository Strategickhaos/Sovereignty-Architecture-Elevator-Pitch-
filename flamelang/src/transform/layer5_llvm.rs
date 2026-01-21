//! # Layer 5: LLVM IR Generation
//! 
//! DNA → LLVM IR → Binary

use crate::parser::ast::*;
use crate::Result;

/// Generate LLVM IR from AST and DNA codons
pub fn generate_llvm_ir(program: &Program, dna_codons: &[String]) -> Result<String> {
    let mut ir = String::new();
    
    // LLVM module header
    ir.push_str("; ModuleID = 'flamelang_module'\n");
    ir.push_str("source_filename = \"flamelang_module\"\n");
    ir.push_str("target datalayout = \"e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128\"\n");
    ir.push_str("target triple = \"x86_64-unknown-linux-gnu\"\n\n");
    
    // Declare printf for output
    ir.push_str("declare i32 @printf(i8*, ...)\n\n");
    
    // Format strings
    ir.push_str("@.str = private unnamed_addr constant [4 x i8] c\"%d\\0A\\00\", align 1\n");
    ir.push_str("@.str.1 = private unnamed_addr constant [6 x i8] c\"%.2f\\0A\\00\", align 1\n");
    ir.push_str("@.str.2 = private unnamed_addr constant [4 x i8] c\"%s\\0A\\00\", align 1\n\n");
    
    // DNA codon metadata as comments
    ir.push_str("; DNA Codons: ");
    ir.push_str(&dna_codons.join(" "));
    ir.push_str("\n\n");
    
    // Generate functions
    for func in &program.functions {
        ir.push_str(&generate_function_ir(func)?);
    }
    
    // Add main function if not present
    if !program.functions.iter().any(|f| f.name == "main") {
        ir.push_str("\ndefine i32 @main() {\n");
        ir.push_str("  ret i32 0\n");
        ir.push_str("}\n");
    }
    
    Ok(ir)
}

fn generate_function_ir(func: &Function) -> Result<String> {
    let mut ir = String::new();
    
    // Function signature
    let return_type = "i32"; // Simplified - all functions return i32
    let params = func.params
        .iter()
        .enumerate()
        .map(|(i, _p)| format!("i32 %{}", i))
        .collect::<Vec<_>>()
        .join(", ");
    
    ir.push_str(&format!("define {} @{}({}) {{\n", return_type, func.name, params));
    ir.push_str("entry:\n");
    
    // Generate function body
    let mut var_counter = func.params.len();
    for stmt in &func.body {
        ir.push_str(&generate_statement_ir(stmt, &mut var_counter)?);
    }
    
    // Default return if no explicit return
    if !func.body.iter().any(|s| matches!(s, Stmt::Return(_))) {
        ir.push_str("  ret i32 0\n");
    }
    
    ir.push_str("}\n\n");
    
    Ok(ir)
}

fn generate_statement_ir(stmt: &Stmt, var_counter: &mut usize) -> Result<String> {
    let mut ir = String::new();
    
    match stmt {
        Stmt::Let { name, value } => {
            let (val_ir, val_reg) = generate_expr_ir(value, var_counter)?;
            ir.push_str(&val_ir);
            ir.push_str(&format!("  %{} = alloca i32\n", name));
            ir.push_str(&format!("  store i32 {}, i32* %{}\n", val_reg, name));
        }
        Stmt::Return(expr) => {
            let (expr_ir, expr_reg) = generate_expr_ir(expr, var_counter)?;
            ir.push_str(&expr_ir);
            ir.push_str(&format!("  ret i32 {}\n", expr_reg));
        }
        Stmt::Expr(expr) => {
            let (expr_ir, _) = generate_expr_ir(expr, var_counter)?;
            ir.push_str(&expr_ir);
        }
        Stmt::If { condition, then_block, else_block } => {
            let label_then = *var_counter;
            *var_counter += 1;
            let label_else = *var_counter;
            *var_counter += 1;
            let label_end = *var_counter;
            *var_counter += 1;
            
            let (cond_ir, cond_reg) = generate_expr_ir(condition, var_counter)?;
            ir.push_str(&cond_ir);
            
            if else_block.is_some() {
                ir.push_str(&format!("  br i1 {}, label %then{}, label %else{}\n", 
                    cond_reg, label_then, label_else));
            } else {
                ir.push_str(&format!("  br i1 {}, label %then{}, label %end{}\n", 
                    cond_reg, label_then, label_end));
            }
            
            ir.push_str(&format!("then{}:\n", label_then));
            for stmt in then_block {
                ir.push_str(&generate_statement_ir(stmt, var_counter)?);
            }
            ir.push_str(&format!("  br label %end{}\n", label_end));
            
            if let Some(else_stmts) = else_block {
                ir.push_str(&format!("else{}:\n", label_else));
                for stmt in else_stmts {
                    ir.push_str(&generate_statement_ir(stmt, var_counter)?);
                }
                ir.push_str(&format!("  br label %end{}\n", label_end));
            }
            
            ir.push_str(&format!("end{}:\n", label_end));
        }
        Stmt::While { condition, body } => {
            let label_cond = *var_counter;
            *var_counter += 1;
            let label_body = *var_counter;
            *var_counter += 1;
            let label_end = *var_counter;
            *var_counter += 1;
            
            ir.push_str(&format!("  br label %cond{}\n", label_cond));
            ir.push_str(&format!("cond{}:\n", label_cond));
            
            let (cond_ir, cond_reg) = generate_expr_ir(condition, var_counter)?;
            ir.push_str(&cond_ir);
            ir.push_str(&format!("  br i1 {}, label %body{}, label %end{}\n", 
                cond_reg, label_body, label_end));
            
            ir.push_str(&format!("body{}:\n", label_body));
            for stmt in body {
                ir.push_str(&generate_statement_ir(stmt, var_counter)?);
            }
            ir.push_str(&format!("  br label %cond{}\n", label_cond));
            
            ir.push_str(&format!("end{}:\n", label_end));
        }
    }
    
    Ok(ir)
}

fn generate_expr_ir(expr: &Expr, var_counter: &mut usize) -> Result<(String, String)> {
    let mut ir = String::new();
    let result_reg;
    
    match expr {
        Expr::Literal(lit) => {
            match lit {
                Literal::Number(n) => {
                    result_reg = format!("{}", *n as i32);
                }
                Literal::Bool(b) => {
                    result_reg = if *b { "1" } else { "0" }.to_string();
                }
                _ => {
                    result_reg = "0".to_string();
                }
            }
        }
        Expr::Identifier(name) => {
            let reg = *var_counter;
            *var_counter += 1;
            ir.push_str(&format!("  %{} = load i32, i32* %{}\n", reg, name));
            result_reg = format!("%{}", reg);
        }
        Expr::Binary { left, op, right } => {
            let (left_ir, left_reg) = generate_expr_ir(left, var_counter)?;
            let (right_ir, right_reg) = generate_expr_ir(right, var_counter)?;
            ir.push_str(&left_ir);
            ir.push_str(&right_ir);
            
            let reg = *var_counter;
            *var_counter += 1;
            
            let op_str = match op {
                BinOp::Add => "add",
                BinOp::Sub => "sub",
                BinOp::Mul => "mul",
                BinOp::Div => "sdiv",
                BinOp::Mod => "srem",
                BinOp::Eq => "icmp eq",
                BinOp::Ne => "icmp ne",
                BinOp::Lt => "icmp slt",
                BinOp::Le => "icmp sle",
                BinOp::Gt => "icmp sgt",
                BinOp::Ge => "icmp sge",
                BinOp::And => "and",
                BinOp::Or => "or",
            };
            
            ir.push_str(&format!("  %{} = {} i32 {}, {}\n", reg, op_str, left_reg, right_reg));
            result_reg = format!("%{}", reg);
        }
        Expr::Call { name, args: _ } => {
            // Simplified call handling
            let reg = *var_counter;
            *var_counter += 1;
            ir.push_str(&format!("  %{} = call i32 @{}()\n", reg, name));
            result_reg = format!("%{}", reg);
        }
        _ => {
            result_reg = "0".to_string();
        }
    }
    
    Ok((ir, result_reg))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_simple_function() {
        let func = Function {
            name: "test".to_string(),
            params: vec![],
            body: vec![Stmt::Return(Expr::Literal(Literal::Number(42.0)))],
        };
        
        let program = Program {
            functions: vec![func],
        };
        
        let codons = vec!["ATG".to_string()];
        let ir = generate_llvm_ir(&program, &codons).unwrap();
        
        assert!(ir.contains("define i32 @test"));
        assert!(ir.contains("ret i32 42"));
    }
}
