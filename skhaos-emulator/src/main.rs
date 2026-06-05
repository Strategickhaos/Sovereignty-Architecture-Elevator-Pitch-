// BPEC Command Line Interface
// Bio-Physics Entanglement Compiler main executable

use skhaos_emulator::{BPECCompiler, UDAPBioParser, VERSION};
use std::env;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        print_usage();
        process::exit(1);
    }

    let command = &args[1];

    match command.as_str() {
        "version" | "-v" | "--version" => {
            println!("BPEC v{} - Bio-Physics Entanglement Compiler", VERSION);
            println!("INVENTION_074 - Strategickhaos Sovereignty Architecture");
        }
        "compile" => {
            if args.len() < 3 {
                eprintln!("Error: 'compile' requires a URI argument");
                print_usage();
                process::exit(1);
            }
            compile_uri(&args[2]);
        }
        "parse" => {
            if args.len() < 3 {
                eprintln!("Error: 'parse' requires a URI argument");
                print_usage();
                process::exit(1);
            }
            parse_uri(&args[2]);
        }
        "analyze-zipf" => {
            if args.len() < 3 {
                eprintln!("Error: 'analyze-zipf' requires data");
                print_usage();
                process::exit(1);
            }
            analyze_zipf(&args[2]);
        }
        "dolphin-whistle" => {
            if args.len() < 4 {
                eprintln!("Error: 'dolphin-whistle' requires frequency and pod_id");
                print_usage();
                process::exit(1);
            }
            dolphin_whistle(&args[2], &args[3]);
        }
        "help" | "-h" | "--help" => {
            print_usage();
        }
        _ => {
            eprintln!("Error: Unknown command '{}'", command);
            print_usage();
            process::exit(1);
        }
    }
}

fn print_usage() {
    println!("BPEC - Bio-Physics Entanglement Compiler");
    println!("\nUsage: bpec <command> [arguments]");
    println!("\nCommands:");
    println!("  version                          Show version information");
    println!("  compile <uri>                    Compile bio-physics URI to bytes");
    println!("  parse <uri>                      Parse and display URI components");
    println!("  analyze-zipf <data>              Analyze Zipf distribution");
    println!("  dolphin-whistle <hz> <pod_id>    Generate dolphin signature whistle");
    println!("  help                             Show this help message");
    println!("\nExamples:");
    println!("  bpec compile 'skhaos://bio/zipf/unit?rank=1&hz=20'");
    println!("  bpec compile 'skhaos://bio/dolphin/whistle?signature=true&hz=10'");
    println!("  bpec compile 'skhaos://bio/physics/rondo?law=conservation&hz=10'");
    println!("  bpec parse 'skhaos://bio/zipf/unit?rank=5&hz=100'");
    println!("  bpec dolphin-whistle 15.0 pod_alpha");
}

fn compile_uri(uri: &str) {
    let compiler = BPECCompiler::new();
    
    match compiler.compile(uri) {
        Ok(bytes) => {
            println!("✓ Compiled successfully");
            println!("URI: {}", uri);
            println!("Output size: {} bytes", bytes.len());
            println!("First 32 bytes (hex): {}", hex_preview(&bytes, 32));
        }
        Err(e) => {
            eprintln!("✗ Compilation failed: {}", e);
            process::exit(1);
        }
    }
}

fn parse_uri(uri: &str) {
    match UDAPBioParser::parse(uri) {
        Ok(bio_uri) => {
            println!("✓ Parsed successfully");
            println!("Scheme: {}", bio_uri.scheme);
            println!("Domain: {}", bio_uri.domain);
            println!("Resource: {}", bio_uri.resource);
            println!("Parameters:");
            for (key, value) in &bio_uri.params {
                println!("  {} = {}", key, value);
            }
            
            // Show domain-specific info
            if bio_uri.is_zipf() {
                if let Some(rank) = bio_uri.zipf_rank() {
                    println!("Zipf rank: {}", rank);
                }
            } else if bio_uri.is_dolphin() {
                if bio_uri.is_signature() {
                    println!("Type: Signature whistle");
                }
                if let Some(burst) = bio_uri.burst_count() {
                    println!("Burst count: {}", burst);
                }
            } else if bio_uri.is_physics() {
                if let Some(law) = bio_uri.physics_law() {
                    println!("Physics law: {}", law);
                }
            }
            
            if let Some(hz) = bio_uri.frequency_hz() {
                println!("Frequency: {} Hz", hz);
            }
        }
        Err(e) => {
            eprintln!("✗ Parse failed: {}", e);
            process::exit(1);
        }
    }
}

fn analyze_zipf(data_str: &str) {
    use skhaos_emulator::ZipfAnalyzer;
    
    let data = data_str.as_bytes();
    let analyzer = ZipfAnalyzer::new();
    
    let ranks = analyzer.rank_units(data);
    let coefficient = analyzer.zipf_coefficient(data);
    
    println!("✓ Zipf analysis complete");
    println!("Data size: {} bytes", data.len());
    println!("Unique units: {}", ranks.len());
    println!("Zipf coefficient: {:.4} (1.0 = perfect fit)", coefficient);
    println!("\nTop 10 ranked units:");
    
    for (rank, unit) in ranks.iter().take(10) {
        let expected_freq = analyzer.zipf_frequency(*rank);
        println!("  Rank {}: {} (expected freq: {:.4})", rank, hex_preview(&unit, 4), expected_freq);
    }
}

fn dolphin_whistle(hz_str: &str, pod_id: &str) {
    use skhaos_emulator::DolphinComm;
    
    let hz: f64 = match hz_str.parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("✗ Invalid frequency: {}", hz_str);
            process::exit(1);
        }
    };
    
    let comm = DolphinComm::new();
    let whistle = comm.signature_whistle(hz, pod_id);
    
    println!("✓ Generated dolphin signature whistle");
    println!("Frequency: {} Hz", whistle.frequency_hz);
    println!("Pod ID: {}", whistle.pod_id);
    println!("Duration: {} ms", whistle.duration_ms);
    println!("Pattern size: {} bytes", whistle.pattern.len());
    println!("Pattern preview (hex): {}", hex_preview(&whistle.to_bytes(), 32));
}

fn hex_preview(bytes: &[u8], max_len: usize) -> String {
    bytes
        .iter()
        .take(max_len)
        .map(|b| format!("{:02x}", b))
        .collect::<Vec<String>>()
        .join(" ")
}
