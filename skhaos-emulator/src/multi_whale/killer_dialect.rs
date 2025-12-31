// Killer Whale (Orca) Dialect Module
// Pod-specific vocalizations with matrilineal learning
// Frequency range: 1-25 kHz
// Call types: clicks, whistles, pulsed calls

use std::collections::HashMap;

/// Call types for killer whales
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CallType {
    Click,          // Echolocation (1-25 kHz)
    Whistle,        // Social communication (1-15 kHz)
    PulsedCall,     // Discrete calls (1-6 kHz)
    LowFreqBellow,  // < 1 kHz
    JawClap,        // Physical acoustic display
}

/// Orca ecotype classification
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Ecotype {
    Resident,   // Fish-eating, vocal
    Biggs,      // Mammal-eating (transient), quieter
    Offshore,   // Pelagic, less studied
}

/// Pacific Northwest pod designations
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PodIdentity {
    J, // Southern Residents (J-pod)
    K, // Southern Residents (K-pod)
    L, // Southern Residents (L-pod)
    Northern(String), // Northern Residents (A, G, R clans, etc.)
    Biggs(String),    // Biggs/Transient pods
    Unknown,
}

/// Killer whale dialect call
#[derive(Debug, Clone)]
pub struct KillerDialectCall {
    pub call_type: CallType,
    pub pod: PodIdentity,
    pub ecotype: Ecotype,
    pub frequency_hz: f64,
    pub duration_sec: f64,
    pub matriline_id: usize, // Matrilineal transmission lineage
    pub call_number: Option<usize>, // Discrete call catalog number (e.g., S1, N4)
}

impl KillerDialectCall {
    /// Create a new killer whale call
    pub fn new(call_type: CallType, pod: PodIdentity, ecotype: Ecotype) -> Self {
        Self {
            call_type,
            pod,
            ecotype,
            frequency_hz: 5000.0,
            duration_sec: 1.0,
            matriline_id: 0,
            call_number: None,
        }
    }

    /// Validate frequency range (1-25 kHz for killer whales)
    pub fn validate_frequency(&self) -> Result<(), String> {
        // Allow sub-1kHz for low freq bellows
        let min_freq = if matches!(self.call_type, CallType::LowFreqBellow) { 0.1 } else { 1.0 };
        
        if self.frequency_hz < min_freq || self.frequency_hz > 25000.0 {
            return Err(format!(
                "Killer whale frequency {} Hz outside range [{}-25000 Hz]",
                self.frequency_hz, min_freq
            ));
        }
        Ok(())
    }

    /// Check if call is pod-specific (dialect marker)
    pub fn is_dialect_specific(&self) -> bool {
        matches!(self.call_type, CallType::PulsedCall | CallType::Whistle)
    }

    /// Get call catalog identifier
    pub fn catalog_id(&self) -> String {
        let pod_code = match &self.pod {
            PodIdentity::J => "J",
            PodIdentity::K => "K",
            PodIdentity::L => "L",
            PodIdentity::Northern(clan) => clan,
            PodIdentity::Biggs(id) => id,
            PodIdentity::Unknown => "U",
        };
        
        let call_code = match self.call_type {
            CallType::Click => "CK",
            CallType::Whistle => "WH",
            CallType::PulsedCall => "PC",
            CallType::LowFreqBellow => "LF",
            CallType::JawClap => "JC",
        };
        
        if let Some(num) = self.call_number {
            format!("{}-{}{}", pod_code, call_code, num)
        } else {
            format!("{}-{}", pod_code, call_code)
        }
    }

