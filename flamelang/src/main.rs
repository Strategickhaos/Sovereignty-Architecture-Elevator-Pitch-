// FlameLang Compiler Main Entry Point
//
// This is a placeholder main binary for the FlameLang compiler.
// In the future, this will handle command-line arguments, file I/O,
// and orchestrate the compilation pipeline.

use flamelang::{IR_VERSION, builder::*, InvariantChecker};

fn main() {
    println!("🔥 FlameLang Compiler v{}", IR_VERSION);
    println!("════════════════════════════════════════════════════════════");
    println!();
    println!("Intermediate Representation FROZEN at v{}", IR_VERSION);
    println!("All passes must consume and produce this exact structure.");
    println!();
    
    // Demonstrate IR construction with the hello.flame example
    println!("Building hello.flame IR example...");
    
    let ir = module("hello", vec![
        extern_fn("print", vec![flamelang::FlameType::String], flamelang::FlameType::Unit),
        fn_def("main", vec![], flamelang::FlameType::Unit,
            block(vec![
                call("print", vec![const_string("Hello, FlameLang!")]),
                ret(None),
            ])
        ),
    ]);
    
    println!("✓ IR constructed successfully");
    
    // Run invariant checks
    println!("Running invariant checks...");
    let diagnostics = InvariantChecker::check_all(&ir);
    
    if diagnostics.is_empty() {
        println!("✓ All invariants passed!");
    } else {
        println!("✗ Invariant violations detected:");
        for diag in &diagnostics {
            println!("  [{:?}] {}", diag.level, diag.message);
        }
    }
    
    println!();
    println!("════════════════════════════════════════════════════════════");
    println!("🔥 FlameLang IR v{} operational. Reignite.", IR_VERSION);
}
