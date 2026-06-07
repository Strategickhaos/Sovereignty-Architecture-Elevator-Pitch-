pub mod lex_pass;
pub mod parse_pass;
pub mod semantic_pass;
pub mod unit_pass;
pub mod guard_pass;
pub mod eru_pass;

use crate::sheet::Sheet;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PassResult {
    pub pass_name: String,
    pub passed: bool,
    pub warnings: Vec<String>,
    pub errors: Vec<String>,
}

impl PassResult {
    pub fn new(pass_name: &str) -> Self {
        PassResult {
            pass_name: pass_name.to_string(),
            passed: true,
            warnings: Vec::new(),
            errors: Vec::new(),
        }
    }

    pub fn add_error(&mut self, e: impl Into<String>) {
        self.errors.push(e.into());
        self.passed = false;
    }

    pub fn add_warning(&mut self, w: impl Into<String>) {
        self.warnings.push(w.into());
    }
}

impl std::fmt::Display for PassResult {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let status = if self.passed { "PASS" } else { "FAIL" };
        write!(f, "[{}] {}", status, self.pass_name)?;
        for e in &self.errors {
            write!(f, "\n  ERROR: {}", e)?;
        }
        for w in &self.warnings {
            write!(f, "\n  WARN:  {}", w)?;
        }
        Ok(())
    }
}

pub trait Pipeline {
    fn run(&self, sheet: &mut Sheet) -> PassResult;
}
