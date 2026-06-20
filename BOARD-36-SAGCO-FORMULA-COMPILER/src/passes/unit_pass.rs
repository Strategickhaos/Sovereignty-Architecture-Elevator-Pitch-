use super::{PassResult, Pipeline};
use crate::ast::Expr;
use crate::sheet::Sheet;

const VALID_UNITS: &[&str] = &[
    "km", "mi", "miles", "m", "meters", "ft", "feet",
    "kg", "lb", "lbs",
    "c", "f", "celsius", "fahrenheit",
];

pub struct UnitPass;

impl Pipeline for UnitPass {
    fn run(&self, sheet: &mut Sheet) -> PassResult {
        use crate::parser::parse;
        let mut result = PassResult::new("UnitPass");

        for (addr, cell) in &sheet.cells {
            if cell.is_formula() {
                if let Ok(ast) = parse(&cell.formula) {
                    check_units_expr(&ast, addr, &mut result);
                }
            }
        }
        result
    }
}

fn check_units_expr(expr: &Expr, addr: &str, result: &mut PassResult) {
    match expr {
        Expr::Call { name, args } if name.to_uppercase() == "SAGCO_UNITS" => {
            if args.len() == 3 {
                // args[1] and args[2] should be string literals
                if let Expr::Str(from_unit) = &args[1] {
                    if !VALID_UNITS.contains(&from_unit.to_lowercase().as_str()) {
                        result.add_error(format!(
                            "{}: SAGCO_UNITS unknown from_unit '{}'",
                            addr, from_unit
                        ));
                    }
                }
                if let Expr::Str(to_unit) = &args[2] {
                    if !VALID_UNITS.contains(&to_unit.to_lowercase().as_str()) {
                        result.add_error(format!(
                            "{}: SAGCO_UNITS unknown to_unit '{}'",
                            addr, to_unit
                        ));
                    }
                }
            }
            for a in args {
                check_units_expr(a, addr, result);
            }
        }
        Expr::Call { args, .. } => {
            for a in args {
                check_units_expr(a, addr, result);
            }
        }
        Expr::BinOp { left, right, .. } => {
            check_units_expr(left, addr, result);
            check_units_expr(right, addr, result);
        }
        Expr::UnaryOp { expr, .. } => {
            check_units_expr(expr, addr, result);
        }
        Expr::IfExpr { cond, then, else_ } => {
            check_units_expr(cond, addr, result);
            check_units_expr(then, addr, result);
            check_units_expr(else_, addr, result);
        }
        _ => {}
    }
}
