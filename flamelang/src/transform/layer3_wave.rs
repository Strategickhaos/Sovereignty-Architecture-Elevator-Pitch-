//! # Layer 3: Wave Transformation
//! 
//! Gematria → Wave (c=2πr → Hz)

use crate::{FlameError, Result};

/// Transform gematria values to wave frequencies
/// Using the relationship c = 2πr to derive frequencies
pub fn transform_to_wave(gematria_values: &[u32]) -> Result<Vec<f64>> {
    let mut frequencies = Vec::new();
    
    // Base frequency: 432 Hz (natural tuning)
    const BASE_FREQ: f64 = 432.0;
    const PI: f64 = std::f64::consts::PI;
    
    for &value in gematria_values {
        if value == 0 {
            continue;
        }
        
        // Transform gematria value to frequency using harmonic ratios
        // c = 2πr, where c is circumference and r is radius
        // Map gematria value to a radius, then calculate frequency
        let radius = value as f64;
        let circumference = 2.0 * PI * radius;
        
        // Scale to audible frequency range (20 Hz - 20,000 Hz)
        let freq = (BASE_FREQ * circumference / 1000.0) % 20000.0 + 20.0;
        
        // Ensure finite values (Proof 2)
        if !freq.is_finite() {
            return Err(FlameError::TransformError(
                "Wave transformation produced non-finite value".to_string()
            ));
        }
        
        frequencies.push(freq);
    }
    
    Ok(frequencies)
}

/// Calculate wavelength from frequency
pub fn frequency_to_wavelength(freq: f64) -> f64 {
    const SPEED_OF_SOUND: f64 = 343.0; // m/s at 20°C
    SPEED_OF_SOUND / freq
}

/// Verify setback identity: arc = r × θ
pub fn verify_setback_identity(radius: f64, theta: f64, arc: f64) -> bool {
    let expected_arc = radius * theta;
    (expected_arc - arc).abs() < 1e-6
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gematria_to_wave() {
        let gematria = vec![203, 100, 50];
        let frequencies = transform_to_wave(&gematria).unwrap();
        
        // Verify all frequencies are finite
        for freq in &frequencies {
            assert!(freq.is_finite());
            assert!(*freq >= 20.0);
            assert!(*freq <= 20000.0);
        }
    }
    
    #[test]
    fn test_setback_identity() {
        let radius = 10.0;
        let theta = std::f64::consts::PI / 2.0; // 90 degrees
        let arc = radius * theta;
        assert!(verify_setback_identity(radius, theta, arc));
    }
}
