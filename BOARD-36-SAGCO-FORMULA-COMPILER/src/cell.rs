use serde::{Deserialize, Serialize};

/// Runtime value of a cell
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum Value {
    Number(f64),
    Str(String),
    Bool(bool),
    Error(String),
    Empty,
}

impl Value {
    pub fn is_error(&self) -> bool {
        matches!(self, Value::Error(_))
    }

    pub fn as_number(&self) -> Option<f64> {
        match self {
            Value::Number(n) => Some(*n),
            Value::Str(s) => s.parse().ok(),
            Value::Bool(b) => Some(if *b { 1.0 } else { 0.0 }),
            _ => None,
        }
    }

    pub fn as_bool(&self) -> bool {
        match self {
            Value::Bool(b) => *b,
            Value::Number(n) => *n != 0.0,
            Value::Str(s) => !s.is_empty(),
            Value::Empty => false,
            Value::Error(_) => false,
        }
    }

    pub fn as_str(&self) -> String {
        match self {
            Value::Number(n) => {
                if n.fract() == 0.0 {
                    format!("{}", *n as i64)
                } else {
                    format!("{}", n)
                }
            }
            Value::Str(s) => s.clone(),
            Value::Bool(b) => if *b { "TRUE".to_string() } else { "FALSE".to_string() },
            Value::Error(e) => e.clone(),
            Value::Empty => String::new(),
        }
    }
}

impl std::fmt::Display for Value {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.as_str())
    }
}

/// A single spreadsheet cell
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Cell {
    pub addr: String,
    pub formula: String, // raw formula string (may start with '=')
    pub value: Value,
    pub deps: Vec<String>, // cell addresses this cell depends on
    pub dirty: bool,
}

impl Cell {
    pub fn new(addr: impl Into<String>, formula: impl Into<String>) -> Self {
        Cell {
            addr: addr.into(),
            formula: formula.into(),
            value: Value::Empty,
            deps: Vec::new(),
            dirty: true,
        }
    }

    pub fn is_formula(&self) -> bool {
        self.formula.starts_with('=')
    }

    pub fn literal_value(&self) -> Option<Value> {
        if self.is_formula() {
            return None;
        }
        let s = self.formula.trim();
        // Try number
        if let Ok(n) = s.parse::<f64>() {
            return Some(Value::Number(n));
        }
        // Strip surrounding quotes
        if s.starts_with('"') && s.ends_with('"') && s.len() >= 2 {
            return Some(Value::Str(s[1..s.len() - 1].to_string()));
        }
        // Bool
        match s.to_uppercase().as_str() {
            "TRUE" => return Some(Value::Bool(true)),
            "FALSE" => return Some(Value::Bool(false)),
            _ => {}
        }
        Some(Value::Str(s.to_string()))
    }
}
