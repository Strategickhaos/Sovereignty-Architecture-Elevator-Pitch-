use sagco_formula_compiler::cell::Value;
use sagco_formula_compiler::funcs;
use sagco_formula_compiler::passes::eru_pass::EruPass;
use sagco_formula_compiler::passes::lex_pass::LexPass;
use sagco_formula_compiler::passes::parse_pass::ParsePass;
use sagco_formula_compiler::passes::semantic_pass::SemanticPass;
use sagco_formula_compiler::passes::Pipeline;
use sagco_formula_compiler::registry::FuncRegistry;
use sagco_formula_compiler::sheet::Sheet;

fn make_registry() -> FuncRegistry {
    let mut r = FuncRegistry::new();
    funcs::register_all(&mut r);
    r
}

fn load_sagco(content: &str) -> (Sheet, FuncRegistry) {
    let reg = make_registry();
    let mut sheet = Sheet::from_sagco(content);
    sheet.recalc(&reg);
    (sheet, reg)
}

#[test]
fn test_excel_if_then_pipeline() {
    let content = include_str!("../examples/excel_if_then.sagco");
    let (mut sheet, reg) = load_sagco(content);

    // All passes should run without crashing
    let lex = LexPass;
    let pr = lex.run(&mut sheet);
    assert!(pr.passed, "LexPass failed: {:?}", pr.errors);

    let parse_p = ParsePass;
    let pr = parse_p.run(&mut sheet);
    assert!(pr.passed, "ParsePass failed: {:?}", pr.errors);

    let sem = SemanticPass { registry: &reg };
    let pr = sem.run(&mut sheet);
    assert!(pr.passed, "SemanticPass failed: {:?}", pr.errors);

    // Check results
    assert_eq!(sheet.get("B1"), Some(Value::Str("LOW".to_string())));
    assert_eq!(sheet.get("B2"), Some(Value::Str("HIGH".to_string())));
    assert_eq!(sheet.get("C1"), Some(Value::Number(142.0)));
}

#[test]
fn test_refinery_wafer_pipeline() {
    let content = include_str!("../examples/refinery_wafer.sagco");
    let (mut sheet, reg) = load_sagco(content);

    let lex = LexPass;
    let pr = lex.run(&mut sheet);
    assert!(pr.passed, "LexPass failed: {:?}", pr.errors);

    let parse_p = ParsePass;
    let pr = parse_p.run(&mut sheet);
    assert!(pr.passed, "ParsePass failed: {:?}", pr.errors);

    // B1 should be MORSE of "SOS"
    let b1 = sheet.get("B1");
    assert_eq!(b1, Some(Value::Str("... --- ...".to_string())));
}

#[test]
fn test_mobius_gate_pipeline() {
    let content = include_str!("../examples/mobius_first_gate.sagco");
    let (mut sheet, reg) = load_sagco(content);

    let sem = SemanticPass { registry: &reg };
    let pr = sem.run(&mut sheet);
    // B1 should be MOBIUS_READY since no bad markers in "-37/sqrt(590078)"
    assert_eq!(sheet.get("B1"), Some(Value::Str("MOBIUS_READY".to_string())));
}

#[test]
fn test_eru_report() {
    let content = include_str!("../examples/excel_if_then.sagco");
    let (sheet, _reg) = load_sagco(content);
    let report = EruPass::build_report(&sheet);
    assert_eq!(report.total_cells, 6);
    assert_eq!(report.errors, 0);
}

#[test]
fn test_circular_dependency() {
    let reg = make_registry();
    let mut sheet = Sheet::new();
    sheet.set("A1", "=B1");
    sheet.set("B1", "=A1");
    sheet.recalc(&reg);
    // Both cells should have circular error
    assert!(matches!(sheet.get("A1"), Some(Value::Error(_))));
}
