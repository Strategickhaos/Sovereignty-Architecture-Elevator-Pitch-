// Dolphin Communication Patterns
// - Signature whistles: 1-20kHz, unique ID "names" for individuals
// - Echolocation clicks: 120-200kHz burst pulses for navigation/hunting
// - Pod dialects: Matrilineal learning, culturally transmitted

use std::collections::HashMap;

/// Dolphin communication pattern analyzer
pub struct DolphinComm {
    pub whistles: Vec<SignatureWhistle>,
    pub clicks: Vec<EcholocationClick>,
    pub dialects: HashMap<String, PodDialect>,
}

/// Signature whistle - unique identifier for individual dolphins
#[derive(Debug, Clone)]
pub struct SignatureWhistle {
    pub dolphin_id: String,
    pub frequency_contour: Vec<f64>,  // Hz over time (1-20kHz range)
    pub duration_ms: f64,
    pub pod_id: String,
    pub learned_from: Option<String>,  // Matrilineal transmission
}

/// Echolocation click burst for navigation and object detection
#[derive(Debug, Clone)]
pub struct EcholocationClick {
    pub click_id: String,
    pub center_frequency_khz: f64,     // 120-200kHz
    pub bandwidth_khz: f64,
    pub inter_click_interval_ms: f64,  // Rapid succession
    pub burst_count: u32,
    pub purpose: EcholocationPurpose,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum EcholocationPurpose {
    Navigation,
    Hunting,
    SocialInteraction,
    ObjectIdentification,
}

/// Pod-specific dialect (culturally learned patterns)
#[derive(Debug, Clone)]
pub struct PodDialect {
    pub pod_id: String,
    pub matriline: String,              // Maternal lineage
    pub call_repertoire: Vec<String>,   // Unique vocalizations
    pub whistle_variants: Vec<String>,  // Dialect-specific whistle types
    pub geographic_region: String,
}

impl DolphinComm {
    /// Create new dolphin communication analyzer
    pub fn new() -> Self {
        Self {
            whistles: Vec::new(),
            clicks: Vec::new(),
            dialects: HashMap::new(),
        }
    }

    /// Add signature whistle
    pub fn add_whistle(&mut self, whistle: SignatureWhistle) {
        self.whistles.push(whistle);
    }

    /// Add echolocation click burst
    pub fn add_click(&mut self, click: EcholocationClick) {
        self.clicks.push(click);
    }

    /// Register pod dialect
    pub fn register_dialect(&mut self, dialect: PodDialect) {
        self.dialects.insert(dialect.pod_id.clone(), dialect);
    }

    /// Find dolphin by signature whistle similarity
    pub fn identify_by_whistle(&self, contour: &[f64]) -> Option<String> {
        for whistle in &self.whistles {
            if self.contour_similarity(&whistle.frequency_contour, contour) > 0.8 {
                return Some(whistle.dolphin_id.clone());
            }
        }
        None
    }

    /// Calculate frequency contour similarity (simple correlation)
    fn contour_similarity(&self, contour1: &[f64], contour2: &[f64]) -> f64 {
        if contour1.len() != contour2.len() || contour1.is_empty() {
            return 0.0;
        }

        let mean1: f64 = contour1.iter().sum::<f64>() / contour1.len() as f64;
        let mean2: f64 = contour2.iter().sum::<f64>() / contour2.len() as f64;

        let mut numerator = 0.0;
        let mut sum_sq1 = 0.0;
        let mut sum_sq2 = 0.0;

        for i in 0..contour1.len() {
            let diff1 = contour1[i] - mean1;
            let diff2 = contour2[i] - mean2;
            numerator += diff1 * diff2;
            sum_sq1 += diff1 * diff1;
            sum_sq2 += diff2 * diff2;
        }

        if sum_sq1 == 0.0 || sum_sq2 == 0.0 {
            return 0.0;
        }

        numerator / (sum_sq1 * sum_sq2).sqrt()
    }

    /// Analyze echolocation click pattern
    pub fn analyze_clicks(&self, click_id: &str) -> Option<ClickAnalysis> {
        let click = self.clicks.iter().find(|c| c.click_id == click_id)?;

        Some(ClickAnalysis {
            frequency_range: (
                click.center_frequency_khz - click.bandwidth_khz / 2.0,
                click.center_frequency_khz + click.bandwidth_khz / 2.0,
            ),
            pulse_rate_hz: if click.inter_click_interval_ms > 0.0 {
                1000.0 / click.inter_click_interval_ms
            } else {
                0.0
            },
            purpose: click.purpose,
            efficiency_score: self.calculate_efficiency(click),
        })
    }

    /// Calculate echolocation efficiency (higher frequency = better resolution)
    fn calculate_efficiency(&self, click: &EcholocationClick) -> f64 {
        // Higher center frequency and wider bandwidth = better resolution
        let freq_factor = click.center_frequency_khz / 200.0; // Normalize to max 200kHz
        let bandwidth_factor = click.bandwidth_khz / 50.0;     // Assume 50kHz good bandwidth
        (freq_factor + bandwidth_factor) / 2.0
    }

    /// Get pod dialect information
    pub fn get_dialect(&self, pod_id: &str) -> Option<&PodDialect> {
        self.dialects.get(pod_id)
    }

    /// Convert whistle to UDAP URI
    pub fn whistle_to_udap(&self, whistle_id: &str) -> Option<String> {
        let whistle = self.whistles.iter().find(|w| w.dolphin_id == whistle_id)?;
        
        let avg_freq = if !whistle.frequency_contour.is_empty() {
            whistle.frequency_contour.iter().sum::<f64>() / whistle.frequency_contour.len() as f64
        } else {
            10000.0 // Default mid-range
        };

        Some(format!(
            "skhaos://bio/dolphin/whistle?signature=true&pod={}&hz={}",
            whistle.pod_id,
            avg_freq as u32
        ))
    }

