/// Membrane = explicit boundary traits.
/// Anything crossing this boundary must be typed, validated, and traceable.
pub trait Membrane<I, O> {
    fn pass(&self, input: I) -> O;
}
