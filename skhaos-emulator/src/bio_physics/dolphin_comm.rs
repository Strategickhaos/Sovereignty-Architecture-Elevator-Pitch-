// Dolphin Communication Patterns
// Signature whistles (1-20kHz), echolocation clicks (120-200kHz), pod dialects

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Dolphin communication module
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DolphinComm {
    /// Known pod signatures
    pod_signatures: HashMap<String, SignatureWhistle>,
    /// Dialect database (pod-specific patterns)
    dialects: HashMap<String, Vec<u8>>,
}

/// Signature whistle - unique identifier for individual dolphins
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SignatureWhistle {
    /// Frequency in Hz (typically 1-20kHz)
    pub frequency_hz: f64,
    /// Pod identifier
    pub pod_id: String,
    /// Duration in milliseconds
    pub duration_ms: u64,
    /// Waveform pattern
    pub pattern: Vec<u8>,
}

impl SignatureWhistle {
    /// Create a new signature whistle
    pub fn new(frequency_hz: f64, pod_id: &str) -> Self {
        let duration_ms = 500; // Typical whistle duration
        let pattern = Self::generate_whistle_pattern(frequency_hz, duration_ms);
        
        Self {
            frequency_hz,
            pod_id: pod_id.to_string(),
            duration_ms,
            pattern,
        }
    }

    /// Generate whistle waveform pattern
    fn generate_whistle_pattern(freq: f64, duration_ms: u64) -> Vec<u8> {
        let sample_rate = 44100.0; // Hz
        let samples = (duration_ms as f64 * sample_rate / 1000.0) as usize;
        let mut pattern = Vec::with_capacity(samples);
        
        for i in 0..samples {
            let t = i as f64 / sample_rate;
            let phase = 2.0 * std::f64::consts::PI * freq * t;
            let amplitude = (phase.sin() * 127.0 + 128.0) as u8;
            pattern.push(amplitude);
        }
        
        pattern
    }

    /// Convert to bytes for transmission
    pub fn to_bytes(&self) -> Vec<u8> {
        // Simplified: return the pattern
        self.pattern.clone()
    }

    /// Create from bytes
    pub fn from_bytes(bytes: &[u8], freq: f64, pod_id: &str) -> Self {
        Self {
            frequency_hz: freq,
            pod_id: pod_id.to_string(),
            duration_ms: (bytes.len() as f64 * 1000.0 / 44100.0) as u64,
            pattern: bytes.to_vec(),
        }
    }
}

/// Echolocation burst - high-frequency clicks for navigation/hunting
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EcholocationBurst {
    /// Click frequency in Hz (typically 120-200kHz)
    pub frequency_hz: f64,
    /// Number of clicks in burst
    pub click_count: usize,
    /// Inter-click interval in microseconds
    pub interval_us: u64,
    /// Burst pattern
    pub pattern: Vec<u8>,
}

impl EcholocationBurst {
    /// Create a new echolocation burst
    pub fn new(frequency_hz: f64, click_count: usize) -> Self {
        let interval_us = 50; // Typical inter-click interval
        let pattern = Self::generate_burst_pattern(frequency_hz, click_count, interval_us);
        
        Self {
            frequency_hz,
            click_count,
            interval_us,
            pattern,
        }
    }

    /// Generate burst pattern (simplified representation)
    fn generate_burst_pattern(freq: f64, count: usize, interval_us: u64) -> Vec<u8> {
        let mut pattern = Vec::new();
        
        for i in 0..count {
            // Each click is a short pulse
            let click_duration_samples = 10; // Very short clicks
            for j in 0..click_duration_samples {
                let t = j as f64 / 44100.0;
                let phase = 2.0 * std::f64::consts::PI * (freq / 1000.0) * t; // Downscaled symbolically
                let amplitude = (phase.sin() * 127.0 + 128.0) as u8;
                pattern.push(amplitude);
            }
            
            // Inter-click silence
            if i < count - 1 {
                let silence_samples = (interval_us as f64 * 44.1) as usize;
                pattern.extend(vec![128; silence_samples]); // 128 = zero amplitude
            }
        }
        
        pattern
    }

    /// Convert to bytes
    pub fn to_bytes(&self) -> Vec<u8> {
        self.pattern.clone()
    }
}

/// Dolphin pod dialect - matrilineal cultural transmission
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PodDialect {
    /// Pod identifier
    pub pod_id: String,
    /// Dialect-specific call patterns
    pub calls: Vec<Vec<u8>>,
    /// Matrilineal lineage depth
    pub lineage_depth: usize,
}

impl PodDialect {
    /// Create a new pod dialect
    pub fn new(pod_id: &str) -> Self {
        Self {
            pod_id: pod_id.to_string(),
            calls: Vec::new(),
            lineage_depth: 1,
        }
    }

    /// Add a call to the dialect
    pub fn add_call(&mut self, call: Vec<u8>) {
        self.calls.push(call);
    }

