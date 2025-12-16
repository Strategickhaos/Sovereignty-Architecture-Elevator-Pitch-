use crate::primitives::error::SynapseError;

/// Reflex = local policy response to spikes/fields.
pub enum ReflexDecision {
    Flow,
    Clamp(String),
    Dissolve(String),
}

pub trait Reflex<C, I> {
    fn decide(&self, ctx: &C, input: &I) -> Result<ReflexDecision, SynapseError>;
}
