use super::{PassResult, Pipeline};
use crate::sheet::Sheet;

pub struct ParsePass;

impl Pipeline for ParsePass {
    fn run(&self, sheet: &mut Sheet) -> PassResult {
        use crate::parser::parse;
        let mut result = PassResult::new("ParsePass");
        for (addr, cell) in &sheet.cells {
            if cell.is_formula() {
                if let Err(e) = parse(&cell.formula) {
                    result.add_error(format!("{}: {}", addr, e));
                }
            }
        }
        result
    }
}
