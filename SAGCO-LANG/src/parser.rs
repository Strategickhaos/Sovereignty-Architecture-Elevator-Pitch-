use crate::lexer::Token;
use crate::ast::{Brick, PadRef, Program, Route};

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, pos: 0 }
    }

    fn peek(&self) -> &Token {
        &self.tokens[self.pos]
    }

    fn consume(&mut self) -> Token {
        let t = self.tokens[self.pos].clone();
        self.pos += 1;
        t
    }

    fn expect(&mut self, expected: &Token) -> Result<(), String> {
        let t = self.consume();
        if std::mem::discriminant(&t) == std::mem::discriminant(expected) {
            Ok(())
        } else {
            Err(format!("expected {:?} got {:?}", expected, t))
        }
    }

    fn skip_newlines(&mut self) {
        while self.peek() == &Token::Newline {
            self.consume();
        }
    }

    fn parse_pad_ref(&mut self) -> Result<PadRef, String> {
        self.expect(&Token::Pad)?;
        self.expect(&Token::LParen)?;
        let mut path = Vec::new();
        loop {
            match self.peek() {
                Token::Ident(_) => {
                    if let Token::Ident(s) = self.consume() {
                        path.push(s);
                    }
                }
                Token::Dot => { self.consume(); }
                _ => break,
            }
        }
        self.expect(&Token::RParen)?;
        Ok(PadRef { path })
    }

    fn parse_brick(&mut self) -> Result<Brick, String> {
        self.expect(&Token::Brick)?;
        let name = match self.consume() {
            Token::Ident(s) => s,
            t => return Err(format!("expected brick name, got {:?}", t)),
        };
        self.expect(&Token::Route)?;
        let from = self.parse_pad_ref()?;
        self.expect(&Token::Arrow)?;
        let to = self.parse_pad_ref()?;
        Ok(Brick { name, route: Route { from, to } })
    }

    pub fn parse(&mut self) -> Result<Program, String> {
        let mut bricks = Vec::new();
        self.skip_newlines();
        while self.peek() != &Token::Eof {
            bricks.push(self.parse_brick()?);
            self.skip_newlines();
        }
        Ok(Program { bricks })
    }
}
