// FlameLang DSL: Domain-Specific Language for Whale Pattern Compilation
// Compiles UDAP URIs to executable pattern simulation code

// Grammar Definition
grammar WhaleDSL {
    // Top-level URI structure
    uri := "skhaos://" domain "/" species "/" pattern query?
    
    domain := "whale"
    
    species := "humpback" | "sperm" | "killer" | "hybrid"
    
    pattern := identifier
    
    query := "?" param ("&" param)*
    
    param := key "=" value
    
    key := identifier
    
    value := number | boolean | identifier
    
    identifier := [a-zA-Z_][a-zA-Z0-9_]*
    
    number := [0-9]+ ("." [0-9]+)?
    
    boolean := "true" | "false"
}

// Compilation Rules
compile_rules {
    // Humpback patterns
    rule "humpback/theme" {
        input: hz, theme?, zipf?, rubato?, duration?
        output: HumpbackTheme {
            level: Theme,
            frequency_range: (hz * 0.4, hz * 2.0),
            zipf_rank: theme ?? 1,
            duration_sec: duration ?? 180.0
        }
        quantum_map: "theme_entanglement"
    }
    
    rule "humpback/song" {
        input: hz, duration
        output: HumpbackTheme {
            level: Song,
            frequency_range: (20.0, 4000.0),
            duration_sec: duration
        }
        quantum_map: "recursive_hierarchy"
    }
    
    // Sperm patterns
    rule "sperm/coda" {
        input: clicks, tempo, hz, rubato?, ornament?
        output: SpermCoda {
            click_count: clicks,
            tempo: parse_tempo(tempo),
            frequency_hz: hz * 1000.0,
            rubato: rubato ?? false,
            ornamentation: ornament ?? 0
        }
        quantum_map: "phonetic_alphabet"
    }
    
    rule "sperm/vowel" {
        input: a?, i?, hz
        output: SpermCoda {
            vowel_formant: select_vowel(a, i),
            frequency_hz: hz * 1000.0
        }
        quantum_map: "dialogue_coarticulation"
    }
    
    // Killer patterns
    rule "killer/whistle" {
        input: dialect, pod?, hz
        output: KillerDialectCall {
            call_type: Whistle,
            pod: parse_pod(dialect, pod),
            frequency_hz: hz * 1000.0
        }
        quantum_map: "pod_cohesion"
    }
    
    rule "killer/resident" {
        input: bigg, hz
        output: KillerDialectCall {
            ecotype: if bigg then Biggs else Resident,
            frequency_hz: hz * 1000.0
        }
        quantum_map: "cultural_divergence"
    }
    
    // Hybrid patterns
    rule "hybrid/hump_sperm" {
        input: hz
        output: QuantumWhaleState {
            species: Hybrid([Humpback, Sperm]),
            frequency_hz: hz,
            entanglement_depth: 1
        }
        quantum_map: "theme_coda_link"
    }
    
    rule "hybrid/validate" {
        input: hz
        output: ValidationRequest {
            frequency_hz: hz,
            check_all_species: true
        }
        quantum_map: "schema_evolution"
    }
}

// Helper Functions
function parse_tempo(tempo_str: string) -> Tempo {
    match tempo_str {
        "slow" | "s" => Tempo::Slow,
        "medium" | "mid" | "m" => Tempo::Medium,
        "fast" | "f" => Tempo::Fast,
        _ => Tempo::Medium  // default
    }
}

function parse_pod(dialect: string, pod: string?) -> PodIdentity {
    match (dialect, pod) {
        ("J", _) => PodIdentity::J,
        ("K", _) => PodIdentity::K,
        ("L", _) => PodIdentity::L,
        ("Northern", Some(clan)) => PodIdentity::Northern(clan),
        ("Biggs", Some(id)) => PodIdentity::Biggs(id),
        _ => PodIdentity::Unknown
    }
}

function select_vowel(a: bool?, i: bool?) -> VowelFormant {
    match (a, i) {
        (Some(true), _) => VowelFormant::A,
        (_, Some(true)) => VowelFormant::I,
        _ => VowelFormant::Neutral
    }
}

// Code Generation Templates
templates {
    template rust_code {
        "
        // Auto-generated from UDAP URI: {{uri}}
        let pattern = {{pattern_type}}::new({{params}});
        pattern.validate_frequency()?;
        let simulation = pattern.simulate_pattern();
        // Quantum mapping: {{quantum_map}}
        "
    }
    
    template json_output {
        {
            "uri": "{{uri}}",
            "species": "{{species}}",
            "pattern": "{{pattern}}",
            "quantum_mapping": "{{quantum_map}}",
            "frequency_hz": {{hz}},
            "parameters": {{params_json}}
        }
    }
}

// Optimization Passes
optimizations {
    // Merge adjacent frequency operations
    pass merge_frequencies {
        pattern: freq_adjust(freq_adjust(x, a), b)
        replace: freq_adjust(x, a + b)
    }
    
    // Precompute constant Zipf ranks
    pass precompute_zipf {
        pattern: zipf_probability(constant_rank)
        replace: constant(1.0 / rank)
    }
    
    // Inline small pattern functions
    pass inline_patterns {
        threshold: 10 instructions
        inline: generate_clicks, formant_frequencies
    }
}

// Type System
types {
    Frequency := Hz(f64) | Symbolic(f64)
    Duration := Seconds(f64) | Samples(u64)
    Pattern := Humpback | Sperm | Killer | Hybrid
    QuantumMap := String  // Quantum analog identifier
}

// Error Handling
errors {
    InvalidFrequency(species, hz) := "Frequency {hz} Hz invalid for {species}"
    InvalidParameter(param, value) := "Parameter {param} has invalid value {value}"
    MissingRequired(param) := "Required parameter {param} is missing"
    CompilationFailed(reason) := "Compilation failed: {reason}"
}

// Examples
examples {
    // Humpback theme compilation
    input: "skhaos://whale/humpback/theme?hz=500&theme=1"
    output: {
        code: "HumpbackTheme::new(SongLevel::Theme, 200.0, 1000.0, 180.0)",
        quantum: "theme_entanglement"
    }
    
    // Sperm coda compilation
    input: "skhaos://whale/sperm/coda?clicks=10&tempo=mid&hz=5"
    output: {
        code: "SpermCoda::new(10, Rhythm::Regular, Tempo::Medium)",
        quantum: "phonetic_alphabet"
    }
    
    // Killer dialect compilation
    input: "skhaos://whale/killer/whistle?dialect=J&hz=5"
    output: {
        code: "KillerDialectCall::new(CallType::Whistle, PodIdentity::J, Ecotype::Resident)",
        quantum: "pod_cohesion"
    }
}
