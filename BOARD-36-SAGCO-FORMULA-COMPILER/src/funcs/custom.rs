use crate::cell::Value;
use crate::registry::EvalError;

/// MORSE code map
fn morse_char(c: char) -> Option<&'static str> {
    match c.to_ascii_uppercase() {
        'A' => Some(".-"),
        'B' => Some("-..."),
        'C' => Some("-.-."),
        'D' => Some("-.."),
        'E' => Some("."),
        'F' => Some("..-."),
        'G' => Some("--."),
        'H' => Some("...."),
        'I' => Some(".."),
        'J' => Some(".---"),
        'K' => Some("-.-"),
        'L' => Some(".-.."),
        'M' => Some("--"),
        'N' => Some("-."),
        'O' => Some("---"),
        'P' => Some(".--."),
        'Q' => Some("--.-"),
        'R' => Some(".-."),
        'S' => Some("..."),
        'T' => Some("-"),
        'U' => Some("..-"),
        'V' => Some("...-"),
        'W' => Some(".--"),
        'X' => Some("-..-"),
        'Y' => Some("-.--"),
        'Z' => Some("--.."),
        '0' => Some("-----"),
        '1' => Some(".----"),
        '2' => Some("..---"),
        '3' => Some("...--"),
        '4' => Some("....-"),
        '5' => Some("....."),
        '6' => Some("-...."),
        '7' => Some("--..."),
        '8' => Some("---.."),
        '9' => Some("----."),
        _ => None,
    }
}

/// MORSE(text) → Morse code string
/// Letters separated by space, words separated by " / "
pub fn func_morse(args: &[Value]) -> Result<Value, EvalError> {
    if args.len() != 1 {
        return Err(EvalError::WrongArgCount(
            "MORSE".to_string(),
            "1".to_string(),
            args.len(),
        ));
    }
    let text = args[0].as_str();
    let mut words_encoded: Vec<String> = Vec::new();

    for word in text.split_whitespace() {
        let mut letters: Vec<String> = Vec::new();
        for ch in word.chars() {
            if let Some(code) = morse_char(ch) {
                letters.push(code.to_string());
            }
        }
        if !letters.is_empty() {
            words_encoded.push(letters.join(" "));
        }
    }

    Ok(Value::Str(words_encoded.join(" / ")))
}
