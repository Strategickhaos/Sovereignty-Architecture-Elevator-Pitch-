use super::{PassResult, Pipeline};
use crate::sheet::Sheet;

pub struct LexPass;

impl Pipeline for LexPass {
    fn run(&self, sheet: &mut Sheet) -> PassResult {
        use crate::lexer::tokenize;
        let mut result = PassResult::new("LexPass");
        for (addr, cell) in &sheet.cells {
            if cell.is_formula() {
                if let Err(e) = tokenize(&cell.formula) {
                    result.add_error(format!("{}: {}", addr, e));
                }
            }
        }
        result
    }
}
