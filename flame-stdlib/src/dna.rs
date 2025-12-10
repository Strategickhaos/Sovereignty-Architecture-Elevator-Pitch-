//! # FLAME DNA Module - Biological Computation Layer
//! 
//! This module provides the world's first DNA-to-opcode compilation layer,
//! enabling biological computation as a first-class programming paradigm.
//! 
//! ## Key Features
//! 
//! - DNA base types (Adenine, Thymine, Guanine, Cytosine)
//! - Codon triplets (64 standard genetic code entries)
//! - RNA transcription
//! - Protein synthesis
//! - DNA sequence manipulation
//! - Codon-to-opcode compilation
//! - Biological validation
//! - Mutation operations
//! 
//! ## Example
//! 
//! ```rust
//! use flame::dna::{Base, Codon, DNASequence, AminoAcid};
//! 
//! // Create DNA sequence
//! let seq = DNASequence::from_string("ATCGTA");
//! 
//! // Transcribe to RNA
//! let rna = seq.transcribe();
//! 
//! // Translate to protein
//! let protein = seq.translate();
//! 
//! // Compile to opcodes
//! let opcodes = seq.compile_to_opcodes();
//! ```

use std::fmt;

/// DNA nucleotide bases
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Base {
    /// Adenine - pairs with Thymine (RNA: Uracil)
    Adenine,
    /// Thymine - pairs with Adenine
    Thymine,
    /// Guanine - pairs with Cytosine
    Guanine,
    /// Cytosine - pairs with Guanine
    Cytosine,
}

impl Base {
    /// Create base from character
    pub fn from_char(c: char) -> Option<Self> {
        match c.to_ascii_uppercase() {
            'A' => Some(Base::Adenine),
            'T' => Some(Base::Thymine),
            'G' => Some(Base::Guanine),
            'C' => Some(Base::Cytosine),
            _ => None,
        }
    }

    /// Convert to character
    pub fn to_char(self) -> char {
        match self {
            Base::Adenine => 'A',
            Base::Thymine => 'T',
            Base::Guanine => 'G',
            Base::Cytosine => 'C',
        }
    }

    /// Get complementary base (Watson-Crick pairing)
    pub fn complement(self) -> Self {
        match self {
            Base::Adenine => Base::Thymine,
            Base::Thymine => Base::Adenine,
            Base::Guanine => Base::Cytosine,
            Base::Cytosine => Base::Guanine,
        }
    }

    /// Transcribe to RNA base (T -> U)
    pub fn transcribe(self) -> RNABase {
        match self {
            Base::Adenine => RNABase::Adenine,
            Base::Thymine => RNABase::Uracil,
            Base::Guanine => RNABase::Guanine,
            Base::Cytosine => RNABase::Cytosine,
        }
    }

    /// Get GC content contribution (G or C = true)
    pub fn is_gc(self) -> bool {
        matches!(self, Base::Guanine | Base::Cytosine)
    }
}

impl fmt::Display for Base {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_char())
    }
}

/// RNA nucleotide bases
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum RNABase {
    Adenine,
    Uracil,
    Guanine,
    Cytosine,
}

impl RNABase {
    pub fn to_char(self) -> char {
        match self {
            RNABase::Adenine => 'A',
            RNABase::Uracil => 'U',
            RNABase::Guanine => 'G',
            RNABase::Cytosine => 'C',
        }
    }
}

/// A codon - triplet of DNA bases encoding an amino acid
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Codon(pub Base, pub Base, pub Base);

impl Codon {
    /// Create codon from three bases
    pub fn new(b1: Base, b2: Base, b3: Base) -> Self {
        Codon(b1, b2, b3)
    }

