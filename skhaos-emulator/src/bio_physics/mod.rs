// Bio-Physics Entanglement Compiler (BPEC)
// INVENTION_074 - Main module entry point
// Compiles whale/dolphin patterns + physics laws into symbolic quantum ops

pub mod zipf_analyzer;
pub mod dolphin_comm;
pub mod physics_dom;
pub mod udap_bio;

pub use zipf_analyzer::ZipfAnalyzer;
pub use dolphin_comm::{DolphinComm, SignatureWhistle, EcholocationBurst};
pub use physics_dom::{PhysicsDOM, PhysicsLaw};
pub use udap_bio::{UDAPBioParser, BioURI};

use serde::{Deserialize, Serialize};

/// Core BPEC compiler that integrates all bio-physics components
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BPECCompiler {
    pub zipf: ZipfAnalyzer,
    pub dolphin: DolphinComm,
    pub physics: PhysicsDOM,
}

impl BPECCompiler {
    /// Create a new BPEC compiler instance
    pub fn new() -> Self {
        Self {
            zipf: ZipfAnalyzer::new(),
            dolphin: DolphinComm::new(),
            physics: PhysicsDOM::new(),
        }
    }

    /// Compile bio-physics patterns into quantum operations
    pub fn compile(&self, uri: &str) -> Result<Vec<u8>, String> {
        let bio_uri = UDAPBioParser::parse(uri)?;
        
        match bio_uri.domain.as_str() {
            "zipf" => self.compile_zipf(&bio_uri),
            "dolphin" => self.compile_dolphin(&bio_uri),
            "physics" => self.compile_physics(&bio_uri),
            _ => Err(format!("Unknown bio-physics domain: {}", bio_uri.domain)),
        }
    }

    fn compile_zipf(&self, uri: &BioURI) -> Result<Vec<u8>, String> {
        let rank = uri.params.get("rank")
            .and_then(|r| r.parse::<usize>().ok())
            .unwrap_or(1);
        
        let hz = uri.params.get("hz")
            .and_then(|h| h.parse::<f64>().ok())
            .unwrap_or(20.0);

        let pattern = self.zipf.generate_pattern(rank, hz);
        Ok(pattern)
    }

    fn compile_dolphin(&self, uri: &BioURI) -> Result<Vec<u8>, String> {
        let signature = uri.params.get("signature")
            .map(|s| s == "true")
            .unwrap_or(false);
        
        let hz = uri.params.get("hz")
            .and_then(|h| h.parse::<f64>().ok())
            .unwrap_or(10.0);

        if signature {
            let whistle = self.dolphin.signature_whistle(hz, "default_pod");
            Ok(whistle.to_bytes())
        } else {
            let burst = self.dolphin.echolocation_burst(hz, 200);
            Ok(burst.to_bytes())
        }
    }

    fn compile_physics(&self, uri: &BioURI) -> Result<Vec<u8>, String> {
        let law = uri.params.get("law")
            .map(|l| l.as_str())
            .unwrap_or("entropy");
        
        let hz = uri.params.get("hz")
            .and_then(|h| h.parse::<f64>().ok())
            .unwrap_or(10.0);

        let constraint = self.physics.apply_law(law, hz)?;
        Ok(constraint)
    }

    /// Entangle whale patterns with dolphin communications
    pub fn entangle_bio(&self, whale_data: &[u8], dolphin_data: &[u8]) -> Vec<u8> {
        let mut result = Vec::new();
        
        // Apply Zipf ranking to whale data
        let whale_ranks = self.zipf.rank_units(whale_data);
        
        // Apply dolphin signature to create hybrid
        for (rank, _unit) in whale_ranks.iter().enumerate() {
            let hybrid_freq = 20.0 + (rank as f64 * 10.0);
            let whistle = self.dolphin.signature_whistle(hybrid_freq, &format!("whale_pod_{}", rank));
            result.extend_from_slice(&whistle.to_bytes());
        }
        
        // Apply physics constraints
        self.physics.apply_conservation(&result)
    }

    /// Evolve patterns using Zipf mutations with physics constraints
    pub fn evolve_with_constraints(&self, pattern: &[u8], generations: usize) -> Vec<Vec<u8>> {
        let mut evolution = Vec::new();
        let mut current = pattern.to_vec();
        
        for gen in 0..generations {
            // Apply Zipf-based mutation (frequent units mutate less)
            let mutated = self.zipf.mutate_pattern(&current, gen);
            
            // Apply physics constraint (entropy increases)
            let constrained = self.physics.apply_entropy_decay(&mutated, gen);
            
            evolution.push(constrained.clone());
            current = constrained;
        }
        
        evolution
    }
}

impl Default for BPECCompiler {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bpec_compiler_creation() {
        let compiler = BPECCompiler::new();
        assert!(compiler.zipf.rank_units(&[]).is_empty());
    }

    #[test]
    fn test_compile_zipf_uri() {
        let compiler = BPECCompiler::new();
        let result = compiler.compile("skhaos://bio/zipf/unit?rank=1&hz=20");
        assert!(result.is_ok());
    }

    #[test]
    fn test_compile_dolphin_uri() {
        let compiler = BPECCompiler::new();
        let result = compiler.compile("skhaos://bio/dolphin/whistle?signature=true&hz=10");
        assert!(result.is_ok());
    }

    #[test]
    fn test_bio_entanglement() {
        let compiler = BPECCompiler::new();
        let whale = vec![1, 2, 3, 4, 5];
        let dolphin = vec![6, 7, 8, 9, 10];
        let result = compiler.entangle_bio(&whale, &dolphin);
        assert!(!result.is_empty());
    }
}
