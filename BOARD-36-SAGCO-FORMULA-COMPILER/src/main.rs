use clap::Parser as ClapParser;
use sagco_formula_compiler::funcs;
use sagco_formula_compiler::passes::eru_pass::EruPass;
use sagco_formula_compiler::passes::guard_pass::GuardPass;
use sagco_formula_compiler::passes::lex_pass::LexPass;
use sagco_formula_compiler::passes::parse_pass::ParsePass;
use sagco_formula_compiler::passes::semantic_pass::SemanticPass;
use sagco_formula_compiler::passes::unit_pass::UnitPass;
use sagco_formula_compiler::passes::Pipeline;
use sagco_formula_compiler::registry::FuncRegistry;
use sagco_formula_compiler::sheet::Sheet;
use std::io::Read;

#[derive(ClapParser, Debug)]
#[command(
    name = "sagco_formula_compiler",
    version = "1.0",
    about = "SAGCO Formula Compiler — headless formula engine"
)]
struct Args {
    /// Path to .sagco file (omit for --pipe mode)
    #[arg(required = false)]
    input: Option<String>,

    /// Dump AST for all formulas
    #[arg(long)]
    dump_ast: bool,

    /// Run all compiler passes
    #[arg(long)]
    run_passes: bool,

    /// Print ERU proof report
    #[arg(long)]
    eru: bool,

    /// Read .sagco content from stdin
    #[arg(long)]
    pipe: bool,
}

fn main() {
    let args = Args::parse();

    // Read content
    let content = if args.pipe {
        let mut buf = String::new();
        std::io::stdin().read_to_string(&mut buf).expect("failed to read stdin");
        buf
    } else if let Some(path) = &args.input {
        std::fs::read_to_string(path).unwrap_or_else(|e| {
            eprintln!("Error reading file '{}': {}", path, e);
            std::process::exit(1);
        })
    } else {
        eprintln!("Error: provide a .sagco file or use --pipe");
        std::process::exit(1);
    };

    // Build registry
    let mut registry = FuncRegistry::new();
    funcs::register_all(&mut registry);

    // Parse sheet
    let mut sheet = Sheet::from_sagco(&content);

    // Evaluate
    sheet.recalc(&registry);

    // Dump AST
    if args.dump_ast {
        println!("=== AST DUMP ===");
        let mut addrs: Vec<String> = sheet.cells.keys().cloned().collect();
        addrs.sort();
        for addr in &addrs {
            let cell = &sheet.cells[addr];
            if cell.is_formula() {
                match sagco_formula_compiler::parser::parse(&cell.formula) {
                    Ok(ast) => println!("{}: {:#?}", addr, ast),
                    Err(e) => println!("{}: PARSE ERROR: {}", addr, e),
                }
            }
        }
        println!();
    }

    // Print evaluated sheet
    println!("=== CELL VALUES ===");
    let mut addrs: Vec<String> = sheet.cells.keys().cloned().collect();
    addrs.sort();
    for addr in &addrs {
        let cell = &sheet.cells[addr];
        println!("  {} = {}", addr, cell.value);
    }
    println!();

    // Run passes
    if args.run_passes {
        println!("=== COMPILER PASSES ===");

        let lex = LexPass;
        let pr = lex.run(&mut sheet);
        println!("{}", pr);

        let parse_p = ParsePass;
        let pr = parse_p.run(&mut sheet);
        println!("{}", pr);

        let sem = SemanticPass { registry: &registry };
        let pr = sem.run(&mut sheet);
        println!("{}", pr);

        let unit = UnitPass;
        let pr = unit.run(&mut sheet);
        println!("{}", pr);

        let guard = GuardPass;
        let pr = guard.run(&mut sheet);
        println!("{}", pr);

        let eru_p = EruPass;
        let pr = eru_p.run(&mut sheet);
        println!("{}", pr);

        println!();
    }

    // ERU report
    if args.eru {
        println!("=== ERU PROOF REPORT ===");
        let report = EruPass::build_report(&sheet);
        println!("{}", report.to_yaml());
    }
}
