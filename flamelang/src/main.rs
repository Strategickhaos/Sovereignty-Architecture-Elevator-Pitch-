//! FlameLang Compiler CLI

use clap::{Parser, Subcommand};
use flamelang::{compile, VERSION, COMPILER_NAME};
use std::process;

#[derive(Parser)]
#[command(name = COMPILER_NAME)]
#[command(version = VERSION)]
#[command(about = "FlameLang Compiler - 5-Layer Transformation: Linguistic → Numeric → Wave → DNA → LLVM", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Compile a .flame file to native binary
    Compile {
        /// Input .flame source file
        input: String,
        
        /// Output binary path
        #[arg(short, long, default_value = "a.out")]
        output: String,
        
        /// Enable debug output
        #[arg(short, long)]
        debug: bool,
    },
    
    /// Run a .flame file (compile and execute)
    Run {
        /// Input .flame source file
        input: String,
        
        /// Enable debug output
        #[arg(short, long)]
        debug: bool,
    },
    
    /// Display version and build info
    Version,
}

fn main() {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Compile { input, output, debug } => {
            if debug {
                println!("🔥 FlameLang Compiler v{}", VERSION);
                println!("   Compiling: {} -> {}", input, output);
                println!();
            }
            
            match compile(&input, &output, debug) {
                Ok(()) => {
                    if !debug {
                        println!("✓ Compiled successfully: {}", output);
                    }
                    process::exit(0);
                }
                Err(e) => {
                    eprintln!("❌ Compilation failed: {}", e);
                    process::exit(1);
                }
            }
        }
        
        Commands::Run { input, debug } => {
            if debug {
                println!("🔥 FlameLang Compiler v{}", VERSION);
                println!("   Running: {}", input);
                println!();
            }
            
            // Compile to temporary executable
            let output = "/tmp/flame_temp_exe";
            
            match compile(&input, output, debug) {
                Ok(()) => {
                    if debug {
                        println!("\n--- Program Output ---");
                    }
                    
                    // Execute
                    let status = std::process::Command::new(output)
                        .status();
                    
                    match status {
                        Ok(exit_status) => {
                            if debug {
                                println!("----------------------");
                                println!("Exit code: {}", exit_status.code().unwrap_or(-1));
                            }
                            process::exit(exit_status.code().unwrap_or(1));
                        }
                        Err(e) => {
                            eprintln!("❌ Execution failed: {}", e);
                            process::exit(1);
                        }
                    }
                }
                Err(e) => {
                    eprintln!("❌ Compilation failed: {}", e);
                    process::exit(1);
                }
            }
        }
        
        Commands::Version => {
            println!("╔══════════════════════════════════════════════════════════════╗");
            println!("║  🔥 FlameLang Compiler v{}                              ║", VERSION);
            println!("╠══════════════════════════════════════════════════════════════╣");
            println!("║  5-Layer Transformation Pipeline:                            ║");
            println!("║    1. Linguistic: English → Hebrew triconsonantal roots     ║");
            println!("║    2. Numeric:    Hebrew → Gematria values                  ║");
            println!("║    3. Wave:       Gematria → c=2πr frequency encoding       ║");
            println!("║    4. DNA:        Frequency → 64-codon bijection            ║");
            println!("║    5. LLVM:       Codon → LLVM IR → Native Binary           ║");
            println!("╠══════════════════════════════════════════════════════════════╣");
            println!("║  16 Mathematical Proofs Enforced at Compile-Time            ║");
            println!("╠══════════════════════════════════════════════════════════════╣");
            println!("║  Copyright © 2025 Strategickhaos DAO LLC (EIN: 39-2900295)  ║");
            println!("║  Inventor: Domenic Gabriel Garza                             ║");
            println!("╚══════════════════════════════════════════════════════════════╝");
        }
    }
}
