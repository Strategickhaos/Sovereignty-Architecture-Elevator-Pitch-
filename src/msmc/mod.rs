// mod.rs - MSMC v2.0 Module Root
// Musical State Machine Compiler Backend

pub mod backend;
pub mod flame;

// Re-export commonly used types
pub use backend::{
    FormKind, SectionId, VoiceId, SectionSpec, VoiceSpec, FormSpec,
    Transition, TransitionCondition, Clock, MSMCNode, MSMCGraph,
    FlameIR, FlameAudioBackend, RenderConfig, WavBuffer,
    extract_form_spec_from_flame, build_state_machine, render_msmc_to_wav,
};

// Re-export flame integration types
pub use flame::{FlameTheme, FlameFormAnnotation, RondoBuilder, CanonBuilder};
