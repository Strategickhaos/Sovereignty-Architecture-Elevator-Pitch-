//! # Parser Module
//!
//! Constructs Abstract Syntax Tree from tokens

use crate::lexer::{Keyword, Operator, Token};
use crate::{FlameError, FlameResult};

/// AST Node types
#[derive(Debug, Clone, PartialEq)]
pub enum AstNode {
    /// Program root
    Program(Vec<Statement>),
    /// Statement
    Statement(Statement),
    /// Expression
    Expression(Expression),
}

/// Statement types
#[derive(Debug, Clone, PartialEq)]
pub enum Statement {
    /// Let binding: let name: type = value;
    LetBinding {
        /// Variable name
        name: String,
        /// Type annotation
        type_name: String,
        /// Initial value
        value: Expression,
    },
    /// Bend operation
    Bend {
        /// Angle parameter
        angle: Expression,
        /// Radius parameter
        radius: Expression,
    },
}

/// Expression types
#[derive(Debug, Clone, PartialEq)]
pub enum Expression {
    /// Numeric literal
    Number(f64),
    /// String literal
    String(String),
    /// Identifier
    Identifier(String),
}

/// Parser state
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

    /// Parse tokens into AST
    pub fn parse(&mut self) -> FlameResult<AstNode> {
        let mut statements = Vec::new();

        while self.position < self.tokens.len() {
            if matches!(self.current_token(), Token::Eof) {
                break;
            }

            statements.push(self.parse_statement()?);
        }

        Ok(AstNode::Program(statements))
    }

    fn current_token(&self) -> &Token {
        self.tokens.get(self.position).unwrap_or(&Token::Eof)
    }

    fn advance(&mut self) {
        if self.position < self.tokens.len() {
            self.position += 1;
        }
    }

    fn parse_statement(&mut self) -> FlameResult<Statement> {
        match self.current_token() {
            Token::Keyword(Keyword::Let) => self.parse_let_binding(),
            Token::Keyword(Keyword::Bend) => self.parse_bend(),
            _ => Err(FlameError::Parser(format!(
                "Unexpected token: {:?}",
                self.current_token()
            ))),
        }
    }

    fn parse_let_binding(&mut self) -> FlameResult<Statement> {
        self.advance(); // Skip 'let'

        let name = match self.current_token() {
            Token::Identifier(n) => n.clone(),
            _ => return Err(FlameError::Parser("Expected identifier".to_string())),
        };
        self.advance();

        // Expect ':'
        if !matches!(self.current_token(), Token::Operator(Operator::Colon)) {
            return Err(FlameError::Parser("Expected ':'".to_string()));
        }
        self.advance();

        let type_name = match self.current_token() {
            Token::Identifier(t) => t.clone(),
            _ => return Err(FlameError::Parser("Expected type name".to_string())),
        };
        self.advance();

        // Expect '='
        if !matches!(self.current_token(), Token::Operator(Operator::Assign)) {
            return Err(FlameError::Parser("Expected '='".to_string()));
        }
        self.advance();

        let value = self.parse_expression()?;

        // Expect ';'
        if !matches!(self.current_token(), Token::Operator(Operator::Semicolon)) {
            return Err(FlameError::Parser("Expected ';'".to_string()));
        }
        self.advance();

        Ok(Statement::LetBinding {
            name,
            type_name,
            value,
        })
    }

    fn parse_bend(&mut self) -> FlameResult<Statement> {
        self.advance(); // Skip 'bend'

        let angle = self.parse_expression()?;

        if !matches!(self.current_token(), Token::Keyword(Keyword::Radius)) {
            return Err(FlameError::Parser("Expected 'radius'".to_string()));
        }
        self.advance();

        let radius = self.parse_expression()?;

        // Expect ';'
        if !matches!(self.current_token(), Token::Operator(Operator::Semicolon)) {
            return Err(FlameError::Parser("Expected ';'".to_string()));
        }
        self.advance();

        Ok(Statement::Bend { angle, radius })
    }

    fn parse_expression(&mut self) -> FlameResult<Expression> {
        match self.current_token() {
            Token::Number(n) => {
                let num = *n;
                self.advance();
                Ok(Expression::Number(num))
            }
            Token::String(s) => {
                let string = s.clone();
                self.advance();
                Ok(Expression::String(string))
            }
            Token::Identifier(id) => {
                let ident = id.clone();
                self.advance();
                Ok(Expression::Identifier(ident))
            }
            _ => Err(FlameError::Parser(format!(
                "Unexpected token in expression: {:?}",
                self.current_token()
            ))),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::Lexer;

    #[test]
    fn test_parse_let_binding() {
        let mut lexer = Lexer::new("let x: float = 5.0;");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        if let AstNode::Program(statements) = ast {
            assert_eq!(statements.len(), 1);
            assert!(matches!(statements[0], Statement::LetBinding { .. }));
        } else {
            panic!("Expected Program node");
        }
    }
}
