//! Layer 2: Numeric Transform
//! Hebrew → Gematria values

use crate::FlameResult;
use crate::transform::layer1::HebrewAST;
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct NumericData {
    pub hebrew_ast: HebrewAST,
    pub gematria_values: HashMap<String, u64>,
}

/// Calculate gematria values for Hebrew roots
pub fn transform(hebrew_ast: &HebrewAST) -> FlameResult<NumericData> {
    let mut gematria_values = HashMap::new();
    
    // Gematria letter values (simplified)
    let letter_values: HashMap<char, u64> = [
        ('א', 1), ('ב', 2), ('ג', 3), ('ד', 4), ('ה', 5),
        ('ו', 6), ('ז', 7), ('ח', 8), ('ט', 9), ('י', 10),
        ('כ', 20), ('ל', 30), ('מ', 40), ('נ', 50), ('ס', 60),
        ('ע', 70), ('פ', 80), ('צ', 90), ('ק', 100), ('ר', 200),
        ('ש', 300), ('ת', 400),
    ].iter().cloned().collect();
    
    for (name, hebrew) in &hebrew_ast.root_mappings {
        let value: u64 = hebrew.chars()
            .filter_map(|c| letter_values.get(&c))
            .sum();
        gematria_values.insert(name.clone(), value);
    }
    
    Ok(NumericData {
        hebrew_ast: hebrew_ast.clone(),
        gematria_values,
    })
}
