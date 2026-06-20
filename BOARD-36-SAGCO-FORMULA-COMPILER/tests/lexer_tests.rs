use sagco_formula_compiler::lexer::tokenize;
use sagco_formula_compiler::token::Token;

fn tokens(input: &str) -> Vec<Token> {
    tokenize(input)
        .expect("tokenize failed")
        .into_iter()
        .filter(|t| t.token != Token::EOF)
        .map(|t| t.token)
        .collect()
}

#[test]
fn test_number() {
    let toks = tokens("42");
    assert_eq!(toks, vec![Token::Number(42.0)]);
}

#[test]
fn test_float() {
    let toks = tokens("3.14");
    assert_eq!(toks, vec![Token::Number(3.14)]);
}

#[test]
fn test_string() {
    let toks = tokens(r#""hello""#);
    assert_eq!(toks, vec![Token::Str("hello".to_string())]);
}

#[test]
fn test_cell_ref() {
    let toks = tokens("A1");
    assert_eq!(toks, vec![Token::CellRef("A1".to_string())]);
}

#[test]
fn test_cell_ref_multi_col() {
    let toks = tokens("AB3");
    assert_eq!(toks, vec![Token::CellRef("AB3".to_string())]);
}

#[test]
fn test_range_ref() {
    let toks = tokens("A1:A10");
    assert_eq!(toks, vec![Token::RangeRef("A1".to_string(), "A10".to_string())]);
}

#[test]
fn test_operators() {
    let toks = tokens("+ - * / ^");
    assert_eq!(toks, vec![
        Token::Plus, Token::Minus, Token::Star, Token::Slash, Token::Caret
    ]);
}

#[test]
fn test_comparison_ops() {
    let toks = tokens("> >= < <= = <>");
    assert_eq!(toks, vec![
        Token::Gt, Token::GtEq, Token::Lt, Token::LtEq, Token::Eq, Token::NEq
    ]);
}

#[test]
fn test_function_call_tokens() {
    let toks = tokens("=SUM(A1,A2)");
    assert_eq!(toks, vec![
        Token::Ident("SUM".to_string()),
        Token::LParen,
        Token::CellRef("A1".to_string()),
        Token::Comma,
        Token::CellRef("A2".to_string()),
        Token::RParen,
    ]);
}

#[test]
fn test_bool_literals() {
    let toks = tokens("TRUE FALSE");
    assert_eq!(toks, vec![Token::Bool(true), Token::Bool(false)]);
}

#[test]
fn test_if_formula_tokens() {
    let toks = tokens(r#"=IF(A1>5, "HIGH", "LOW")"#);
    assert!(toks.contains(&Token::Ident("IF".to_string())));
    assert!(toks.contains(&Token::CellRef("A1".to_string())));
    assert!(toks.contains(&Token::Gt));
}
