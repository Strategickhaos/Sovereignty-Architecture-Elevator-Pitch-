use crate::token::Span;

#[derive(Debug, Clone, PartialEq)]
pub enum DiagLevel {
    Error,
    Warning,
    Info,
}

impl std::fmt::Display for DiagLevel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            DiagLevel::Error => write!(f, "ERROR"),
            DiagLevel::Warning => write!(f, "WARNING"),
            DiagLevel::Info => write!(f, "INFO"),
        }
    }
}

#[derive(Debug, Clone)]
pub struct Diagnostic {
    pub level: DiagLevel,
    pub span: Span,
    pub message: String,
}

impl Diagnostic {
    pub fn error(message: impl Into<String>) -> Self {
        Diagnostic {
            level: DiagLevel::Error,
            span: Span::default(),
            message: message.into(),
        }
    }

    pub fn warning(message: impl Into<String>) -> Self {
        Diagnostic {
            level: DiagLevel::Warning,
            span: Span::default(),
            message: message.into(),
        }
    }

    pub fn info(message: impl Into<String>) -> Self {
        Diagnostic {
            level: DiagLevel::Info,
            span: Span::default(),
            message: message.into(),
        }
    }

    pub fn with_span(mut self, span: Span) -> Self {
        self.span = span;
        self
    }
}

impl std::fmt::Display for Diagnostic {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{}] {}:{} — {}", self.level, self.span.line, self.span.col, self.message)
    }
}

pub struct DiagnosticEngine {
    diagnostics: Vec<Diagnostic>,
}

impl DiagnosticEngine {
    pub fn new() -> Self {
        DiagnosticEngine {
            diagnostics: Vec::new(),
        }
    }

    pub fn collect(&mut self, diag: Diagnostic) {
        self.diagnostics.push(diag);
    }

    pub fn report(&self) -> &[Diagnostic] {
        &self.diagnostics
    }

    pub fn has_errors(&self) -> bool {
        self.diagnostics.iter().any(|d| d.level == DiagLevel::Error)
    }

    pub fn error_count(&self) -> usize {
        self.diagnostics.iter().filter(|d| d.level == DiagLevel::Error).count()
    }

    pub fn warning_count(&self) -> usize {
        self.diagnostics.iter().filter(|d| d.level == DiagLevel::Warning).count()
    }

    pub fn print_all(&self) {
        for d in &self.diagnostics {
            println!("{}", d);
        }
    }
}

impl Default for DiagnosticEngine {
    fn default() -> Self {
        Self::new()
    }
}
