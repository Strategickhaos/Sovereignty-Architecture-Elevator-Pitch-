//! Layer 1: Linguistic Transform
//! English → Hebrew triconsonantal roots

use crate::FlameResult;
use crate::ast::Program;
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct HebrewAST {
    pub program: Program,
    pub root_mappings: HashMap<String, String>,
}

/// Transform English identifiers to Hebrew roots
pub fn transform(program: &Program) -> FlameResult<HebrewAST> {
    let mut root_mappings = HashMap::new();
    
    // Basic root mappings (simplified)
    root_mappings.insert("main".to_string(), "אמת".to_string()); // emet = truth
    root_mappings.insert("add".to_string(), "חבר".to_string());  // chaver = connect
    root_mappings.insert("sub".to_string(), "גרע".to_string());  // gara = reduce
    root_mappings.insert("mul".to_string(), "רבה".to_string());  // rabah = multiply
    root_mappings.insert("div".to_string(), "חלק".to_string());  // chalak = divide
    
    Ok(HebrewAST {
        program: program.clone(),
        root_mappings,
    })
}