    /// Convert echolocation to UDAP URI
    pub fn click_to_udap(&self, click_id: &str) -> Option<String> {
        let click = self.clicks.iter().find(|c| c.click_id == click_id)?;
        
        Some(format!(
            "skhaos://bio/dolphin/click?burst={}&hz={}&purpose={:?}",
            click.burst_count,
            (click.center_frequency_khz * 1000.0) as u32,
            click.purpose
        ))
    }

    /// Generate statistics
    pub fn stats(&self) -> DolphinStats {
        let total_pods = self.dialects.len();
        let total_whistles = self.whistles.len();
        let total_clicks = self.clicks.len();

        let avg_whistle_freq = if !self.whistles.is_empty() {
            let sum: f64 = self.whistles.iter()
                .filter(|w| !w.frequency_contour.is_empty())
                .map(|w| w.frequency_contour.iter().sum::<f64>() / w.frequency_contour.len() as f64)
                .sum();
            sum / self.whistles.len() as f64
        } else {
            0.0
        };

        let avg_click_freq = if !self.clicks.is_empty() {
            self.clicks.iter()
                .map(|c| c.center_frequency_khz)
                .sum::<f64>() / self.clicks.len() as f64
        } else {
            0.0
        };

        DolphinStats {
            total_pods,
            total_whistles,
            total_clicks,
            avg_whistle_frequency_hz: avg_whistle_freq,
            avg_click_frequency_khz: avg_click_freq,
        }
    }
}

#[derive(Debug)]
pub struct ClickAnalysis {
    pub frequency_range: (f64, f64),  // kHz
    pub pulse_rate_hz: f64,
    pub purpose: EcholocationPurpose,
    pub efficiency_score: f64,
}

#[derive(Debug)]
pub struct DolphinStats {
    pub total_pods: usize,
    pub total_whistles: usize,
    pub total_clicks: usize,
    pub avg_whistle_frequency_hz: f64,
    pub avg_click_frequency_khz: f64,
}

impl Default for DolphinComm {
    fn default() -> Self {
        Self::new()
    }
}

/// Helper function to generate sample dolphin patterns
pub fn sample_dolphin_patterns() -> DolphinComm {
    let mut comm = DolphinComm::new();

    // Add signature whistles
    comm.add_whistle(SignatureWhistle {
        dolphin_id: "alpha_001".to_string(),
        frequency_contour: vec![5000.0, 8000.0, 12000.0, 8000.0, 5000.0],
        duration_ms: 800.0,
        pod_id: "matrilineal_a".to_string(),
        learned_from: Some("mother_alpha".to_string()),
    });

    comm.add_whistle(SignatureWhistle {
        dolphin_id: "beta_002".to_string(),
        frequency_contour: vec![3000.0, 10000.0, 15000.0, 10000.0, 3000.0],
        duration_ms: 950.0,
        pod_id: "matrilineal_a".to_string(),
        learned_from: Some("mother_beta".to_string()),
    });

    // Add echolocation clicks
    comm.add_click(EcholocationClick {
        click_id: "nav_001".to_string(),
        center_frequency_khz: 120.0,
        bandwidth_khz: 40.0,
        inter_click_interval_ms: 50.0,
        burst_count: 10,
        purpose: EcholocationPurpose::Navigation,
    });

    comm.add_click(EcholocationClick {
        click_id: "hunt_001".to_string(),
        center_frequency_khz: 180.0,
        bandwidth_khz: 50.0,
        inter_click_interval_ms: 20.0,
        burst_count: 25,
        purpose: EcholocationPurpose::Hunting,
    });

    // Register pod dialect
    comm.register_dialect(PodDialect {
        pod_id: "matrilineal_a".to_string(),
        matriline: "grandmother_alpha_lineage".to_string(),
        call_repertoire: vec![
            "greeting_chirp".to_string(),
            "distress_scream".to_string(),
            "play_whistle".to_string(),
        ],
        whistle_variants: vec![
            "rising_contour".to_string(),
            "falling_contour".to_string(),
            "loop_contour".to_string(),
        ],
        geographic_region: "Pacific_Northwest".to_string(),
    });

    comm
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dolphin_comm_creation() {
        let comm = DolphinComm::new();
        assert_eq!(comm.whistles.len(), 0);
        assert_eq!(comm.clicks.len(), 0);
    }

    #[test]
    fn test_sample_patterns() {
        let comm = sample_dolphin_patterns();
        assert_eq!(comm.whistles.len(), 2);
        assert_eq!(comm.clicks.len(), 2);
        assert_eq!(comm.dialects.len(), 1);
    }

    #[test]
    fn test_whistle_to_udap() {
        let comm = sample_dolphin_patterns();
        let uri = comm.whistle_to_udap("alpha_001");
        assert!(uri.is_some());
        assert!(uri.unwrap().contains("skhaos://bio/dolphin/whistle"));
    }

    #[test]
    fn test_click_analysis() {
        let comm = sample_dolphin_patterns();
        let analysis = comm.analyze_clicks("nav_001");
        assert!(analysis.is_some());
        let analysis = analysis.unwrap();
        assert_eq!(analysis.frequency_range, (100.0, 140.0));
        assert!(analysis.efficiency_score > 0.0);
    }

    #[test]
    fn test_dialect_retrieval() {
        let comm = sample_dolphin_patterns();
        let dialect = comm.get_dialect("matrilineal_a");
        assert!(dialect.is_some());
        assert_eq!(dialect.unwrap().matriline, "grandmother_alpha_lineage");
    }
}
