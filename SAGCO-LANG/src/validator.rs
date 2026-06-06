use crate::ast::Program;
use std::collections::HashSet;

pub fn validate(prog: &Program) -> Vec<String> {
    let mut errors = Vec::new();
    let mut seen = HashSet::new();
    for brick in &prog.bricks {
        if !seen.insert(brick.name.clone()) {
            errors.push(format!("duplicate brick name: {}", brick.name));
        }
        if brick.route.from.path.is_empty() {
            errors.push(format!("brick {}: empty from-pad", brick.name));
        }
        if brick.route.to.path.is_empty() {
            errors.push(format!("brick {}: empty to-pad", brick.name));
        }
    }
    errors
}
