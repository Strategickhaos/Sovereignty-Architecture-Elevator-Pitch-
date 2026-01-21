//! # FlameLang Parser
//! 
//! Recursive descent parser for FlameLang source code.

pub mod ast;

use crate::lexer::tokens::Token;
use crate::{FlameError, Result};
use ast::*;

pub struct Parser {
    tokens: Vec<Token>,
    position: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, position: 0 }
    }

    fn current(&self) -> &Token {
        self.tokens.get(self.position).unwrap_or(&Token::Eof)
    }

    fn advance(&mut self) {
        if self.position < self.tokens.len() {
            self.position += 1;
        }
    }

    fn expect(&mut self, expected: Token) -> Result<()> {
        if self.current() == &expected {
            self.advance();
            Ok(())
        } else {
            Err(FlameError::ParseError(format!(
                "Expected {:?}, found {:?}",
                expected,
                self.current()
            )))
        }
    }

    pub fn parse(&mut self) -> Result<Program> {
        let mut functions = Vec::new();
        
        while !matches!(self.current(), Token::Eof) {
            functions.push(self.parse_function()?);
        }
        
        Ok(Program { functions })
    }

    fn parse_function(&mut self) -> Result<Function> {
        self.expect(Token::Fn)?;
        
        let name = match self.current() {
            Token::Identifier(n) => n.clone(),
            _ => return Err(FlameError::ParseError("Expected function name".to_string())),
        };
        self.advance();

        self.expect(Token::LeftParen)?;
        
        let mut params = Vec::new();
        while !matches!(self.current(), Token::RightParen) {
            if let Token::Identifier(param) = self.current() {
                params.push(param.clone());
                self.advance();
                if matches!(self.current(), Token::Comma) {
                    self.advance();
                }
            } else {
                return Err(FlameError::ParseError("Expected parameter name".to_string()));
            }
        }
        
        self.expect(Token::RightParen)?;
        self.expect(Token::LeftBrace)?;
        
        let mut body = Vec::new();
        while !matches!(self.current(), Token::RightBrace) {
            body.push(self.parse_statement()?);
        }
        
        self.expect(Token::RightBrace)?;
        
        Ok(Function { name, params, body })
    }

    fn parse_statement(&mut self) -> Result<Stmt> {
        match self.current() {
            Token::Let => self.parse_let(),
            Token::Return => self.parse_return(),
            Token::If => self.parse_if(),
            Token::While => self.parse_while(),
            _ => {
                let expr = self.parse_expression()?;
                self.expect(Token::Semicolon)?;
                Ok(Stmt::Expr(expr))
            }
        }
    }

    fn parse_let(&mut self) -> Result<Stmt> {
        self.advance(); // consume 'let'
        
        let name = match self.current() {
            Token::Identifier(n) => n.clone(),
            _ => return Err(FlameError::ParseError("Expected variable name".to_string())),
        };
        self.advance();
        
        self.expect(Token::Equal)?;
        let value = self.parse_expression()?;
        self.expect(Token::Semicolon)?;
        
        Ok(Stmt::Let { name, value })
    }

    fn parse_return(&mut self) -> Result<Stmt> {
        self.advance(); // consume 'return'
        let expr = self.parse_expression()?;
        self.expect(Token::Semicolon)?;
        Ok(Stmt::Return(expr))
    }

    fn parse_if(&mut self) -> Result<Stmt> {
        self.advance(); // consume 'if'
        
        self.expect(Token::LeftParen)?;
        let condition = self.parse_expression()?;
        self.expect(Token::RightParen)?;
        
        self.expect(Token::LeftBrace)?;
        let mut then_block = Vec::new();
        while !matches!(self.current(), Token::RightBrace) {
            then_block.push(self.parse_statement()?);
        }
        self.expect(Token::RightBrace)?;
        
        let else_block = if matches!(self.current(), Token::Else) {
            self.advance();
            self.expect(Token::LeftBrace)?;
            let mut else_stmts = Vec::new();
            while !matches!(self.current(), Token::RightBrace) {
                else_stmts.push(self.parse_statement()?);
            }
            self.expect(Token::RightBrace)?;
            Some(else_stmts)
        } else {
            None
        };
        
        Ok(Stmt::If {
            condition,
            then_block,
            else_block,
        })
    }

    fn parse_while(&mut self) -> Result<Stmt> {
        self.advance(); // consume 'while'
        
        self.expect(Token::LeftParen)?;
        let condition = self.parse_expression()?;
        self.expect(Token::RightParen)?;
        
        self.expect(Token::LeftBrace)?;
        let mut body = Vec::new();
        while !matches!(self.current(), Token::RightBrace) {
            body.push(self.parse_statement()?);
        }
        self.expect(Token::RightBrace)?;
        
        Ok(Stmt::While { condition, body })
    }

    fn parse_expression(&mut self) -> Result<Expr> {
        self.parse_or()
    }

    fn parse_or(&mut self) -> Result<Expr> {
        let mut left = self.parse_and()?;
        
        while matches!(self.current(), Token::Or) {
            self.advance();
            let right = self.parse_and()?;
            left = Expr::Binary {
                left: Box::new(left),
                op: BinOp::Or,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }

    fn parse_and(&mut self) -> Result<Expr> {
        let mut left = self.parse_equality()?;
        
        while matches!(self.current(), Token::And) {
            self.advance();
            let right = self.parse_equality()?;
            left = Expr::Binary {
                left: Box::new(left),
                op: BinOp::And,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }

    fn parse_equality(&mut self) -> Result<Expr> {
        let mut left = self.parse_comparison()?;
        
        while let Token::EqualEqual | Token::NotEqual = self.current() {
            let op = match self.current() {
                Token::EqualEqual => BinOp::Eq,
                Token::NotEqual => BinOp::Ne,
                _ => unreachable!(),
            };
            self.advance();
            let right = self.parse_comparison()?;
            left = Expr::Binary {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }

    fn parse_comparison(&mut self) -> Result<Expr> {
        let mut left = self.parse_term()?;
        
        while let Token::Less | Token::LessEqual | Token::Greater | Token::GreaterEqual = self.current() {
            let op = match self.current() {
                Token::Less => BinOp::Lt,
                Token::LessEqual => BinOp::Le,
                Token::Greater => BinOp::Gt,
                Token::GreaterEqual => BinOp::Ge,
                _ => unreachable!(),
            };
            self.advance();
            let right = self.parse_term()?;
            left = Expr::Binary {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }

    fn parse_term(&mut self) -> Result<Expr> {
        let mut left = self.parse_factor()?;
        
        while let Token::Plus | Token::Minus = self.current() {
            let op = match self.current() {
                Token::Plus => BinOp::Add,
                Token::Minus => BinOp::Sub,
                _ => unreachable!(),
            };
            self.advance();
            let right = self.parse_factor()?;
            left = Expr::Binary {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }

    fn parse_factor(&mut self) -> Result<Expr> {
        let mut left = self.parse_unary()?;
        
        while let Token::Star | Token::Slash | Token::Percent = self.current() {
            let op = match self.current() {
                Token::Star => BinOp::Mul,
                Token::Slash => BinOp::Div,
                Token::Percent => BinOp::Mod,
                _ => unreachable!(),
            };
            self.advance();
            let right = self.parse_unary()?;
            left = Expr::Binary {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }

    fn parse_unary(&mut self) -> Result<Expr> {
        match self.current() {
            Token::Minus | Token::Not => {
                let op = self.current().to_string();
                self.advance();
                let expr = self.parse_unary()?;
                Ok(Expr::Unary {
                    op,
                    expr: Box::new(expr),
                })
            }
            _ => self.parse_primary(),
        }
    }

    fn parse_primary(&mut self) -> Result<Expr> {
        match self.current().clone() {
            Token::Number(n) => {
                self.advance();
                Ok(Expr::Literal(Literal::Number(n)))
            }
            Token::String(s) => {
                self.advance();
                Ok(Expr::Literal(Literal::String(s)))
            }
            Token::True => {
                self.advance();
                Ok(Expr::Literal(Literal::Bool(true)))
            }
            Token::False => {
                self.advance();
                Ok(Expr::Literal(Literal::Bool(false)))
            }
            Token::Identifier(name) => {
                self.advance();
                // Check for function call
                if matches!(self.current(), Token::LeftParen) {
                    self.advance();
                    let mut args = Vec::new();
                    while !matches!(self.current(), Token::RightParen) {
                        args.push(self.parse_expression()?);
                        if matches!(self.current(), Token::Comma) {
                            self.advance();
                        }
                    }
                    self.expect(Token::RightParen)?;
                    Ok(Expr::Call { name, args })
                } else {
                    Ok(Expr::Identifier(name))
                }
            }
            Token::LeftParen => {
                self.advance();
                let expr = self.parse_expression()?;
                self.expect(Token::RightParen)?;
                Ok(expr)
            }
            _ => Err(FlameError::ParseError(format!(
                "Unexpected token: {:?}",
                self.current()
            ))),
        }
    }
}
