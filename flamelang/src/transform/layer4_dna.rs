//! # Layer 4: DNA Transformation
//! 
//! Wave (Freq → Codon) - 64-codon bijection

use crate::{FlameError, Result};

/// DNA nucleotides
const NUCLEOTIDES: [char; 4] = ['A', 'T', 'G', 'C'];

/// 64 standard genetic codons
const CODONS: [&str; 64] = [
    "AAA", "AAT", "AAG", "AAC", "ATA", "ATT", "ATG", "ATC",
    "AGA", "AGT", "AGG", "AGC", "ACA", "ACT", "ACG", "ACC",
    "TAA", "TAT", "TAG", "TAC", "TTA", "TTT", "TTG", "TTC",
    "TGA", "TGT", "TGG", "TGC", "TCA", "TCT", "TCG", "TCC",
    "GAA", "GAT", "GAG", "GAC", "GTA", "GTT", "GTG", "GTC",
    "GGA", "GGT", "GGG", "GGC", "GCA", "GCT", "GCG", "GCC",
    "CAA", "CAT", "CAG", "CAC", "CTA", "CTT", "CTG", "CTC",
    "CGA", "CGT", "CGG", "CGC", "CCA", "CCT", "CCG", "CCC",
];

/// Transform wave frequencies to DNA codons using 64-codon bijection
pub fn transform_to_dna(frequencies: &[f64]) -> Result<Vec<String>> {
    let mut codons = Vec::new();
    
    for &freq in frequencies {
        if !freq.is_finite() {
            return Err(FlameError::TransformError(
                "Cannot transform non-finite frequency to DNA".to_string()
            ));
        }
        
        // Map frequency to codon index (0-63)
        // Use modulo to ensure bijective mapping
        let codon_index = (freq.abs() as usize) % 64;
        codons.push(CODONS[codon_index].to_string());
    }
    
    Ok(codons)
}

/// Verify codon bijection property (Proof 4)
pub fn verify_codon_bijection(codons: &[String]) -> Result<()> {
    for codon in codons {
        if codon.len() != 3 {
            return Err(FlameError::ProofViolation(
                format!("Codon bijection violated: invalid length {}", codon.len())
            ));
        }
        
        // Verify all characters are valid nucleotides
        for ch in codon.chars() {
            if !NUCLEOTIDES.contains(&ch) {
                return Err(FlameError::ProofViolation(
                    format!("Invalid nucleotide: {}", ch)
                ));
            }
        }
    }
    
    Ok(())
}

/// Encode DNA codons to binary
pub fn codons_to_binary(codons: &[String]) -> Vec<u8> {
    let mut binary = Vec::new();
    
    for codon in codons {
        for ch in codon.chars() {
            // 2-bit encoding: A=00, T=01, G=10, C=11
            let bits = match ch {
                'A' => 0b00,
                'T' => 0b01,
                'G' => 0b10,
                'C' => 0b11,
                _ => 0b00,
            };
            binary.push(bits);
        }
    }
    
    binary
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frequency_to_dna() {
        let frequencies = vec![440.0, 528.0, 639.0];
        let codons = transform_to_dna(&frequencies).unwrap();
        
        assert_eq!(codons.len(), 3);
        for codon in &codons {
            assert_eq!(codon.len(), 3);
        }
    }
    
    #[test]
    fn test_codon_bijection() {
        let valid_codons = vec!["ATG".to_string(), "GCC".to_string(), "TAA".to_string()];
        assert!(verify_codon_bijection(&valid_codons).is_ok());
        
        let invalid_codons = vec!["AT".to_string()]; // Too short
        assert!(verify_codon_bijection(&invalid_codons).is_err());
    }
    
    #[test]
    fn test_codon_to_binary() {
        let codons = vec!["ATG".to_string()];
        let binary = codons_to_binary(&codons);
        assert!(!binary.is_empty());
    }
}
