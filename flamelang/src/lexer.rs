//! # Layer 1: Linguistic Transformation
//! 
//! English → Hebrew → Glyph
//!
//! This module handles lexical analysis and tokenization of FlameLang source code.

use crate::{FlameError, FlameResult};

/// Token types in FlameLang
#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    /// Identifier (variable, function name, etc.)
    Identifier(String),
    /// Numeric literal
    Number(f64),
    /// String literal
    String(String),
    /// Keyword
    Keyword(Keyword),
    /// Operator
    Operator(Operator),
    /// Hebrew glyph
    HebrewGlyph(char),
    /// End of file
    Eof,
}

/// Keywords in FlameLang
#[derive(Debug, Clone, PartialEq)]
pub enum Keyword {
    /// Let binding
    Let,
    /// Bend operation (geometric transformation)
    Bend,
    /// Radius parameter
    Radius,
}

/// Operators
#[derive(Debug, Clone, PartialEq)]
pub enum Operator {
    /// Assignment =
    Assign,
    /// Colon :
    Colon,
    /// Semicolon ;
    Semicolon,
}

/// Lexer state
pub struct Lexer {
    source: String,
    position: usize,
}

impl Lexer {
    /// Create a new lexer
    pub fn new(source: &str) -> Self {
        Self {
            source: source.to_string(),
            position: 0,
        }
    }

    /// Tokenize the source code
    pub fn tokenize(&mut self) -> FlameResult<Vec<Token>> {
        let mut tokens = Vec::new();
        
        while self.position < self.source.len() {
            self.skip_whitespace();
            
            if self.position >= self.source.len() {
                break;
            }
            
            tokens.push(self.next_token()?);
        }
        
        tokens.push(Token::Eof);
        Ok(tokens)
    }

    fn skip_whitespace(&mut self) {
        while self.position < self.source.len() {
            let ch = self.source.chars().nth(self.position).unwrap();
            if ch.is_whitespace() {
                self.position += 1;
            } else {
                break;
            }
        }
    }

    fn next_token(&mut self) -> FlameResult<Token> {
        let ch = self.source.chars().nth(self.position).unwrap();
        
        match ch {
            '=' => {
                self.position += 1;
                Ok(Token::Operator(Operator::Assign))
            }
            ':' => {
                self.position += 1;
                Ok(Token::Operator(Operator::Colon))
            }
            ';' => {
                self.position += 1;
                Ok(Token::Operator(Operator::Semicolon))
            }
            '"' => self.read_string(),
            _ if ch.is_ascii_digit() => self.read_number(),
            _ if ch.is_alphabetic() => self.read_identifier(),
            _ => Err(FlameError::Lexer(format!("Unexpected character: {}", ch))),
        }
    }

    fn read_string(&mut self) -> FlameResult<Token> {
        self.position += 1; // Skip opening quote
        let start = self.position;
        
        while self.position < self.source.len() {
            let ch = self.source.chars().nth(self.position).unwrap();
            if ch == '"' {
                let string = self.source[start..self.position].to_string();
                self.position += 1; // Skip closing quote
                return Ok(Token::String(string));
            }
            self.position += 1;
        }
        
        Err(FlameError::Lexer("Unterminated string".to_string()))
    }

    fn read_number(&mut self) -> FlameResult<Token> {
        let start = self.position;
        
        while self.position < self.source.len() {
            let ch = self.source.chars().nth(self.position).unwrap();
            if ch.is_ascii_digit() || ch == '.' {
                self.position += 1;
            } else {
                break;
            }
        }
        
        let num_str = &self.source[start..self.position];
        let num = num_str.parse::<f64>()
            .map_err(|e| FlameError::Lexer(format!("Invalid number: {}", e)))?;
        
        Ok(Token::Number(num))
    }

    fn read_identifier(&mut self) -> FlameResult<Token> {
        let start = self.position;
        
        while self.position < self.source.len() {
            let ch = self.source.chars().nth(self.position).unwrap();
            if ch.is_alphanumeric() || ch == '_' {
                self.position += 1;
            } else {
                break;
            }
        }
        
        let ident = self.source[start..self.position].to_string();
        
        let token = match ident.as_str() {
            "let" => Token::Keyword(Keyword::Let),
            "bend" => Token::Keyword(Keyword::Bend),
            "radius" => Token::Keyword(Keyword::Radius),
            _ => Token::Identifier(ident),
        };
        
        Ok(token)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize_simple() {
        let mut lexer = Lexer::new("let x = 5;");
        let tokens = lexer.tokenize().unwrap();
        
        assert_eq!(tokens.len(), 6);
        assert!(matches!(tokens[0], Token::Keyword(Keyword::Let)));
        assert!(matches!(tokens[1], Token::Identifier(_)));
    }
}
