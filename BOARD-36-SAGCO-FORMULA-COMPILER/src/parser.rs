use crate::ast::{BinOp, Expr, UnaryOp};
use crate::token::{Spanned, Token};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ParseError {
    #[error("Unexpected token {0:?} at line {1}, col {2}")]
    UnexpectedToken(Token, usize, usize),
    #[error("Expected {0}, got {1:?}")]
    Expected(String, Token),
    #[error("Unexpected end of input")]
    UnexpectedEof,
}

pub struct Parser {
    tokens: Vec<Spanned<Token>>,
    pos: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Spanned<Token>>) -> Self {
        Parser { tokens, pos: 0 }
    }

    fn peek(&self) -> &Token {
        self.tokens
            .get(self.pos)
            .map(|s| &s.token)
            .unwrap_or(&Token::EOF)
    }

    fn peek_span(&self) -> (usize, usize) {
        self.tokens
            .get(self.pos)
            .map(|s| (s.span.line, s.span.col))
            .unwrap_or((0, 0))
    }

    fn advance(&mut self) -> &Token {
        let tok = &self.tokens[self.pos].token;
        if self.pos < self.tokens.len() - 1 {
            self.pos += 1;
        }
        tok
    }

    fn expect(&mut self, expected: Token) -> Result<(), ParseError> {
        if self.peek() == &expected {
            self.advance();
            Ok(())
        } else {
            Err(ParseError::Expected(
                format!("{:?}", expected),
                self.peek().clone(),
            ))
        }
    }

    pub fn parse(&mut self) -> Result<Expr, ParseError> {
        let expr = self.parse_or()?;
        Ok(expr)
    }

    fn parse_or(&mut self) -> Result<Expr, ParseError> {
        let mut left = self.parse_and()?;
        loop {
            match self.peek() {
                Token::Ident(s) if s == "OR" => {
                    self.advance();
                    let right = self.parse_and()?;
                    left = Expr::BinOp {
                        left: Box::new(left),
                        op: BinOp::Or,
                        right: Box::new(right),
                    };
                }
                _ => break,
            }
        }
        Ok(left)
    }

    fn parse_and(&mut self) -> Result<Expr, ParseError> {
        let mut left = self.parse_comparison()?;
        loop {
            match self.peek() {
                Token::Ident(s) if s == "AND" => {
                    self.advance();
                    let right = self.parse_comparison()?;
                    left = Expr::BinOp {
                        left: Box::new(left),
                        op: BinOp::And,
                        right: Box::new(right),
                    };
                }
                _ => break,
            }
        }
        Ok(left)
    }

    fn parse_comparison(&mut self) -> Result<Expr, ParseError> {
        let mut left = self.parse_concat()?;
        loop {
            let op = match self.peek() {
                Token::Eq => BinOp::Eq,
                Token::NEq => BinOp::NEq,
                Token::Lt => BinOp::Lt,
                Token::Gt => BinOp::Gt,
                Token::LtEq => BinOp::LtEq,
                Token::GtEq => BinOp::GtEq,
                _ => break,
            };
            self.advance();
            let right = self.parse_concat()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        Ok(left)
    }

    fn parse_concat(&mut self) -> Result<Expr, ParseError> {
        let mut left = self.parse_additive()?;
        loop {
            if self.peek() == &Token::Ampersand {
                self.advance();
                let right = self.parse_additive()?;
                left = Expr::BinOp {
                    left: Box::new(left),
                    op: BinOp::Concat,
                    right: Box::new(right),
                };
            } else {
                break;
            }
        }
        Ok(left)
    }

    fn parse_additive(&mut self) -> Result<Expr, ParseError> {
        let mut left = self.parse_multiplicative()?;
        loop {
            let op = match self.peek() {
                Token::Plus => BinOp::Add,
                Token::Minus => BinOp::Sub,
                _ => break,
            };
            self.advance();
            let right = self.parse_multiplicative()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        Ok(left)
    }

    fn parse_multiplicative(&mut self) -> Result<Expr, ParseError> {
        let mut left = self.parse_power()?;
        loop {
            let op = match self.peek() {
                Token::Star => BinOp::Mul,
                Token::Slash => BinOp::Div,
                _ => break,
            };
            self.advance();
            let right = self.parse_power()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        Ok(left)
    }

    fn parse_power(&mut self) -> Result<Expr, ParseError> {
        let base = self.parse_unary()?;
        if self.peek() == &Token::Caret {
            self.advance();
            let exp = self.parse_power()?; // right-associative
            Ok(Expr::BinOp {
                left: Box::new(base),
                op: BinOp::Pow,
                right: Box::new(exp),
            })
        } else {
            Ok(base)
        }
    }

    fn parse_unary(&mut self) -> Result<Expr, ParseError> {
        match self.peek().clone() {
            Token::Minus => {
                self.advance();
                let expr = self.parse_unary()?;
                Ok(Expr::UnaryOp {
                    op: UnaryOp::Neg,
                    expr: Box::new(expr),
                })
            }
            Token::Bang => {
                self.advance();
                let expr = self.parse_unary()?;
                Ok(Expr::UnaryOp {
                    op: UnaryOp::Not,
                    expr: Box::new(expr),
                })
            }
            _ => self.parse_primary(),
        }
    }

    fn parse_primary(&mut self) -> Result<Expr, ParseError> {
        match self.peek().clone() {
            Token::Number(n) => {
                self.advance();
                Ok(Expr::Number(n))
            }
            Token::Str(s) => {
                self.advance();
                Ok(Expr::Str(s))
            }
            Token::Bool(b) => {
                self.advance();
                Ok(Expr::Bool(b))
            }
            Token::CellRef(addr) => {
                self.advance();
                Ok(Expr::CellRef(addr))
            }
            Token::RangeRef(from, to) => {
                self.advance();
                Ok(Expr::RangeRef(from, to))
            }
            Token::LParen => {
                self.advance();
                let expr = self.parse()?;
                self.expect(Token::RParen)?;
                Ok(expr)
            }
            Token::Ident(name) => {
                self.advance();
                // Special IF form
                if name == "IF" {
                    return self.parse_if();
                }
                // Function call
                if self.peek() == &Token::LParen {
                    self.advance(); // consume '('
                    let args = self.parse_args()?;
                    self.expect(Token::RParen)?;
                    Ok(Expr::Call { name, args })
                } else {
                    // bare identifier (shouldn't normally happen but handle gracefully)
                    Ok(Expr::Str(name))
                }
            }
            Token::EOF => Err(ParseError::UnexpectedEof),
            other => {
                let (line, col) = self.peek_span();
                Err(ParseError::UnexpectedToken(other, line, col))
            }
        }
    }

    fn parse_if(&mut self) -> Result<Expr, ParseError> {
        self.expect(Token::LParen)?;
        let cond = self.parse()?;
        // accept comma or semicolon
        match self.peek() {
            Token::Comma | Token::Semicolon => { self.advance(); }
            _ => return Err(ParseError::Expected("comma".to_string(), self.peek().clone())),
        }
        let then = self.parse()?;
        match self.peek() {
            Token::Comma | Token::Semicolon => { self.advance(); }
            _ => return Err(ParseError::Expected("comma".to_string(), self.peek().clone())),
        }
        let else_ = self.parse()?;
        self.expect(Token::RParen)?;
        Ok(Expr::IfExpr {
            cond: Box::new(cond),
            then: Box::new(then),
            else_: Box::new(else_),
        })
    }

    fn parse_args(&mut self) -> Result<Vec<Expr>, ParseError> {
        let mut args = Vec::new();
        if self.peek() == &Token::RParen {
            return Ok(args);
        }
        args.push(self.parse()?);
        loop {
            match self.peek() {
                Token::Comma | Token::Semicolon => {
                    self.advance();
                    if self.peek() == &Token::RParen {
                        break;
                    }
                    args.push(self.parse()?);
                }
                _ => break,
            }
        }
        Ok(args)
    }
}

pub fn parse(input: &str) -> Result<Expr, ParseError> {
    use crate::lexer::tokenize;

    let tokens = tokenize(input).map_err(|e| ParseError::Expected(e.to_string(), Token::EOF))?;
    let mut parser = Parser::new(tokens);
    parser.parse()
}
