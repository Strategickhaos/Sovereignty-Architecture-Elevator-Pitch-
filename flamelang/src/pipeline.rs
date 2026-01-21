//! # Compilation Pipeline
//! 
//! Orchestrates the full 5-layer transformation pipeline

use crate::{FlameResult, Target};
use crate::lexer::Lexer;
use crate::parser::Parser;
use crate::transform;

/// Compile source code through all layers to binary
pub fn compile(source: &str) -> FlameResult<Vec<u8>> {
    compile_with_target(source, Target::Native)
}

/// Compile source code to a specific target
pub fn compile_with_target(source: &str, target: Target) -> FlameResult<Vec<u8>> {
    // Layer 1: Lexical analysis (Linguistic)
    let mut lexer = Lexer::new(source);
    let tokens = lexer.tokenize()?;
    
    if target == Target::Hebrew {
        return Ok(serialize_tokens(&tokens));
    }
    
    // Parse tokens to AST
    let mut parser = Parser::new(tokens);
    let ast = parser.parse()?;
    
    // Layer 2: Numeric transformation
    let numeric = transform::transform_layer2(&ast)?;
    
    if target == Target::Numeric {
        return Ok(serialize_numeric(&numeric));
    }
    
    // Layer 3: Wave transformation
    let wave = transform::transform_layer3(&numeric)?;
    
    if target == Target::Wave {
        return Ok(serialize_wave(&wave));
    }
    
    // Layer 4: DNA transformation
    let dna = transform::transform_layer4(&wave)?;
    
    if target == Target::Dna {
        return Ok(serialize_dna(&dna));
    }
    
    // Layer 5: LLVM codegen (simplified)
    let llvm_ir = generate_llvm(&dna)?;
    
    if target == Target::LlvmIr {
        return Ok(llvm_ir.as_bytes().to_vec());
    }
    
    // Generate native binary (simplified)
    let binary = compile_to_native(&llvm_ir)?;
    
    Ok(binary)
}

fn serialize_tokens(tokens: &[crate::lexer::Token]) -> Vec<u8> {
    format!("{:?}", tokens).as_bytes().to_vec()
}

fn serialize_numeric(numeric: &transform::NumericForm) -> Vec<u8> {
    let mut bytes = Vec::new();
    for &dec in &numeric.decimals {
        bytes.extend_from_slice(&dec.to_le_bytes());
    }
    bytes
}

fn serialize_wave(wave: &transform::WaveForm) -> Vec<u8> {
    let mut bytes = Vec::new();
    for &freq in &wave.frequencies {
        bytes.extend_from_slice(&freq.to_le_bytes());
    }
    bytes
}

fn serialize_dna(dna: &transform::DnaForm) -> Vec<u8> {
    dna.sequence.as_bytes().to_vec()
}

fn generate_llvm(dna: &transform::DnaForm) -> FlameResult<String> {
    // Simplified LLVM IR generation
    let mut ir = String::new();
    
    ir.push_str("; FlameLang v2.0.0 - LLVM IR\n");
    ir.push_str("; Generated from DNA sequence\n\n");
    ir.push_str("target triple = \"x86_64-unknown-linux-gnu\"\n\n");
    
    ir.push_str(&format!("; DNA Sequence: {}\n", dna.sequence));
    ir.push_str(&format!("; Codons: {:?}\n\n", dna.codons));
    
    ir.push_str("define i32 @main() {\n");
    ir.push_str("entry:\n");
    
    // Map DNA codons to LLVM instructions
    for codon in &dna.codons {
        let opcode = codon_to_opcode(codon)?;
        ir.push_str(&format!("  {}\n", opcode));
    }
    
    ir.push_str("  ret i32 0\n");
    ir.push_str("}\n");
    
    Ok(ir)
}

fn codon_to_opcode(codon: &str) -> FlameResult<String> {
    // Simplified codon to LLVM opcode mapping
    let opcode = match codon {
        "AAA" => "%tmp0 = alloca i32",
        "AAC" => "%tmp1 = load i32, i32* %tmp0",
        "AAG" => "%tmp2 = add i32 %tmp1, 1",
        "AAU" => "store i32 %tmp2, i32* %tmp0",
        _ => "; nop",
    };
    
    Ok(opcode.to_string())
}

fn compile_to_native(llvm_ir: &str) -> FlameResult<Vec<u8>> {
    // Simplified native compilation
    // In a real implementation, this would invoke LLVM or another backend
    
    // For now, return a minimal ELF-like header with the IR as data
    let mut binary = Vec::new();
    
    // Minimal ELF header magic (not a real ELF)
    binary.extend_from_slice(b"\x7FELF");
    
    // Append LLVM IR as data section
    binary.extend_from_slice(llvm_ir.as_bytes());
    
    Ok(binary)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compile_simple() {
        let source = "let x: float = 5.0;";
        let result = compile(source);
        assert!(result.is_ok());
        let binary = result.unwrap();
        assert!(!binary.is_empty());
    }

    #[test]
    fn test_compile_with_targets() {
        let source = "let x: float = 5.0;";
        
        let hebrew = compile_with_target(source, Target::Hebrew);
        assert!(hebrew.is_ok());
        
        let numeric = compile_with_target(source, Target::Numeric);
        assert!(numeric.is_ok());
        
        let wave = compile_with_target(source, Target::Wave);
        assert!(wave.is_ok());
        
        let dna = compile_with_target(source, Target::Dna);
        assert!(dna.is_ok());
    }

    #[test]
    fn test_version_constants() {
        assert_eq!(crate::VERSION, "2.0.0");
        assert_eq!(crate::BUILD_ID, "ratio-ex-nihilo");
    }
}
