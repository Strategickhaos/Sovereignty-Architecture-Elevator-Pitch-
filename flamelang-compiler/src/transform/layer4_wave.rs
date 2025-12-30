/// Transform Layer 4: Wave/Quantum
/// Applies quantum fluctuations and wave mechanics
/// Fluctuations via 'נוע', unify LQC/String with 'אחד'

use crate::transform::layer3_unicode::{UnicodeAst, GlyphOperation};

#[derive(Debug, Clone)]
pub struct WaveAst {
    pub quantum_ops: Vec<QuantumOperation>,
}

#[derive(Debug, Clone)]
pub struct QuantumOperation {
    pub wave_type: WaveType,
    pub parameters: QuantumParams,
    pub glyph_ref: String,
}

#[derive(Debug, Clone)]
pub enum WaveType {
    Bounce,
    Fluctuation,
    Suppression,
    Observation,
    Unification,
    Anomaly,
}

#[derive(Debug, Clone)]
pub struct QuantumParams {
    pub amplitude: f64,
    pub frequency: f64,
    pub phase: f64,
    pub damping: f64,
}

impl Default for QuantumParams {
    fn default() -> Self {
        QuantumParams {
            amplitude: 1.0,
            frequency: 1.0,
            phase: 0.0,
            damping: 0.0,
        }
    }
}

pub fn transform(uni_ast: UnicodeAst) -> Result<WaveAst, String> {
    let quantum_ops = uni_ast.glyphs.into_iter()
        .map(|glyph| apply_quantum_mechanics(glyph))
        .collect();
    
    Ok(WaveAst { quantum_ops })
}

fn apply_quantum_mechanics(glyph: GlyphOperation) -> QuantumOperation {
    let (wave_type, params) = if glyph.operation.contains("bounce") {
        let tau = extract_param_value(&glyph.operation, "τ");
        (WaveType::Bounce, QuantumParams {
            amplitude: 1.0,
            frequency: 1.0 / tau,
            phase: 0.0,
            damping: 1.0 / tau,  // exp(-l/τ) damping
        })
    } else if glyph.operation.contains("fluctuate") {
        let amp = extract_param_value(&glyph.operation, "amp");
        (WaveType::Fluctuation, QuantumParams {
            amplitude: amp,
            frequency: 1.0,
            phase: 0.0,
            damping: 0.0,
        })
    } else if glyph.operation.contains("suppress") {
        let factor = extract_param_value(&glyph.operation, "factor");
        (WaveType::Suppression, QuantumParams {
            amplitude: 1.0 - factor,
            frequency: 1.0,
            phase: 0.0,
            damping: factor,
        })
    } else if glyph.operation.contains("observe") {
        (WaveType::Observation, QuantumParams {
            amplitude: 1.0,
            frequency: f64::INFINITY,  // Instantaneous collapse
            phase: 0.0,
            damping: 0.0,
        })
    } else if glyph.operation.contains("unify") {
        // Unify LQC and String theory: blend parameters
        (WaveType::Unification, QuantumParams {
            amplitude: 1.0,
            frequency: 1e-7,  // String tension μG² ≈ 10^-7
            phase: 0.0,
            damping: 0.065,  // LQC bounce scale
        })
    } else if glyph.operation.contains("anomaly") {
        let asym = extract_param_value(&glyph.operation, "asym");
        (WaveType::Anomaly, QuantumParams {
            amplitude: asym,
            frequency: 1.0,
            phase: std::f64::consts::PI / 4.0,  // Phase shift for asymmetry
            damping: 0.0,
        })
    } else {
        (WaveType::Fluctuation, QuantumParams::default())
    };
    
    QuantumOperation {
        wave_type,
        parameters: params,
        glyph_ref: glyph.glyph,
    }
}

fn extract_param_value(operation: &str, param_name: &str) -> f64 {
    // Simple parameter extraction from operation string
    if let Some(start) = operation.find(&format!("{}=", param_name)) {
        let start_idx = start + param_name.len() + 1;
        let substr = &operation[start_idx..];
        let end_idx = substr.find(|c: char| !c.is_numeric() && c != '.' && c != '-' && c != 'e')
            .unwrap_or(substr.len());
        substr[..end_idx].parse::<f64>().unwrap_or(0.0)
    } else {
        // Default values
        match param_name {
            "τ" => 0.065,
            "amp" => 1e-5,
            "factor" => 0.15,
            "asym" => 0.1,
            _ => 1.0,
        }
    }
}

/// Apply Gaussian noise for quantum fluctuations
pub fn apply_gaussian_noise(value: f64, amplitude: f64) -> f64 {
    // Simple pseudo-random Gaussian approximation using Box-Muller
    let u1 = (value.abs().fract() + 0.1) % 1.0;
    let u2 = (value.abs() * 1.5 + 0.2) % 1.0;
    let noise = amplitude * (-2.0 * u1.ln()).sqrt() * (2.0 * std::f64::consts::PI * u2).cos();
    value + noise
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::transform::layer3_unicode::UnicodeAst;

    #[test]
    fn test_wave_transform() {
        let uni_ast = UnicodeAst {
            glyphs: vec![GlyphOperation {
                glyph: "⚛️".to_string(),
                operation: "bounce(τ=0.065)".to_string(),
                encoding: vec![],
            }],
        };
        
        let wave_ast = transform(uni_ast).unwrap();
        assert_eq!(wave_ast.quantum_ops.len(), 1);
        match wave_ast.quantum_ops[0].wave_type {
            WaveType::Bounce => {
                assert!((wave_ast.quantum_ops[0].parameters.damping - 1.0/0.065).abs() < 1.0);
            }
            _ => panic!("Expected Bounce wave type"),
        }
    }

    #[test]
    fn test_gaussian_noise() {
        let original = 42.0;
        let noisy = apply_gaussian_noise(original, 0.1);
        // Should be different but close
        assert!((noisy - original).abs() < 1.0);
    }
}
