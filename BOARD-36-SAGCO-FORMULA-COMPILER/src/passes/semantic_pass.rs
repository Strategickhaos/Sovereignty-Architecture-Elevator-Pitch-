use super::{PassResult, Pipeline};
use crate::ast::Expr;
use crate::registry::FuncRegistry;
use crate::sheet::Sheet;

pub struct SemanticPass<'a> {
    pub registry: &'a FuncRegistry,
}

impl<'a> Pipeline for SemanticPass<'a> {
    fn run(&self, sheet: &mut Sheet) -> PassResult {
        use crate::parser::parse;
        let mut result = PassResult::new("SemanticPass");

        let cell_addrs: Vec<String> = sheet.cells.keys().cloned().collect();

        for addr in &cell_addrs {
            let cell = &sheet.cells[addr];
            if cell.is_formula() {
                match parse(&cell.formula) {
                    Ok(ast) => {
                        self.check_expr(&ast, addr, &cell_addrs, &mut result);
                    }
                    Err(_) => {
                        // ParsePass handles parse errors
                    }
                }
            }
        }
        result
    }
}

impl<'a> SemanticPass<'a> {
    fn check_expr(
        &self,
        expr: &Expr,
        addr: &str,
        known_cells: &[String],
        result: &mut PassResult,
    ) {
        match expr {
            Expr::CellRef(ref_addr) => {
                if !known_cells.contains(ref_addr) {
                    result.add_warning(format!(
                        "{}: references undefined cell {}",
                        addr, ref_addr
                    ));
                }
            }
            Expr::Call { name, args } => {
                if !self.registry.has(name) {
                    result.add_error(format!("{}: unknown function '{}'", addr, name));
                }
                for a in args {
                    self.check_expr(a, addr, known_cells, result);
                }
            }
            Expr::BinOp { left, right, .. } => {
                self.check_expr(left, addr, known_cells, result);
                self.check_expr(right, addr, known_cells, result);
            }
            Expr::UnaryOp { expr, .. } => {
                self.check_expr(expr, addr, known_cells, result);
            }
            Expr::IfExpr { cond, then, else_ } => {
                self.check_expr(cond, addr, known_cells, result);
                self.check_expr(then, addr, known_cells, result);
                self.check_expr(else_, addr, known_cells, result);
            }
            _ => {}
        }
    }
}
