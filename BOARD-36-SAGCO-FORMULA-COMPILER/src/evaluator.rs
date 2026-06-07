use crate::ast::{BinOp, Expr, UnaryOp};
use crate::cell::Value;
use crate::registry::{EvalError, FuncRegistry};
use crate::sheet::Sheet;

pub struct Evaluator<'a> {
    pub registry: &'a FuncRegistry,
    pub sheet: &'a Sheet,
}

impl<'a> Evaluator<'a> {
    pub fn new(registry: &'a FuncRegistry, sheet: &'a Sheet) -> Self {
        Evaluator { registry, sheet }
    }

    pub fn eval(&self, expr: &Expr) -> Result<Value, EvalError> {
        match expr {
            Expr::Number(n) => Ok(Value::Number(*n)),
            Expr::Str(s) => Ok(Value::Str(s.clone())),
            Expr::Bool(b) => Ok(Value::Bool(*b)),

            Expr::CellRef(addr) => {
                Ok(self.sheet.get(addr).unwrap_or(Value::Empty))
            }

            Expr::RangeRef(from, to) => {
                // Return as a list disguised as first value (evaluator expands at call site)
                // For now return the range description — functions handle range expansion
                Ok(Value::Str(format!("{}:{}", from, to)))
            }

            Expr::BinOp { left, op, right } => {
                self.eval_binop(left, op, right)
            }

            Expr::UnaryOp { op, expr } => {
                let val = self.eval(expr)?;
                match op {
                    UnaryOp::Neg => {
                        if let Some(n) = val.as_number() {
                            Ok(Value::Number(-n))
                        } else {
                            Err(EvalError::TypeError("NEG".to_string(), format!("cannot negate {:?}", val)))
                        }
                    }
                    UnaryOp::Not => Ok(Value::Bool(!val.as_bool())),
                }
            }

            Expr::Call { name, args } => {
                // Evaluate args, expanding range refs using the sheet
                let mut eval_args = Vec::new();
                for arg in args {
                    match arg {
                        Expr::RangeRef(from, to) => {
                            let vals = self.expand_range(from, to);
                            eval_args.extend(vals);
                        }
                        _ => {
                            eval_args.push(self.eval(arg)?);
                        }
                    }
                }
                self.registry.call(name, &eval_args)
            }

            Expr::IfExpr { cond, then, else_ } => {
                let cond_val = self.eval(cond)?;
                if cond_val.as_bool() {
                    self.eval(then)
                } else {
                    self.eval(else_)
                }
            }

            Expr::Error(s) => Ok(Value::Error(s.clone())),
        }
    }

    fn eval_binop(&self, left: &Expr, op: &BinOp, right: &Expr) -> Result<Value, EvalError> {
        let lv = self.eval(left)?;
        let rv = self.eval(right)?;

        match op {
            BinOp::Add => {
                match (lv.as_number(), rv.as_number()) {
                    (Some(a), Some(b)) => Ok(Value::Number(a + b)),
                    _ => Err(EvalError::TypeError("ADD".to_string(), format!("{:?} + {:?}", lv, rv))),
                }
            }
            BinOp::Sub => {
                match (lv.as_number(), rv.as_number()) {
                    (Some(a), Some(b)) => Ok(Value::Number(a - b)),
                    _ => Err(EvalError::TypeError("SUB".to_string(), format!("{:?} - {:?}", lv, rv))),
                }
            }
            BinOp::Mul => {
                match (lv.as_number(), rv.as_number()) {
                    (Some(a), Some(b)) => Ok(Value::Number(a * b)),
                    _ => Err(EvalError::TypeError("MUL".to_string(), format!("{:?} * {:?}", lv, rv))),
                }
            }
            BinOp::Div => {
                match (lv.as_number(), rv.as_number()) {
                    (Some(a), Some(b)) => {
                        if b == 0.0 {
                            Err(EvalError::DivisionByZero)
                        } else {
                            Ok(Value::Number(a / b))
                        }
                    }
                    _ => Err(EvalError::TypeError("DIV".to_string(), format!("{:?} / {:?}", lv, rv))),
                }
            }
            BinOp::Pow => {
                match (lv.as_number(), rv.as_number()) {
                    (Some(a), Some(b)) => Ok(Value::Number(a.powf(b))),
                    _ => Err(EvalError::TypeError("POW".to_string(), format!("{:?} ^ {:?}", lv, rv))),
                }
            }
            BinOp::Concat => Ok(Value::Str(format!("{}{}", lv.as_str(), rv.as_str()))),
            BinOp::Eq => Ok(Value::Bool(values_eq(&lv, &rv))),
            BinOp::NEq => Ok(Value::Bool(!values_eq(&lv, &rv))),
            BinOp::Lt => Ok(Value::Bool(compare_values(&lv, &rv) < 0)),
            BinOp::Gt => Ok(Value::Bool(compare_values(&lv, &rv) > 0)),
            BinOp::LtEq => Ok(Value::Bool(compare_values(&lv, &rv) <= 0)),
            BinOp::GtEq => Ok(Value::Bool(compare_values(&lv, &rv) >= 0)),
            BinOp::And => Ok(Value::Bool(lv.as_bool() && rv.as_bool())),
            BinOp::Or => Ok(Value::Bool(lv.as_bool() || rv.as_bool())),
        }
    }

