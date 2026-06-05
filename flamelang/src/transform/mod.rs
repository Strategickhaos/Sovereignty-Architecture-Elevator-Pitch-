//! FlameLang 5-Layer Transform Pipeline
//! Layer 1: Linguistic (English → Hebrew triconsonantal roots)
//! Layer 2: Numeric (Hebrew → Gematria values)
//! Layer 3: Wave (Gematria → c=2πr frequency encoding)
//! Layer 4: DNA (Frequency → 64-codon bijection)

pub mod layer1;
pub mod layer2;
pub mod layer3;
pub mod layer4;

use crate::FlameResult;
use crate::ast::Program;
use crate::ir::FlameIR;

/// Complete transformation pipeline from AST to FlameIR
pub fn transform_pipeline(program: &Program, module_name: &str) -> FlameResult<FlameIR> {
    // Layer 1: Linguistic transformation
    let hebrew_ast = layer1::transform(program)?;
    
    // Layer 2: Numeric transformation
    let numeric_data = layer2::transform(&hebrew_ast)?;
    
    // Layer 3: Wave transformation
    let wave_data = layer3::transform(&numeric_data)?;
    
    // Layer 4: DNA transformation (produces final IR)
    let ir = layer4::transform(&wave_data, module_name)?;
    
    Ok(ir)
}
