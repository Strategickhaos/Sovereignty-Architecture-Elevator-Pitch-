//! # Transformation Layers 2-4
//! 
//! - Layer 2: Numeric (Unicode → Decimal → Hex)
//! - Layer 3: Wave (Decimal → c=2πr → Hz/BPS)
//! - Layer 4: DNA (Freq → Codon → ACGT Sequence)

use crate::FlameResult;
use crate::parser::{AstNode, Statement, Expression};

/// Layer 2: Numeric transformation result
#[derive(Debug, Clone)]
pub struct NumericForm {
    /// Decimal values
    pub decimals: Vec<u32>,
    /// Hex representations
    pub hex: Vec<String>,
}

/// Layer 3: Wave transformation result
#[derive(Debug, Clone)]
pub struct WaveForm {
    /// Frequency values (Hz)
    pub frequencies: Vec<f64>,
    /// Bits per second
    pub bps: Vec<u64>,
}

/// Layer 4: DNA transformation result
#[derive(Debug, Clone)]
pub struct DnaForm {
    /// Codon sequences
    pub codons: Vec<String>,
    /// ACGT sequence
    pub sequence: String,
}

/// Transform AST through Layer 2 (Numeric)
pub fn transform_layer2(ast: &AstNode) -> FlameResult<NumericForm> {
    let mut decimals = Vec::new();
    let mut hex = Vec::new();
    
    // Extract numeric values from AST
    if let AstNode::Program(statements) = ast {
        for stmt in statements {
            match stmt {
                Statement::LetBinding { value, .. } => {
                    if let Expression::Number(n) = value {
                        let dec = *n as u32;
                        decimals.push(dec);
                        hex.push(format!("0x{:X}", dec));
                    }
                }
                Statement::Bend { angle, radius } => {
                    if let Expression::Number(a) = angle {
                        let dec = *a as u32;
                        decimals.push(dec);
                        hex.push(format!("0x{:X}", dec));
                    }
                    if let Expression::Number(r) = radius {
                        let dec = *r as u32;
                        decimals.push(dec);
                        hex.push(format!("0x{:X}", dec));
                    }
                }
            }
        }
    }
    
    Ok(NumericForm { decimals, hex })
}

/// Transform numeric form through Layer 3 (Wave)
pub fn transform_layer3(numeric: &NumericForm) -> FlameResult<WaveForm> {
    let mut frequencies = Vec::new();
    let mut bps = Vec::new();
    
    // c = 2πr formula: convert decimals to frequencies
    for &dec in &numeric.decimals {
        let radius = dec as f64;
        let circumference = 2.0 * std::f64::consts::PI * radius;
        let freq = circumference * 1e6; // Scale to Hz
        frequencies.push(freq);
        
        // Convert to bits per second (simplified)
        let bits = (freq / 8.0) as u64;
        bps.push(bits);
    }
    
    Ok(WaveForm { frequencies, bps })
}

/// Transform wave form through Layer 4 (DNA)
pub fn transform_layer4(wave: &WaveForm) -> FlameResult<DnaForm> {
    let mut codons = Vec::new();
    let mut sequence = String::new();
    
    // Map frequencies to DNA codons
    for &freq in &wave.frequencies {
        let codon = freq_to_codon(freq)?;
        codons.push(codon.clone());
        sequence.push_str(&codon_to_acgt(&codon));
    }
    
    Ok(DnaForm { codons, sequence })
}

/// Map frequency to codon (64 possible codons)
fn freq_to_codon(freq: f64) -> FlameResult<String> {
    // DNA codons: 4 bases (A, C, G, T/U) × 3 positions = 64 possible codons
    let bases = ['A', 'C', 'G', 'U'];
    let index = (freq as u64) % 64;
    
    // Decode index to 3-base codon
    let base1 = bases[(index / 16) as usize % 4];
    let base2 = bases[(index / 4) as usize % 4];
    let base3 = bases[(index % 4) as usize];
    
    Ok(format!("{}{}{}", base1, base2, base3))
}

/// Convert codon to ACGT sequence (replace U with T for DNA)
fn codon_to_acgt(codon: &str) -> String {
    codon.replace('U', "T")
}

/// Apply all transformation layers
pub fn transform_all(ast: &AstNode) -> FlameResult<DnaForm> {
    let numeric = transform_layer2(ast)?;
    let wave = transform_layer3(&numeric)?;
    let dna = transform_layer4(&wave)?;
    Ok(dna)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::Lexer;
    use crate::parser::Parser;

    #[test]
    fn test_transform_layer2() {
        let mut lexer = Lexer::new("let x: float = 5.0;");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();
        
        let numeric = transform_layer2(&ast).unwrap();
        assert!(!numeric.decimals.is_empty());
        assert!(!numeric.hex.is_empty());
    }

    #[test]
    fn test_transform_layer3() {
        let numeric = NumericForm {
            decimals: vec![5],
            hex: vec!["0x5".to_string()],
        };
        
        let wave = transform_layer3(&numeric).unwrap();
        assert!(!wave.frequencies.is_empty());
        assert!(!wave.bps.is_empty());
    }

    #[test]
    fn test_transform_layer4() {
        let wave = WaveForm {
            frequencies: vec![440.0],
            bps: vec![55],
        };
        
        let dna = transform_layer4(&wave).unwrap();
        assert!(!dna.codons.is_empty());
        assert!(!dna.sequence.is_empty());
    }
}
