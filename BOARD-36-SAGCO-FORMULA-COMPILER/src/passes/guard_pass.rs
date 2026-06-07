use super::{PassResult, Pipeline};
use crate::cell::Value;
use crate::funcs::sagco_guard::func_sagco_guard;
use crate::sheet::Sheet;

pub struct GuardPass;

impl Pipeline for GuardPass {
    fn run(&self, sheet: &mut Sheet) -> PassResult {
        let mut result = PassResult::new("GuardPass");

        for (addr, cell) in &sheet.cells {
            // Run SAGCO_GUARD on derivative/formula answers (evaluated values that are strings)
            if cell.is_formula() {
                let val_str = cell.value.as_str();
                if !val_str.is_empty() && !val_str.starts_with('#') {
                    match func_sagco_guard(&[Value::Str(val_str.clone())]) {
                        Ok(Value::Str(s)) if s == "NOT_READY" => {
                            result.add_warning(format!(
                                "{}: SAGCO_GUARD flagged value '{}' as NOT_READY",
                                addr, val_str
                            ));
                        }
                        Ok(Value::Str(s)) if s == "MOBIUS_READY" => {
                            result.add_warning(format!("{}: MOBIUS_READY", addr));
                        }
                        _ => {}
                    }
                }
            }
        }
        result
    }
}
