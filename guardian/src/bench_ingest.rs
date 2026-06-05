use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

/// Represents uncertainty metrics for a specific concept or operation
#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct ConceptUncertainty {
    pub tag: String,
    pub p_correct: f64,
    pub entropy: f64,
    pub alpha: f64,
    pub beta: f64,
    pub sample_size: u64,
}

/// Overall statistics from benchmark run
#[derive(Debug, Deserialize, Serialize)]
pub struct OverallStats {
    pub p_success: f64,
    pub entropy: f64,
}

/// Guardian's benchmark export format
/// This is the JSON structure exported by FlameBench after running tests
#[derive(Debug, Deserialize, Serialize)]
pub struct GuardianBenchExport {
    pub source: String,
    pub dna_strand: String,
    pub uncertainties: Vec<ConceptUncertainty>,
    pub overall: OverallStats,
}

/// Load Guardian uncertainty data from a JSON file
///
/// # Arguments
/// * `path` - Path to the guardian-uncertainty.json file
///
/// # Returns
/// * `Ok(GuardianBenchExport)` - Successfully loaded benchmark data
/// * `Err(anyhow::Error)` - Failed to read or parse the file
///
/// # Example
/// ```no_run
/// use sagco_guardian::bench_ingest::load_guardian_uncertainty;
///
/// let export = load_guardian_uncertainty("guardian-uncertainty.json")?;
/// println!("FLM2 health: p={:.3}", export.overall.p_success);
/// # Ok::<(), anyhow::Error>(())
/// ```
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
            "dna_strand": "FLM2-CMD4-MESH5-ORB1",
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
                "p_success": 0.95,
                "entropy": 0.30
            }
        }"#;

        let mut temp_file = NamedTempFile::new().unwrap();
        temp_file.write_all(json_data.as_bytes()).unwrap();
        
        let result = load_guardian_uncertainty(temp_file.path());
        assert!(result.is_ok());
        
        let export = result.unwrap();
        assert_eq!(export.source, "flamebench");
        assert_eq!(export.dna_strand, "FLM2-CMD4-MESH5-ORB1");
        assert_eq!(export.uncertainties.len(), 1);
        assert_eq!(export.overall.p_success, 0.95);
    }
}
