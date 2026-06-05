/// FlameLang lexer/scanner - tokenizes source code
/// Supports English, Hebrew, Unicode glyphs, and physics operators

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Keywords
    Intent,
    Bounce,
    Suppress,
    Observe,
    Unify,
    Fluctuate,
    
    // Hebrew operators (roots)
    HebrewRoot(String),  // דחה, כבש, ראה, נוע, אחד, פלא
    
    // Literals
    Number(f64),
    String(String),
    Identifier(String),
    
    // Glyphs/Unicode
    Glyph(char),  // 🛠️, etc.
    
    // Punctuation
    LeftParen,
    RightParen,
    LeftBrace,
    RightBrace,
    Comma,
    Semicolon,
    Arrow,  // ->
    
    // EOF
    Eof,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: TokenType,
    pub lexeme: String,
    pub line: usize,
    pub column: usize,
}

impl Token {
    pub fn new(token_type: TokenType, lexeme: String, line: usize, column: usize) -> Self {
        Token { token_type, lexeme, line, column }
    }
}

/// Scan source code and return tokens
pub fn scan(source: &str) -> Result<Vec<Token>, String> {
    let mut tokens = Vec::new();
    let mut chars = source.chars().peekable();
    let mut line = 1;
    let mut column = 1;
    
    while let Some(&ch) = chars.peek() {
        match ch {
            // Whitespace
            ' ' | '\r' | '\t' => {
                chars.next();
                column += 1;
            }
            '\n' => {
                chars.next();
                line += 1;
                column = 1;
            }
            
            // Comments
            '/' if chars.clone().nth(1) == Some('/') => {
                while chars.peek().is_some() && chars.peek() != Some(&'\n') {
                    chars.next();
                }
            }
            
            // Single-char tokens
            '(' => {
                tokens.push(Token::new(TokenType::LeftParen, ch.to_string(), line, column));
                chars.next();
                column += 1;
            }
            ')' => {
                tokens.push(Token::new(TokenType::RightParen, ch.to_string(), line, column));
                chars.next();
                column += 1;
            }
            '{' => {
                tokens.push(Token::new(TokenType::LeftBrace, ch.to_string(), line, column));
                chars.next();
                column += 1;
            }
            '}' => {
                tokens.push(Token::new(TokenType::RightBrace, ch.to_string(), line, column));
                chars.next();
                column += 1;
            }
            ',' => {
                tokens.push(Token::new(TokenType::Comma, ch.to_string(), line, column));
                chars.next();
                column += 1;
            }
            ';' => {
                tokens.push(Token::new(TokenType::Semicolon, ch.to_string(), line, column));
                chars.next();
                column += 1;
            }
            
            // Arrow
            '-' if chars.clone().nth(1) == Some('>') => {
                tokens.push(Token::new(TokenType::Arrow, "->".to_string(), line, column));
                chars.next();
                chars.next();
                column += 2;
            }
            
            // Numbers
            '0'..='9' => {
                let start_col = column;
                let mut num_str = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_ascii_digit() || ch == '.' {
                        num_str.push(ch);
                        chars.next();
                        column += 1;
                    } else {
                        break;
                    }
                }
                let value = num_str.parse::<f64>()
                    .map_err(|_| format!("Invalid number: {}", num_str))?;
                tokens.push(Token::new(TokenType::Number(value), num_str, line, start_col));
            }
            
            // Strings
            '"' => {
                let start_col = column;
                chars.next();
                column += 1;
                let mut string_val = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch == '"' {
                        break;
                    }
                    if ch == '\n' {
                        return Err(format!("Unterminated string at line {}", line));
                    }
                    string_val.push(ch);
                    chars.next();
                    column += 1;
                }
                if chars.peek().is_none() {
                    return Err(format!("Unterminated string at line {}", line));
                }
                chars.next(); // closing "
                column += 1;
                tokens.push(Token::new(
                    TokenType::String(string_val.clone()), 
                    format!("\"{}\"", string_val), 
                    line, 
                    start_col
                ));
            }
            
            // Hebrew characters or identifiers
            _ if ch.is_alphabetic() || is_hebrew(ch) => {
                let start_col = column;
                let mut lexeme = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_alphanumeric() || ch == '_' || is_hebrew(ch) {
                        lexeme.push(ch);
                        chars.next();
                        column += 1;
                    } else {
                        break;
                    }
                }
                
                // Check for keywords
                let token_type = match lexeme.as_str() {
                    "intent" => TokenType::Intent,
                    "bounce" => TokenType::Bounce,
                    "suppress" => TokenType::Suppress,
                    "observe" => TokenType::Observe,
                    "unify" => TokenType::Unify,
                    "fluctuate" => TokenType::Fluctuate,
                    // Hebrew roots
                    "דחה" | "כבש" | "ראה" | "נוע" | "אחד" | "פלא" => 
                        TokenType::HebrewRoot(lexeme.clone()),
                    _ => TokenType::Identifier(lexeme.clone()),
                };
                
                tokens.push(Token::new(token_type, lexeme, line, start_col));
            }
            
            // Unicode glyphs
            _ if is_glyph(ch) => {
                tokens.push(Token::new(TokenType::Glyph(ch), ch.to_string(), line, column));
                chars.next();
                column += 1;
            }
            
            _ => {
                return Err(format!("Unexpected character '{}' at line {}, column {}", ch, line, column));
            }
        }
    }
    
    tokens.push(Token::new(TokenType::Eof, String::new(), line, column));
    Ok(tokens)
}

fn is_hebrew(ch: char) -> bool {
    ('\u{0590}'..='\u{05FF}').contains(&ch)
}

fn is_glyph(ch: char) -> bool {
    // Emoji and symbol ranges
    ('\u{1F300}'..='\u{1F9FF}').contains(&ch) || 
    ('\u{2600}'..='\u{26FF}').contains(&ch)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_scan() {
        let source = "intent bounce suppress";
        let tokens = scan(source).unwrap();
        assert_eq!(tokens.len(), 4); // 3 tokens + EOF
        assert_eq!(tokens[0].token_type, TokenType::Intent);
        assert_eq!(tokens[1].token_type, TokenType::Bounce);
        assert_eq!(tokens[2].token_type, TokenType::Suppress);
    }

    #[test]
    fn test_hebrew_scan() {
        let source = "דחה";
        let tokens = scan(source).unwrap();
        assert_eq!(tokens.len(), 2); // 1 token + EOF
        match &tokens[0].token_type {
            TokenType::HebrewRoot(s) => assert_eq!(s, "דחה"),
            _ => panic!("Expected HebrewRoot"),
        }
    }

    #[test]
    fn test_numbers() {
        let source = "42 3.14";
        let tokens = scan(source).unwrap();
        assert_eq!(tokens.len(), 3); // 2 tokens + EOF
        match tokens[0].token_type {
            TokenType::Number(n) => assert_eq!(n, 42.0),
            _ => panic!("Expected Number"),
        }
    }
}
