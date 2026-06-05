//! # Layer 2: Numeric Transformation
//! 
//! Hebrew → Gematria (Unicode → Numeric values)

use crate::Result;

/// Convert Hebrew text to Gematria values
pub fn transform_to_gematria(hebrew_text: &str) -> Result<Vec<u32>> {
    let mut gematria_values = Vec::new();
    
    // Hebrew gematria mapping (simplified)
    let gematria_map: std::collections::HashMap<char, u32> = [
        ('א', 1), ('ב', 2), ('ג', 3), ('ד', 4), ('ה', 5),
        ('ו', 6), ('ז', 7), ('ח', 8), ('ט', 9), ('י', 10),
        ('כ', 20), ('ך', 20), ('ל', 30), ('מ', 40), ('ם', 40),
        ('נ', 50), ('ן', 50), ('ס', 60), ('ע', 70), ('פ', 80),
        ('ף', 80), ('צ', 90), ('ץ', 90), ('ק', 100), ('ר', 200),
        ('ש', 300), ('ת', 400),
    ].iter().cloned().collect();
    
    for ch in hebrew_text.chars() {
        if let Some(&value) = gematria_map.get(&ch) {
            gematria_values.push(value);
        } else if ch.is_alphanumeric() || ch == '_' {
            // For ASCII/English letters and numbers, use Unicode value
            gematria_values.push(ch as u32);
        }
        // Skip whitespace and punctuation
    }
    
    Ok(gematria_values)
}

/// Calculate total gematria value of a word/phrase
pub fn calculate_total(values: &[u32]) -> u32 {
    values.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hebrew_to_gematria() {
        let result = transform_to_gematria("בָּרָא").unwrap();
        assert!(!result.is_empty());
    }
    
    #[test]
    fn test_calculate_total() {
        let values = vec![2, 200, 1]; // ב = 2, ר = 200, א = 1
        assert_eq!(calculate_total(&values), 203);
    }
}
