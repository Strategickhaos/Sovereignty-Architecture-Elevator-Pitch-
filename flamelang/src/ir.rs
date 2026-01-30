// ═══════════════════════════════════════════════════════════════════════════════
// FLAMELANG INTERMEDIATE REPRESENTATION v0.1.0
// ═══════════════════════════════════════════════════════════════════════════════
//
// STATUS: FROZEN
// DATE: 2026-01-30
// AUTHOR: Dom (Me10101) / Strategickhaos DAO LLC
//
// This IR is LOCKED. No modifications without version bump.
// All passes must consume and produce this exact structure.
//
// VERSIONING:
//   Major (0.x.x → 1.x.x): Breaking changes to node kinds or semantics
//   Minor (0.1.x → 0.2.x): New optional fields, new ops with default behavior
//   Patch (0.1.0 → 0.1.1): Bugfix only, no schema change
//
// ═══════════════════════════════════════════════════════════════════════════════

pub const IR_VERSION: &str = "0.1.0";
pub const IR_VERSION_MAJOR: u32 = 0;
pub const IR_VERSION_MINOR: u32 = 1;
pub const IR_VERSION_PATCH: u32 = 0;

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION A: IR DATA MODEL (Frozen Node Kinds)
// ═══════════════════════════════════════════════════════════════════════════════

/// The complete set of IR node kinds for FlameIR v0.1.0
/// This enum is FROZEN. Adding variants requires version bump.
#[derive(Debug, Clone, PartialEq)]
pub enum FlameIR {
    /// Top-level module containing function definitions
    Module(Module),
    
    /// Function definition
    FnDef(FnDef),
    
    /// Sequence of statements
    Block(Block),
    
    /// Variable binding: let name = expr
    Let(Let),
    
    /// Constant value (number, string, bool)
    Const(Const),
    
    /// Function call: name(args...)
    Call(Call),
    
    /// Return from function
    Return(Return),
    
    /// External function declaration (for host calls like print)
    Extern(Extern),
    
    /// Variable reference
    Var(Var),
    
    /// Binary operation: left op right
    BinOp(BinOp),
}

// ─────────────────────────────────────────────────────────────────────────────
// Node Definitions
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, PartialEq)]
pub struct Module {
    pub name: String,
    pub items: Vec<FlameIR>,  // FnDef or Extern only
    pub version: String,       // Must match IR_VERSION
}

#[derive(Debug, Clone, PartialEq)]
pub struct FnDef {
    pub name: String,
    pub params: Vec<Param>,
    pub return_type: FlameType,
    pub body: Box<FlameIR>,    // Must be Block
}

