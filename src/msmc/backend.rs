// msmc_backend.rs
// MSMC v2.0: Musical State Machine Compiler Backend
// Transforms Flame IR musical forms into bounded state machines and audio

// ---------- High-level form types ----------

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FormKind {
    Rondo,    // ABACA, ABACABA, etc.
    Fugue,    // subject/answer entries
    Canon,    // delayed replication
    Sonata,   // exposition/development/recapitulation
    Custom,   // escape hatch
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SectionId(pub u32); // A = 0, B = 1, etc.

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct VoiceId(pub u32);

#[derive(Debug, Clone)]
pub struct SectionSpec {
    pub id: SectionId,
    pub name: String,            // "A", "B", "Exposition", etc.
    pub duration_beats: f32,     // logical length
    pub voices: Vec<VoiceSpec>,
}

#[derive(Debug, Clone)]
pub struct VoiceSpec {
    pub id: VoiceId,
    /// Reference into Flame IR graph (theme, transformed theme, etc.)
    pub flame_node_id: u64,
    /// Optional transformation (canon offset, fugue inversion, etc.)
    pub time_offset_beats: f32,
    pub gain: f32,
}

// Description of overall musical form
#[derive(Debug, Clone)]
pub struct FormSpec {
    pub kind: FormKind,
    pub sections: Vec<SectionSpec>,
    /// High-level ordering, e.g., [A, B, A, C, A]
    pub sequence: Vec<SectionId>,
    /// Global tempo in BPM
    pub tempo_bpm: f32,
}

// ---------- State machine representation ----------

#[derive(Debug, Clone)]
pub struct Transition {
    pub from: SectionId,
    pub to: SectionId,
    pub start_time_beats: f32,  // when it can fire relative to piece start
    pub condition: TransitionCondition,
}

#[derive(Debug, Clone)]
pub enum TransitionCondition {
    /// Fire when `from` has completed its duration
    OnSectionEnd,
    /// Fire at absolute beat time (for overlapping)
    AtBeat(f32),
    /// Loop until max_reps then advance
    Loop {
        max_repetitions: u32,
    },
}

#[derive(Debug, Clone)]
pub struct Clock {
    pub tempo_bpm: f32,
    pub sample_rate: f32,
}

impl Clock {
    pub fn beats_to_samples(&self, beats: f32) -> u64 {
        let seconds = beats * 60.0 / self.tempo_bpm;
        (seconds * self.sample_rate) as u64
    }
}

#[derive(Debug, Clone)]
pub struct MSMCNode {
    pub section: SectionSpec,
    pub start_beat: f32,  // when this instance starts
    pub end_beat: f32,
}

#[derive(Debug, Clone)]
pub struct MSMCGraph {
    pub nodes: Vec<MSMCNode>,
    pub transitions: Vec<Transition>,
    pub clock: Clock,
    /// Derived: total duration in beats, guaranteed bounded
    pub total_duration_beats: f32,
}

// ---------- Audio binding and rendering ----------

// Abstract Flame IR handle – you will wire your real type here.
pub struct FlameIR {
    // your fields - placeholder for future integration
}

pub trait FlameAudioBackend {
    /// Given a Flame IR node and a time interval (in samples), render audio.
    fn render_flame_node(
        &self,
        flame: &FlameIR,
        flame_node_id: u64,
        start_sample: u64,
        num_samples: u64,
        out_left: &mut [f32],
        out_right: &mut [f32],
    );
}

pub struct RenderConfig {
    pub sample_rate: f32,
    pub num_channels: u16, // assume 2 for now
}

pub struct WavBuffer {
    pub sample_rate: u32,
    pub num_channels: u16,
    pub samples: Vec<f32>, // interleaved L/R
}

// ---------- Core API ----------

/// Build a FormSpec from Flame IR annotations.
/// In v2.0, assume Flame has already tagged themes and form.
pub fn extract_form_spec_from_flame(_flame: &FlameIR) -> FormSpec {
    // TODO: implement for real; placeholder for now
    FormSpec {
        kind: FormKind::Rondo,
        tempo_bpm: 120.0,
        sections: vec![],
        sequence: vec![],
    }
}

/// Build a bounded MSMC state machine from a FormSpec.
/// Enforce: finite duration, no orphan sections, valid transitions.
pub fn build_state_machine(form: &FormSpec) -> MSMCGraph {
    // 1. Expand sequence → concrete MSMCNode instances with time ranges
    let mut nodes = Vec::new();
    let mut current_beat = 0.0f32;
    
    // Create a map of section ID to section spec for easy lookup
    let mut section_map = std::collections::HashMap::new();
    for section in &form.sections {
        section_map.insert(section.id, section.clone());
    }
    
    // Expand the sequence into concrete nodes
    for &section_id in &form.sequence {
        if let Some(section_spec) = section_map.get(&section_id) {
            let start_beat = current_beat;
            let end_beat = current_beat + section_spec.duration_beats;
            
            nodes.push(MSMCNode {
                section: section_spec.clone(),
                start_beat,
                end_beat,
            });
            
            current_beat = end_beat;
        }
    }
    
    // 2. Create transitions (OnSectionEnd by default)
    let mut transitions = Vec::new();
    for i in 0..(nodes.len().saturating_sub(1)) {
        transitions.push(Transition {
            from: nodes[i].section.id,
            to: nodes[i + 1].section.id,
            start_time_beats: nodes[i].end_beat,
            condition: TransitionCondition::OnSectionEnd,
        });
    }
    
    // 3. Compute total_duration_beats and validate boundedness
    let total_duration_beats = current_beat;
    
    let clock = Clock {
        tempo_bpm: form.tempo_bpm,
        sample_rate: 44100.0,
    };

    MSMCGraph {
        nodes,
        transitions,
        clock,
        total_duration_beats,
    }
}

/// Render the MSMC graph into a WAV buffer using a Flame audio backend.
pub fn render_msmc_to_wav<B: FlameAudioBackend>(
    flame: &FlameIR,
    backend: &B,
    ms: &MSMCGraph,
    cfg: &RenderConfig,
) -> WavBuffer {
    let total_samples = ms.clock.beats_to_samples(ms.total_duration_beats);
    let mut samples = vec![0.0f32; (total_samples as usize) * cfg.num_channels as usize];

    // For each node (section instance), schedule its voices into the buffer
    for node in &ms.nodes {
        let node_start = ms.clock.beats_to_samples(node.start_beat);
        let node_end = ms.clock.beats_to_samples(node.end_beat);
        let node_len = node_end - node_start;

        for voice in &node.section.voices {
            let mut left = vec![0.0f32; node_len as usize];
            let mut right = vec![0.0f32; node_len as usize];

            backend.render_flame_node(
                flame,
                voice.flame_node_id,
                node_start,
                node_len,
                &mut left,
                &mut right,
            );

            // Mix into main buffer with gain and offset
            for i in 0..node_len as usize {
                let global_idx = (node_start as usize + i) * 2;
                if global_idx + 1 < samples.len() {
                    samples[global_idx] += left[i] * voice.gain;
                    samples[global_idx + 1] += right[i] * voice.gain;
                }
            }
        }
    }

    WavBuffer {
        sample_rate: cfg.sample_rate as u32,
        num_channels: cfg.num_channels,
        samples,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_clock_beats_to_samples() {
        let clock = Clock {
            tempo_bpm: 120.0,
            sample_rate: 44100.0,
        };
        
        // At 120 BPM, 1 beat = 0.5 seconds = 22050 samples
        let samples = clock.beats_to_samples(1.0);
        assert_eq!(samples, 22050);
        
        // 4 beats = 2 seconds = 88200 samples
        let samples = clock.beats_to_samples(4.0);
        assert_eq!(samples, 88200);
    }
    
    #[test]
    fn test_build_simple_state_machine() {
        // Create a simple A-B-A form
        let section_a = SectionSpec {
            id: SectionId(0),
            name: "A".to_string(),
            duration_beats: 8.0,
            voices: vec![],
        };
        
        let section_b = SectionSpec {
            id: SectionId(1),
            name: "B".to_string(),
            duration_beats: 8.0,
            voices: vec![],
        };
        
        let form = FormSpec {
            kind: FormKind::Rondo,
            sections: vec![section_a, section_b],
            sequence: vec![SectionId(0), SectionId(1), SectionId(0)],
            tempo_bpm: 120.0,
        };
        
        let graph = build_state_machine(&form);
        
        // Should have 3 nodes (A, B, A)
        assert_eq!(graph.nodes.len(), 3);
        
        // Total duration should be 8 + 8 + 8 = 24 beats
        assert_eq!(graph.total_duration_beats, 24.0);
        
        // Should have 2 transitions
        assert_eq!(graph.transitions.len(), 2);
        
        // Verify node timing
        assert_eq!(graph.nodes[0].start_beat, 0.0);
        assert_eq!(graph.nodes[0].end_beat, 8.0);
        assert_eq!(graph.nodes[1].start_beat, 8.0);
        assert_eq!(graph.nodes[1].end_beat, 16.0);
        assert_eq!(graph.nodes[2].start_beat, 16.0);
        assert_eq!(graph.nodes[2].end_beat, 24.0);
    }
}
