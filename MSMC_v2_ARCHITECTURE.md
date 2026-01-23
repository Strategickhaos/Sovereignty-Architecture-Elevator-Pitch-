# MSMC v2.0: Musical State Machine Compiler

## Overview

The Musical State Machine Compiler (MSMC) v2.0 is an architecture for transforming high-level musical forms (defined in Flame IR) into bounded state machines and rendered audio. It provides a complete pipeline from symbolic musical representation to PCM audio output.

## Architecture Layers

The MSMC v2.0 architecture consists of five distinct layers:

### 1. Flame IR (Symbolic Layer)
- **Purpose**: Typed symbolic graph representation of music
- **Components**: Frequency, energy, angle, and other musical parameters
- **Annotations**: Form annotations (rondo, fugue, canon) and theme definitions
- **Output**: Abstract musical structure independent of rendering

### 2. Form Spec (MSMC-Form Layer)
- **Purpose**: High-level musical form specification
- **Components**: 
  - `FormKind`: Enumeration of supported forms (Rondo, Fugue, Canon, Sonata, Custom)
  - `SectionSpec`: Definition of musical sections with duration and voices
  - `VoiceSpec`: Individual voice configuration within sections
- **Example**: `Rondo(ABACA)`, `Canon(subject, delay, voices)`

### 3. Musical State Machine (MSMCGraph Layer)
- **Purpose**: Deterministic state machine representation
- **Components**:
  - `MSMCNode`: Section instances with time bounds
  - `Transition`: Connections between sections with timing constraints
  - `Clock`: Tempo and sample rate management
- **Constraints**: Guaranteed bounded execution, no infinite loops

### 4. Signal Graph Layer
- **Purpose**: Binding musical structure to audio generation
- **Components**: Each node's content bound to Flame IR fragments
- **Scheduling**: Time-scheduled per voice with sample-accurate timing

### 5. Renderer Layer
- **Purpose**: Deterministic audio generation
- **Components**: PCM buffer generation from MSMCGraph traversal
- **Output**: WAV buffer or live audio stream

## Core Data Model

### Form Specification Types

```rust
// Musical form kinds
pub enum FormKind {
    Rondo,    // ABACA, ABACABA patterns
    Fugue,    // Subject/answer entries
    Canon,    // Delayed replication
    Sonata,   // Exposition/development/recapitulation
    Custom,   // User-defined forms
}

// Section specification
pub struct SectionSpec {
    pub id: SectionId,
    pub name: String,
    pub duration_beats: f32,
    pub voices: Vec<VoiceSpec>,
}

// Voice within a section
pub struct VoiceSpec {
    pub id: VoiceId,
    pub flame_node_id: u64,        // Reference to Flame IR node
    pub time_offset_beats: f32,    // Canon/fugue offset
    pub gain: f32,                 // Audio level
}
```

### State Machine Types

```rust
// State machine node (section instance)
pub struct MSMCNode {
    pub section: SectionSpec,
    pub start_beat: f32,
    pub end_beat: f32,
}

// Transition between sections
pub struct Transition {
    pub from: SectionId,
    pub to: SectionId,
    pub start_time_beats: f32,
    pub condition: TransitionCondition,
}

// Transition conditions
pub enum TransitionCondition {
    OnSectionEnd,                    // Fire when section completes
    AtBeat(f32),                     // Fire at absolute beat time
    Loop { max_repetitions: u32 },   // Loop with bounds
}
```

### Audio Types

```rust
// Audio backend trait
pub trait FlameAudioBackend {
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

// Output buffer
pub struct WavBuffer {
    pub sample_rate: u32,
    pub num_channels: u16,
    pub samples: Vec<f32>,  // Interleaved L/R
}
```

## Core API

### 1. Extract Form Spec from Flame IR

```rust
pub fn extract_form_spec_from_flame(flame: &FlameIR) -> FormSpec
```

Reads Flame IR annotations and theme metadata to produce a `FormSpec`. This includes:
- Parsing form annotations (rondo, fugue, canon, etc.)
- Extracting theme definitions and durations
- Determining section sequence
- Setting global tempo

### 2. Build State Machine

```rust
pub fn build_state_machine(form: &FormSpec) -> MSMCGraph
```

Converts a `FormSpec` into a bounded `MSMCGraph`:
- Expands sequence into concrete `MSMCNode` instances
- Assigns start/end beat times to each node
- Creates transitions between nodes
- Validates boundedness (no infinite loops)
- Computes total duration in beats

**Guarantees**:
- Finite duration
- No orphan sections
- All sections in sequence exist
- Valid transitions
- Fanout within limits

### 3. Render to Audio

```rust
pub fn render_msmc_to_wav<B: FlameAudioBackend>(
    flame: &FlameIR,
    backend: &B,
    ms: &MSMCGraph,
    cfg: &RenderConfig,
) -> WavBuffer
```