    /// Simulate call frequency pattern
    pub fn simulate_pattern(&self) -> Vec<f64> {
        let samples = 100;
        let mut pattern = Vec::with_capacity(samples);
        
        for i in 0..samples {
            let t = i as f64 / samples as f64;
            
            let freq = match self.call_type {
                CallType::Click => {
                    // Broadband pulse
                    self.frequency_hz * (1.0 + 0.5 * (t * 20.0 * std::f64::consts::PI).sin())
                }
                CallType::Whistle => {
                    // Frequency modulated whistle
                    self.frequency_hz * (1.0 + 0.3 * (t * 4.0 * std::f64::consts::PI).sin())
                }
                CallType::PulsedCall => {
                    // Discrete pulsed structure
                    self.frequency_hz * (1.0 + 0.2 * (t * 10.0 * std::f64::consts::PI).cos())
                }
                CallType::LowFreqBellow => {
                    // Steady low frequency
                    self.frequency_hz
                }
                CallType::JawClap => {
                    // Broadband transient
                    self.frequency_hz * (1.0 - t * 0.9)
                }
            };
            
            pattern.push(freq);
        }
        
        pattern
    }
}

/// Killer whale pod dialect system
pub struct KillerDialectSystem {
    calls: Vec<KillerDialectCall>,
    pod: PodIdentity,
    matrilines: HashMap<usize, Vec<usize>>, // matriline_id -> call indices
}

impl KillerDialectSystem {
    /// Create new dialect system for a pod
    pub fn new(pod: PodIdentity) -> Self {
        Self {
            calls: Vec::new(),
            pod,
            matrilines: HashMap::new(),
        }
    }

    /// Add call to dialect
    pub fn add_call(&mut self, call: KillerDialectCall) -> Result<usize, String> {
        call.validate_frequency()?;
        
        let call_idx = self.calls.len();
        let matriline = call.matriline_id;
        
        self.calls.push(call);
        
        // Track matrilineal transmission
        self.matrilines.entry(matriline)
            .or_insert_with(Vec::new)
            .push(call_idx);
        
        Ok(call_idx)
    }

    /// Get calls for specific matriline
    pub fn get_matriline_calls(&self, matriline_id: usize) -> Vec<&KillerDialectCall> {
        if let Some(indices) = self.matrilines.get(&matriline_id) {
            indices.iter().map(|&idx| &self.calls[idx]).collect()
        } else {
            Vec::new()
        }
    }

    /// Compare dialect similarity with another pod (Jaccard index)
    pub fn dialect_similarity(&self, other: &KillerDialectSystem) -> f64 {
        let my_calls: std::collections::HashSet<String> = 
            self.calls.iter().map(|c| c.catalog_id()).collect();
        let other_calls: std::collections::HashSet<String> = 
            other.calls.iter().map(|c| c.catalog_id()).collect();
        
        let intersection = my_calls.intersection(&other_calls).count();
        let union = my_calls.union(&other_calls).count();
        
        if union == 0 {
            0.0
        } else {
            intersection as f64 / union as f64
        }
    }

    /// Simulate cultural learning (matrilineal transmission)
    pub fn learn_from_matriline(&mut self, source_matriline: usize, target_matriline: usize) -> Result<usize, String> {
        let source_calls = self.get_matriline_calls(source_matriline);
        
        if source_calls.is_empty() {
            return Err("Source matriline has no calls".to_string());
        }
        
        let mut learned_count = 0;
        for call in source_calls {
            let mut new_call = call.clone();
            new_call.matriline_id = target_matriline;
            
            // Add some variation during learning (imperfect transmission)
            new_call.frequency_hz *= 1.0 + (0.05 * (target_matriline as f64).sin()); // +/- 5%
            
            self.add_call(new_call)?;
            learned_count += 1;
        }
        
        Ok(learned_count)
    }

