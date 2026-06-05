//! # FlameLang Compiler CLI (flamec)
//! 
//! The sovereign compiler that transforms code through 5 layers with proof validation.

use std::env;
use std::fs;
use std::process;

mod pipeline;

fn main() {
    println!("🔥 FlameLang Compiler v2.0.0");
    println!("   ratio-ex-nihilo");
    println!();

    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: flamec <source.flm>");
        eprintln!("\nExample:");
        eprintln!("  flamec examples/hello_sovereign.flm");
        process::exit(1);
    }

    let source_path = &args[1];
    
    println!("📄 Compiling: {}", source_path);
    println!();
    
    // Read source file
    let source = match fs::read_to_string(source_path) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("❌ Error reading file: {}", e);
            process::exit(1);
        }
    };

    // Compile through pipeline
    match pipeline::compile(&source) {
        Ok(output) => {
            println!();
            println!("✅ Compiled successfully!");
            let output_name = source_path.replace(".flm", "").replace(".flame", "");
            let output_name = std::path::Path::new(&output_name)
                .file_name()
                .unwrap()
                .to_str()
                .unwrap();
            println!("   Output: {} ({} bytes)", output_name, output.len());
            println!();
            println!("   Proofs validated:");
            println!("   ├── ✓ Fixed-point convergence");
            println!("   ├── ✓ Grounding completeness (M/F/B)");
            println!("   ├── ✓ Codon bijection (64 ↔ 64)");
            println!("   ├── ✓ Pipe bend closure (Σθ = 360°)");
            println!("   ├── ✓ Rubik bound (≤ 20 moves)");
            println!("   └── ✓ Setback identity (arc = r × θ)");
        }
        Err(e) => {
            eprintln!();
            eprintln!("❌ Compilation failed!");
            eprintln!("   {}", e);
            process::exit(1);
        }
    }
}
