// FlameLang Compiler - Main Entry Point
// KHAOS Script → FlameIR → TRIG6 → Executable

mod ir;
mod lexer;
mod parser;
mod trig6;
mod codegen;

use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("🔥 FlameLang Compiler v0.1.0");
        eprintln!("Usage: flamec <input.flame> [options]");
        eprintln!();
        eprintln!("Options:");
        eprintln!("  --ir-only     Output FlameIR JSON only");
        eprintln!("  --no-trig6    Disable TRIG6 transformation pass");
        eprintln!("  --run         Compile and run immediately");
        eprintln!();
        eprintln!("Example:");
        eprintln!("  flamec hello.flame");
        eprintln!("  flamec hello.flame --run");
        std::process::exit(1);
    }
    
    let input_file = &args[1];
    let ir_only = args.contains(&"--ir-only".to_string());
    let no_trig6 = args.contains(&"--no-trig6".to_string());
    let run = args.contains(&"--run".to_string());
    
    // Read source file
    let source = match fs::read_to_string(input_file) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("❌ Error reading file '{}': {}", input_file, e);
            std::process::exit(1);
        }
    };
    
    println!("🔥 Compiling {}...", input_file);
    
    // Phase 1: Lexing
    println!("📝 Phase 1: Lexical analysis...");
    let mut lexer = lexer::Lexer::new(source);
    let tokens = lexer.tokenize();
    println!("   Found {} tokens", tokens.len());
    
    // Phase 2: Parsing
    println!("🌳 Phase 2: Parsing to FlameIR...");
    let mut parser = parser::Parser::new(tokens);
    let mut program = match parser.parse() {
        Ok(prog) => prog,
        Err(e) => {
            eprintln!("❌ Parse error: {}", e);
            std::process::exit(1);
        }
    };
    println!("   Generated {} IR instructions", program.instructions.len());
    
    // Output IR if requested
    if ir_only {
        match serde_json::to_string_pretty(&program) {
            Ok(json) => {
                println!("{}", json);
                return;
            }
            Err(e) => {
                eprintln!("❌ Error serializing IR: {}", e);
                std::process::exit(1);
            }
        }
    }
    
    // Phase 3: TRIG6 Transformation Pass
    if !no_trig6 {
        println!("⚡ Phase 3: TRIG6 transformation pass...");
        let codec = trig6::Trig6Codec::new();
        codec.transform(&mut program);
        println!("   TRIG6 optimizations applied");
    }
    
    // Phase 4: Code Generation
    println!("🔧 Phase 4: Generating Rust code...");
    let mut codegen = codegen::CodeGenerator::new();
    let rust_code = match codegen.generate(&program) {
        Ok(code) => code,
        Err(e) => {
            eprintln!("❌ Codegen error: {}", e);
            std::process::exit(1);
        }
    };
    
    // Write output file
    let output_file = input_file.replace(".flame", ".rs");
    match fs::write(&output_file, &rust_code) {
        Ok(_) => println!("   Generated: {}", output_file),
        Err(e) => {
            eprintln!("❌ Error writing output: {}", e);
            std::process::exit(1);
        }
    }
    
    // Phase 5: Compile with rustc
    println!("🛠️  Phase 5: Compiling with rustc...");
    let executable = input_file.replace(".flame", "");
    let compile_result = Command::new("rustc")
        .arg(&output_file)
        .arg("-o")
        .arg(&executable)
        .output();
    
    match compile_result {
        Ok(output) => {
            if output.status.success() {
                println!("✅ Compilation successful!");
                println!("   Executable: {}", executable);
                
                // Generate birth certificate
                println!();
                println!("🎉 BIRTH CERTIFICATE 🎉");
                println!("═══════════════════════════════════════");
                println!("Source:     {}", input_file);
                println!("FlameIR:    {} instructions", program.instructions.len());
                println!("Output:     {}", executable);
                println!("TRIG6:      {}", if no_trig6 { "disabled" } else { "enabled" });
                println!("Timestamp:  {}", chrono::Local::now().format("%Y-%m-%d %H:%M:%S"));
                println!("═══════════════════════════════════════");
                println!("First successful FlameLang compilation!");
                
                // Run if requested
                if run {
                    println!();
                    println!("🚀 Running executable...");
                    println!("───────────────────────────────────────");
                    let run_result = Command::new(format!("./{}", executable))
                        .output();
                    
                    match run_result {
                        Ok(output) => {
                            print!("{}", String::from_utf8_lossy(&output.stdout));
                            eprint!("{}", String::from_utf8_lossy(&output.stderr));
                        }
                        Err(e) => {
                            eprintln!("❌ Error running executable: {}", e);
                        }
                    }
                    println!("───────────────────────────────────────");
                }
            } else {
                eprintln!("❌ rustc compilation failed:");
                eprint!("{}", String::from_utf8_lossy(&output.stderr));
                std::process::exit(1);
            }
        }
        Err(e) => {
            eprintln!("❌ Error invoking rustc: {}", e);
            eprintln!("   Make sure rustc is installed and in PATH");
            std::process::exit(1);
        }
    }
}

