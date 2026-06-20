use crate::cell::Value;
use crate::registry::EvalError;

/// SAGCO_SANITY(val) — checks for hallucination markers
pub fn func_sagco_sanity(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 1 {
        return Err(EvalError::WrongArgCount(
            "SAGCO_SANITY".to_string(),
            "1".to_string(),
            args.len(),
        ));
    }
    let s = args[0].as_str();
    // Hallucination markers: **, LaTeX patterns, Unicode math symbols
    let hallucination_markers = [
        "**",
        "\\frac",
        "\\sqrt",
        "\\int",
        "\\sum",
        "\\prod",
        "\\alpha",
        "\\beta",
        "\\gamma",
        "\\delta",
        "\\epsilon",
        "\\theta",
        "\\lambda",
        "\\mu",
        "\\pi",
        "\\sigma",
        "\\phi",
        "\\omega",
        "$",
        "≈",
        "≠",
        "≤",
        "≥",
        "∞",
        "∑",
        "∫",
        "∂",
        "√",
        "∏",
        "∀",
        "∃",
        "∈",
        "∉",
        "⊂",
        "⊃",
        "⊆",
        "⊇",
        "→",
        "⇒",
        "⟺",
    ];

    for marker in &hallucination_markers {
        if s.contains(marker) {
            return Ok(Value::Str("HALLUCINATION_RISK".to_string()));
        }
    }
    Ok(Value::Str("SOVEREIGN".to_string()))
}

/// SAGCO_ERU(expected, actual) → "VARIANCE_0" | "OPEN_VARIANCE"
pub fn func_sagco_eru(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 2 {
        return Err(EvalError::WrongArgCount(
            "SAGCO_ERU".to_string(),
            "2".to_string(),
            args.len(),
        ));
    }
    let expected = args[0].as_str();
    let actual = args[1].as_str();
    if expected == actual {
        Ok(Value::Str("VARIANCE_0".to_string()))
    } else {
        Ok(Value::Str("OPEN_VARIANCE".to_string()))
    }
}

/// SAGCO_GUARD(formula_str) → runs mobius formatting check
pub fn func_sagco_guard(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 1 {
        return Err(EvalError::WrongArgCount(
            "SAGCO_GUARD".to_string(),
            "1".to_string(),
            args.len(),
        ));
    }
    let s = args[0].as_str();
    // Mobius formatting check: no hallucination markers, no empty, valid chars
    let bad_markers = ["**", "\\frac", "\\sqrt", "$", "≈", "∞", "∑", "∫", "∂"];
    for marker in &bad_markers {
        if s.contains(marker) {
            return Ok(Value::Str("NOT_READY".to_string()));
        }
    }
    // Must be non-empty and not contain obvious error markers
    if s.is_empty() || s.starts_with('#') {
        return Ok(Value::Str("NOT_READY".to_string()));
    }
    Ok(Value::Str("MOBIUS_READY".to_string()))
}

/// SAGCO_UNITS(val, from_unit, to_unit) → basic unit conversion
pub fn func_sagco_units(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 3 {
        return Err(EvalError::WrongArgCount(
            "SAGCO_UNITS".to_string(),
            "3".to_string(),
            args.len(),
        ));
    }
    let val = args[0].as_number().ok_or_else(|| {
        EvalError::TypeError("SAGCO_UNITS".to_string(), "first arg must be a number".to_string())
    })?;
    let from = args[1].as_str().to_lowercase();
    let to = args[2].as_str().to_lowercase();

    let result = match (from.as_str(), to.as_str()) {
        ("km", "mi") | ("km", "miles") => val * 0.621371,
        ("mi", "km") | ("miles", "km") => val * 1.60934,
        ("c", "f") | ("celsius", "fahrenheit") => val * 9.0 / 5.0 + 32.0,
        ("f", "c") | ("fahrenheit", "celsius") => (val - 32.0) * 5.0 / 9.0,
        ("m", "ft") | ("meters", "feet") => val * 3.28084,
        ("ft", "m") | ("feet", "meters") => val / 3.28084,
        ("kg", "lb") | ("kg", "lbs") => val * 2.20462,
        ("lb", "kg") | ("lbs", "kg") => val / 2.20462,
        _ => {
            return Ok(Value::Error(format!(
                "#UNIT_ERR! Cannot convert {} to {}",
                from, to
            )));
        }
    };
    Ok(Value::Number(result))
}
