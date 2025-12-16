/// Proton/Electron push-pull gradient stub.
/// In v0: treat as a typed vector field update rule.
pub fn gradient_step(push: f32, pull: f32) -> f32 {
    push - pull
}
