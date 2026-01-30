// TRIG6 Codec - Transformation layer for FlameLang
// Based on KHAOS Periodic Table's 6 families: SIN, COS, TAN, CSC, SEC, COT

use crate::ir::{FlameIR, FlameProgram};

/// TRIG6 Transformation Pass
/// Applies trigonometric modulation to the IR for optimization/obfuscation
pub struct Trig6Codec {
    /// Enable TRIG6 transformations
    pub enabled: bool,
}

impl Trig6Codec {
    pub fn new() -> Self {
        Self { enabled: true }
    }
    
    /// Apply TRIG6 transformations to a program
    pub fn transform(&self, program: &mut FlameProgram) {
        if !self.enabled {
            return;
        }
        
        // Apply TRIG6 modulation: optimize sequences, apply curve geometry
        let mut i = 0;
        while i < program.instructions.len() {
            match &program.instructions[i] {
                // Transform: LoadConst + LoadConst + Add → optimized constant
                FlameIR::LoadConst(a) => {
                    if i + 2 < program.instructions.len() {
                        if let (FlameIR::LoadConst(b), FlameIR::Add) = 
                            (&program.instructions[i + 1], &program.instructions[i + 2]) {
                            // Fold constants: a + b
                            let result = a + b;
                            program.instructions[i] = FlameIR::LoadConst(result);
                            program.instructions.remove(i + 1);
                            program.instructions.remove(i + 1);
                            continue;
                        }
                    }
                }
                _ => {}
            }
            i += 1;
        }
    }
    
    /// Apply TRIG6 sin transformation (SIN family)
    pub fn apply_sin(&self, angle: f64) -> f64 {
        // TRIG6 SIN family modulation
        // Based on French curve geometry with tan(θ) bending
        let theta = angle.to_radians();
        theta.sin()
    }
    
    /// Apply TRIG6 cos transformation (COS family)
    pub fn apply_cos(&self, angle: f64) -> f64 {
        let theta = angle.to_radians();
        theta.cos()
    }
    
    /// Apply TRIG6 tan transformation (TAN family)
    pub fn apply_tan(&self, angle: f64) -> f64 {
        let theta = angle.to_radians();
        theta.tan()
    }
}

impl Default for Trig6Codec {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_trig6_constant_folding() {
        let mut program = FlameProgram::new();
        program.push(FlameIR::LoadConst(10));
        program.push(FlameIR::LoadConst(5));
        program.push(FlameIR::Add);
        
        let codec = Trig6Codec::new();
        codec.transform(&mut program);
        
        // Should fold to single LoadConst(15)
        assert_eq!(program.instructions.len(), 1);
        assert!(matches!(program.instructions[0], FlameIR::LoadConst(15)));
    }
    
    #[test]
    fn test_trig6_sin() {
        let codec = Trig6Codec::new();
        let result = codec.apply_sin(90.0);
        assert!((result - 1.0).abs() < 0.0001);
    }
    
    #[test]
    fn test_trig6_cos() {
        let codec = Trig6Codec::new();
        let result = codec.apply_cos(0.0);
        assert!((result - 1.0).abs() < 0.0001);
    }
}
