//! Example: Hello FlameLang
//!
//! Demonstrates the 5-layer transformation pipeline

use flamelang::{compile, FlameResult, BUILD_ID, VERSION};

fn main() -> FlameResult<()> {
    println!("🔥 FlameLang v{} - {}", VERSION, BUILD_ID);
    println!("Sovereign 5-Layer Transformation Pipeline\n");

    let source = r#"
        let r: float = 5.0;
        let theta: angle = 90;
        bend theta radius r;
    "#;

    println!("Source Code:");
    println!("{}", source);

    println!("\nCompiling through 5 layers...");
    println!("  LAYER 1: LINGUISTIC    English → Hebrew → Glyph");
    println!("  LAYER 2: NUMERIC       Unicode → Decimal → Hex");
    println!("  LAYER 3: WAVE          Decimal → c=2πr → Hz/BPS");
    println!("  LAYER 4: DNA           Freq → Codon → ACGT Sequence");
    println!("  LAYER 5: LLVM          Codon → Opcode → Native Binary");

    match compile(source) {
        Ok(binary) => {
            println!("\n✅ Compilation successful!");
            println!("Binary size: {} bytes", binary.len());
            println!("First 100 bytes: {:?}", &binary[..binary.len().min(100)]);
        }
        Err(e) => {
            eprintln!("\n❌ Compilation failed: {}", e);
            return Err(e);
        }
    }

    println!("\n© 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo");

    Ok(())
}
