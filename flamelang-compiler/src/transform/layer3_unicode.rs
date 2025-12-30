/// Transform Layer 3: Unicode/Glyph
/// Encodes operations as visual glyphs and Unicode symbols
/// e.g., 🛠️ for pipefit, injecting Rubik PLL/OLL as quantum gates

use crate::transform::layer2_hebrew::{HebrewAst, HebrewOperation};

#[derive(Debug, Clone)]
pub struct UnicodeAst {
    pub glyphs: Vec<GlyphOperation>,
}

#[derive(Debug, Clone)]
pub struct GlyphOperation {
    pub glyph: String,
    pub operation: String,
    pub encoding: Vec<u8>,
}

pub fn transform(heb_ast: HebrewAst) -> Result<UnicodeAst, String> {
    let glyphs = heb_ast.operations.into_iter()
        .map(|op| encode_as_glyph(op))
        .collect();
    
    Ok(UnicodeAst { glyphs })
}

fn encode_as_glyph(op: HebrewOperation) -> GlyphOperation {
    match op {
        HebrewOperation::Bounce { tau } => {
            GlyphOperation {
                glyph: "⚛️".to_string(),  // Atom symbol for quantum bounce
                operation: format!("bounce(τ={})", tau),
                encoding: encode_to_bytes("bounce", tau),
            }
        }
        HebrewOperation::Suppress { mode, factor } => {
            GlyphOperation {
                glyph: "🔇".to_string(),  // Mute symbol for suppression
                operation: format!("suppress({}, factor={})", mode, factor),
                encoding: encode_to_bytes("suppress", factor),
            }
        }
        HebrewOperation::Observe { collapse } => {
            GlyphOperation {
                glyph: "👁️".to_string(),  // Eye for observation
                operation: format!("observe(collapse={})", collapse),
                encoding: encode_to_bytes("observe", if collapse { 1.0 } else { 0.0 }),
            }
        }
        HebrewOperation::Fluctuate { amplitude } => {
            GlyphOperation {
                glyph: "🌊".to_string(),  // Wave for fluctuation
                operation: format!("fluctuate(amp={})", amplitude),
                encoding: encode_to_bytes("fluctuate", amplitude),
            }
        }
        HebrewOperation::Unify { theories } => {
            GlyphOperation {
                glyph: "🔗".to_string(),  // Link for unification
                operation: format!("unify({:?})", theories),
                encoding: encode_to_bytes("unify", theories.len() as f64),
            }
        }
        HebrewOperation::Anomaly { asymmetry } => {
            GlyphOperation {
                glyph: "⚡".to_string(),  // Lightning for anomaly
                operation: format!("anomaly(asym={})", asymmetry),
                encoding: encode_to_bytes("anomaly", asymmetry),
            }
        }
        HebrewOperation::Generic { op, .. } => {
            GlyphOperation {
                glyph: "🛠️".to_string(),  // Tool for generic operations
                operation: op,
                encoding: vec![0x42, 0x00],  // Generic marker
            }
        }
    }
}

fn encode_to_bytes(op_name: &str, param: f64) -> Vec<u8> {
    // Simple encoding: operation name hash + parameter bytes
    let mut bytes = Vec::new();
    
    // Operation type identifier
    let op_id = match op_name {
        "bounce" => 0x01,
        "suppress" => 0x02,
        "observe" => 0x03,
        "fluctuate" => 0x04,
        "unify" => 0x05,
        "anomaly" => 0x06,
        _ => 0xFF,
    };
    bytes.push(op_id);
    
    // Encode parameter as f64 bytes (simplified)
    let param_bytes = param.to_bits().to_le_bytes();
    bytes.extend_from_slice(&param_bytes);
    
    // Rubik's cube encoding (PLL/OLL inspired quantum gate patterns)
    // Map to cube moves: U, D, L, R, F, B
    let cube_encoding = encode_rubik_pattern(param);
    bytes.extend_from_slice(&cube_encoding);
    
    bytes
}

fn encode_rubik_pattern(param: f64) -> Vec<u8> {
    // Encode parameter as Rubik's cube algorithm pattern
    // U=1, D=2, L=3, R=4, F=5, B=6
    let normalized = (param.abs() * 100.0) as u32;
    let moves = vec![
        ((normalized >> 0) & 0x07) as u8,
        ((normalized >> 3) & 0x07) as u8,
        ((normalized >> 6) & 0x07) as u8,
        ((normalized >> 9) & 0x07) as u8,
    ];
    moves.into_iter().map(|m| (m % 6) + 1).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_glyph_encoding() {
        let heb_ast = HebrewAst {
            operations: vec![
                HebrewOperation::Bounce { tau: 0.065 },
            ],
        };
        
        let uni_ast = transform(heb_ast).unwrap();
        assert_eq!(uni_ast.glyphs.len(), 1);
        assert_eq!(uni_ast.glyphs[0].glyph, "⚛️");
        assert!(uni_ast.glyphs[0].operation.contains("bounce"));
    }

    #[test]
    fn test_rubik_pattern() {
        let pattern = encode_rubik_pattern(0.065);
        assert_eq!(pattern.len(), 4);
        // All values should be 1-6 (cube moves)
        assert!(pattern.iter().all(|&m| m >= 1 && m <= 6));
    }
}
