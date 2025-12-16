/// Dissolve = energy return / cleanup primitive.
pub fn dissolve_tag(reason: &str) -> String {
    format!("DISSOLVE::{reason}")
}
