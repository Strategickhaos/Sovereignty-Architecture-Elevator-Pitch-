use crate::token::{Span, Spanned, Token};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum LexError {
    #[error("Unexpected character '{0}' at line {1}, col {2}")]
    UnexpectedChar(char, usize, usize),
    #[error("Unterminated string at line {0}, col {1}")]
    UnterminatedString(usize, usize),
}

pub struct Lexer {
    input: Vec<char>,
    pos: usize,
    line: usize,
    col: usize,
}

impl Lexer {
    pub fn new(input: &str) -> Self {
        // Strip leading '=' if present
        let s = if input.starts_with('=') {
            &input[1..]
        } else {
            input
        };
        Lexer {
            input: s.chars().collect(),
            pos: 0,
            line: 1,
            col: 1,
        }
    }

    fn peek(&self) -> Option<char> {
        self.input.get(self.pos).copied()
    }

    fn advance(&mut self) -> Option<char> {
        let c = self.input.get(self.pos).copied();
        self.pos += 1;
        if c == Some('\n') {
            self.line += 1;
            self.col = 1;
        } else {
            self.col += 1;
        }
        c
    }

    fn span(&self) -> Span {
        Span::new(self.line, self.col)
    }

    fn skip_whitespace(&mut self) {
        while matches!(self.peek(), Some(' ') | Some('\t') | Some('\r') | Some('\n')) {
            self.advance();
        }
    }

    fn read_number(&mut self) -> Token {
        let mut s = String::new();
        while let Some(c) = self.peek() {
            if c.is_ascii_digit() || c == '.' {
                s.push(c);
                self.advance();
            } else {
                break;
            }
        }
        Token::Number(s.parse().unwrap_or(0.0))
    }

    fn read_string(&mut self) -> Result<Token, LexError> {
        let (line, col) = (self.line, self.col);
        self.advance(); // consume opening quote
        let mut s = String::new();
        loop {
            match self.peek() {
                Some('"') => {
                    self.advance();
                    return Ok(Token::Str(s));
                }
                Some(c) => {
                    s.push(c);
                    self.advance();
                }
                None => return Err(LexError::UnterminatedString(line, col)),
            }
        }
    }

    /// Read an identifier or cell ref (e.g. A1, B2, SUM, IF)
    fn read_ident_or_cell(&mut self) -> Token {
        let mut s = String::new();
        while let Some(c) = self.peek() {
            if c.is_alphanumeric() || c == '_' {
                s.push(c);
                self.advance();
            } else {
                break;
            }
        }

        // Check if it's a range ref like A1:B10 — peek ahead
        // Already consumed ident; check if next is ':' and next-next looks like cell
        if self.peek() == Some(':') {
            // peek to see if right side is a cell ref
            let saved_pos = self.pos;
            let saved_line = self.line;
            let saved_col = self.col;
            self.advance(); // consume ':'
            let mut right = String::new();
            while let Some(c) = self.peek() {
                if c.is_alphanumeric() {
                    right.push(c);
                    self.advance();
                } else {
                    break;
                }
            }
            if is_cell_ref(&right) {
                return Token::RangeRef(s, right);
            } else {
                // Not a range, backtrack
                self.pos = saved_pos;
                self.line = saved_line;
                self.col = saved_col;
            }
        }

        // Check keywords
        match s.as_str() {
            "TRUE" | "true" => return Token::Bool(true),
            "FALSE" | "false" => return Token::Bool(false),
            _ => {}
        }

        if is_cell_ref(&s) {
            Token::CellRef(s)
        } else {
            Token::Ident(s)
        }
    }

    pub fn tokenize(&mut self) -> Result<Vec<Spanned<Token>>, LexError> {
        let mut tokens = Vec::new();
        loop {
            self.skip_whitespace();
            let span = self.span();
            match self.peek() {
                None => {
                    tokens.push(Spanned::new(Token::EOF, span));
                    break;
                }
                Some(c) => {
                    let tok = match c {
                        '(' => { self.advance(); Token::LParen }
                        ')' => { self.advance(); Token::RParen }
                        ',' => { self.advance(); Token::Comma }
                        ';' => { self.advance(); Token::Semicolon }
                        '+' => { self.advance(); Token::Plus }
                        '-' => { self.advance(); Token::Minus }
                        '*' => { self.advance(); Token::Star }
                        '/' => { self.advance(); Token::Slash }
                        '^' => { self.advance(); Token::Caret }
                        '&' => { self.advance(); Token::Ampersand }
                        '<' => {
                            self.advance();
                            if self.peek() == Some('=') {
                                self.advance();
                                Token::LtEq
                            } else if self.peek() == Some('>') {
                                self.advance();
                                Token::NEq
                            } else {
                                Token::Lt
                            }
                        }
                        '>' => {
                            self.advance();
                            if self.peek() == Some('=') {
                                self.advance();
                                Token::GtEq
                            } else {
                                Token::Gt
                            }
                        }
                        '=' => {
                            self.advance();
                            if self.peek() == Some('=') {
                                self.advance();
                            }
                            Token::Eq
                        }
                        '!' => {
                            self.advance();
                            if self.peek() == Some('=') {
                                self.advance();
                                Token::NEq
                            } else {
                                Token::Bang
                            }
                        }
                        ':' => { self.advance(); Token::Colon }
                        '"' => self.read_string()?,
                        c if c.is_ascii_digit() || c == '.' => self.read_number(),
                        c if c.is_alphabetic() || c == '_' => self.read_ident_or_cell(),
                        other => {
                            return Err(LexError::UnexpectedChar(other, self.line, self.col));
                        }
                    };
                    tokens.push(Spanned::new(tok, span));
                }
            }
        }
        Ok(tokens)
    }
}

/// A cell ref has uppercase letters followed by digits, e.g. A1, B10, AB3
fn is_cell_ref(s: &str) -> bool {
    if s.is_empty() {
        return false;
    }
    let mut chars = s.chars().peekable();
    let mut has_letters = false;
    let mut has_digits = false;
    while let Some(&c) = chars.peek() {
        if c.is_ascii_uppercase() {
            has_letters = true;
            chars.next();
        } else {
            break;
        }
    }
    while let Some(&c) = chars.peek() {
        if c.is_ascii_digit() {
            has_digits = true;
            chars.next();
        } else {
            break;
        }
    }
    has_letters && has_digits && chars.peek().is_none()
}

pub fn tokenize(input: &str) -> Result<Vec<Spanned<Token>>, LexError> {
    Lexer::new(input).tokenize()
}
