/// Transform Layer 5: DNA/Periodic Table + LLVM Base
/// Maps vectors to ACGT/codons and periodic elements
/// Begins LLVM IR generation with base structures

use crate::transform::layer4_wave::{WaveAst, QuantumOperation, WaveType};

#[derive(Debug, Clone)]
pub struct DnaLlvmAst {
    pub dna_sequences: Vec<DnaSequence>,
    pub llvm_base: String,
}

#[derive(Debug, Clone)]
pub struct DnaSequence {
    pub sequence: String,  // ACGT sequence
    pub element: String,   // Periodic table element
    pub atomic_number: u8,
    pub quantum_ref: String,
}

pub fn transform(wave_ast: WaveAst) -> Result<DnaLlvmAst, String> {
    let dna_sequences = wave_ast.quantum_ops.iter()
        .map(|qop| encode_to_dna(qop))
        .collect();
    
    let llvm_base = generate_llvm_base(&wave_ast);
    
    Ok(DnaLlvmAst { dna_sequences, llvm_base })
}

fn encode_to_dna(qop: &QuantumOperation) -> DnaSequence {
    // Convert quantum parameters to binary, then to ACGT
    let amplitude_bits = (qop.parameters.amplitude * 100.0) as u32;
    let frequency_bits = (qop.parameters.frequency * 100.0) as u32;
    
    let binary = format!("{:08b}{:08b}", amplitude_bits & 0xFF, frequency_bits & 0xFF);
    let sequence = binary_to_acgt(&binary);
    
    // Map to periodic table element based on atomic number
    let atomic_number = calculate_atomic_number(&qop.parameters);
    let element = get_element_symbol(atomic_number);
    
    DnaSequence {
        sequence,
        element,
        atomic_number,
        quantum_ref: qop.glyph_ref.clone(),
    }
}

fn binary_to_acgt(binary: &str) -> String {
    // Convert binary pairs to ACGT: 00=A, 01=C, 10=G, 11=T
    binary.chars()
        .collect::<Vec<_>>()
        .chunks(2)
        .map(|chunk| {
            match chunk {
                ['0', '0'] => 'A',
                ['0', '1'] => 'C',
                ['1', '0'] => 'G',
                ['1', '1'] => 'T',
                ['0'] => 'A',
                ['1'] => 'G',
                _ => 'A',
            }
        })
        .collect()
}

fn calculate_atomic_number(params: &crate::transform::layer4_wave::QuantumParams) -> u8 {
    // Map quantum parameters to atomic number (mod 118 for valid elements)
    let combined = (params.amplitude * 10.0 + params.frequency + params.damping * 100.0).abs();
    ((combined * 10.0) as u32 % 118 + 1) as u8
}

fn get_element_symbol(atomic_number: u8) -> String {
    // Simplified periodic table mapping
    match atomic_number {
        1 => "H",
        2 => "He",
        6 => "C",
        7 => "N",
        8 => "O",
        26 => "Fe",
        29 => "Cu",
        47 => "Ag",
        79 => "Au",
        _ => "X",  // Generic element
    }.to_string()
}

fn generate_llvm_base(wave_ast: &WaveAst) -> String {
    let mut ir = String::new();
    
    // LLVM module header
    ir.push_str("; FlameLang Compiler Output\n");
    ir.push_str("; Generated LLVM IR for quantum/CMB simulation\n\n");
    ir.push_str("target datalayout = \"e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128\"\n");
    ir.push_str("target triple = \"x86_64-unknown-linux-gnu\"\n\n");
    
    // Define common structures
    ir.push_str("; Quantum parameter structure\n");
    ir.push_str("%QuantumParams = type { double, double, double, double }\n\n");
    
    // Declare math intrinsics
    ir.push_str("declare double @llvm.exp.f64(double)\n");
    ir.push_str("declare double @llvm.sin.f64(double)\n");
    ir.push_str("declare double @llvm.cos.f64(double)\n");
    ir.push_str("declare double @llvm.pow.f64(double, double)\n");
    ir.push_str("declare double @llvm.sqrt.f64(double)\n\n");
    
    // Generate functions for each quantum operation
    for (idx, qop) in wave_ast.quantum_ops.iter().enumerate() {
        ir.push_str(&generate_quantum_function(idx, qop));
        ir.push_str("\n");
    }
    
    // Main function stub
    ir.push_str("define i32 @main() {\n");
    ir.push_str("entry:\n");
    ir.push_str("  ; Initialize quantum simulation\n");
    
    for idx in 0..wave_ast.quantum_ops.len() {
        ir.push_str(&format!("  %result{} = call double @quantum_op_{}(double 1.0)\n", idx, idx));
    }
    
    ir.push_str("  ret i32 0\n");
    ir.push_str("}\n");
    
    ir
}

