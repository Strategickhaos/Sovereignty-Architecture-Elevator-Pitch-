//! # FlameLang Compiler Binary
//! 
//! Command-line interface for the FlameLang compiler
//! 
//! © 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

use flamelang::compiler::compile;
use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: flamelang <source_file>");
        eprintln!("");
        eprintln!("FlameLang v2.0.0 - Ratio Ex Nihilo");
        eprintln!("© 2025 Strategickhaos DAO LLC");
        process::exit(1);
    }
    
    let filename = &args[1];
    
    // Read source file
    let source = match fs::read_to_string(filename) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("Error reading file '{}': {}", filename, e);
            process::exit(1);
        }
    };
    
    // Compile
    match compile(&source) {
        Ok(binary) => {
            println!("✓ Compilation successful!");
            println!("  Output size: {} bytes", binary.len());
            
            // Write output
            let output_filename = filename.replace(".flame", ".out");
            if let Err(e) = fs::write(&output_filename, binary) {
                eprintln!("Error writing output '{}': {}", output_filename, e);
                process::exit(1);
            }
            
            println!("  Written to: {}", output_filename);
        }
        Err(e) => {
            eprintln!("✗ Compilation failed: {}", e);
            process::exit(1);
        }
    }
}
