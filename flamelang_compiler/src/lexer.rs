// Lexer for FlameLang source code

#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    // Keywords
    Fn,
    Let,
    Print,
    If,
    Else,
    While,
    Return,
    Assert,
    
    // TRIG6 keywords
    Sin,
    Cos,
    Tan,
    
    // Literals
    Number(i64),
    Float(f64),
    String(String),
    Identifier(String),
    
    // Operators
    Plus,
    Minus,
    Star,
    Slash,
    Equal,
    EqualEqual,
    Bang,
    BangEqual,
    Less,
    Greater,
    LessEqual,
    GreaterEqual,
    
    // Delimiters
    LeftParen,
    RightParen,
    LeftBrace,
    RightBrace,
    Comma,
    Semicolon,
    Arrow,  // ->
    
    // Special
    Eof,
}

pub struct Lexer {
    input: Vec<char>,
    position: usize,
    current_char: Option<char>,
}

impl Lexer {
    pub fn new(input: String) -> Self {
        let chars: Vec<char> = input.chars().collect();
        let current = chars.get(0).copied();
        Self {
            input: chars,
            position: 0,
            current_char: current,
        }
    }
    
    fn advance(&mut self) {
        self.position += 1;
        self.current_char = self.input.get(self.position).copied();
    }
    
    fn peek(&self, offset: usize) -> Option<char> {
        self.input.get(self.position + offset).copied()
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
        // Skip // comments
        if self.current_char == Some('/') && self.peek(1) == Some('/') {
            while self.current_char.is_some() && self.current_char != Some('\n') {
                self.advance();
            }
        }
    }
    
    fn read_number(&mut self) -> Token {
        let mut num_str = String::new();
        let mut is_float = false;
        
        while let Some(ch) = self.current_char {
            if ch.is_ascii_digit() {
                num_str.push(ch);
                self.advance();
            } else if ch == '.' && !is_float {
                is_float = true;
                num_str.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        if is_float {
            Token::Float(num_str.parse().unwrap_or(0.0))
        } else {
            Token::Number(num_str.parse().unwrap_or(0))
        }
    }
    
    fn read_string(&mut self) -> Token {
        self.advance(); // Skip opening quote
        let mut string = String::new();
        
        while let Some(ch) = self.current_char {
            if ch == '"' {
                self.advance(); // Skip closing quote
                break;
            }
            string.push(ch);
            self.advance();
        }
        
        Token::String(string)
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
        
        // Check for keywords
        match ident.as_str() {
            "fn" => Token::Fn,
            "let" => Token::Let,
            "print" => Token::Print,
            "if" => Token::If,
            "else" => Token::Else,
            "while" => Token::While,
            "return" => Token::Return,
            "assert" => Token::Assert,
            "sin" => Token::Sin,
            "cos" => Token::Cos,
            "tan" => Token::Tan,
            _ => Token::Identifier(ident),
        }
    }
    
    pub fn next_token(&mut self) -> Token {
        self.skip_whitespace();
        self.skip_comment();
        self.skip_whitespace();
        
        match self.current_char {
            None => Token::Eof,
            Some(ch) => match ch {
                '+' => {
                    self.advance();
                    Token::Plus
                }
                '-' => {
                    self.advance();
                    if self.current_char == Some('>') {
                        self.advance();
                        Token::Arrow
                    } else {
                        Token::Minus
                    }
                }
                '*' => {
                    self.advance();
                    Token::Star
                }
                '/' => {
                    self.advance();
                    Token::Slash
                }
                '=' => {
                    self.advance();
                    if self.current_char == Some('=') {
                        self.advance();
                        Token::EqualEqual
                    } else {
                        Token::Equal
                    }
                }
                '!' => {
                    self.advance();
                    if self.current_char == Some('=') {
                        self.advance();
                        Token::BangEqual
                    } else {
                        Token::Bang
                    }
                }
                '<' => {
                    self.advance();
                    if self.current_char == Some('=') {
                        self.advance();
                        Token::LessEqual
                    } else {
                        Token::Less
                    }
                }
                '>' => {
                    self.advance();
                    if self.current_char == Some('=') {
                        self.advance();
                        Token::GreaterEqual
                    } else {
                        Token::Greater
                    }
                }
                '(' => {
                    self.advance();
                    Token::LeftParen
                }
                ')' => {
                    self.advance();
                    Token::RightParen
                }
                '{' => {
                    self.advance();
                    Token::LeftBrace
                }
                '}' => {
                    self.advance();
                    Token::RightBrace
                }
                ',' => {
                    self.advance();
                    Token::Comma
                }
                ';' => {
                    self.advance();
                    Token::Semicolon
                }
                '"' => self.read_string(),
                _ if ch.is_ascii_digit() => self.read_number(),
                _ if ch.is_alphabetic() || ch == '_' => self.read_identifier(),
                _ => {
                    self.advance();
                    self.next_token() // Skip unknown characters
                }
            }
        }
    }
    
    pub fn tokenize(&mut self) -> Vec<Token> {
        let mut tokens = Vec::new();
        loop {
            let token = self.next_token();
            if token == Token::Eof {
                tokens.push(token);
                break;
            }
            tokens.push(token);
        }
        tokens
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_lexer_simple() {
        let mut lexer = Lexer::new("let x = 42;".to_string());
        let tokens = lexer.tokenize();
        
        assert!(matches!(tokens[0], Token::Let));
        assert!(matches!(tokens[1], Token::Identifier(_)));
        assert!(matches!(tokens[2], Token::Equal));
        assert!(matches!(tokens[3], Token::Number(42)));
    }
    
    #[test]
    fn test_lexer_string() {
        let mut lexer = Lexer::new(r#"print("Hello, World!");"#.to_string());
        let tokens = lexer.tokenize();
        
        assert!(matches!(tokens[0], Token::Print));
        assert!(matches!(tokens[2], Token::String(_)));
    }
}
