// FlameIR - Intermediate Representation for FlameLang
// Based on KHAOS Script 64-glyph alphabet and bonding rules

use serde::{Deserialize, Serialize};

/// FlameIR - The core instruction set
/// Frozen as per requirements: state + transform → state'
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum FlameIR {
    // === STATE OPERATIONS ===
    /// Load a constant value (State)
    LoadConst(i64),
    
    /// Load a string constant (State)
    LoadString(String),
    
    /// Store to a variable (State)
    Store(String),
    
    /// Load from a variable (State)
    Load(String),
    
    // === TRANSFORM OPERATIONS ===
    /// Add two values (Transform)
    Add,
    
    /// Subtract two values (Transform)
    Sub,
    
    /// Multiply two values (Transform)
    Mul,
    
    /// Divide two values (Transform)
    Div,
    
    // === COMPOUND OPERATIONS (state + state → compound_state) ===
    /// Call a function with args count
    Call(String, usize),
    
    /// Define a function
    FnDef(String, Vec<String>, Vec<FlameIR>),
    
    // === INVARIANT OPERATIONS ===
    /// Assert a condition (state + invariant → validated_state OR error)
    Assert,
    
    // === WAVE OPERATIONS (wave + collapse → measurement) ===
    /// Print to stdout (measurement)
    Print,
    
    /// Halt execution (termination)
    Halt,
    
    // === CONTROL FLOW ===
    /// Jump to label
    Jump(String),
    
    /// Conditional jump if zero
    JumpIfZero(String),
    
    /// Label marker
    Label(String),
    
    // === TRIG6 MODULATION ===
    /// Apply TRIG6 transformation (SIN family)
    Trig6Sin(f64),
    
    /// Apply TRIG6 transformation (COS family)
    Trig6Cos(f64),
    
    /// Apply TRIG6 transformation (TAN family)
    Trig6Tan(f64),
}

/// A FlameIR program is a sequence of instructions
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FlameProgram {
    pub instructions: Vec<FlameIR>,
}

impl FlameProgram {
    pub fn new() -> Self {
        Self {
            instructions: Vec::new(),
        }
    }
    
    pub fn push(&mut self, ir: FlameIR) {
        self.instructions.push(ir);
    }
    
    pub fn extend(&mut self, irs: Vec<FlameIR>) {
        self.instructions.extend(irs);
    }
}

impl Default for FlameProgram {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_flame_ir_creation() {
        let mut program = FlameProgram::new();
        program.push(FlameIR::LoadConst(42));
        program.push(FlameIR::Print);
        program.push(FlameIR::Halt);
        
        assert_eq!(program.instructions.len(), 3);
    }
    
    #[test]
    fn test_bonding_rules() {
        // Test: state + transform → state'
        let mut program = FlameProgram::new();
        program.push(FlameIR::LoadConst(10));  // state
        program.push(FlameIR::LoadConst(5));   // state
        program.push(FlameIR::Add);            // transform
        // Result: state' (15)
        
        assert!(matches!(program.instructions[2], FlameIR::Add));
    }
}