    /// Translate codon to amino acid using standard genetic code
    pub fn to_amino_acid(self) -> AminoAcid {
        use Base::*;
        match (self.0, self.1, self.2) {
            // Phenylalanine
            (Thymine, Thymine, Thymine) | (Thymine, Thymine, Cytosine) => AminoAcid::Phe,
            
            // Leucine
            (Thymine, Thymine, Adenine) | (Thymine, Thymine, Guanine) |
            (Cytosine, Thymine, _) => AminoAcid::Leu,
            
            // Isoleucine
            (Adenine, Thymine, Thymine) | (Adenine, Thymine, Cytosine) | 
            (Adenine, Thymine, Adenine) => AminoAcid::Ile,
            
            // Methionine (Start codon)
            (Adenine, Thymine, Guanine) => AminoAcid::Met,
            
            // Valine
            (Guanine, Thymine, _) => AminoAcid::Val,
            
            // Serine
            (Thymine, Cytosine, _) | (Adenine, Guanine, Thymine) | (Adenine, Guanine, Cytosine) => AminoAcid::Ser,
            
            // Proline
            (Cytosine, Cytosine, _) => AminoAcid::Pro,
            
            // Threonine
            (Adenine, Cytosine, _) => AminoAcid::Thr,
            
            // Alanine
            (Guanine, Cytosine, _) => AminoAcid::Ala,
            
            // Tyrosine
            (Thymine, Adenine, Thymine) | (Thymine, Adenine, Cytosine) => AminoAcid::Tyr,
            
            // Stop codons
            (Thymine, Adenine, Adenine) | (Thymine, Adenine, Guanine) | 
            (Thymine, Guanine, Adenine) => AminoAcid::Stop,
            
            // Histidine
            (Cytosine, Adenine, Thymine) | (Cytosine, Adenine, Cytosine) => AminoAcid::His,
            
            // Glutamine
            (Cytosine, Adenine, Adenine) | (Cytosine, Adenine, Guanine) => AminoAcid::Gln,
            
            // Asparagine
            (Adenine, Adenine, Thymine) | (Adenine, Adenine, Cytosine) => AminoAcid::Asn,
            
            // Lysine
            (Adenine, Adenine, Adenine) | (Adenine, Adenine, Guanine) => AminoAcid::Lys,
            
            // Aspartic acid
            (Guanine, Adenine, Thymine) | (Guanine, Adenine, Cytosine) => AminoAcid::Asp,
            
            // Glutamic acid
            (Guanine, Adenine, Adenine) | (Guanine, Adenine, Guanine) => AminoAcid::Glu,
            
            // Cysteine
            (Thymine, Guanine, Thymine) | (Thymine, Guanine, Cytosine) => AminoAcid::Cys,
            
            // Tryptophan
            (Thymine, Guanine, Guanine) => AminoAcid::Trp,
            
            // Arginine
            (Cytosine, Guanine, _) | (Adenine, Guanine, Adenine) | (Adenine, Guanine, Guanine) => AminoAcid::Arg,
            
            // Glycine
            (Guanine, Guanine, _) => AminoAcid::Gly,
        }
    }

    /// Compile codon to opcode (biological computation)
    pub fn to_opcode(self) -> u8 {
        // Map codon to opcode using base values
        // A=0, T=1, G=2, C=3
        let b1 = match self.0 {
            Base::Adenine => 0,
            Base::Thymine => 1,
            Base::Guanine => 2,
            Base::Cytosine => 3,
        };
        let b2 = match self.1 {
            Base::Adenine => 0,
            Base::Thymine => 1,
            Base::Guanine => 2,
            Base::Cytosine => 3,
        };
        let b3 = match self.2 {
            Base::Adenine => 0,
            Base::Thymine => 1,
            Base::Guanine => 2,
            Base::Cytosine => 3,
        };
        
        // Encode as base-4 number (0-63)
        b1 * 16 + b2 * 4 + b3
    }

    /// Convert to string representation
    pub fn to_string(self) -> String {
        format!("{}{}{}", self.0, self.1, self.2)
    }
}

/// Standard amino acids
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum AminoAcid {
    Ala, Arg, Asn, Asp, Cys, Gln, Glu, Gly, His, Ile,
    Leu, Lys, Met, Phe, Pro, Ser, Thr, Trp, Tyr, Val,
    Stop,
}

