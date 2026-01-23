//! Layer 3: Wave Transform
//! Gematria → c=2πr frequency encoding

use crate::FlameResult;
use crate::transform::layer2::NumericData;
use std::collections::HashMap;
use std::f64::consts::PI;

#[derive(Debug, Clone)]
pub struct WaveData {
    pub numeric_data: NumericData,
    pub frequencies: HashMap<String, f64>,
}

/// Transform gematria values to wave frequencies using c=2πr
pub fn transform(numeric_data: &NumericData) -> FlameResult<WaveData> {
    let mut frequencies = HashMap::new();
    
    for (name, gematria) in &numeric_data.gematria_values {
        // Use c=2πr formula where r is derived from gematria
        let radius = *gematria as f64;
        let circumference = 2.0 * PI * radius;
        
        // Frequency encoding: map to audible/visible spectrum
        let frequency = circumference / 100.0; // Normalized
        
        frequencies.insert(name.clone(), frequency);
    }
    
    Ok(WaveData {
        numeric_data: numeric_data.clone(),
        frequencies,
    })
}

/// Convert value to frequency
pub fn to_frequency(value: u64) -> f64 {
    let radius = value as f64;
    2.0 * PI * radius / 100.0
}
