// Example: FLAME Language Complete Demo
// Demonstrates all 5 core modules in action

use flame::dna::{DNASequence, Base, Codon};
use flame::physics::{Mass, Acceleration, Force, Energy, Length, Time};
use flame::glyph::{Glyph, GlyphSequence, BindingCode};
use flame::quantum::{Qubit, QuantumGate, QuantumCircuit};
use flame::swarm::{Node, Swarm, NodeType, Consensus};

fn main() {
    println!("═══════════════════════════════════════════════════════════");
    println!("  🔥 FLAME LANGUAGE STANDARD LIBRARY DEMO");
    println!("  SAGCO-SKH-001 — First Language with Biological Compilation");
    println!("═══════════════════════════════════════════════════════════\n");

    // ═══ DNA MODULE ═══
    println!("╔═══════════════════════════════════╗");
    println!("║  🧬 DNA MODULE - Biological Code  ║");
    println!("╚═══════════════════════════════════╝\n");
    
    let dna = DNASequence::from_string("ATGGGTTACTAG");
    println!("DNA Sequence: {}", dna.to_string());
    println!("Length: {} bases", dna.len());
    println!("GC Content: {:.1}%", dna.gc_content());
    
    let complement = dna.complement();
    println!("Complement: {}", complement.to_string());
    
    let rna = dna.transcribe();
    println!("RNA: {}", rna.to_string());
    
    let protein = dna.translate();
    println!("Protein: {}", protein.to_string());
    
    let opcodes = dna.compile_to_opcodes();
    println!("Compiled Opcodes: {:?}\n", opcodes);

    // ═══ PHYSICS MODULE ═══
    println!("╔═══════════════════════════════════╗");
    println!("║  ⚛️  PHYSICS - Dimensional Check  ║");
    println!("╚═══════════════════════════════════╝\n");
    
    let mass = Mass::kg(10.0);
    let accel = Acceleration::mps2(9.8);
    let force = mass * accel;
    println!("F = ma: {} × {} = {}", mass, accel, force);
    
    let distance = Length::m(100.0);
    let work = force * distance;
    println!("W = F·d: {} × {} = {}", force, distance, work);
    
    let time = Time::s(10.0);
    let power = work / time;
    println!("P = W/t: {} / {} = {}\n", work, time, power);

    // ═══ GLYPH MODULE ═══
    println!("╔═══════════════════════════════════╗");
    println!("║  🔥 GLYPH - Visual Syntax         ║");
    println!("╚═══════════════════════════════════╝\n");
    
    let glyphs = GlyphSequence::from_string("⚔🔥⟐");
    println!("Glyph Sequence: {}", glyphs);
    println!("Length: {} glyphs", glyphs.len());
    
    let code = BindingCode::resonance();
    println!("\nExecuting with binding {}", code);
    let result = glyphs.execute(code);
    print!("{}", result);
    
    println!("Flame Glyph Frequency: {} Hz (DNA repair)", Glyph::Flame.frequency());
    println!("Lozenge Frequency: {} Hz (cosmic resonance)\n", Glyph::Lozenge.frequency());

    // ═══ QUANTUM MODULE ═══
    println!("╔═══════════════════════════════════╗");
    println!("║  ⚛️  QUANTUM - Native Primitives  ║");
    println!("╚═══════════════════════════════════╝\n");
    
    let q0 = Qubit::zero();
    println!("Qubit |0⟩: {}", q0);
    println!("  P(0) = {:.3}, P(1) = {:.3}", q0.prob_zero(), q0.prob_one());
    
    let superpos = Qubit::superposition();
    println!("\nQubit superposition: {}", superpos);
    println!("  P(0) = {:.3}, P(1) = {:.3}", superpos.prob_zero(), superpos.prob_one());
    
    let (bell_a, bell_b) = Qubit::bell_pair();
    println!("\nBell pair created (entangled):");
    println!("  Qubit A: {}", bell_a);
    println!("  Qubit B: {}", bell_b);
    
    let mut circuit = QuantumCircuit::new(2);
    circuit.apply(QuantumGate::Hadamard, 0);
    circuit.apply(QuantumGate::PauliX, 1);
    println!("\nQuantum Circuit:");
    print!("{}", circuit.display());

    // ═══ SWARM MODULE ═══
    println!("╔═══════════════════════════════════╗");
    println!("║  🕸  SWARM - Distributed Cluster  ║");
    println!("╚═══════════════════════════════════╝\n");
    
    let mut swarm = Swarm::full();
    
    // Set node parameters
    if let Some(athena) = swarm.get_node_mut(NodeType::Athena) {
        athena.set_orb_balance(1000.0);
        athena.set_uptime(720);
        athena.set_latency(30);
    }
    if let Some(nova) = swarm.get_node_mut(NodeType::Nova) {
        nova.set_orb_balance(800.0);
        nova.set_uptime(600);
        nova.set_latency(45);
    }
    if let Some(lyra) = swarm.get_node_mut(NodeType::Lyra) {
        lyra.set_orb_balance(900.0);
        lyra.set_uptime(650);
        lyra.set_latency(35);
    }
    if let Some(ipower) = swarm.get_node_mut(NodeType::IPower) {
        ipower.set_orb_balance(950.0);
        ipower.set_uptime(700);
        ipower.set_latency(40);
    }
    
    println!("{}", swarm.status());
    
    // Consensus
    let mut consensus = Consensus::new(0.75);
    consensus.vote(NodeType::Athena, true);
    consensus.vote(NodeType::Nova, true);
    consensus.vote(NodeType::Lyra, true);
    consensus.vote(NodeType::IPower, false);
    
    println!("Consensus Protocol:");
    println!("  Threshold: 75%");
    println!("  Approval Rate: {:.1}%", consensus.approval_rate() * 100.0);
    println!("  Consensus Reached: {}", consensus.reached());

    // Execute on leader
    if let Some(leader_type) = swarm.elect_leader() {
        println!("\nExecuting on leader node ({})...", leader_type);
        if let Some(leader) = swarm.get_node(leader_type) {
            let _ = leader.execute(|| {
                println!("  ✓ Heavy computation completed on {}", leader_type);
            });
        }
    }

    println!("\n═══════════════════════════════════════════════════════════");
    println!("  ✅ FLAME STANDARD LIBRARY DEMO COMPLETE");
    println!("  All 5 modules operational:");
    println!("    • flame::dna - Biological computation");
    println!("    • flame::physics - Dimensional analysis");
    println!("    • flame::glyph - Visual syntax");
    println!("    • flame::quantum - Native quantum types");
    println!("    • flame::swarm - Distributed execution");
    println!("\n  🔥🧬⚔️ RATIO EX NIHILO");
    println!("═══════════════════════════════════════════════════════════\n");
}