impl AminoAcid {
    /// Get three-letter code
    pub fn three_letter(self) -> &'static str {
        match self {
            AminoAcid::Ala => "Ala",
            AminoAcid::Arg => "Arg",
            AminoAcid::Asn => "Asn",
            AminoAcid::Asp => "Asp",
            AminoAcid::Cys => "Cys",
            AminoAcid::Gln => "Gln",
            AminoAcid::Glu => "Glu",
            AminoAcid::Gly => "Gly",
            AminoAcid::His => "His",
            AminoAcid::Ile => "Ile",
            AminoAcid::Leu => "Leu",
            AminoAcid::Lys => "Lys",
            AminoAcid::Met => "Met",
            AminoAcid::Phe => "Phe",
            AminoAcid::Pro => "Pro",
            AminoAcid::Ser => "Ser",
            AminoAcid::Thr => "Thr",
            AminoAcid::Trp => "Trp",
            AminoAcid::Tyr => "Tyr",
            AminoAcid::Val => "Val",
            AminoAcid::Stop => "***",
        }
    }

    /// Get single-letter code
    pub fn single_letter(self) -> char {
        match self {
            AminoAcid::Ala => 'A',
            AminoAcid::Arg => 'R',
            AminoAcid::Asn => 'N',
            AminoAcid::Asp => 'D',
            AminoAcid::Cys => 'C',
            AminoAcid::Gln => 'Q',
            AminoAcid::Glu => 'E',
            AminoAcid::Gly => 'G',
            AminoAcid::His => 'H',
            AminoAcid::Ile => 'I',
            AminoAcid::Leu => 'L',
            AminoAcid::Lys => 'K',
            AminoAcid::Met => 'M',
            AminoAcid::Phe => 'F',
            AminoAcid::Pro => 'P',
            AminoAcid::Ser => 'S',
            AminoAcid::Thr => 'T',
            AminoAcid::Trp => 'W',
            AminoAcid::Tyr => 'Y',
            AminoAcid::Val => 'V',
            AminoAcid::Stop => '*',
        }
    }
}

/// DNA sequence - the fundamental biological computation unit
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DNASequence {
    bases: Vec<Base>,
}

impl DNASequence {
    /// Create empty sequence
    pub fn new() -> Self {
        Self { bases: Vec::new() }
    }

    /// Create from string (e.g., "ATCG")
    pub fn from_string(s: &str) -> Self {
        let bases = s.chars()
            .filter_map(Base::from_char)
            .collect();
        Self { bases }
    }

    /// Create from bases
    pub fn from_bases(bases: Vec<Base>) -> Self {
        Self { bases }
    }

