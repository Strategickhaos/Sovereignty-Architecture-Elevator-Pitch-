use crate::cell::Value;
use std::collections::HashMap;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum EvalError {
    #[error("Unknown function: {0}")]
    UnknownFunction(String),
    #[error("Wrong number of arguments for {0}: expected {1}, got {2}")]
    WrongArgCount(String, String, usize),
    #[error("Type error in {0}: {1}")]
    TypeError(String, String),
    #[error("Division by zero")]
    DivisionByZero,
    #[error("Circular reference: {0}")]
    CircularRef(String),
    #[error("Cell not found: {0}")]
    CellNotFound(String),
    #[error("{0}")]
    Other(String),
}

pub type Func = fn(&[Value]) -> Result<Value, EvalError>;

/// Registry of named functions callable from formulas
pub struct FuncRegistry {
    funcs: HashMap<String, Func>,
}

impl FuncRegistry {
    pub fn new() -> Self {
        FuncRegistry {
            funcs: HashMap::new(),
        }
    }

    pub fn register(&mut self, name: &str, func: Func) {
        self.funcs.insert(name.to_uppercase(), func);
    }

    pub fn call(&self, name: &str, args: &[Value]) -> Result<Value, EvalError> {
        match self.funcs.get(&name.to_uppercase()) {
            Some(f) => f(args),
            None => Err(EvalError::UnknownFunction(name.to_string())),
        }
    }

    pub fn list(&self) -> Vec<String> {
        let mut names: Vec<String> = self.funcs.keys().cloned().collect();
        names.sort();
        names
    }

    pub fn has(&self, name: &str) -> bool {
        self.funcs.contains_key(&name.to_uppercase())
    }
}

impl Default for FuncRegistry {
    fn default() -> Self {
        Self::new()
    }
}