    /// Get dialect statistics
    pub fn get_stats(&self) -> HashMap<String, f64> {
        let mut stats = HashMap::new();
        
        let avg_freq = self.calls.iter()
            .map(|c| c.frequency_hz)
            .sum::<f64>() / self.calls.len() as f64;
        
        let avg_duration = self.calls.iter()
            .map(|c| c.duration_sec)
            .sum::<f64>() / self.calls.len() as f64;
        
        let dialect_specific = self.calls.iter()
            .filter(|c| c.is_dialect_specific())
            .count() as f64;
        
        stats.insert("call_count".to_string(), self.calls.len() as f64);
        stats.insert("avg_frequency_hz".to_string(), avg_freq);
        stats.insert("avg_duration_sec".to_string(), avg_duration);
        stats.insert("dialect_specific_percent".to_string(), 
            dialect_specific / self.calls.len() as f64 * 100.0);
        stats.insert("matriline_count".to_string(), self.matrilines.len() as f64);
        
        stats
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_killer_call_creation() {
        let call = KillerDialectCall::new(
            CallType::Whistle,
            PodIdentity::J,
            Ecotype::Resident,
        );
        assert!(call.validate_frequency().is_ok());
    }

    #[test]
    fn test_catalog_id() {
        let mut call = KillerDialectCall::new(
            CallType::PulsedCall,
            PodIdentity::J,
            Ecotype::Resident,
        );
        call.call_number = Some(1);
        
        assert_eq!(call.catalog_id(), "J-PC1");
    }

    #[test]
    fn test_dialect_specific() {
        let whistle = KillerDialectCall::new(
            CallType::Whistle,
            PodIdentity::K,
            Ecotype::Resident,
        );
        assert!(whistle.is_dialect_specific());
        
        let click = KillerDialectCall::new(
            CallType::Click,
            PodIdentity::K,
            Ecotype::Resident,
        );
        assert!(!click.is_dialect_specific());
    }

    #[test]
    fn test_pattern_simulation() {
        let call = KillerDialectCall::new(
            CallType::Whistle,
            PodIdentity::L,
            Ecotype::Resident,
        );
        let pattern = call.simulate_pattern();
        
        assert_eq!(pattern.len(), 100);
        assert!(pattern.iter().all(|&f| f > 0.0));
    }

    #[test]
    fn test_dialect_system() {
        let mut system = KillerDialectSystem::new(PodIdentity::J);
        
        let mut call1 = KillerDialectCall::new(
            CallType::Whistle,
            PodIdentity::J,
            Ecotype::Resident,
        );
        call1.matriline_id = 1;
        
        let mut call2 = KillerDialectCall::new(
            CallType::PulsedCall,
            PodIdentity::J,
            Ecotype::Resident,
        );
        call2.matriline_id = 1;
        
        assert!(system.add_call(call1).is_ok());
        assert!(system.add_call(call2).is_ok());
        
        let matriline_calls = system.get_matriline_calls(1);
        assert_eq!(matriline_calls.len(), 2);
    }

    #[test]
    fn test_matrilineal_learning() {
        let mut system = KillerDialectSystem::new(PodIdentity::J);
        
        let mut call = KillerDialectCall::new(
            CallType::Whistle,
            PodIdentity::J,
            Ecotype::Resident,
        );
        call.matriline_id = 1;
        
        assert!(system.add_call(call).is_ok());
        assert!(system.learn_from_matriline(1, 2).is_ok());
        
        let matriline2_calls = system.get_matriline_calls(2);
        assert_eq!(matriline2_calls.len(), 1);
    }

    #[test]
    fn test_dialect_similarity() {
        let mut system1 = KillerDialectSystem::new(PodIdentity::J);
        let mut system2 = KillerDialectSystem::new(PodIdentity::K);
        
        let mut call1 = KillerDialectCall::new(
            CallType::Whistle,
            PodIdentity::J,
            Ecotype::Resident,
        );
        call1.call_number = Some(1);
        
        let mut call2 = KillerDialectCall::new(
            CallType::Whistle,
            PodIdentity::K,
            Ecotype::Resident,
        );
        call2.call_number = Some(1);
        
        system1.add_call(call1).ok();
        system2.add_call(call2).ok();
        
        let similarity = system1.dialect_similarity(&system2);
        assert!(similarity >= 0.0 && similarity <= 1.0);
    }
}
