use sagco_formula_compiler::cell::Value;
use sagco_formula_compiler::evaluator::Evaluator;
use sagco_formula_compiler::funcs;
use sagco_formula_compiler::parser::parse;
use sagco_formula_compiler::registry::FuncRegistry;
use sagco_formula_compiler::sheet::Sheet;

fn make_registry() -> FuncRegistry {
    let mut r = FuncRegistry::new();
    funcs::register_all(&mut r);
    r
}

fn eval(formula: &str, sheet: &Sheet, registry: &FuncRegistry) -> Value {
    let ast = parse(formula).expect("parse failed");
    let evaluator = Evaluator::new(registry, sheet);
    evaluator.eval(&ast).unwrap_or_else(|e| Value::Error(e.to_string()))
}

#[test]
fn test_eval_number() {
    let sheet = Sheet::new();
    let reg = make_registry();
    assert_eq!(eval("42", &sheet, &reg), Value::Number(42.0));
}

#[test]
fn test_eval_add() {
    let sheet = Sheet::new();
    let reg = make_registry();
    assert_eq!(eval("3+4", &sheet, &reg), Value::Number(7.0));
}

#[test]
fn test_eval_if_true() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=IF(TRUE, "yes", "no")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("yes".to_string()));
}

#[test]
fn test_eval_if_false() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=IF(FALSE, "yes", "no")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("no".to_string()));
}

#[test]
fn test_eval_sum() {
    let sheet = Sheet::new();
    let reg = make_registry();
    assert_eq!(eval("=SUM(1,2,3,4)", &sheet, &reg), Value::Number(10.0));
}

#[test]
fn test_eval_len() {
    let sheet = Sheet::new();
    let reg = make_registry();
    assert_eq!(eval(r#"=LEN("hello")"#, &sheet, &reg), Value::Number(5.0));
}

#[test]
fn test_eval_morse_sos() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=MORSE("SOS")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("... --- ...".to_string()));
}

#[test]
fn test_eval_sagco_sanity_clean() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=SAGCO_SANITY("clean text")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("SOVEREIGN".to_string()));
}

#[test]
fn test_eval_sagco_sanity_hallucination() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=SAGCO_SANITY("** bold text")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("HALLUCINATION_RISK".to_string()));
}

#[test]
fn test_eval_sagco_eru_match() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=SAGCO_ERU("MOBIUS_READY","MOBIUS_READY")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("VARIANCE_0".to_string()));
}

#[test]
fn test_eval_sagco_eru_mismatch() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=SAGCO_ERU("MOBIUS_READY","NOT_READY")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("OPEN_VARIANCE".to_string()));
}

#[test]
fn test_eval_cell_ref() {
    let mut sheet = Sheet::new();
    let reg = make_registry();
    sheet.set("A1", "42");
    sheet.recalc(&reg);
    let result = eval("=A1", &sheet, &reg);
    assert_eq!(result, Value::Number(42.0));
}

#[test]
fn test_eval_sagco_guard_ready() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=SAGCO_GUARD("clean formula answer")"#, &sheet, &reg);
    assert_eq!(result, Value::Str("MOBIUS_READY".to_string()));
}

#[test]
fn test_eval_sagco_units_km_to_mi() {
    let sheet = Sheet::new();
    let reg = make_registry();
    let result = eval(r#"=SAGCO_UNITS(100,"km","mi")"#, &sheet, &reg);
    if let Value::Number(n) = result {
        assert!((n - 62.1371).abs() < 0.01);
    } else {
        panic!("Expected number");
    }
}

#[test]
fn test_eval_abs() {
    let sheet = Sheet::new();
    let reg = make_registry();
    assert_eq!(eval("=ABS(-5)", &sheet, &reg), Value::Number(5.0));
}

#[test]
fn test_eval_round() {
    let sheet = Sheet::new();
    let reg = make_registry();
    assert_eq!(eval("=ROUND(3.456, 2)", &sheet, &reg), Value::Number(3.46));
}
