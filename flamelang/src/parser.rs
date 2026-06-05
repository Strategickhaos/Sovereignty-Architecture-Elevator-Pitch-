//! # FlameLang Parser
//! 
//! Minimal parser implementation for FlameLang
//! 
//! © 2025 Strategickhaos DAO LLC - Ratio Ex Nihilo

use crate::lexer::Token;

/// AST Expression types
#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    /// Literal value
    Literal(Literal),
    /// Binary operation
    Binary {
        left: Box<Expr>,
        op: BinOp,
        right: Box<Expr>,
    },
    /// Glyph symbol
    Glyph(char),
    /// Variable reference
    Var(String),
}

/// Literal types
#[derive(Debug, Clone, PartialEq)]
pub enum Literal {
    /// Integer
    Integer(i64),
    /// Float
    Float(f64),
    /// String
    String(String),
    /// Boolean
    Bool(bool),
}

/// Binary operators
#[derive(Debug, Clone, PartialEq)]
pub enum BinOp {
    /// Addition
    Add,
    /// Subtraction
    Sub,
    /// Multiplication
    Mul,
    /// Division
    Div,
}

/// Parser for FlameLang
pub struct Parser {
    tokens: Vec<Token>,
    position: usize,
}

impl Parser {
    /// Create a new parser
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            position: 0,
        }
    }
    
    /// Parse the tokens into an AST
    pub fn parse(&mut self) -> Result<Vec<Expr>, String> {
        let mut exprs = Vec::new();
        
        while self.position < self.tokens.len() {
            if matches!(self.tokens[self.position], Token::Eof) {
                break;
            }
            
            exprs.push(self.parse_expr()?);
        }
        
        Ok(exprs)
    }
    
    fn parse_expr(&mut self) -> Result<Expr, String> {
        self.parse_additive()
    }
    
    fn parse_additive(&mut self) -> Result<Expr, String> {
        let mut left = self.parse_multiplicative()?;
        
        while self.position < self.tokens.len() {
            match &self.tokens[self.position] {
                Token::Plus => {
                    self.position += 1;
                    let right = self.parse_multiplicative()?;
                    left = Expr::Binary {
                        left: Box::new(left),
                        op: BinOp::Add,
                        right: Box::new(right),
                    };
                }
                Token::Minus => {
                    self.position += 1;
                    let right = self.parse_multiplicative()?;
                    left = Expr::Binary {
                        left: Box::new(left),
                        op: BinOp::Sub,
                        right: Box::new(right),
                    };
                }
                _ => break,
            }
        }
        
        Ok(left)
    }
    
    fn parse_multiplicative(&mut self) -> Result<Expr, String> {
        let mut left = self.parse_primary()?;
        
        while self.position < self.tokens.len() {
            match &self.tokens[self.position] {
                Token::Star => {
                    self.position += 1;
                    let right = self.parse_primary()?;
                    left = Expr::Binary {
                        left: Box::new(left),
                        op: BinOp::Mul,
                        right: Box::new(right),
                    };
                }
                Token::Slash => {
                    self.position += 1;
                    let right = self.parse_primary()?;
                    left = Expr::Binary {
                        left: Box::new(left),
                        op: BinOp::Div,
                        right: Box::new(right),
                    };
                }
                _ => break,
            }
        }
        
        Ok(left)
    }
    
    fn parse_primary(&mut self) -> Result<Expr, String> {
        if self.position >= self.tokens.len() {
            return Err("Unexpected end of input".to_string());
        }
        
        let token = self.tokens[self.position].clone();
        self.position += 1;
        
        match token {
            Token::Integer(i) => Ok(Expr::Literal(Literal::Integer(i))),
            Token::Float(f) => Ok(Expr::Literal(Literal::Float(f))),
            Token::String(s) => Ok(Expr::Literal(Literal::String(s))),
            Token::Bool(b) => Ok(Expr::Literal(Literal::Bool(b))),
            Token::Glyph(c) => Ok(Expr::Glyph(c)),
            Token::Ident(name) => Ok(Expr::Var(name)),
            Token::LParen => {
                let expr = self.parse_expr()?;
                if self.position < self.tokens.len() && matches!(self.tokens[self.position], Token::RParen) {
                    self.position += 1;
                    Ok(expr)
                } else {
                    Err("Expected closing parenthesis".to_string())
                }
            }
            _ => Err(format!("Unexpected token: {:?}", token)),
        }
    }
}