Renders the state machine to audio:
- Converts beats to samples via `Clock`
- Iterates nodes and voices
- Calls `backend.render_flame_node` for each voice
- Mixes voices with gain control
- Returns interleaved PCM buffer

## Data Flow Example: Rondo Form

### Step 1: Flame Program
```flame
// Define themes
theme A = freq(440) * env(attack=0.1, release=0.5)
theme B = freq(493.88) * env(attack=0.2, release=0.4)
theme C = freq(523.25) * env(attack=0.15, release=0.6)

// Declare form
form rondo
compose A B A C A
tempo 120
```

### Step 2: Flame Compiler
Builds `FlameIR` graph:
- Node per theme (A, B, C)
- Form annotation: `FormKind::Rondo`
- Sequence: `[A, B, A, C, A]`
- Tempo: 120 BPM

### Step 3: Extract Form Spec
```rust
let form_spec = extract_form_spec_from_flame(&flame_ir);
// form_spec.kind = FormKind::Rondo
// form_spec.sequence = [SectionId(0), SectionId(1), SectionId(0), SectionId(2), SectionId(0)]
// form_spec.tempo_bpm = 120.0
```

### Step 4: Build State Machine
```rust
let state_machine = build_state_machine(&form_spec);
// Expands to 5 nodes:
// Node 0: Section A, beats 0.0 → 8.0
// Node 1: Section B, beats 8.0 → 16.0
// Node 2: Section A, beats 16.0 → 24.0
// Node 3: Section C, beats 24.0 → 32.0
// Node 4: Section A, beats 32.0 → 40.0
// total_duration_beats = 40.0
```

### Step 5: Render Audio
```rust
let wav_buffer = render_msmc_to_wav(&flame_ir, &backend, &state_machine, &config);
// Total samples: 40 beats × 0.5 sec/beat × 44100 Hz = 882,000 samples
// Duration: 20 seconds
// Output: Interleaved stereo PCM
```

## Flame Integration API

The `flame` module provides builders for constructing musical forms:

### Rondo Builder

```rust
use msmc_backend::flame::RondoBuilder;

let mut builder = RondoBuilder::new(120.0);
builder
    .add_theme("A", 1, 8.0)  // name, node_id, duration
    .add_theme("B", 2, 8.0)
    .add_theme("C", 3, 8.0);

// Build standard ABACA form
let form = builder.build_abaca();

// Build extended ABACABA form
let form = builder.build_abacaba();

// Build custom sequence
let form = builder.build_custom(vec!["A".to_string(), "B".to_string(), "C".to_string()]);

// Convert to FormSpec
let form_spec = form.to_form_spec();
```

### Canon Builder

```rust
use msmc_backend::flame::CanonBuilder;

let mut builder = CanonBuilder::new(120.0);
builder
    .set_subject("Subject", 1, 16.0)
    .set_voices(3)
    .set_delay(4.0);

let form = builder.build();
let form_spec = form.to_form_spec();
```

## Validation and Constraints

MSMC v2.0 enforces several critical constraints:

### Boundedness
- **Requirement**: Total duration must be finite
- **Enforcement**: `build_state_machine` computes exact beat count
- **Prevention**: No infinite loops, all transitions terminate

### Completeness
- **Requirement**: All sections in sequence must exist
- **Enforcement**: Section ID validation during node expansion
- **Prevention**: No dangling references or orphan sections

### Temporal Consistency
- **Requirement**: Node timings must be sequential and non-overlapping
- **Enforcement**: Sequential beat assignment during expansion
- **Prevention**: Temporal paradoxes or overlaps

### Fanout Limits
- **Requirement**: Transitions from each node must be bounded
- **Enforcement**: Maximum one outgoing transition per node
- **Prevention**: Exponential state explosion

## Example Usage

See `examples/rondo_example.rs` for a complete working example that:
1. Defines themes using the Flame integration API
2. Builds a Rondo form (ABACA)
3. Converts to FormSpec
4. Builds the state machine
5. Renders to audio
6. Verifies structural properties

Run the example:
```bash
cargo run --example rondo_example
```

## Testing

The implementation includes unit tests for core functionality:

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_build_simple_state_machine
```

## Future Extensions

Planned enhancements for MSMC v2.0:

1. **Advanced Forms**: Sonata-allegro, theme and variations, binary/ternary forms
2. **Dynamic Transitions**: Conditional transitions based on musical parameters
3. **Voice Transformations**: Inversion, retrograde, augmentation, diminution
4. **Real-time Rendering**: Streaming audio output for live performance
5. **MIDI Integration**: MIDI input/output for hardware synthesis
6. **Optimization**: Parallel voice rendering, SIMD audio processing

## Dependencies

- `sha2`: Cryptographic hashing (for future integrity features)
- `hex`: Hexadecimal encoding (for debug/logging)
- `serde`: Serialization framework
- `serde_json`: JSON serialization for configuration

## License

MIT License - See LICENSE file for details

---

**Built with 🔥 by the Strategickhaos DAO LLC**

*Part of the Sovereignty Architecture - FlameLang Integration*