    /// Expand a range like A1:A10 into individual cell values
    pub fn expand_range(&self, from: &str, to: &str) -> Vec<Value> {
        let cells = expand_range_addrs(from, to);
        cells.into_iter()
            .map(|addr| self.sheet.get(&addr).unwrap_or(Value::Empty))
            .collect()
    }
}

fn values_eq(a: &Value, b: &Value) -> bool {
    match (a, b) {
        (Value::Number(x), Value::Number(y)) => x == y,
        (Value::Str(x), Value::Str(y)) => x == y,
        (Value::Bool(x), Value::Bool(y)) => x == y,
        (Value::Empty, Value::Empty) => true,
        _ => false,
    }
}

fn compare_values(a: &Value, b: &Value) -> i32 {
    match (a.as_number(), b.as_number()) {
        (Some(x), Some(y)) => {
            if x < y { -1 } else if x > y { 1 } else { 0 }
        }
        _ => {
            let sa = a.as_str();
            let sb = b.as_str();
            sa.cmp(&sb) as i32
        }
    }
}

/// Expand A1:A10 into ["A1","A2",...,"A10"]
pub fn expand_range_addrs(from: &str, to: &str) -> Vec<String> {
    let (fc, fr) = parse_cell_addr(from);
    let (tc, tr) = parse_cell_addr(to);
    if fc.is_empty() || tc.is_empty() {
        return vec![];
    }
    let mut result = Vec::new();
    let col_start = col_to_num(&fc);
    let col_end = col_to_num(&tc);
    let row_start = fr.min(tr);
    let row_end = fr.max(tr);
    let cs = col_start.min(col_end);
    let ce = col_start.max(col_end);
    for row in row_start..=row_end {
        for col in cs..=ce {
            result.push(format!("{}{}", num_to_col(col), row));
        }
    }
    result
}

fn parse_cell_addr(addr: &str) -> (String, usize) {
    let mut col = String::new();
    let mut row = String::new();
    for c in addr.chars() {
        if c.is_alphabetic() {
            col.push(c.to_ascii_uppercase());
        } else if c.is_ascii_digit() {
            row.push(c);
        }
    }
    let r = row.parse::<usize>().unwrap_or(0);
    (col, r)
}

fn col_to_num(col: &str) -> usize {
    col.chars().fold(0, |acc, c| {
        acc * 26 + (c.to_ascii_uppercase() as usize - 'A' as usize + 1)
    })
}

fn num_to_col(n: usize) -> String {
    let mut n = n;
    let mut result = String::new();
    while n > 0 {
        n -= 1;
        result.push((b'A' + (n % 26) as u8) as char);
        n /= 26;
    }
    result.chars().rev().collect()
}
