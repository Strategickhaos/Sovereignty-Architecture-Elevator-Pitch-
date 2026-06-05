//! Intermediate Representation for FlameLang
//! This is the output of the 4-layer transform (Linguistic → Numeric → Wave → DNA)

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct FlameIR {
    pub module_name: String,
    pub functions: Vec<FlameFunction>,
    pub globals: Vec<FlameGlobal>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct FlameFunction {
    pub name: String,
    pub params: Vec<FlameParam>,
    pub return_type: FlameType,
    pub body: Vec<FlameExpr>,
    /// Metadata from transforms
    pub hebrew_root: Option<String>,
    pub gematria_value: Option<u64>,
    pub frequency: Option<f64>,
    pub codon: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct FlameParam {
    pub name: String,
    pub param_type: FlameType,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct FlameGlobal {
    pub name: String,
    pub global_type: FlameType,
    pub value: FlameValue,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum FlameExpr {
    Constant(FlameValue),
    BinaryOp {
        op: FlameOp,
        left: Box<FlameExpr>,
        right: Box<FlameExpr>,
    },
    UnaryOp {
        op: FlameOp,
        operand: Box<FlameExpr>,
    },
    Call {
        function: String,
        args: Vec<FlameExpr>,
    },
    Variable(String),
    Return(Box<FlameExpr>),
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub enum FlameOp {
    // Arithmetic
    Add,
    Sub,
    Mul,
    Div,
    Mod,
    // Trigonometric (from wave layer)
    Sin,
    Cos,
    Tan,
    // FlameLang-specific operations
    Bend,      // Pipe bend operation: c=2πr
    Codon,     // DNA encoding operation
    Perm,      // Permutation operation (Rubik's cube)
    Frequency, // Wave frequency encoding
    Gematria,  // Hebrew gematria calculation
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum FlameValue {
    Integer(i64),
    Float(f64),
    Boolean(bool),
    String(String),
    Codon([u8; 3]), // DNA triplet
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum FlameType {
    I32,
    I64,
    F64,
    Bool,
    String,
    Codon,  // [u8; 3]
    Array(Box<FlameType>, usize),
    Void,
}

impl FlameIR {
    pub fn new(module_name: impl Into<String>) -> Self {
        Self {
            module_name: module_name.into(),
            functions: Vec::new(),
            globals: Vec::new(),
        }
    }
    
    pub fn add_function(&mut self, func: FlameFunction) {
        self.functions.push(func);
    }
}
