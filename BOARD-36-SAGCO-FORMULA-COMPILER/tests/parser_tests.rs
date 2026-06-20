use sagco_formula_compiler::ast::{BinOp, Expr};
use sagco_formula_compiler::parser::parse;

#[test]
fn test_parse_number() {
    let ast = parse("42").unwrap();
    assert_eq!(ast, Expr::Number(42.0));
}

#[test]
fn test_parse_string() {
    let ast = parse(r#""hello""#).unwrap();
    assert_eq!(ast, Expr::Str("hello".to_string()));
}

#[test]
fn test_parse_binop_add() {
    let ast = parse("1+2").unwrap();
    assert_eq!(
        ast,
        Expr::BinOp {
            left: Box::new(Expr::Number(1.0)),
            op: BinOp::Add,
            right: Box::new(Expr::Number(2.0)),
        }
    );
}

#[test]
fn test_parse_if() {
    let ast = parse(r#"=IF(A1>5, "HIGH", "LOW")"#).unwrap();
    assert!(matches!(ast, Expr::IfExpr { .. }));
}

#[test]
fn test_parse_sum_call() {
    let ast = parse("=SUM(A1,A2)").unwrap();
    assert!(matches!(ast, Expr::Call { ref name, .. } if name == "SUM"));
}

#[test]
fn test_parse_nested_call() {
    let ast = parse("=IF(SUM(A1,A2)>100, \"HIGH\", \"LOW\")").unwrap();
    assert!(matches!(ast, Expr::IfExpr { .. }));
}

#[test]
fn test_parse_range_ref() {
    let ast = parse("=SUM(A1:A5)").unwrap();
    assert!(matches!(ast, Expr::Call { ref name, .. } if name == "SUM"));
}

#[test]
fn test_parse_unary_neg() {
    let ast = parse("-42").unwrap();
    assert!(matches!(ast, Expr::UnaryOp { .. }));
}

#[test]
fn test_parse_comparison() {
    let ast = parse("A1>50").unwrap();
    assert!(matches!(ast, Expr::BinOp { op: BinOp::Gt, .. }));
}

#[test]
fn test_parse_power() {
    let ast = parse("2^10").unwrap();
    assert!(matches!(ast, Expr::BinOp { op: BinOp::Pow, .. }));
}
