/// Span tracks position in source
#[derive(Debug, Clone, PartialEq)]
pub struct Span {
    pub line: usize,
    pub col: usize,
}

impl Span {
    pub fn new(line: usize, col: usize) -> Self {
        Span { line, col }
    }
}

impl Default for Span {
    fn default() -> Self {
        Span { line: 1, col: 1 }
    }
}

/// Spanned wraps a token with position info
#[derive(Debug, Clone, PartialEq)]
pub struct Spanned<T> {
    pub token: T,
    pub span: Span,
}

impl<T> Spanned<T> {
    pub fn new(token: T, span: Span) -> Self {
        Spanned { token, span }
    }
}

/// All token variants for the SAGCO formula language
#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    // Literals
    Number(f64),
    Str(String),
    Bool(bool),

    // References
    Ident(String),
    CellRef(String),
    RangeRef(String, String),

    // Delimiters
    LParen,
    RParen,
    Comma,
    Colon,
    Semicolon,

    // Arithmetic
    Plus,
    Minus,
    Star,
    Slash,
    Caret,

    // Comparison
    Eq,
    NEq,
    Lt,
    Gt,
    LtEq,
    GtEq,

    // Logical
    Bang,

    // Special
    Ampersand, // string concat &

    EOF,
}
