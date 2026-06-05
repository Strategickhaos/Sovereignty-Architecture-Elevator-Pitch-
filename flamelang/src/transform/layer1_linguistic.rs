//! # Layer 1: Linguistic Transformation
//! 
//! English → Hebrew (בָּרָא)

use crate::parser::ast::*;
use crate::Result;
use std::collections::HashMap;

/// Map English words to Hebrew equivalents
pub fn transform_to_hebrew(program: &Program) -> Result<String> {
    let mut hebrew_output = String::new();
    
    // Create a basic English -> Hebrew mapping
    let mut word_map: HashMap<&str, &str> = HashMap::new();
    word_map.insert("create", "בָּרָא");
    word_map.insert("begin", "רֵאשִׁית");
    word_map.insert("end", "סוֹף");
    word_map.insert("function", "פוּנְקְצִיָּה");
    word_map.insert("return", "חָזַר");
    word_map.insert("let", "יְהִי");
    word_map.insert("if", "אִם");
    word_map.insert("else", "אַחֵר");
    word_map.insert("while", "בְּעוֹד");
    word_map.insert("true", "אֱמֶת");
    word_map.insert("false", "שֶׁקֶר");
    
    // Transform program structure to Hebrew representation
    for func in &program.functions {
        hebrew_output.push_str(&format!("פוּנְקְצִיָּה {}\n", func.name));
        hebrew_output.push_str(&transform_statements_to_hebrew(&func.body));
        hebrew_output.push_str("סוֹף\n");
    }
    
    Ok(hebrew_output)
}

fn transform_statements_to_hebrew(stmts: &[Stmt]) -> String {
    let mut output = String::new();
    
    for stmt in stmts {
        match stmt {
            Stmt::Let { name, value } => {
                output.push_str(&format!("  יְהִי {} = {}\n", name, expr_to_hebrew(value)));
            }
            Stmt::Return(expr) => {
                output.push_str(&format!("  חָזַר {}\n", expr_to_hebrew(expr)));
            }
            Stmt::Expr(expr) => {
                output.push_str(&format!("  {}\n", expr_to_hebrew(expr)));
            }
            Stmt::If { condition, then_block, else_block } => {
                output.push_str(&format!("  אִם ({})\n", expr_to_hebrew(condition)));
                output.push_str(&transform_statements_to_hebrew(then_block));
                if let Some(else_stmts) = else_block {
                    output.push_str("  אַחֵר\n");
                    output.push_str(&transform_statements_to_hebrew(else_stmts));
                }
            }
            Stmt::While { condition, body } => {
                output.push_str(&format!("  בְּעוֹד ({})\n", expr_to_hebrew(condition)));
                output.push_str(&transform_statements_to_hebrew(body));
            }
        }
    }
    
    output
}

fn expr_to_hebrew(expr: &Expr) -> String {
    match expr {
        Expr::Literal(lit) => match lit {
            Literal::Number(n) => n.to_string(),
            Literal::String(s) => format!("\"{}\"", s),
            Literal::Bool(b) => if *b { "אֱמֶת" } else { "שֶׁקֶר" }.to_string(),
        },
        Expr::Identifier(name) => name.clone(),
        Expr::Binary { left, op, right } => {
            format!("({} {} {})", expr_to_hebrew(left), op, expr_to_hebrew(right))
        }
        Expr::Unary { op, expr } => {
            format!("({}{})", op, expr_to_hebrew(expr))
        }
        Expr::Call { name, args } => {
            let args_str = args.iter()
                .map(|a| expr_to_hebrew(a))
                .collect::<Vec<_>>()
                .join(", ");
            format!("{}({})", name, args_str)
        }
    }
}
