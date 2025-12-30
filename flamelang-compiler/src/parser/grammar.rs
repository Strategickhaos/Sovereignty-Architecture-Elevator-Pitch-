/// FlameLang parser - builds AST from tokens
use crate::lexer::scanner::{Token, TokenType};

#[derive(Debug, Clone)]
pub enum AstNode {
    Intent {
        operation: String,
        params: Vec<AstNode>,
    },
    HebrewOp {
        root: String,
        args: Vec<AstNode>,
    },
    Literal(LiteralValue),
    Identifier(String),
    Block(Vec<AstNode>),
}

#[derive(Debug, Clone)]
pub enum LiteralValue {
    Number(f64),
    String(String),
}

pub struct Parser {
    tokens: Vec<Token>,
    current: usize,
}

impl Parser {
    fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, current: 0 }
    }
    
    fn is_at_end(&self) -> bool {
        matches!(self.peek().token_type, TokenType::Eof)
    }
    
    fn peek(&self) -> &Token {
        &self.tokens[self.current]
    }
    
    fn advance(&mut self) -> &Token {
        if !self.is_at_end() {
            self.current += 1;
        }
        &self.tokens[self.current - 1]
    }
    
    fn check(&self, token_type: &TokenType) -> bool {
        if self.is_at_end() {
            return false;
        }
        std::mem::discriminant(&self.peek().token_type) == std::mem::discriminant(token_type)
    }
    
    fn consume(&mut self, expected: TokenType, message: &str) -> Result<&Token, String> {
        if self.check(&expected) {
            Ok(self.advance())
        } else {
            Err(format!("{} at line {}", message, self.peek().line))
        }
    }
    
    fn parse_program(&mut self) -> Result<Vec<AstNode>, String> {
        let mut statements = Vec::new();
        
        while !self.is_at_end() {
            statements.push(self.parse_statement()?);
        }
        
        Ok(statements)
    }
    
    fn parse_statement(&mut self) -> Result<AstNode, String> {
        match &self.peek().token_type {
            TokenType::Intent => self.parse_intent(),
            TokenType::HebrewRoot(_) => self.parse_hebrew_op(),
            TokenType::LeftBrace => self.parse_block(),
            _ => self.parse_expression(),
        }
    }
    
    fn parse_intent(&mut self) -> Result<AstNode, String> {
        self.advance(); // consume 'intent'
        
        let operation = match &self.peek().token_type {
            TokenType::Identifier(id) => {
                let op = id.clone();
                self.advance();
                op
            }
            TokenType::Bounce => {
                self.advance();
                "bounce".to_string()
            }
            TokenType::Suppress => {
                self.advance();
                "suppress".to_string()
            }
            TokenType::Observe => {
                self.advance();
                "observe".to_string()
            }
            TokenType::Unify => {
                self.advance();
                "unify".to_string()
            }
            TokenType::Fluctuate => {
                self.advance();
                "fluctuate".to_string()
            }
            _ => return Err(format!("Expected operation after 'intent' at line {}", self.peek().line)),
        };
        
        let mut params = Vec::new();
        
        if self.check(&TokenType::LeftParen) {
            self.advance();
            
            if !self.check(&TokenType::RightParen) {
                loop {
                    params.push(self.parse_expression()?);
                    
                    if !self.check(&TokenType::Comma) {
                        break;
                    }
                    self.advance();
                }
            }
            
            self.consume(TokenType::RightParen, "Expected ')' after parameters")?;
        }
        
        Ok(AstNode::Intent { operation, params })
    }
    
    fn parse_hebrew_op(&mut self) -> Result<AstNode, String> {
        let root = match &self.advance().token_type {
            TokenType::HebrewRoot(r) => r.clone(),
            _ => unreachable!(),
        };
        
        let mut args = Vec::new();
        
        if self.check(&TokenType::LeftParen) {
            self.advance();
            
            if !self.check(&TokenType::RightParen) {
                loop {
                    args.push(self.parse_expression()?);
                    
                    if !self.check(&TokenType::Comma) {
                        break;
                    }
                    self.advance();
                }
            }
            
            self.consume(TokenType::RightParen, "Expected ')' after arguments")?;
        }
        
        Ok(AstNode::HebrewOp { root, args })
    }
    
    fn parse_block(&mut self) -> Result<AstNode, String> {
        self.consume(TokenType::LeftBrace, "Expected '{'")?;
        
        let mut statements = Vec::new();
        
        while !self.check(&TokenType::RightBrace) && !self.is_at_end() {
            statements.push(self.parse_statement()?);
        }
        
        self.consume(TokenType::RightBrace, "Expected '}'")?;
        
        Ok(AstNode::Block(statements))
    }
    
    fn parse_expression(&mut self) -> Result<AstNode, String> {
        match &self.peek().token_type {
            TokenType::Number(n) => {
                let val = *n;
                self.advance();
                Ok(AstNode::Literal(LiteralValue::Number(val)))
            }
            TokenType::String(s) => {
                let val = s.clone();
                self.advance();
                Ok(AstNode::Literal(LiteralValue::String(val)))
            }
            TokenType::Identifier(id) => {
                let name = id.clone();
                self.advance();
                Ok(AstNode::Identifier(name))
            }
            TokenType::Glyph(g) => {
                let glyph_str = g.to_string();
                self.advance();
                Ok(AstNode::Identifier(glyph_str))
            }
            _ => Err(format!("Unexpected token at line {}", self.peek().line)),
        }
    }
}

/// Parse tokens into AST
pub fn parse(tokens: &[Token]) -> Result<Vec<AstNode>, String> {
    let mut parser = Parser::new(tokens.to_vec());
    parser.parse_program()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::scanner::scan;

    #[test]
    fn test_parse_intent() {
        let source = "intent bounce";
        let tokens = scan(source).unwrap();
        let ast = parse(&tokens).unwrap();
        assert_eq!(ast.len(), 1);
        match &ast[0] {
            AstNode::Intent { operation, .. } => assert_eq!(operation, "bounce"),
            _ => panic!("Expected Intent node"),
        }
    }

    #[test]
    fn test_parse_hebrew() {
        let source = "דחה";
        let tokens = scan(source).unwrap();
        let ast = parse(&tokens).unwrap();
        assert_eq!(ast.len(), 1);
        match &ast[0] {
            AstNode::HebrewOp { root, .. } => assert_eq!(root, "דחה"),
            _ => panic!("Expected HebrewOp node"),
        }
    }
}
