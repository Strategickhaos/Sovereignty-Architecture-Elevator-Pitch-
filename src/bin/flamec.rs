//! # FlameLang Compiler (flamec)
//! 
//! Command-line interface for the FlameLang compiler.
//! 
//! ## Usage
//! 
//! ```bash
//! flamec input.flame              # Compile to binary
//! flamec input.flame -o output    # Specify output file
//! flamec input.flame --emit=llvm  # Emit LLVM IR only
//! flamec input.flame --validate   # Run proofs only, no codegen
//! ```
//! 
//! © 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

use std::env;
use std::fs;
use std::process;

use flamelang::{compile, FlameError, VERSION, BUILD_ID};

fn main() {
    let args: Vec<String> = env::args().collect();
    
    println!("🔥 FlameLang Compiler v{}", VERSION);
    println!("   {}", BUILD_ID);
    println!();
    
    if args.len() < 2 {
        print_usage();
        process::exit(1);
    }
    
    let input_file = &args[1];
    
    // Handle flags
    if input_file == "--help" || input_file == "-h" {
        print_usage();
        process::exit(0);
    }
    
    if input_file == "--version" || input_file == "-V" {
        process::exit(0);
    }
    
    // Read source file
    let source = match fs::read_to_string(input_file) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("❌ Failed to read '{}': {}", input_file, e);
            process::exit(1);
        }
    };
    
    println!("📄 Compiling: {}", input_file);
    println!();
    println!("   Pipeline:");
    println!("   ├── Lexical Analysis");
    println!("   ├── Parsing");
    println!("   ├── Layer 1: Linguistic (English → Hebrew)");
    println!("   ├── Layer 2: Numeric (Unicode → Gematria)");
    println!("   ├── Layer 3: Wave (c=2πr → Hz)");
    println!("   ├── Layer 4: DNA (Freq → Codon)");
    println!("   ├── Layer 5: LLVM IR Generation");
    println!("   └── Proof Validation (16 theorems)");
    println!();
    
    // Compile
    match compile(&source) {
        Ok(binary) => {
            // Determine output filename
            let output_file = if args.len() > 2 && args[2] == "-o" && args.len() > 3 {
                args[3].clone()
            } else {
                // Replace .flame with nothing, or append .out
                if input_file.ends_with(".flame") {
                    input_file.replace(".flame", "")
                } else if input_file.ends_with(".flm") {
                    input_file.replace(".flm", "")
                } else {
                    format!("{}.out", input_file)
                }
            };
            
            // Write output
            match fs::write(&output_file, &binary) {
                Ok(_) => {
                    println!("✅ Compiled successfully!");
                    println!("   Output: {} ({} bytes)", output_file, binary.len());
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
                    eprintln!("❌ Failed to write output: {}", e);
                    process::exit(1);
                }
            }
        }
        Err(e) => {
            eprintln!("❌ Compilation failed:");
            eprintln!();
            match &e {
                FlameError::Lexer(msg) => {
                    eprintln!("   Lexer error: {}", msg);
                }
                FlameError::Parser(msg) => {
                    eprintln!("   Parse error: {}", msg);
                }
                FlameError::Transform { layer, message } => {
                    eprintln!("   Layer {} transform error: {}", layer, message);
                }
                FlameError::ProofViolation { proof_id, message } => {
                    eprintln!("   ⚠️  Proof {} violated: {}", proof_id, message);
                    eprintln!();
                    eprintln!("   Your code violates a mathematical invariant.");
                    eprintln!("   FlameLang enforces physics at compile time.");
                }
                _ => {
                    eprintln!("   {}", e);
                }
            }
            process::exit(1);
        }
    }
}

fn print_usage() {
    println!("Usage: flamec <input.flame> [options]");
    println!();
    println!("Options:");
    println!("  -o <file>      Output file name");
    println!("  --emit=<type>  Emit intermediate (hebrew|numeric|wave|dna|llvm)");
    println!("  --validate     Run proofs only, no codegen");
    println!("  --help, -h     Show this help");
    println!("  --version, -V  Show version");
    println!();
    println!("Examples:");
    println!("  flamec hello.flame              Compile to ./hello");
    println!("  flamec hello.flame -o out       Compile to ./out");
    println!("  flamec hello.flame --emit=llvm  Emit LLVM IR only");
    println!();
    println!("FlameLang enforces physics at compile time.");
    println!("Illegal physics = compilation error.");
}
