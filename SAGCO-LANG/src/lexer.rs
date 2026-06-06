#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    Brick,
    Route,
    Pad,
    Arrow,
    Dot,
    Ident(String),
    LParen,
    RParen,
    Newline,
    Eof,
}

pub fn lex(input: &str) -> Vec<Token> {
    let mut out = Vec::new();
    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let spaced = line
            .replace("->", " -> ")
            .replace('(', " ( ")
            .replace(')', " ) ")
            .replace('.', " . ");
        for part in spaced.split_whitespace() {
            let tok = match part {
                "brick" => Token::Brick,
                "route" => Token::Route,
                "pad"   => Token::Pad,
                "->"    => Token::Arrow,
                "("     => Token::LParen,
                ")"     => Token::RParen,
                "."     => Token::Dot,
                x       => Token::Ident(x.to_string()),
            };
            out.push(tok);
        }
        out.push(Token::Newline);
    }
    out.push(Token::Eof);
    out
}
