//! # FlameLang Lexer
//! 
//! Minimal lexer implementation for FlameLang
//! 
//! © 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

/// Token types for FlameLang
#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    /// Integer literal
    Integer(i64),
    /// Float literal
    Float(f64),
    /// String literal
    String(String),
    /// Boolean literal
    Bool(bool),
    /// Glyph character
    Glyph(char),
    /// Identifier
    Ident(String),
    /// Operators
    Plus,
    Minus,
    Star,
    Slash,
    /// Delimiters
    LParen,
    RParen,
    LBrace,
    RBrace,
    /// End of file
    Eof,
}

/// Lexer for FlameLang source code
pub struct Lexer {
    input: Vec<char>,
    position: usize,
}

impl Lexer {
    /// Create a new lexer
    pub fn new(input: &str) -> Self {
        Self {
            input: input.chars().collect(),
            position: 0,
        }
    }
    
    /// Tokenize the input
    pub fn tokenize(&mut self) -> Vec<Token> {
        let mut tokens = Vec::new();
        
        while self.position < self.input.len() {
            self.skip_whitespace();
            
            if self.position >= self.input.len() {
                break;
            }
            
            let ch = self.input[self.position];
            
            // Check for glyphs (Unicode symbols)
            if ch > '\u{007F}' {
                tokens.push(Token::Glyph(ch));
                self.position += 1;
                continue;
            }
            
            // Numbers
            if ch.is_ascii_digit() {
                tokens.push(self.read_number());
                continue;
            }
            
            // Identifiers
            if ch.is_ascii_alphabetic() || ch == '_' {
                tokens.push(self.read_ident());
                continue;
            }
            
            // Operators and delimiters
            match ch {
                '+' => {
                    tokens.push(Token::Plus);
                    self.position += 1;
                }
                '-' => {
                    tokens.push(Token::Minus);
                    self.position += 1;
                }
                '*' => {
                    tokens.push(Token::Star);
                    self.position += 1;
                }
                '/' => {
                    tokens.push(Token::Slash);
                    self.position += 1;
                }
                '(' => {
                    tokens.push(Token::LParen);
                    self.position += 1;
                }
                ')' => {
                    tokens.push(Token::RParen);
                    self.position += 1;
                }
                '{' => {
                    tokens.push(Token::LBrace);
                    self.position += 1;
                }
                '}' => {
                    tokens.push(Token::RBrace);
                    self.position += 1;
                }
                _ => {
                    // Unknown character, skip it
                    self.position += 1;
                }
            }
        }
        
        tokens.push(Token::Eof);
        tokens
    }
    
    fn skip_whitespace(&mut self) {
        while self.position < self.input.len() && self.input[self.position].is_whitespace() {
            self.position += 1;
        }
    }
    
    fn read_number(&mut self) -> Token {
        let start = self.position;
        let mut has_dot = false;
        
        while self.position < self.input.len() {
            let ch = self.input[self.position];
            if ch.is_ascii_digit() {
                self.position += 1;
            } else if ch == '.' && !has_dot {
                has_dot = true;
                self.position += 1;
            } else {
                break;
            }
        }
        
        let num_str: String = self.input[start..self.position].iter().collect();
        
        if has_dot {
            Token::Float(num_str.parse().unwrap())
        } else {
            Token::Integer(num_str.parse().unwrap())
        }
    }
    
    fn read_ident(&mut self) -> Token {
        let start = self.position;
        
        while self.position < self.input.len() {
            let ch = self.input[self.position];
            if ch.is_ascii_alphanumeric() || ch == '_' {
                self.position += 1;
            } else {
                break;
            }
        }
        
        let ident: String = self.input[start..self.position].iter().collect();
        
        // Check for boolean literals
        match ident.as_str() {
            "true" => Token::Bool(true),
            "false" => Token::Bool(false),
            _ => Token::Ident(ident),
        }
    }
}
