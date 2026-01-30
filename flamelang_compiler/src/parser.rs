// Parser for FlameLang - converts tokens to FlameIR

use crate::lexer::{Token, Lexer};
use crate::ir::{FlameIR, FlameProgram};

pub struct Parser {
    tokens: Vec<Token>,
    position: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            position: 0,
        }
    }
    
    pub fn from_source(source: String) -> Self {
        let mut lexer = Lexer::new(source);
        let tokens = lexer.tokenize();
        Self::new(tokens)
    }
    
    fn current(&self) -> &Token {
        self.tokens.get(self.position).unwrap_or(&Token::Eof)
    }
    
    fn advance(&mut self) {
        if self.position < self.tokens.len() {
            self.position += 1;
        }
    }
    
    fn expect(&mut self, expected: Token) -> Result<(), String> {
        if self.current() == &expected {
            self.advance();
            Ok(())
        } else {
            Err(format!("Expected {:?}, got {:?}", expected, self.current()))
        }
    }
    
    pub fn parse(&mut self) -> Result<FlameProgram, String> {
        let mut program = FlameProgram::new();
        
        while self.current() != &Token::Eof {
            match self.parse_statement()? {
                Some(irs) => program.extend(irs),
                None => {}
            }
        }
        
        program.push(FlameIR::Halt);
        Ok(program)
    }
    
    fn parse_statement(&mut self) -> Result<Option<Vec<FlameIR>>, String> {
        match self.current() {
            Token::Print => self.parse_print(),
            Token::Let => self.parse_let(),
            Token::Fn => self.parse_function(),
            Token::Assert => self.parse_assert(),
            Token::Identifier(_) => self.parse_assignment_or_call(),
            _ => {
                self.advance();
                Ok(None)
            }
        }
    }
    
    fn parse_print(&mut self) -> Result<Option<Vec<FlameIR>>, String> {
        self.advance(); // consume 'print'
        self.expect(Token::LeftParen)?;
        
        let mut irs = Vec::new();
        
        // Parse the expression to print
        irs.extend(self.parse_expression()?);
        
        self.expect(Token::RightParen)?;
        self.expect(Token::Semicolon)?;
        
        irs.push(FlameIR::Print);
        
        Ok(Some(irs))
    }
    
    fn parse_let(&mut self) -> Result<Option<Vec<FlameIR>>, String> {
        self.advance(); // consume 'let'
        
        let name = match self.current() {
            Token::Identifier(n) => n.clone(),
            _ => return Err("Expected identifier after 'let'".to_string()),
        };
        self.advance();
        
        self.expect(Token::Equal)?;
        
        let mut irs = self.parse_expression()?;
        self.expect(Token::Semicolon)?;
        
        irs.push(FlameIR::Store(name));
        
        Ok(Some(irs))
    }
    
    fn parse_assignment_or_call(&mut self) -> Result<Option<Vec<FlameIR>>, String> {
        let name = match self.current() {
            Token::Identifier(n) => n.clone(),
            _ => return Err("Expected identifier".to_string()),
        };
        self.advance();
        
        match self.current() {
            Token::Equal => {
                self.advance();
                let mut irs = self.parse_expression()?;
                self.expect(Token::Semicolon)?;
                irs.push(FlameIR::Store(name));
                Ok(Some(irs))
            }
            Token::LeftParen => {
                self.advance();
                let mut irs = Vec::new();
                let mut arg_count = 0;
                
                // Parse arguments
                if self.current() != &Token::RightParen {
                    loop {
                        irs.extend(self.parse_expression()?);
                        arg_count += 1;
                        
                        if self.current() == &Token::Comma {
                            self.advance();
                        } else {
                            break;
                        }
                    }
                }
                
                self.expect(Token::RightParen)?;
                self.expect(Token::Semicolon)?;
                
                irs.push(FlameIR::Call(name, arg_count));
                Ok(Some(irs))
            }
            _ => Err(format!("Unexpected token after identifier: {:?}", self.current()))
        }
    }
    
    fn parse_function(&mut self) -> Result<Option<Vec<FlameIR>>, String> {
        self.advance(); // consume 'fn'
        
        let name = match self.current() {
            Token::Identifier(n) => n.clone(),
            _ => return Err("Expected function name".to_string()),
        };
        self.advance();
        
        self.expect(Token::LeftParen)?;
        
        let mut params = Vec::new();
        if self.current() != &Token::RightParen {
            loop {
                match self.current() {
                    Token::Identifier(p) => {
                        params.push(p.clone());
                        self.advance();
                    }
                    _ => return Err("Expected parameter name".to_string()),
                }
                
                if self.current() == &Token::Comma {
                    self.advance();
                } else {
                    break;
                }
            }
        }
        
        self.expect(Token::RightParen)?;
        self.expect(Token::LeftBrace)?;
        
        let mut body = Vec::new();
        while self.current() != &Token::RightBrace && self.current() != &Token::Eof {
            if let Some(irs) = self.parse_statement()? {
                body.extend(irs);
            }
        }
        
        self.expect(Token::RightBrace)?;
        
        Ok(Some(vec![FlameIR::FnDef(name, params, body)]))
    }
    
    fn parse_assert(&mut self) -> Result<Option<Vec<FlameIR>>, String> {
        self.advance(); // consume 'assert'
        self.expect(Token::LeftParen)?;
        
        let mut irs = self.parse_expression()?;
        
        self.expect(Token::RightParen)?;
        self.expect(Token::Semicolon)?;
        
        irs.push(FlameIR::Assert);
        
        Ok(Some(irs))
    }
    
    fn parse_expression(&mut self) -> Result<Vec<FlameIR>, String> {
        self.parse_additive()
    }
    
    fn parse_additive(&mut self) -> Result<Vec<FlameIR>, String> {
        let mut irs = self.parse_multiplicative()?;
        
        while matches!(self.current(), Token::Plus | Token::Minus) {
            let op = self.current().clone();
            self.advance();
            
            irs.extend(self.parse_multiplicative()?);
            
            match op {
                Token::Plus => irs.push(FlameIR::Add),
                Token::Minus => irs.push(FlameIR::Sub),
                _ => unreachable!()
            }
        }
        
        Ok(irs)
    }
    
    fn parse_multiplicative(&mut self) -> Result<Vec<FlameIR>, String> {
        let mut irs = self.parse_primary()?;
        
        while matches!(self.current(), Token::Star | Token::Slash) {
            let op = self.current().clone();
            self.advance();
            
            irs.extend(self.parse_primary()?);
            
            match op {
                Token::Star => irs.push(FlameIR::Mul),
                Token::Slash => irs.push(FlameIR::Div),
                _ => unreachable!()
            }
        }
        
        Ok(irs)
    }
    
    fn parse_primary(&mut self) -> Result<Vec<FlameIR>, String> {
        match self.current().clone() {
            Token::Number(n) => {
                self.advance();
                Ok(vec![FlameIR::LoadConst(n)])
            }
            Token::Float(f) => {
                self.advance();
                // For now, convert float to int, or handle specially
                Ok(vec![FlameIR::LoadConst(f as i64)])
            }
            Token::String(s) => {
                self.advance();
                Ok(vec![FlameIR::LoadString(s)])
            }
            Token::Identifier(name) => {
                self.advance();
                Ok(vec![FlameIR::Load(name)])
            }
            Token::LeftParen => {
                self.advance();
                let irs = self.parse_expression()?;
                self.expect(Token::RightParen)?;
                Ok(irs)
            }
            Token::Sin => {
                self.advance();
                self.expect(Token::LeftParen)?;
                let angle = match self.current() {
                    Token::Number(n) => *n as f64,
                    Token::Float(f) => *f,
                    _ => return Err("Expected number for sin()".to_string()),
                };
                self.advance();
                self.expect(Token::RightParen)?;
                Ok(vec![FlameIR::Trig6Sin(angle)])
            }
            Token::Cos => {
                self.advance();
                self.expect(Token::LeftParen)?;
                let angle = match self.current() {
                    Token::Number(n) => *n as f64,
                    Token::Float(f) => *f,
                    _ => return Err("Expected number for cos()".to_string()),
                };
                self.advance();
                self.expect(Token::RightParen)?;
                Ok(vec![FlameIR::Trig6Cos(angle)])
            }
            Token::Tan => {
                self.advance();
                self.expect(Token::LeftParen)?;
                let angle = match self.current() {
                    Token::Number(n) => *n as f64,
                    Token::Float(f) => *f,
                    _ => return Err("Expected number for tan()".to_string()),
                };
                self.advance();
                self.expect(Token::RightParen)?;
                Ok(vec![FlameIR::Trig6Tan(angle)])
            }
            _ => Err(format!("Unexpected token in expression: {:?}", self.current()))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_print() {
        let source = r#"print("Hello, World!");"#.to_string();
        let mut parser = Parser::from_source(source);
        let program = parser.parse().unwrap();
        
        assert!(program.instructions.iter().any(|ir| matches!(ir, FlameIR::Print)));
    }
    
    #[test]
    fn test_parse_let() {
        let source = "let x = 42;".to_string();
        let mut parser = Parser::from_source(source);
        let program = parser.parse().unwrap();
        
        assert!(program.instructions.iter().any(|ir| matches!(ir, FlameIR::Store(_))));
    }
    
    #[test]
    fn test_parse_arithmetic() {
        let source = "let x = 10 + 5 * 2;".to_string();
        let mut parser = Parser::from_source(source);
        let program = parser.parse().unwrap();
        
        // Should have Add and Mul operations
        assert!(program.instructions.iter().any(|ir| matches!(ir, FlameIR::Add)));
        assert!(program.instructions.iter().any(|ir| matches!(ir, FlameIR::Mul)));
    }
}
