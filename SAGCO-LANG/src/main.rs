mod ast;
mod lexer;
mod parser;
mod validator;
mod emitter_yaml;
mod emitter_machine;

use std::fs;
use std::path::PathBuf;

fn main() {
    let args: Vec<String> = std::env::args().collect();

    let (input, source_name) = if args.len() > 1 {
        let path = PathBuf::from(&args[1]);
        let text = fs::read_to_string(&path)
            .unwrap_or_else(|e| { eprintln!("ERROR: cannot read {:?}: {}", path, e); std::process::exit(1); });
        (text, args[1].clone())
    } else {
        (
            "brick ENTRY route pad(J8.PIN_03) -> pad(BOARD.CORE.PIN_5)".to_string(),
            "<inline>".to_string(),
        )
    };

    println!("SAGCO LANG v0.1  source: {}", source_name);
    println!("---");

    // Lex
    let tokens = lexer::lex(&input);
    println!("TOKENS:");
    for t in &tokens {
        println!("  {:?}", t);
    }
    println!();

    // Parse
    let mut p = parser::Parser::new(tokens);
    let program = match p.parse() {
        Ok(prog) => prog,
        Err(e) => { eprintln!("PARSE ERROR: {}", e); std::process::exit(1); }
    };

    // Validate
    let errors = validator::validate(&program);
    if !errors.is_empty() {
        for e in &errors { eprintln!("VALIDATION ERROR: {}", e); }
        std::process::exit(1);
    }

    // Emit YAML
    let yaml = emitter_yaml::emit(&program);
    println!("AST YAML:\n{}", yaml);

    // Emit machine
    let machine = emitter_machine::emit(&program);
    println!("MACHINE:\n{}", machine);

    // Write output files if input was a file
    if args.len() > 1 {
        let stem = PathBuf::from(&args[1])
            .file_stem()
            .unwrap_or_default()
            .to_string_lossy()
            .to_string();
        fs::create_dir_all("output").ok();
        fs::write(format!("output/{}.ast.yaml", stem), &yaml).ok();
        fs::write(format!("output/{}.machine.txt", stem), &machine).ok();
        println!("Written: output/{0}.ast.yaml  output/{0}.machine.txt", stem);
    }
}
