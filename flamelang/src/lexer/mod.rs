//! # FlameLang Lexer
//! 
//! Tokenizes FlameLang source code into a stream of tokens.

pub mod tokens;

use crate::{FlameError, Result};
use tokens::Token;

pub struct Lexer {
    input: Vec<char>,
    position: usize,
    current_char: Option<char>,
}

impl Lexer {
    pub fn new(input: &str) -> Self {
        let chars: Vec<char> = input.chars().collect();
        let current_char = chars.get(0).copied();
        Lexer {
            input: chars,
            position: 0,
            current_char,
        }
    }

    fn advance(&mut self) {
        self.position += 1;
        self.current_char = self.input.get(self.position).copied();
    }

    fn peek(&self) -> Option<char> {
        self.input.get(self.position + 1).copied()
    }

    fn skip_whitespace(&mut self) {
        while let Some(ch) = self.current_char {
            if ch.is_whitespace() {
                self.advance();
            } else {
                break;
            }
        }
    }

    fn skip_comment(&mut self) {
        if self.current_char == Some('/') && self.peek() == Some('/') {
            // Skip '//'
            self.advance();
            self.advance();
            // Skip until end of line
            while self.current_char.is_some() && self.current_char != Some('\n') {
                self.advance();
            }
            // Skip the newline
            if self.current_char == Some('\n') {
                self.advance();
            }
        }
    }

    fn skip_whitespace_and_comments(&mut self) {
        loop {
            let start_pos = self.position;
            self.skip_whitespace();
            self.skip_comment();
            // If position didn't change, we're done
            if self.position == start_pos {
                break;
            }
        }
    }

    fn read_number(&mut self) -> Result<Token> {
        let mut num_str = String::new();
        while let Some(ch) = self.current_char {
            if ch.is_numeric() || ch == '.' {
                num_str.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        num_str.parse::<f64>()
            .map(Token::Number)
            .map_err(|e| FlameError::LexError(format!("Invalid number: {}", e)))
    }

    fn read_string(&mut self) -> Result<Token> {
        self.advance(); // Skip opening quote
        let mut string = String::new();
        
        while let Some(ch) = self.current_char {
            if ch == '"' {
                self.advance(); // Skip closing quote
                return Ok(Token::String(string));
            }
            if ch == '\\' {
                self.advance();
                if let Some(escaped) = self.current_char {
                    match escaped {
                        'n' => string.push('\n'),
                        't' => string.push('\t'),
                        '\\' => string.push('\\'),
                        '"' => string.push('"'),
                        _ => string.push(escaped),
                    }
                    self.advance();
                }
            } else {
                string.push(ch);
                self.advance();
            }
        }
        
        Err(FlameError::LexError("Unterminated string".to_string()))
    }

    fn read_identifier(&mut self) -> Token {
        let mut ident = String::new();
        while let Some(ch) = self.current_char {
            if ch.is_alphanumeric() || ch == '_' {
                ident.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        match ident.as_str() {
            "fn" => Token::Fn,
            "let" => Token::Let,
            "return" => Token::Return,
            "if" => Token::If,
            "else" => Token::Else,
            "while" => Token::While,
            "true" => Token::True,
            "false" => Token::False,
            _ => Token::Identifier(ident),
        }
    }

    pub fn next_token(&mut self) -> Result<Token> {
        self.skip_whitespace_and_comments();

        let current = match self.current_char {
            Some(ch) => ch,
            None => return Ok(Token::Eof),
        };

        let token = match current {
            '0'..='9' => return self.read_number(),
            '"' => return self.read_string(),
            'a'..='z' | 'A'..='Z' | '_' => return Ok(self.read_identifier()),
            '+' => Token::Plus,
            '-' => {
                if self.peek() == Some('>') {
                    self.advance();
                    Token::Arrow
                } else {
                    Token::Minus
                }
            }
            '*' => Token::Star,
            '/' => Token::Slash,
            '%' => Token::Percent,
            '=' => {
                if self.peek() == Some('=') {
                    self.advance();
                    Token::EqualEqual
                } else {
                    Token::Equal
                }
            }
            '!' => {
                if self.peek() == Some('=') {
                    self.advance();
                    Token::NotEqual
                } else {
                    Token::Not
                }
            }
            '<' => {
                if self.peek() == Some('=') {
                    self.advance();
                    Token::LessEqual
                } else {
                    Token::Less
                }
            }
            '>' => {
                if self.peek() == Some('=') {
                    self.advance();
                    Token::GreaterEqual
                } else {
                    Token::Greater
                }
            }
            '&' => {
                if self.peek() == Some('&') {
                    self.advance();
                    Token::And
                } else {
                    return Err(FlameError::LexError(format!("Unexpected character: {}", current)));
                }
            }
            '|' => {
                if self.peek() == Some('|') {
                    self.advance();
                    Token::Or
                } else {
                    return Err(FlameError::LexError(format!("Unexpected character: {}", current)));
                }
            }
            '(' => Token::LeftParen,
            ')' => Token::RightParen,
            '{' => Token::LeftBrace,
            '}' => Token::RightBrace,
            '[' => Token::LeftBracket,
            ']' => Token::RightBracket,
            ',' => Token::Comma,
            ';' => Token::Semicolon,
            ':' => Token::Colon,
            _ => return Err(FlameError::LexError(format!("Unexpected character: {}", current))),
        };

        self.advance();
        Ok(token)
    }

    pub fn tokenize(&mut self) -> Result<Vec<Token>> {
        let mut tokens = Vec::new();
        loop {
            let token = self.next_token()?;
            let is_eof = matches!(token, Token::Eof);
            tokens.push(token);
            if is_eof {
                break;
            }
        }
        Ok(tokens)
    }
}
