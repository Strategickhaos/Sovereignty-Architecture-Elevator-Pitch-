use thiserror::Error;

#[derive(Error, Debug)]
pub enum SynapseError {
    #[error("Gate dissolved request: {0}")]
    Dissolve(String),

    #[error("Gate clamped request: {0}")]
    Clamp(String),

    #[error("Invalid input: {0}")]
    Invalid(String),
}