    /// Get length
    pub fn len(&self) -> usize {
        self.bases.len()
    }

    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.bases.is_empty()
    }

    /// Get base at position
    pub fn get(&self, index: usize) -> Option<Base> {
        self.bases.get(index).copied()
    }

    /// Get complement sequence
    pub fn complement(&self) -> Self {
        Self {
            bases: self.bases.iter().map(|b| b.complement()).collect(),
        }
    }

    /// Reverse sequence
    pub fn reverse(&self) -> Self {
        Self {
            bases: self.bases.iter().rev().copied().collect(),
        }
    }

    /// Get reverse complement
    pub fn reverse_complement(&self) -> Self {
        self.reverse().complement()
    }

    /// Transcribe DNA to RNA
    pub fn transcribe(&self) -> RNASequence {
        RNASequence {
            bases: self.bases.iter().map(|b| b.transcribe()).collect(),
        }
    }

    /// Translate to protein (amino acid sequence)
    pub fn translate(&self) -> ProteinSequence {
        let amino_acids: Vec<AminoAcid> = self.bases
            .chunks(3)
            .filter_map(|chunk| {
                if chunk.len() == 3 {
                    let codon = Codon::new(chunk[0], chunk[1], chunk[2]);
                    Some(codon.to_amino_acid())
                } else {
                    None
                }
            })
            .take_while(|aa| *aa != AminoAcid::Stop)
            .collect();
        
        ProteinSequence { amino_acids }
    }

    /// Compile to opcodes (biological computation)
    pub fn compile_to_opcodes(&self) -> Vec<u8> {
        self.bases
            .chunks(3)
            .filter_map(|chunk| {
                if chunk.len() == 3 {
                    let codon = Codon::new(chunk[0], chunk[1], chunk[2]);
                    Some(codon.to_opcode())
                } else {
                    None
                }
            })
            .collect()
    }

    /// Calculate GC content (percentage)
    pub fn gc_content(&self) -> f64 {
        if self.bases.is_empty() {
            return 0.0;
        }
        let gc_count = self.bases.iter().filter(|b| b.is_gc()).count();
        (gc_count as f64 / self.bases.len() as f64) * 100.0
    }

    /// Convert to string
    pub fn to_string(&self) -> String {
        self.bases.iter().map(|b| b.to_char()).collect()
    }

    /// Mutate base at position
    pub fn mutate(&mut self, index: usize, new_base: Base) -> Result<(), &'static str> {
        if index >= self.bases.len() {
            return Err("Index out of bounds");
        }
        self.bases[index] = new_base;
        Ok(())
    }

    /// Insert base at position
    pub fn insert(&mut self, index: usize, base: Base) -> Result<(), &'static str> {
        if index > self.bases.len() {
            return Err("Index out of bounds");
        }
        self.bases.insert(index, base);
        Ok(())
    }

    /// Delete base at position
    pub fn delete(&mut self, index: usize) -> Result<Base, &'static str> {
        if index >= self.bases.len() {
            return Err("Index out of bounds");
        }
        Ok(self.bases.remove(index))
    }
}

impl Default for DNASequence {
    fn default() -> Self {
        Self::new()
    }
}

/// RNA sequence
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RNASequence {
    bases: Vec<RNABase>,
}

impl RNASequence {
    pub fn to_string(&self) -> String {
        self.bases.iter().map(|b| b.to_char()).collect()
    }
}

/// Protein sequence (amino acid chain)
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProteinSequence {
    amino_acids: Vec<AminoAcid>,
}

impl ProteinSequence {
    /// Get length
    pub fn len(&self) -> usize {
        self.amino_acids.len()
    }

    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.amino_acids.is_empty()
    }

    /// Convert to three-letter code string
    pub fn to_string(&self) -> String {
        self.amino_acids
            .iter()
            .map(|aa| aa.three_letter())
            .collect::<Vec<_>>()
            .join("-")
    }

    /// Convert to single-letter code string
    pub fn to_single_letter(&self) -> String {
        self.amino_acids.iter().map(|aa| aa.single_letter()).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_base_complement() {
        assert_eq!(Base::Adenine.complement(), Base::Thymine);
        assert_eq!(Base::Thymine.complement(), Base::Adenine);
        assert_eq!(Base::Guanine.complement(), Base::Cytosine);
        assert_eq!(Base::Cytosine.complement(), Base::Guanine);
    }

    #[test]
    fn test_dna_sequence_from_string() {
        let seq = DNASequence::from_string("ATCG");
        assert_eq!(seq.len(), 4);
        assert_eq!(seq.to_string(), "ATCG");
    }

    #[test]
    fn test_complement() {
        let seq = DNASequence::from_string("ATCG");
        let comp = seq.complement();
        assert_eq!(comp.to_string(), "TAGC");
    }

    #[test]
    fn test_gc_content() {
        let seq = DNASequence::from_string("ATCG");
        assert_eq!(seq.gc_content(), 50.0);
    }

    #[test]
    fn test_codon_to_amino_acid() {
        let codon = Codon::new(Base::Adenine, Base::Thymine, Base::Guanine);
        assert_eq!(codon.to_amino_acid(), AminoAcid::Met);
    }

    #[test]
    fn test_translation() {
        // ATG = Met (start), GGT = Gly, TAA = Stop
        let seq = DNASequence::from_string("ATGGGTTAA");
        let protein = seq.translate();
        assert_eq!(protein.len(), 2); // Met and Gly (Stop not included)
    }
}
