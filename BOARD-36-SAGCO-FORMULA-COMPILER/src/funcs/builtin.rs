use crate::cell::Value;
use crate::registry::EvalError;

pub fn func_if(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 3 {
        return Err(EvalError::WrongArgCount("IF".to_string(), "3".to_string(), args.len()));
    }
    if args[0].as_bool() {
        Ok(args[1].clone())
    } else {
        Ok(args[2].clone())
    }
}

pub fn func_sum(args: &[Value]) -> Result<Value, EvalError> {
    let mut total = 0.0;
    for a in args {
        match a {
            Value::Number(n) => total += n,
            Value::Empty => {}
            Value::Str(s) => {
                if let Ok(n) = s.parse::<f64>() {
                    total += n;
                }
            }
            _ => {}
        }
    }
    Ok(Value::Number(total))
}

pub fn func_average(args: &[Value]) -> Result<Value, EvalError> {
    let mut total = 0.0;
    let mut count = 0usize;
    for a in args {
        if let Some(n) = a.as_number() {
            total += n;
            count += 1;
        }
    }
    if count == 0 {
        Ok(Value::Error("#DIV/0!".to_string()))
    } else {
        Ok(Value::Number(total / count as f64))
    }
}

pub fn func_min(args: &[Value]) -> Result<Value, EvalError> {
    let nums: Vec<f64> = args.iter().filter_map(|a| a.as_number()).collect();
    if nums.is_empty() {
        return Ok(Value::Empty);
    }
    Ok(Value::Number(nums.iter().cloned().fold(f64::INFINITY, f64::min)))
}

pub fn func_max(args: &[Value]) -> Result<Value, EvalError> {
    let nums: Vec<f64> = args.iter().filter_map(|a| a.as_number()).collect();
    if nums.is_empty() {
        return Ok(Value::Empty);
    }
    Ok(Value::Number(nums.iter().cloned().fold(f64::NEG_INFINITY, f64::max)))
}

pub fn func_len(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 1 {
        return Err(EvalError::WrongArgCount("LEN".to_string(), "1".to_string(), args.len()));
    }
    Ok(Value::Number(args[0].as_str().len() as f64))
}

pub fn func_concat(args: &[Value]) -> Result<Value, EvalError> {
    let s: String = args.iter().map(|a| a.as_str()).collect();
    Ok(Value::Str(s))
}

pub fn func_and(args: &[Value]) -> Result<Value, EvalError> {
    Ok(Value::Bool(args.iter().all(|a| a.as_bool())))
}

pub fn func_or(args: &[Value]) -> Result<Value, EvalError> {
    Ok(Value::Bool(args.iter().any(|a| a.as_bool())))
}

pub fn func_not(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 1 {
        return Err(EvalError::WrongArgCount("NOT".to_string(), "1".to_string(), args.len()));
    }
    Ok(Value::Bool(!args[0].as_bool()))
}

pub fn func_abs(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 1 {
        return Err(EvalError::WrongArgCount("ABS".to_string(), "1".to_string(), args.len()));
    }
    match args[0].as_number() {
        Some(n) => Ok(Value::Number(n.abs())),
        None => Err(EvalError::TypeError("ABS".to_string(), format!("{:?}", args[0]))),
    }
}

pub fn func_sqrt(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 1 {
        return Err(EvalError::WrongArgCount("SQRT".to_string(), "1".to_string(), args.len()));
    }
    match args[0].as_number() {
        Some(n) => Ok(Value::Number(n.sqrt())),
        None => Err(EvalError::TypeError("SQRT".to_string(), format!("{:?}", args[0]))),
    }
}

pub fn func_round(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() < 1 || args.len() > 2 {
        return Err(EvalError::WrongArgCount("ROUND".to_string(), "1-2".to_string(), args.len()));
    }
    let n = args[0].as_number().ok_or_else(|| {
        EvalError::TypeError("ROUND".to_string(), format!("{:?}", args[0]))
    })?;
    let digits = if args.len() == 2 {
        args[1].as_number().unwrap_or(0.0) as i32
    } else {
        0
    };
    let factor = 10f64.powi(digits);
    Ok(Value::Number((n * factor).round() / factor))
}