#[derive(Debug, Clone, PartialEq)]
pub struct Param {
    pub name: String,
    pub param_type: FlameType,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Block {
    pub statements: Vec<FlameIR>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Let {
    pub name: String,
    pub value: Box<FlameIR>,
    pub let_type: Option<FlameType>,  // Optional type annotation
}

#[derive(Debug, Clone, PartialEq)]
pub enum Const {
    Int(i64),
    Float(f64),
    Bool(bool),
    String(String),
    Unit,  // () / void
}

#[derive(Debug, Clone, PartialEq)]
pub struct Call {
    pub target: String,          // Function name (must resolve to FnDef or Extern)
    pub args: Vec<FlameIR>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Return {
    pub value: Option<Box<FlameIR>>,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Extern {
    pub name: String,
    pub params: Vec<FlameType>,
    pub return_type: FlameType,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Var {
    pub name: String,
}

#[derive(Debug, Clone, PartialEq)]
pub struct BinOp {
    pub op: BinaryOperator,
    pub left: Box<FlameIR>,
    pub right: Box<FlameIR>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOperator {
    Add,    // +
    Sub,    // -
    Mul,    // *
    Div,    // /
    Mod,    // %
    Eq,     // ==
    Ne,     // !=
    Lt,     // <
    Le,     // <=
    Gt,     // >
    Ge,     // >=
    And,    // &&
    Or,     // ||
}

// ─────────────────────────────────────────────────────────────────────────────
// Type System (Minimal)
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, PartialEq)]
pub enum FlameType {
    Int,
    Float,
    Bool,
    String,
    Unit,
    Fn(Vec<FlameType>, Box<FlameType>),  // (params) -> return
}

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION B: PASS INTERFACE
// ═══════════════════════════════════════════════════════════════════════════════

/// Every pass must implement one of these traits.
/// Passes cannot invent new IR kinds without version bump.

/// Transform pass: IR -> IR (pure, no side effects)
pub trait TransformPass {
    fn name(&self) -> &'static str;
    fn transform(&self, ir: FlameIR) -> Result<FlameIR, PassError>;
}

/// Validation pass: IR -> Diagnostics (no mutation)
pub trait ValidatePass {
    fn name(&self) -> &'static str;
    fn validate(&self, ir: &FlameIR) -> Vec<Diagnostic>;
}

#[derive(Debug, Clone)]
pub struct PassError {
    pub pass_name: String,
    pub message: String,
    pub location: Option<Location>,
}

#[derive(Debug, Clone)]
pub struct Diagnostic {
    pub level: DiagnosticLevel,
    pub message: String,
    pub location: Option<Location>,
}

#[derive(Debug, Clone, PartialEq)]
pub enum DiagnosticLevel {
    Error,
    Warning,
    Info,
}

#[derive(Debug, Clone)]
pub struct Location {
    pub file: String,
    pub line: u32,
    pub column: u32,
}

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION C: INVARIANTS (Hard Rules)
// ═══════════════════════════════════════════════════════════════════════════════

/// Invariant checks that must pass for valid IR.
/// These are the "algorithm anatomy constraints" from the spec.

pub struct InvariantChecker;

impl InvariantChecker {
    /// INVARIANT 1: Every Return occurs inside a FnDef
    pub fn check_return_in_fndef(ir: &FlameIR) -> Vec<Diagnostic> {
        let mut diagnostics = Vec::new();
        Self::check_return_recursive(ir, false, &mut diagnostics);
        diagnostics
    }
    
    fn check_return_recursive(ir: &FlameIR, in_fn: bool, diags: &mut Vec<Diagnostic>) {
        match ir {
            FlameIR::Module(m) => {
                for item in &m.items {
                    Self::check_return_recursive(item, false, diags);
                }
            }
            FlameIR::FnDef(f) => {
                Self::check_return_recursive(&f.body, true, diags);
            }
            FlameIR::Block(b) => {
                for stmt in &b.statements {
                    Self::check_return_recursive(stmt, in_fn, diags);
                }
            }
            FlameIR::Return(_) if !in_fn => {
                diags.push(Diagnostic {
                    level: DiagnosticLevel::Error,
                    message: "Return statement outside function definition".into(),
                    location: None,
                });
            }
            FlameIR::Let(l) => {
                Self::check_return_recursive(&l.value, in_fn, diags);
            }
            FlameIR::Call(c) => {
                for arg in &c.args {
                    Self::check_return_recursive(arg, in_fn, diags);
                }
            }
            FlameIR::BinOp(b) => {
                Self::check_return_recursive(&b.left, in_fn, diags);
                Self::check_return_recursive(&b.right, in_fn, diags);
            }
            _ => {}
        }
    }
    
    /// INVARIANT 2: Call targets are resolvable
    pub fn check_call_targets(ir: &FlameIR) -> Vec<Diagnostic> {
        let mut diagnostics = Vec::new();
        let mut defined = std::collections::HashSet::new();
        
        // First pass: collect all defined names
        Self::collect_definitions(ir, &mut defined);
        
        // Second pass: check all calls
        Self::check_calls_recursive(ir, &defined, &mut diagnostics);
        
        diagnostics
    }
    
    fn collect_definitions(ir: &FlameIR, defined: &mut std::collections::HashSet<String>) {
        match ir {
            FlameIR::Module(m) => {
                for item in &m.items {
                    Self::collect_definitions(item, defined);
                }
            }
            FlameIR::FnDef(f) => {
                defined.insert(f.name.clone());
            }
            FlameIR::Extern(e) => {
                defined.insert(e.name.clone());
            }
            _ => {}
        }
    }
    
    fn check_calls_recursive(
        ir: &FlameIR, 
        defined: &std::collections::HashSet<String>,
        diags: &mut Vec<Diagnostic>
    ) {
        match ir {
            FlameIR::Module(m) => {
                for item in &m.items {
                    Self::check_calls_recursive(item, defined, diags);
                }
            }
            FlameIR::FnDef(f) => {
                Self::check_calls_recursive(&f.body, defined, diags);
            }
            FlameIR::Block(b) => {
                for stmt in &b.statements {
                    Self::check_calls_recursive(stmt, defined, diags);
                }
            }
            FlameIR::Call(c) => {
                if !defined.contains(&c.target) {
                    diags.push(Diagnostic {
                        level: DiagnosticLevel::Error,
                        message: format!("Unresolved call target: {}", c.target),
                        location: None,
                    });
                }
                for arg in &c.args {
                    Self::check_calls_recursive(arg, defined, diags);
                }
            }
            FlameIR::Let(l) => {
                Self::check_calls_recursive(&l.value, defined, diags);
            }
            FlameIR::BinOp(b) => {
                Self::check_calls_recursive(&b.left, defined, diags);
                Self::check_calls_recursive(&b.right, defined, diags);
            }
            FlameIR::Return(r) => {
                if let Some(v) = &r.value {
                    Self::check_calls_recursive(v, defined, diags);
                }
            }
            _ => {}
        }
    }
    
    /// INVARIANT 3: Every Let binds exactly once in its scope
    pub fn check_unique_bindings(ir: &FlameIR) -> Vec<Diagnostic> {
        let mut diagnostics = Vec::new();
        Self::check_bindings_recursive(ir, &mut Vec::new(), &mut diagnostics);
        diagnostics
    }
    
    fn check_bindings_recursive(
        ir: &FlameIR,
        scope: &mut Vec<String>,
        diags: &mut Vec<Diagnostic>
    ) {
        match ir {
            FlameIR::Module(m) => {
                for item in &m.items {
                    Self::check_bindings_recursive(item, scope, diags);
                }
            }
            FlameIR::FnDef(f) => {
                let mut fn_scope: Vec<String> = f.params.iter()
                    .map(|p| p.name.clone())
                    .collect();
                Self::check_bindings_recursive(&f.body, &mut fn_scope, diags);
            }
            FlameIR::Block(b) => {
                let mut block_scope = scope.clone();
                for stmt in &b.statements {
                    Self::check_bindings_recursive(stmt, &mut block_scope, diags);
                }
            }
            FlameIR::Let(l) => {
                if scope.contains(&l.name) {
                    diags.push(Diagnostic {
                        level: DiagnosticLevel::Error,
                        message: format!("Duplicate binding: {}", l.name),
                        location: None,
                    });
                }
                scope.push(l.name.clone());
                Self::check_bindings_recursive(&l.value, scope, diags);
            }
            FlameIR::Call(c) => {
                for arg in &c.args {
                    Self::check_bindings_recursive(arg, scope, diags);
                }
            }
            FlameIR::BinOp(b) => {
                Self::check_bindings_recursive(&b.left, scope, diags);
                Self::check_bindings_recursive(&b.right, scope, diags);
            }
            _ => {}
        }
    }
    
    /// Run all invariant checks
    pub fn check_all(ir: &FlameIR) -> Vec<Diagnostic> {
        let mut all = Vec::new();
        all.extend(Self::check_return_in_fndef(ir));
        all.extend(Self::check_call_targets(ir));
        all.extend(Self::check_unique_bindings(ir));
        all
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION D: PASS STUBS (Ready for Implementation)
// ═══════════════════════════════════════════════════════════════════════════════

/// TRIG6 Lowering Pass Stub
/// Role: Convert high-level codec ops to runtime calls
/// Status: STUB - implement after freeze validation
pub struct PassTRIG6Lowering;

impl TransformPass for PassTRIG6Lowering {
    fn name(&self) -> &'static str {
        "trig6_lowering"
    }
    
    fn transform(&self, ir: FlameIR) -> Result<FlameIR, PassError> {
        // TODO: Implement TRIG6 lowering
        // This pass will:
        // 1. Find TRIG6 codec operations in the IR
        // 2. Lower them to runtime function calls
        // 3. Preserve IR structure otherwise
        Ok(ir)
    }
}

/// TRIG6 Validation Pass Stub
/// Role: Validate TRIG6-specific constraints
/// Status: STUB - implement after freeze validation
pub struct PassTRIG6Validate;

impl ValidatePass for PassTRIG6Validate {
    fn name(&self) -> &'static str {
        "trig6_validate"
    }
    
    fn validate(&self, _ir: &FlameIR) -> Vec<Diagnostic> {
        // TODO: Implement TRIG6 validation
        // This pass will:
        // 1. Check angle bounds (0-360°)
        // 2. Validate frequency ranges
        // 3. Ensure TRIG6 operations are well-formed
        Vec::new()
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION E: BUILDER HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

/// Convenience functions for constructing IR nodes
pub mod builder {
    use super::*;
    
    pub fn module(name: &str, items: Vec<FlameIR>) -> FlameIR {
        FlameIR::Module(Module {
            name: name.into(),
            items,
            version: IR_VERSION.into(),
        })
    }
    
    pub fn fn_def(name: &str, params: Vec<(&str, FlameType)>, ret: FlameType, body: FlameIR) -> FlameIR {
        FlameIR::FnDef(FnDef {
            name: name.into(),
            params: params.into_iter()
                .map(|(n, t)| Param { name: n.into(), param_type: t })
                .collect(),
            return_type: ret,
            body: Box::new(body),
        })
    }
    
    pub fn block(statements: Vec<FlameIR>) -> FlameIR {
        FlameIR::Block(Block { statements })
    }
    
    pub fn let_bind(name: &str, value: FlameIR) -> FlameIR {
        FlameIR::Let(Let {
            name: name.into(),
            value: Box::new(value),
            let_type: None,
        })
    }
    
    pub fn const_int(v: i64) -> FlameIR {
        FlameIR::Const(Const::Int(v))
    }
    
    pub fn const_float(v: f64) -> FlameIR {
        FlameIR::Const(Const::Float(v))
    }
    
    pub fn const_string(v: &str) -> FlameIR {
        FlameIR::Const(Const::String(v.into()))
    }
    
    pub fn call(target: &str, args: Vec<FlameIR>) -> FlameIR {
        FlameIR::Call(Call {
            target: target.into(),
            args,
        })
    }
    
    pub fn ret(value: Option<FlameIR>) -> FlameIR {
        FlameIR::Return(Return {
            value: value.map(Box::new),
        })
    }
    
    pub fn extern_fn(name: &str, params: Vec<FlameType>, ret: FlameType) -> FlameIR {
        FlameIR::Extern(Extern {
            name: name.into(),
            params,
            return_type: ret,
        })
    }
    
    pub fn var(name: &str) -> FlameIR {
        FlameIR::Var(Var { name: name.into() })
    }
    
    pub fn binop(op: BinaryOperator, left: FlameIR, right: FlameIR) -> FlameIR {
        FlameIR::BinOp(BinOp {
            op,
            left: Box::new(left),
            right: Box::new(right),
        })
    }
    
    pub fn add(left: FlameIR, right: FlameIR) -> FlameIR {
        binop(BinaryOperator::Add, left, right)
    }
    
    pub fn mul(left: FlameIR, right: FlameIR) -> FlameIR {
        binop(BinaryOperator::Mul, left, right)
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SECTION F: EXAMPLE - hello.flame IR
// ═══════════════════════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use super::builder::*;
    
    /// The "birth certificate" - hello.flame as IR
    #[test]
    fn test_hello_flame_ir() {
        // hello.flame:
        // ```
        // extern fn print(s: String)
        // 
        // fn main() {
        //     print("Hello, FlameLang!")
        // }
        // ```
        
        let ir = module("hello", vec![
            extern_fn("print", vec![FlameType::String], FlameType::Unit),
            fn_def("main", vec![], FlameType::Unit,
                block(vec![
                    call("print", vec![const_string("Hello, FlameLang!")]),
                    ret(None),
                ])
            ),
        ]);
        
        // Validate invariants
        let diagnostics = InvariantChecker::check_all(&ir);
        assert!(diagnostics.is_empty(), "IR should pass all invariant checks: {:?}", diagnostics);
        
        // Verify structure
        if let FlameIR::Module(m) = &ir {
            assert_eq!(m.name, "hello");
            assert_eq!(m.version, IR_VERSION);
            assert_eq!(m.items.len(), 2);
        } else {
            panic!("Expected Module");
        }
    }
    
    /// Test invariant 1: Return outside FnDef
    #[test]
    fn test_invariant_return_outside_fn() {
        let ir = module("bad", vec![
            FlameIR::Return(Return { value: None }),  // Invalid!
        ]);
        
        let diagnostics = InvariantChecker::check_return_in_fndef(&ir);
        assert!(!diagnostics.is_empty(), "Should detect return outside fn");
    }
    
    /// Test invariant 2: Unresolved call target
    #[test]
    fn test_invariant_unresolved_call() {
        let ir = module("bad", vec![
            fn_def("main", vec![], FlameType::Unit,
                block(vec![
                    call("undefined_function", vec![]),  // Invalid!
                ])
            ),
        ]);
        
        let diagnostics = InvariantChecker::check_call_targets(&ir);
        assert!(!diagnostics.is_empty(), "Should detect unresolved call");
    }
    
    /// Test invariant 3: Duplicate binding
    #[test]
    fn test_invariant_duplicate_binding() {
        let ir = module("bad", vec![
            fn_def("main", vec![], FlameType::Unit,
                block(vec![
                    let_bind("x", const_int(1)),
                    let_bind("x", const_int(2)),  // Invalid!
                ])
            ),
        ]);
        
        let diagnostics = InvariantChecker::check_unique_bindings(&ir);
        assert!(!diagnostics.is_empty(), "Should detect duplicate binding");
    }
}
