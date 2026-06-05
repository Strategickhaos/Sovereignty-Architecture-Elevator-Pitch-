//! # FlameLang Compilation Pipeline
//! 
//! Orchestrates the complete 5-layer transformation with proof validation.

use flamelang::lexer::Lexer;
use flamelang::parser::Parser;
use flamelang::transform::*;
use flamelang::Result;

pub fn compile(source: &str) -> Result<Vec<u8>> {
    println!("   Pipeline:");
    
    // Step 1: Lexical Analysis
    println!("   ├── Lexing...");
    let mut lexer = Lexer::new(source);
    let tokens = lexer.tokenize()?;
    
    // Step 2: Parsing
    println!("   ├── Parsing...");
    let mut parser = Parser::new(tokens);
    let ast = parser.parse()?;
    
    // Step 3: Layer 1 - Linguistic (English → Hebrew)
    println!("   ├── Layer 1: Linguistic (English → Hebrew)");
    let hebrew_text = layer1_linguistic::transform_to_hebrew(&ast)?;
    
    // Step 4: Layer 2 - Numeric (Hebrew → Gematria)
    println!("   ├── Layer 2: Numeric (Unicode → Gematria)");
    let gematria_values = layer2_numeric::transform_to_gematria(&hebrew_text)?;
    
    // Step 5: Layer 3 - Wave (Gematria → Hz)
    println!("   ├── Layer 3: Wave (c=2πr → Hz)");
    let wave_frequencies = layer3_wave::transform_to_wave(&gematria_values)?;
    
    // Step 6: Layer 4 - DNA (Freq → Codon)
    println!("   ├── Layer 4: DNA (Freq → Codon)");
    let dna_codons = layer4_dna::transform_to_dna(&wave_frequencies)?;
    
    // Step 7: Create FlameIR
    let ir = FlameIR {
        hebrew_text,
        gematria_values,
        wave_frequencies,
        dna_codons: dna_codons.clone(),
    };
    
    // Step 8: Proof Validation (THE IMMUNITY LAYER)
    println!("   ├── Proof Validation (16 theorems)");
    validate_proofs(&ir)?;
    
    // Step 9: Layer 5 - LLVM IR Generation
    println!("   ├── Layer 5: LLVM IR Generation");
    let llvm_ir = layer5_llvm::generate_llvm_ir(&ast, &dna_codons)?;
    
    // Step 10: Verify codon bijection
    layer4_dna::verify_codon_bijection(&dna_codons)?;
    
    println!("   └── Binary Generation");
    
    // Convert LLVM IR to bytes (in a real implementation, this would use LLVM to compile)
    // For now, we'll return the IR as bytes
    Ok(llvm_ir.into_bytes())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_program() {
        let source = r#"
            fn main() {
                return 42;
            }
        "#;
        
        let result = compile(source);
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_arithmetic() {
        let source = r#"
            fn add(a, b) {
                return a + b;
            }
        "#;
        
        let result = compile(source);
        assert!(result.is_ok());
    }
}