fn generate_quantum_function(idx: usize, qop: &QuantumOperation) -> String {
    let mut func = String::new();
    
    let func_name = match qop.wave_type {
        WaveType::Bounce => "bounce",
        WaveType::Fluctuation => "fluctuate",
        WaveType::Suppression => "suppress",
        WaveType::Observation => "observe",
        WaveType::Unification => "unify",
        WaveType::Anomaly => "anomaly",
    };
    
    func.push_str(&format!("; {} operation ({})\n", func_name, qop.glyph_ref));
    func.push_str(&format!("define double @quantum_op_{}(double %l) {{\n", idx));
    func.push_str("entry:\n");
    
    // Generate IR based on wave type
    match qop.wave_type {
        WaveType::Bounce => {
            // exp(-l/τ) suppression
            let tau = qop.parameters.damping;
            func.push_str(&format!("  %neg_l = fneg double %l\n"));
            func.push_str(&format!("  %div = fdiv double %neg_l, {}\n", tau));
            func.push_str("  %result = call double @llvm.exp.f64(double %div)\n");
        }
        WaveType::Fluctuation => {
            // Add Gaussian noise (simplified as sine modulation)
            let amp = qop.parameters.amplitude;
            func.push_str(&format!("  %scaled = fmul double %l, {}\n", amp));
            func.push_str("  %result = call double @llvm.sin.f64(double %scaled)\n");
        }
        WaveType::Suppression => {
            // Multiply by suppression factor
            let factor = 1.0 - qop.parameters.damping;
            func.push_str(&format!("  %result = fmul double %l, {}\n", factor));
        }
        _ => {
            // Generic: return input scaled by amplitude
            func.push_str(&format!("  %result = fmul double %l, {}\n", qop.parameters.amplitude));
        }
    }
    
    func.push_str("  ret double %result\n");
    func.push_str("}\n");
    
    func
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_binary_to_acgt() {
        let binary = "00011011";
        let acgt = binary_to_acgt(binary);
        assert_eq!(acgt, "ACGT");
    }

    #[test]
    fn test_dna_encoding() {
        let qop = QuantumOperation {
            wave_type: WaveType::Bounce,
            parameters: crate::transform::layer4_wave::QuantumParams {
                amplitude: 1.0,
                frequency: 1.0,
                phase: 0.0,
                damping: 0.065,
            },
            glyph_ref: "⚛️".to_string(),
        };
        
        let dna = encode_to_dna(&qop);
        assert_eq!(dna.sequence.len(), 8);  // 16 bits / 2 = 8 ACGT chars
        assert!(dna.atomic_number >= 1 && dna.atomic_number <= 118);
    }

    #[test]
    fn test_llvm_base_generation() {
        let wave_ast = WaveAst {
            quantum_ops: vec![QuantumOperation {
                wave_type: WaveType::Bounce,
                parameters: crate::transform::layer4_wave::QuantumParams::default(),
                glyph_ref: "⚛️".to_string(),
            }],
        };
        
        let ir = generate_llvm_base(&wave_ast);
        assert!(ir.contains("define double @quantum_op_0"));
        assert!(ir.contains("@llvm.exp.f64"));
    }
}
