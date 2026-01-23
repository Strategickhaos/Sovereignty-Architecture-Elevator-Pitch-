//! Lexer for FlameLang
//! Tokenizes source code including Hebrew glyphs

use logos::Logos;
use crate::{FlameError, FlameResult};

#[derive(Logos, Debug, Clone, PartialEq)]
#[logos(skip r"[ \t\n\f]+")]  // Skip whitespace
#[logos(skip r"//[^\n]*")]     // Skip line comments
pub enum Token {
    // Keywords
    #[token("fn")]
    Fn,
    #[token("let")]
    Let,
    #[token("return")]
    Return,
    #[token("if")]
    If,
    #[token("else")]
    Else,
    #[token("while")]
    While,
    #[token("for")]
    For,
    #[token("in")]
    In,
    #[token("true")]
    True,
    #[token("false")]
    False,
    
    // Types
    #[token("i32")]
    I32Type,
    #[token("i64")]
    I64Type,
    #[token("f64")]
    F64Type,
    #[token("bool")]
    BoolType,
    #[token("string")]
    StringType,
    
    // Operators
    #[token("+")]
    Plus,
    #[token("-")]
    Minus,
    #[token("*")]
    Star,
    #[token("/")]
    Slash,
    #[token("%")]
    Percent,
    #[token("=")]
    Assign,
    #[token("==")]
    Eq,
    #[token("!=")]
    Ne,
    #[token("<")]
    Lt,
    #[token("<=")]
    Le,
    #[token(">")]
    Gt,
    #[token(">=")]
    Ge,
    #[token("&&")]
    And,
    #[token("||")]
    Or,
    #[token("!")]
    Not,
    
    // Delimiters
    #[token("(")]
    LParen,
    #[token(")")]
    RParen,
    #[token("{")]
    LBrace,
    #[token("}")]
    RBrace,
    #[token("[")]
    LBracket,
    #[token("]")]
    RBracket,
    #[token(",")]
    Comma,
    #[token(";")]
    Semicolon,
    #[token(":")]
    Colon,
    #[token("->")]
    Arrow,
    
    // FlameLang-specific operators
    #[token("bend")]
    Bend,
    #[token("codon")]
    Codon,
    #[token("perm")]
    Perm,
    #[token("gematria")]
    Gematria,
    
    // Hebrew glyphs (aleph-tav)
    #[regex(r"[\u0590-\u05FF]+")]
    HebrewGlyph,
    
    // Literals
    #[regex(r"-?[0-9]+", |lex| lex.slice().parse::<i64>().ok())]
    Integer(i64),
    
    #[regex(r"-?[0-9]+\.[0-9]+", |lex| lex.slice().parse::<f64>().ok())]
    Float(f64),
    
    #[regex(r#""([^"\\]|\\.)*""#, |lex| {
        let s = lex.slice();
        Some(s[1..s.len()-1].to_string())
    })]
    String(String),
    
    // Identifiers
    #[regex(r"[a-zA-Z_][a-zA-Z0-9_]*", |lex| lex.slice().to_string())]
    Ident(String),
    
    // End of file
    Eof,
}

pub fn lex(source: &str) -> FlameResult<Vec<Token>> {
    let mut lexer = Token::lexer(source);
    let mut tokens = Vec::new();
    let mut line = 1;
    let mut col = 1;
    
    while let Some(token_result) = lexer.next() {
        match token_result {
            Ok(token) => {
                tokens.push(token);
            }
            Err(()) => {
                return Err(FlameError::LexerError {
                    line,
                    col,
                    message: format!("Invalid token: {}", lexer.slice()),
                });
            }
        }
        
        // Update position tracking
        let slice = lexer.slice();
        for c in slice.chars() {
            if c == '\n' {
                line += 1;
                col = 1;
            } else {
                col += 1;
            }
        }
    }
    
    tokens.push(Token::Eof);
    Ok(tokens)
}