    /// Inherit dialect from mother (matrilineal transmission)
    pub fn inherit_from(&mut self, mother_dialect: &PodDialect) {
        self.calls.extend(mother_dialect.calls.clone());
        self.lineage_depth = mother_dialect.lineage_depth + 1;
    }

    /// Evolve dialect (cultural drift)
    pub fn evolve(&mut self, generation: usize) {
        for call in self.calls.iter_mut() {
            // Apply gradual mutations (cultural evolution)
            for byte in call.iter_mut() {
                if generation % 10 == 0 {
                    *byte = byte.wrapping_add(1);
                }
            }
        }
    }
}

impl DolphinComm {
    /// Create a new dolphin communication module
    pub fn new() -> Self {
        Self {
            pod_signatures: HashMap::new(),
            dialects: HashMap::new(),
        }
    }

    /// Generate signature whistle for a pod
    pub fn signature_whistle(&self, frequency_hz: f64, pod_id: &str) -> SignatureWhistle {
        SignatureWhistle::new(frequency_hz, pod_id)
    }

    /// Generate echolocation burst
    pub fn echolocation_burst(&self, frequency_hz: f64, click_count: usize) -> EcholocationBurst {
        EcholocationBurst::new(frequency_hz, click_count)
    }

    /// Register a pod signature
    pub fn register_pod(&mut self, pod_id: &str, whistle: SignatureWhistle) {
        self.pod_signatures.insert(pod_id.to_string(), whistle);
    }

    /// Get pod signature
    pub fn get_pod_signature(&self, pod_id: &str) -> Option<&SignatureWhistle> {
        self.pod_signatures.get(pod_id)
    }

    /// Add dialect to database
    pub fn add_dialect(&mut self, pod_id: &str, dialect: Vec<u8>) {
        self.dialects.insert(pod_id.to_string(), dialect);
    }

    /// Get pod dialect
    pub fn get_dialect(&self, pod_id: &str) -> Option<&Vec<u8>> {
        self.dialects.get(pod_id)
    }

    /// Simulate pod communication exchange
    pub fn simulate_exchange(&self, pod1: &str, pod2: &str) -> Vec<Vec<u8>> {
        let mut exchange = Vec::new();
        
        // Pod 1 sends signature whistle
        if let Some(sig1) = self.pod_signatures.get(pod1) {
            exchange.push(sig1.to_bytes());
        }
        
        // Pod 2 responds with signature whistle
        if let Some(sig2) = self.pod_signatures.get(pod2) {
            exchange.push(sig2.to_bytes());
        }
        
        // Exchange dialect-specific calls
        if let Some(dial1) = self.dialects.get(pod1) {
            exchange.push(dial1.clone());
        }
        if let Some(dial2) = self.dialects.get(pod2) {
            exchange.push(dial2.clone());
        }
        
        exchange
    }

    /// Entangle dolphin pattern with frequency
    pub fn entangle_with_frequency(&self, pattern: &[u8], target_hz: f64) -> Vec<u8> {
        let mut entangled = Vec::new();
        
        for (i, &byte) in pattern.iter().enumerate() {
            let phase = (i as f64 * target_hz * 0.01) % 256.0;
            let modulated = byte.wrapping_add(phase as u8);
            entangled.push(modulated);
        }
        
        entangled
    }
}

impl Default for DolphinComm {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signature_whistle_creation() {
        let whistle = SignatureWhistle::new(10.0, "pod_alpha");
        assert_eq!(whistle.frequency_hz, 10.0);
        assert_eq!(whistle.pod_id, "pod_alpha");
        assert!(!whistle.pattern.is_empty());
    }

    #[test]
    fn test_echolocation_burst() {
        let burst = EcholocationBurst::new(120.0, 200);
        assert_eq!(burst.frequency_hz, 120.0);
        assert_eq!(burst.click_count, 200);
        assert!(!burst.pattern.is_empty());
    }

    #[test]
    fn test_pod_dialect() {
        let mut dialect = PodDialect::new("pod_beta");
        dialect.add_call(vec![1, 2, 3, 4]);
        assert_eq!(dialect.calls.len(), 1);
    }

    #[test]
    fn test_dolphin_comm_module() {
        let mut comm = DolphinComm::new();
        let whistle = comm.signature_whistle(15.0, "pod_gamma");
        comm.register_pod("pod_gamma", whistle);
        assert!(comm.get_pod_signature("pod_gamma").is_some());
    }

    #[test]
    fn test_pod_exchange() {
        let mut comm = DolphinComm::new();
        comm.register_pod("pod_a", SignatureWhistle::new(10.0, "pod_a"));
        comm.register_pod("pod_b", SignatureWhistle::new(12.0, "pod_b"));
        
        let exchange = comm.simulate_exchange("pod_a", "pod_b");
        assert!(exchange.len() >= 2);
    }
}
