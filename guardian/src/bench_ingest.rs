// Guardian Benchmark Ingest Module
// Loads flamebench results and uncertainty exports

use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Deserialize, Serialize)]
pub struct ConceptUncertainty {
    pub tag: String,
    pub p_correct: f64,
    pub entropy: f64,
    pub alpha: f64,
    pub beta: f64,
    pub sample_size: u64,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct OverallStats {
    pub p_success: f64,
    pub entropy: f64,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct GuardianBenchExport {
    pub source: String,
    pub dna_strand: String,
    pub uncertainties: Vec<ConceptUncertainty>,
    pub overall: OverallStats,
}

/// Load guardian uncertainty export from JSON file
pub fn load_guardian_uncertainty<P: AsRef<Path>>(
    path: P,
) -> anyhow::Result<GuardianBenchExport> {
    let txt = fs::read_to_string(path)?;
    let export: GuardianBenchExport = serde_json::from_str(&txt)?;
    Ok(export)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    #[test]
    fn test_load_guardian_uncertainty() {
        let json_data = r#"{
            "source": "flamebench",
            "dna_strand": "FLM2-CMD1-MESH5-ORB1",
            "uncertainties": [
                {
                    "tag": "if-else",
                    "p_correct": 0.96,
                    "entropy": 0.25,
                    "alpha": 48.0,
                    "beta": 2.0,
                    "sample_size": 50
                }
            ],
            "overall": {
                "p_success": 0.96,
                "entropy": 0.25
            }
        }"#;

        let mut temp_file = NamedTempFile::new().unwrap();
        temp_file.write_all(json_data.as_bytes()).unwrap();
        
        let result = load_guardian_uncertainty(temp_file.path());
        assert!(result.is_ok());
        
        let export = result.unwrap();
        assert_eq!(export.source, "flamebench");
        assert_eq!(export.overall.p_success, 0.96);
    }
}
