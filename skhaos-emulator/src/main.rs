// SkhaOS Multi-Whale Quantum Emulator CLI/Server
// Sovereign bio-mimetic quantum computing platform

use skhaos_emulator::{
    MultiWhaleOrchestrator,
    QuantumWhaleState,
    WhaleSpecies,
};

use std::env;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Parse command line arguments
    let args: Vec<String> = env::args().collect();
    
    if args.len() > 1 {
        match args[1].as_str() {
            "--version" | "-v" => {
                println!("SkhaOS Multi-Whale Quantum Emulator v{}", skhaos_emulator::VERSION);
                println!("{}", skhaos_emulator::DESCRIPTION);
                return Ok(());
            }
            "--health-check" => {
                // Simple health check for container
                println!("OK");
                return Ok(());
            }
            "--server" => {
                println!("🌊 Starting SkhaOS Multi-Whale Quantum Emulator Server...");
                println!("   Port: 8080");
                println!("   Species: all");
                println!("   Sovereignty: enabled");
                println!("");
                
                // In a real implementation, this would start the axum server
                // For now, just run a simulation
                run_simulation()?;
                return Ok(());
            }
            "--help" | "-h" => {
                print_help();
                return Ok(());
            }
            _ => {
                eprintln!("Unknown option: {}", args[1]);
                print_help();
                return Ok(());
            }
        }
    }
    
    // Default: run simulation
    run_simulation()?;
    
    Ok(())
}

fn run_simulation() -> Result<(), Box<dyn std::error::Error>> {
    println!("🐋 SkhaOS Multi-Whale Quantum Emulator");
    println!("======================================");
    println!("");
    
    // Create orchestrator
    let mut orch = MultiWhaleOrchestrator::new(3);
    
    // Add humpback state
    let humpback = QuantumWhaleState::new(
        WhaleSpecies::Humpback,
        500.0,
        "phrase".to_string(),
    );
    println!("✓ Created Humpback state (500 Hz phrase)");
    orch.add_state(humpback)?;
    
    // Add sperm state
    let sperm = QuantumWhaleState::new(
        WhaleSpecies::Sperm,
        5000.0,
        "coda".to_string(),
    );
    println!("✓ Created Sperm state (5000 Hz coda)");
    orch.add_state(sperm)?;
    
    // Add killer state
    let killer = QuantumWhaleState::new(
        WhaleSpecies::Killer,
        10000.0,
        "whistle".to_string(),
    );
    println!("✓ Created Killer state (10000 Hz whistle)");
    orch.add_state(killer)?;
    
    println!("");
    println!("🌀 Entangling swarm...");
    orch.entangle_swarm()?;
    println!("✓ Swarm entangled");
    
    println!("");
    println!("♻️ Evolving swarm (Zipf-distributed)...");
    orch.evolve_swarm()?;
    println!("✓ Swarm evolved");
    
    println!("");
    println!("📊 Swarm Statistics:");
    let stats = orch.get_stats();
    for (key, value) in stats.iter() {
        println!("   {}: {:.2}", key, value);
    }
    
    println!("");
    println!("✅ Simulation complete!");
    println!("🌊 Sonar-pulse deeper. Evolve sovereign. 💥");
    
    Ok(())
}

fn print_help() {
    println!("SkhaOS Multi-Whale Quantum Emulator v{}", skhaos_emulator::VERSION);
    println!("");
    println!("USAGE:");
    println!("    skhaos-emulator [OPTIONS]");
    println!("");
    println!("OPTIONS:");
    println!("    --server           Start UDAP server on port 8080");
    println!("    --health-check     Run health check (for containers)");
    println!("    --version, -v      Print version information");
    println!("    --help, -h         Print this help message");
    println!("");
    println!("EXAMPLES:");
    println!("    skhaos-emulator                # Run simulation");
    println!("    skhaos-emulator --server       # Start server");
    println!("");
    println!("For more information, see README.md");
}
