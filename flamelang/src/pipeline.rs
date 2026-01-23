//! Compilation Pipeline
//! Wires together: Lexer → Parser → Transform → Backend

use crate::lexer::lex;
use crate::parser::parse;
use crate::transform::transform_pipeline;
use crate::backend::LLVMBackend;
use crate::proofs::validate_all;
use crate::{FlameResult, FlameError};
use inkwell::context::Context;
use std::fs;
use std::process::Command;

/// Complete compilation pipeline
pub fn compile(source_path: &str, output_path: &str, debug: bool) -> FlameResult<()> {
    if debug {
        eprintln!("╔══════════════════════════════════════════════════════════════╗");
        eprintln!("║        FLAMELANG COMPILER v2.0.0                           ║");
        eprintln!("║        5-Layer Transformation Pipeline                      ║");
        eprintln!("╚══════════════════════════════════════════════════════════════╝");
    }
    
    // Read source file
    if debug { eprintln!("\n[0/7] Reading source file: {}", source_path); }
    let source = fs::read_to_string(source_path)
        .map_err(|e| FlameError::IoError(format!("Failed to read {}: {}", source_path, e)))?;
    
    // Phase 1: Lexing
    if debug { eprintln!("[1/7] Lexing..."); }
    let tokens = lex(&source)?;
    if debug { eprintln!("      ✓ {} tokens", tokens.len()); }
    
    // Phase 2: Parsing
    if debug { eprintln!("[2/7] Parsing..."); }
    let program = parse(&tokens)?;
    if debug { eprintln!("      ✓ {} statements", program.statements.len()); }
    
    // Phase 3: Transform Layers
    if debug { eprintln!("[3/7] Layer 1: Linguistic (English → Hebrew)..."); }
    if debug { eprintln!("[4/7] Layer 2: Numeric (Hebrew → Gematria)..."); }
    if debug { eprintln!("      Layer 3: Wave (Gematria → Frequency)..."); }
    if debug { eprintln!("      Layer 4: DNA (Frequency → Codon → IR)..."); }
    
    let module_name = std::path::Path::new(source_path)
        .file_stem()
        .and_then(|s| s.to_str())
        .unwrap_or("flame_module");
    
    let ir = transform_pipeline(&program, module_name)?;
    
    if debug { 
        eprintln!("      ✓ {} functions transformed", ir.functions.len()); 
        for func in &ir.functions {
            if let (Some(ref hebrew), Some(gematria), Some(freq), Some(ref codon)) = 
                (&func.hebrew_root, func.gematria_value, func.frequency, &func.codon) {
                eprintln!("        • {} → {} (גמטריא: {}, ƒ: {:.2}, 🧬: {})",
                    func.name, hebrew, gematria, freq, codon);
            }
        }
    }
    
    // Phase 4: Proof Validation
    if debug { eprintln!("[5/7] Validating 16 proofs..."); }
    validate_all(&ir)?;
    if debug { eprintln!("      ✓ All proofs passed"); }
    
    // Phase 5: LLVM Backend
    if debug { eprintln!("[6/7] LLVM codegen..."); }
    let context = Context::create();
    let mut backend = LLVMBackend::new(&context, module_name);
    backend.emit_module(&ir)?;
    
    if debug {
        eprintln!("      ✓ IR generated");
        if std::env::var("FLAME_DUMP_IR").is_ok() {
            eprintln!("\n--- LLVM IR ---\n{}\n---------------", backend.print_ir());
        }
    }
    
    // Phase 6: Write Object File
    if debug { eprintln!("[7/7] Writing binary..."); }
    let obj_path = format!("{}.o", output_path);
    backend.write_object(&obj_path)?;
    
    // Link to executable
    if debug { eprintln!("      Linking executable..."); }
    link_binary(&obj_path, output_path, debug)?;
    
    // Clean up object file
    let _ = fs::remove_file(&obj_path);
    
    if debug { 
        eprintln!("\n╔══════════════════════════════════════════════════════════════╗");
        eprintln!("║  ✓ Compilation successful: {}                         ", output_path);
        eprintln!("╚══════════════════════════════════════════════════════════════╝\n");
    }
    
    Ok(())
}

/// Link object file to executable
fn link_binary(obj_path: &str, output_path: &str, debug: bool) -> FlameResult<()> {
    // Detect platform and use appropriate linker
    let status = if cfg!(target_os = "windows") {
        Command::new("link")
            .arg("/OUT:")
            .arg(output_path)
            .arg(obj_path)
            .arg("/SUBSYSTEM:CONSOLE")
            .status()
    } else if cfg!(target_os = "macos") {
        Command::new("ld")
            .arg("-o")
            .arg(output_path)
            .arg(obj_path)
            .arg("-macosx_version_min")
            .arg("10.7")
            .arg("-lSystem")
            .status()
    } else {
        // Linux
        Command::new("ld")
            .arg("-o")
            .arg(output_path)
            .arg(obj_path)
            .arg("-dynamic-linker")
            .arg("/lib64/ld-linux-x86-64.so.2")
            .arg("-lc")
            .status()
    };
    
    match status {
        Ok(exit_status) if exit_status.success() => {
            if debug { eprintln!("      ✓ Linked successfully"); }
            Ok(())
        }
        Ok(exit_status) => {
            Err(FlameError::BackendError(format!("Linker failed with status: {}", exit_status)))
        }
        Err(e) => {
            // Linker not found - try clang as fallback
            if debug { eprintln!("      ⚠ System linker not found, trying clang..."); }
            
            let status = Command::new("clang")
                .arg("-o")
                .arg(output_path)
                .arg(obj_path)
                .status();
            
            match status {
                Ok(exit_status) if exit_status.success() => {
                    if debug { eprintln!("      ✓ Linked with clang"); }
                    Ok(())
                }
                _ => {
                    Err(FlameError::BackendError(format!("Failed to link binary: {}", e)))
                }
            }
        }
    }
}
