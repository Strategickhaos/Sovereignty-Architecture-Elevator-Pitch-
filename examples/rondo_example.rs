// examples/rondo_example.rs
// Demonstrates creating and rendering a Rondo form (ABACA) using MSMC v2.0

use msmc_backend::{
    FlameIR, FlameAudioBackend, RenderConfig, build_state_machine, render_msmc_to_wav,
};

// Import the Flame integration module
use msmc_backend::flame::RondoBuilder;

// Mock audio backend for demonstration
struct MockAudioBackend;

impl FlameAudioBackend for MockAudioBackend {
    fn render_flame_node(
        &self,
        _flame: &FlameIR,
        flame_node_id: u64,
        start_sample: u64,
        num_samples: u64,
        out_left: &mut [f32],
        out_right: &mut [f32],
    ) {
        // Generate simple sine waves at different frequencies for each theme
        let freq = match flame_node_id {
            1 => 440.0,  // A theme: A4 (440 Hz)
            2 => 493.88, // B theme: B4
            3 => 523.25, // C theme: C5
            _ => 440.0,
        };
        
        let sample_rate = 44100.0;
        let amplitude = 0.3;
        
        for i in 0..num_samples as usize {
            if i < out_left.len() && i < out_right.len() {
                let t = (start_sample as f32 + i as f32) / sample_rate;
                let sample = amplitude * (2.0 * std::f32::consts::PI * freq * t).sin();
                out_left[i] = sample;
                out_right[i] = sample;
            }
        }
    }
}

fn main() {
    println!("═══════════════════════════════════════════════════════════");
    println!("  MSMC v2.0: Rondo Form Example (ABACA)");
    println!("═══════════════════════════════════════════════════════════\n");

    // Step 1: Define themes using Flame IR
    println!("📝 Step 1: Defining Themes");
    let mut builder = RondoBuilder::new(120.0);
    builder
        .add_theme("A", 1, 8.0)  // A theme: 8 beats, node_id=1
        .add_theme("B", 2, 8.0)  // B theme: 8 beats, node_id=2
        .add_theme("C", 3, 8.0); // C theme: 8 beats, node_id=3
    
    println!("   ✓ Theme A: 8 beats (node_id=1)");
    println!("   ✓ Theme B: 8 beats (node_id=2)");
    println!("   ✓ Theme C: 8 beats (node_id=3)\n");

    // Step 2: Build Rondo form annotation
    println!("🎵 Step 2: Building Rondo Form (ABACA)");
    let form_annotation = builder.build_abaca();
    println!("   Form: {:?}", form_annotation.kind);
    println!("   Sequence: {:?}", form_annotation.sequence);
    println!("   Tempo: {} BPM\n", form_annotation.tempo_bpm);

    // Step 3: Convert to FormSpec
    println!("🔄 Step 3: Converting to FormSpec");
    let form_spec = form_annotation.to_form_spec();
    println!("   Sections: {}", form_spec.sections.len());
    println!("   Sequence length: {}", form_spec.sequence.len());
    for section in &form_spec.sections {
        println!("   - Section {}: {} beats, {} voices", 
                 section.name, section.duration_beats, section.voices.len());
    }
    println!();

    // Step 4: Build state machine
    println!("🤖 Step 4: Building State Machine");
    let state_machine = build_state_machine(&form_spec);
    println!("   Nodes: {}", state_machine.nodes.len());
    println!("   Transitions: {}", state_machine.transitions.len());
    println!("   Total duration: {} beats ({:.2} seconds)", 
             state_machine.total_duration_beats,
             state_machine.total_duration_beats * 60.0 / state_machine.clock.tempo_bpm);
    
    println!("\n   Node Timeline:");
    for (i, node) in state_machine.nodes.iter().enumerate() {
        println!("   [{:02}] Section '{}': beats {:.1} → {:.1}", 
                 i, node.section.name, node.start_beat, node.end_beat);
    }
    println!();

    // Step 5: Render to audio
    println!("🎧 Step 5: Rendering to Audio");
    let flame = FlameIR {};
    let backend = MockAudioBackend;
    let config = RenderConfig {
        sample_rate: 44100.0,
        num_channels: 2,
    };
    
    let wav_buffer = render_msmc_to_wav(&flame, &backend, &state_machine, &config);
    println!("   Sample rate: {} Hz", wav_buffer.sample_rate);
    println!("   Channels: {}", wav_buffer.num_channels);
    println!("   Total samples: {}", wav_buffer.samples.len() / wav_buffer.num_channels as usize);
    println!("   Duration: {:.2} seconds", 
             wav_buffer.samples.len() as f32 / (wav_buffer.sample_rate as f32 * wav_buffer.num_channels as f32));
    println!();

    // Step 6: Verify structure
    println!("✅ Step 6: Verification");
    println!("   Form is bounded: {}", state_machine.total_duration_beats > 0.0);
    println!("   No orphan sections: {}", state_machine.nodes.len() == form_spec.sequence.len());
    println!("   Valid transitions: {}", state_machine.transitions.len() == state_machine.nodes.len() - 1);
    
    // Display structure
    println!("\n📊 Musical Structure:");
    println!("   A (8 beats) → B (8 beats) → A (8 beats) → C (8 beats) → A (8 beats)");
    println!("   Total: 40 beats = 20 seconds @ 120 BPM");
    
    println!("\n═══════════════════════════════════════════════════════════");
    println!("✨ MSMC v2.0 Rondo Example Complete!");
    println!("═══════════════════════════════════════════════════════════\n");
}
