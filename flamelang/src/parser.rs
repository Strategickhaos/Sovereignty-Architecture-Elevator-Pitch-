//! Parser for FlameLang
//! Recursive descent parser

use crate::lexer::Token;
use crate::ast::*;
use crate::{FlameError, FlameResult};

pub struct Parser {
    tokens: Vec<Token>,
    current: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self { tokens, current: 0 }
    }
    
    fn current_token(&self) -> &Token {
        self.tokens.get(self.current).unwrap_or(&Token::Eof)
    }
    
    fn advance(&mut self) -> &Token {
        if self.current < self.tokens.len() {
            self.current += 1;
        }
        self.current_token()
    }
    
    fn expect(&mut self, expected: Token) -> FlameResult<()> {
        if self.current_token() == &expected {
            self.advance();
            Ok(())
        } else {
            Err(FlameError::ParserError {
                line: self.current,
                message: format!("Expected {:?}, got {:?}", expected, self.current_token()),
            })
        }
    }
    
    pub fn parse_program(&mut self) -> FlameResult<Program> {
        let mut statements = Vec::new();
        
        while self.current_token() != &Token::Eof {
            statements.push(self.parse_statement()?);
        }
        
        Ok(Program { statements })
    }
    
    fn parse_statement(&mut self) -> FlameResult<Statement> {
        match self.current_token() {
            Token::Fn => self.parse_function_def(),
            Token::Let => self.parse_let_binding(),
            Token::Return => self.parse_return(),
            Token::If => self.parse_if(),
            Token::While => self.parse_while(),
            Token::For => self.parse_for(),
            _ => {
                let expr = self.parse_expression()?;
                self.expect(Token::Semicolon)?;
                Ok(Statement::Expression(expr))
            }
        }
    }
    
    fn parse_function_def(&mut self) -> FlameResult<Statement> {
        self.expect(Token::Fn)?;
        
        let name = match self.current_token() {
            Token::Ident(s) => {
                let name = s.clone();
                self.advance();
                name
            }
            _ => return Err(FlameError::ParserError {
                line: self.current,
                message: "Expected function name".to_string(),
            }),
        };
        
        self.expect(Token::LParen)?;
        let params = self.parse_params()?;
        self.expect(Token::RParen)?;
        
        self.expect(Token::Arrow)?;
        let return_type = self.parse_type()?;
        
        self.expect(Token::LBrace)?;
        let body = self.parse_block()?;
        self.expect(Token::RBrace)?;
        
        Ok(Statement::FunctionDef {
            name,
            params,
            return_type,
            body,
        })
    }
    
    fn parse_let_binding(&mut self) -> FlameResult<Statement> {
        self.expect(Token::Let)?;
        
        let name = match self.current_token() {
            Token::Ident(s) => {
                let name = s.clone();
                self.advance();
                name
            }
            _ => return Err(FlameError::ParserError {
                line: self.current,
                message: "Expected variable name".to_string(),
            }),
        };
        
        let type_annotation = if self.current_token() == &Token::Colon {
            self.advance();
            Some(self.parse_type()?)
        } else {
            None
        };
        
        self.expect(Token::Assign)?;
        let value = self.parse_expression()?;
        self.expect(Token::Semicolon)?;
        
        Ok(Statement::LetBinding {
            name,
            type_annotation,
            value,
        })
    }
    
    fn parse_return(&mut self) -> FlameResult<Statement> {
        self.expect(Token::Return)?;
        
        let value = if self.current_token() == &Token::Semicolon {
            None
        } else {
            Some(self.parse_expression()?)
        };
        
        self.expect(Token::Semicolon)?;
        Ok(Statement::Return(value))
    }
    
    fn parse_if(&mut self) -> FlameResult<Statement> {
        self.expect(Token::If)?;
        let condition = self.parse_expression()?;
        
        self.expect(Token::LBrace)?;
        let then_block = self.parse_block()?;
        self.expect(Token::RBrace)?;
        
        let else_block = if self.current_token() == &Token::Else {
            self.advance();
            self.expect(Token::LBrace)?;
            let block = self.parse_block()?;
            self.expect(Token::RBrace)?;
            Some(block)
        } else {
            None
        };
        
        Ok(Statement::If {
            condition,
            then_block,
            else_block,
        })
    }
    
    fn parse_while(&mut self) -> FlameResult<Statement> {
        self.expect(Token::While)?;
        let condition = self.parse_expression()?;
        
        self.expect(Token::LBrace)?;
        let body = self.parse_block()?;
        self.expect(Token::RBrace)?;
        
        Ok(Statement::While { condition, body })
    }
    
    fn parse_for(&mut self) -> FlameResult<Statement> {
        self.expect(Token::For)?;
        
        let var = match self.current_token() {
            Token::Ident(s) => {
                let var = s.clone();
                self.advance();
                var
            }
            _ => return Err(FlameError::ParserError {
                line: self.current,
                message: "Expected loop variable".to_string(),
            }),
        };
        
        self.expect(Token::In)?;
        let start = self.parse_expression()?;
        // Simplified: we'd need a range operator here
        let end = start.clone();
        
        self.expect(Token::LBrace)?;
        let body = self.parse_block()?;
        self.expect(Token::RBrace)?;
        
        Ok(Statement::For { var, start, end, body })
    }
    
    fn parse_block(&mut self) -> FlameResult<Vec<Statement>> {
        let mut statements = Vec::new();
        
        while self.current_token() != &Token::RBrace && self.current_token() != &Token::Eof {
            statements.push(self.parse_statement()?);
        }
        
        Ok(statements)
    }
    
    fn parse_params(&mut self) -> FlameResult<Vec<(String, Type)>> {
        let mut params = Vec::new();
        
        if self.current_token() == &Token::RParen {
            return Ok(params);
        }
        
        loop {
            let name = match self.current_token() {
                Token::Ident(s) => {
                    let name = s.clone();
                    self.advance();
                    name
                }
                _ => break,
            };
            
            self.expect(Token::Colon)?;
            let param_type = self.parse_type()?;
            
            params.push((name, param_type));
            
            if self.current_token() != &Token::Comma {
                break;
            }
            self.advance();
        }
        
        Ok(params)
    }
    
    fn parse_type(&mut self) -> FlameResult<Type> {
        match self.current_token() {
            Token::I32Type => {
                self.advance();
                Ok(Type::I32)
            }
            Token::I64Type => {
                self.advance();
                Ok(Type::I64)
            }
            Token::F64Type => {
                self.advance();
                Ok(Type::F64)
            }
            Token::BoolType => {
                self.advance();
                Ok(Type::Bool)
            }
            Token::StringType => {
                self.advance();
                Ok(Type::String)
            }
            Token::LBracket => {
                self.advance();
                let elem_type = self.parse_type()?;
                self.expect(Token::Semicolon)?;
                
                let size = match self.current_token() {
                    Token::Integer(n) => {
                        let size = *n as usize;
                        self.advance();
                        Some(size)
                    }
                    _ => None,
                };
                
                self.expect(Token::RBracket)?;
                Ok(Type::Array(Box::new(elem_type), size))
            }
            _ => Err(FlameError::ParserError {
                line: self.current,
                message: format!("Expected type, got {:?}", self.current_token()),
            }),
        }
    }
    
    fn parse_expression(&mut self) -> FlameResult<Expr> {
        self.parse_logical_or()
    }
    
    fn parse_logical_or(&mut self) -> FlameResult<Expr> {
        let mut left = self.parse_logical_and()?;
        
        while self.current_token() == &Token::Or {
            self.advance();
            let right = self.parse_logical_and()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op: BinOp::Or,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }
    
    fn parse_logical_and(&mut self) -> FlameResult<Expr> {
        let mut left = self.parse_equality()?;
        
        while self.current_token() == &Token::And {
            self.advance();
            let right = self.parse_equality()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op: BinOp::And,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }
    
    fn parse_equality(&mut self) -> FlameResult<Expr> {
        let mut left = self.parse_comparison()?;
        
        while matches!(self.current_token(), Token::Eq | Token::Ne) {
            let op = match self.current_token() {
                Token::Eq => BinOp::Eq,
                Token::Ne => BinOp::Ne,
                _ => unreachable!(),
            };
            self.advance();
            let right = self.parse_comparison()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }
    
    fn parse_comparison(&mut self) -> FlameResult<Expr> {
        let mut left = self.parse_additive()?;
        
        while matches!(self.current_token(), Token::Lt | Token::Le | Token::Gt | Token::Ge) {
            let op = match self.current_token() {
                Token::Lt => BinOp::Lt,
                Token::Le => BinOp::Le,
                Token::Gt => BinOp::Gt,
                Token::Ge => BinOp::Ge,
                _ => unreachable!(),
            };
            self.advance();
            let right = self.parse_additive()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }
    
    fn parse_additive(&mut self) -> FlameResult<Expr> {
        let mut left = self.parse_multiplicative()?;
        
        while matches!(self.current_token(), Token::Plus | Token::Minus) {
            let op = match self.current_token() {
                Token::Plus => BinOp::Add,
                Token::Minus => BinOp::Sub,
                _ => unreachable!(),
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
    
    fn parse_multiplicative(&mut self) -> FlameResult<Expr> {
        let mut left = self.parse_unary()?;
        
        while matches!(self.current_token(), Token::Star | Token::Slash | Token::Percent) {
            let op = match self.current_token() {
                Token::Star => BinOp::Mul,
                Token::Slash => BinOp::Div,
                Token::Percent => BinOp::Mod,
                _ => unreachable!(),
            };
            self.advance();
            let right = self.parse_unary()?;
            left = Expr::BinOp {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(left)
    }
    
    fn parse_unary(&mut self) -> FlameResult<Expr> {
        match self.current_token() {
            Token::Minus => {
                self.advance();
                let expr = self.parse_unary()?;
                Ok(Expr::UnaryOp {
                    op: UnaryOp::Neg,
                    expr: Box::new(expr),
                })
            }
            Token::Not => {
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
    
    fn parse_primary(&mut self) -> FlameResult<Expr> {
        match self.current_token().clone() {
            Token::Integer(n) => {
                self.advance();
                Ok(Expr::Literal(Literal::Integer(n)))
            }
            Token::Float(f) => {
                self.advance();
                Ok(Expr::Literal(Literal::Float(f)))
            }
            Token::String(s) => {
                self.advance();
                Ok(Expr::Literal(Literal::String(s)))
            }
            Token::True => {
                self.advance();
                Ok(Expr::Literal(Literal::Boolean(true)))
            }
            Token::False => {
                self.advance();
                Ok(Expr::Literal(Literal::Boolean(false)))
            }
            Token::HebrewGlyph => {
                let glyph = match self.tokens.get(self.current) {
                    Some(Token::HebrewGlyph) => {
                        // Extract the Hebrew text from the token
                        "hebrew_placeholder".to_string()
                    }
                    _ => "hebrew".to_string(),
                };
                self.advance();
                Ok(Expr::Literal(Literal::Hebrew(glyph)))
            }
            Token::Ident(name) => {
                self.advance();
                
                // Check for function call
                if self.current_token() == &Token::LParen {
                    self.advance();
                    let args = self.parse_args()?;
                    self.expect(Token::RParen)?;
                    Ok(Expr::FunctionCall { name, args })
                } else {
                    Ok(Expr::Variable(name))
                }
            }
            Token::LParen => {
                self.advance();
                let expr = self.parse_expression()?;
                self.expect(Token::RParen)?;
                Ok(expr)
            }
            Token::LBracket => {
                self.advance();
                let mut elements = Vec::new();
                
                while self.current_token() != &Token::RBracket && self.current_token() != &Token::Eof {
                    elements.push(self.parse_expression()?);
                    
                    if self.current_token() == &Token::Comma {
                        self.advance();
                    } else {
                        break;
                    }
                }
                
                self.expect(Token::RBracket)?;
                Ok(Expr::Array(elements))
            }
            // FlameLang-specific operations
            Token::Bend | Token::Codon | Token::Perm | Token::Gematria => {
                let op_name = format!("{:?}", self.current_token()).to_lowercase();
                self.advance();
                self.expect(Token::LParen)?;
                let args = self.parse_args()?;
                self.expect(Token::RParen)?;
                Ok(Expr::FunctionCall { name: op_name, args })
            }
            _ => Err(FlameError::ParserError {
                line: self.current,
                message: format!("Unexpected token: {:?}", self.current_token()),
            }),
        }
    }
    
    fn parse_args(&mut self) -> FlameResult<Vec<Expr>> {
        let mut args = Vec::new();
        
        if self.current_token() == &Token::RParen {
            return Ok(args);
        }
        
        loop {
            args.push(self.parse_expression()?);
            
            if self.current_token() != &Token::Comma {
                break;
            }
            self.advance();
        }
        
        Ok(args)
    }
}

pub fn parse(tokens: &[Token]) -> FlameResult<Program> {
    let mut parser = Parser::new(tokens.to_vec());
    parser.parse_program()
}
