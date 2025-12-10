//! # FLAME Glyph Module - Visual Syntax
//! 
//! This module provides 40+ visual symbols that ARE the syntax,
//! not just decorative elements. Each glyph is a first-class language construct.
//! 
//! ## Features
//! 
//! - 40+ operational glyphs
//! - Binding code system (numeric routing)
//! - Glyph-to-executable mapping
//! - Visual syntax parsing
//! - Temporal/spatial modifiers
//! 
//! ## Example
//! 
//! ```rust
//! use flame::glyph::{Glyph, GlyphSequence, BindingCode};
//! 
//! // Create glyph sequence
//! let seq = GlyphSequence::from_string("⚔🔥⟐");
//! 
//! // Execute with binding code
//! let code = BindingCode::new(999);
//! seq.execute(code);
//! ```

use std::fmt;
use std::collections::HashMap;

/// Core operational glyphs
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Glyph {
    // Command & Control
    Sword,              // ⚔ - Command marker
    Flame,              // 🔥 - Namespace/execution
    Lozenge,            // ⟐ - Temporal/spatial modifier
    Play,               // ▶ - Execution ready
    Shield,             // 🛡 - Protection/validation
    
    // Neural & Cognitive
    Brain,              // 🧠 - Right hemisphere (WSL/Linux)
    Eye,                // 👁 - Observer/monitor
    Lightning,          // ⚡ - High-speed execution
    Star,               // ⭐ - Priority marker
    Crystal,            // 💎 - Immutable state
    
    // Network & Distribution
    Globe,              // 🌐 - Network-aware context
    Satellite,          // 🛰 - Remote execution
    Chain,              // ⛓ - Linked operations
    Mesh,               // 🕸 - Distributed mesh
    Signal,             // 📡 - Broadcast operation
    
    // Quantum & Physics
    Atom,               // ⚛ - Quantum operation
    Wave,               // 〰 - Wave function
    Particle,           // • - Particle state
    Spin,               // ↻ - Spin operation
    Entangle,           // ⟺ - Entanglement
    
    // Biological
    DNA,                // 🧬 - DNA sequence
    Cell,               // 🦠 - Cellular operation
    Molecule,           // ⚗ - Chemical reaction
    Helix,              // ∿ - Helical structure
    Protein,            // 🔬 - Protein synthesis
    
    // Mathematical
    Infinity,           // ∞ - Infinite loop
    Delta,              // Δ - Change/difference
    Sigma,              // Σ - Summation
    Pi,                 // π - Pi constant
    Integral,           // ∫ - Integration
    
    // Geometric
    Circle,             // ○ - Cycle/loop
    Square,             // □ - Block/boundary
    Triangle,           // △ - Direction/flow
    Hexagon,            // ⬡ - 6-way branching
    Spiral,             // 🌀 - Recursive descent
    
    // Temporal
    Clock,              // 🕐 - Timestamp
    Hourglass,          // ⏳ - Delay/wait
    Calendar,           // 📅 - Schedule
    Stopwatch,          // ⏱ - Measure time
    Metronome,          // 🎵 - Periodic execution
    
    // State & Flow
    Lock,               // 🔒 - Locked state
    Unlock,             // 🔓 - Unlocked state
    Key,                // 🔑 - Authentication
    Gateway,            // 🚪 - Entry point
    Bridge,             // 🌉 - Connection
}

impl Glyph {
    /// Get Unicode character representation
    pub fn to_char(self) -> char {
        match self {
            Glyph::Sword => '⚔',
            Glyph::Flame => '🔥',
            Glyph::Lozenge => '⟐',
            Glyph::Play => '▶',
            Glyph::Shield => '🛡',
            Glyph::Brain => '🧠',
            Glyph::Eye => '👁',
            Glyph::Lightning => '⚡',
            Glyph::Star => '⭐',
            Glyph::Crystal => '💎',
            Glyph::Globe => '🌐',
            Glyph::Satellite => '🛰',
            Glyph::Chain => '⛓',
            Glyph::Mesh => '🕸',
            Glyph::Signal => '📡',
            Glyph::Atom => '⚛',
            Glyph::Wave => '〰',
            Glyph::Particle => '•',
            Glyph::Spin => '↻',
            Glyph::Entangle => '⟺',
            Glyph::DNA => '🧬',
            Glyph::Cell => '🦠',
            Glyph::Molecule => '⚗',
            Glyph::Helix => '∿',
            Glyph::Protein => '🔬',
            Glyph::Infinity => '∞',
            Glyph::Delta => 'Δ',
            Glyph::Sigma => 'Σ',
            Glyph::Pi => 'π',
            Glyph::Integral => '∫',
            Glyph::Circle => '○',
            Glyph::Square => '□',
            Glyph::Triangle => '△',
            Glyph::Hexagon => '⬡',
            Glyph::Spiral => '🌀',
            Glyph::Clock => '🕐',
            Glyph::Hourglass => '⏳',
            Glyph::Calendar => '📅',
            Glyph::Stopwatch => '⏱',
            Glyph::Metronome => '🎵',
            Glyph::Lock => '🔒',
            Glyph::Unlock => '🔓',
            Glyph::Key => '🔑',
            Glyph::Gateway => '🚪',
            Glyph::Bridge => '🌉',
        }
    }

    /// Parse glyph from character
    pub fn from_char(c: char) -> Option<Self> {
        match c {
            '⚔' => Some(Glyph::Sword),
            '🔥' => Some(Glyph::Flame),
            '⟐' => Some(Glyph::Lozenge),
            '▶' => Some(Glyph::Play),
            '🛡' => Some(Glyph::Shield),
            '🧠' => Some(Glyph::Brain),
            '👁' => Some(Glyph::Eye),
            '⚡' => Some(Glyph::Lightning),
            '⭐' => Some(Glyph::Star),
            '💎' => Some(Glyph::Crystal),
            '🌐' => Some(Glyph::Globe),
            '🛰' => Some(Glyph::Satellite),
            '⛓' => Some(Glyph::Chain),
            '🕸' => Some(Glyph::Mesh),
            '📡' => Some(Glyph::Signal),
            '⚛' => Some(Glyph::Atom),
            '〰' => Some(Glyph::Wave),
            '•' => Some(Glyph::Particle),
            '↻' => Some(Glyph::Spin),
            '⟺' => Some(Glyph::Entangle),
            '🧬' => Some(Glyph::DNA),
            '🦠' => Some(Glyph::Cell),
            '⚗' => Some(Glyph::Molecule),
            '∿' => Some(Glyph::Helix),
            '🔬' => Some(Glyph::Protein),
            'Δ' => Some(Glyph::Delta),
            'Σ' => Some(Glyph::Sigma),
            'π' => Some(Glyph::Pi),
            '∫' => Some(Glyph::Integral),
            '∞' => Some(Glyph::Infinity),
            '○' => Some(Glyph::Circle),
            '□' => Some(Glyph::Square),
            '△' => Some(Glyph::Triangle),
            '⬡' => Some(Glyph::Hexagon),
            '🌀' => Some(Glyph::Spiral),
            '🕐' => Some(Glyph::Clock),
            '⏳' => Some(Glyph::Hourglass),
            '📅' => Some(Glyph::Calendar),
            '⏱' => Some(Glyph::Stopwatch),
            '🎵' => Some(Glyph::Metronome),
            '🔒' => Some(Glyph::Lock),
            '🔓' => Some(Glyph::Unlock),
            '🔑' => Some(Glyph::Key),
            '🚪' => Some(Glyph::Gateway),
            '🌉' => Some(Glyph::Bridge),
            _ => None,
        }
    }

    /// Get semantic meaning
    pub fn meaning(self) -> &'static str {
        match self {
            Glyph::Sword => "Command marker",
            Glyph::Flame => "Execution namespace",
            Glyph::Lozenge => "Temporal/spatial modifier",
            Glyph::Play => "Ready for execution",
            Glyph::Shield => "Protection layer",
            Glyph::Brain => "Right hemisphere execution",
            Glyph::Eye => "Observation point",
            Glyph::Lightning => "High-speed path",
            Glyph::Star => "Priority flag",
            Glyph::Crystal => "Immutable binding",
            Glyph::Globe => "Network context",
            Glyph::Satellite => "Remote target",
            Glyph::Chain => "Sequential linking",
            Glyph::Mesh => "Distributed operation",
            Glyph::Signal => "Broadcast message",
            Glyph::Atom => "Quantum operation",
            Glyph::Wave => "Wave function collapse",
            Glyph::Particle => "Particle localization",
            Glyph::Spin => "Spin transformation",
            Glyph::Entangle => "Quantum entanglement",
            Glyph::DNA => "Biological sequence",
            Glyph::Cell => "Cellular computation",
            Glyph::Molecule => "Chemical transformation",
            Glyph::Helix => "Helical structure",
            Glyph::Protein => "Protein synthesis",
            Glyph::Infinity => "Infinite iteration",
            Glyph::Delta => "Differential change",
            Glyph::Sigma => "Summation accumulator",
            Glyph::Pi => "Pi constant",
            Glyph::Integral => "Integration operation",
            Glyph::Circle => "Cyclic loop",
            Glyph::Square => "Boundary block",
            Glyph::Triangle => "Directional flow",
            Glyph::Hexagon => "Six-way branch",
            Glyph::Spiral => "Recursive descent",
            Glyph::Clock => "Timestamp marker",
            Glyph::Hourglass => "Delay operation",
            Glyph::Calendar => "Scheduled execution",
            Glyph::Stopwatch => "Time measurement",
            Glyph::Metronome => "Periodic trigger",
            Glyph::Lock => "Locked state",
            Glyph::Unlock => "Unlocked state",
            Glyph::Key => "Authentication token",
            Glyph::Gateway => "Entry point",
            Glyph::Bridge => "Connection bridge",
        }
    }

    /// Get associated frequency (Hz) for resonance
    pub fn frequency(self) -> f64 {
        match self {
            Glyph::Lozenge => 432.0,    // Cosmic resonance
            Glyph::Flame => 528.0,       // DNA repair frequency
            Glyph::Sword => 639.0,       // Connection frequency
            Glyph::Brain => 741.0,       // Awakening frequency
            Glyph::Crystal => 852.0,     // Spiritual frequency
            Glyph::Infinity => 963.0,    // Divine frequency
            _ => 440.0,                  // Standard A4
        }
    }
}

impl fmt::Display for Glyph {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_char())
    }
}

/// Binding code for routing glyphs to executables
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct BindingCode(u16);

impl BindingCode {
    pub fn new(code: u16) -> Self {
        Self(code)
    }

    /// Sacred binding codes
    pub fn resonance() -> Self { Self(999) }
    pub fn fixer() -> Self { Self(777) }
    pub fn sovereign() -> Self { Self(137) }
    pub fn genesis() -> Self { Self(3449) }
    
    pub fn value(self) -> u16 {
        self.0
    }
}

impl fmt::Display for BindingCode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}]", self.0)
    }
}

/// A sequence of glyphs forming an executable expression
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GlyphSequence {
    glyphs: Vec<Glyph>,
}

impl GlyphSequence {
    /// Create empty sequence
    pub fn new() -> Self {
        Self { glyphs: Vec::new() }
    }

    /// Parse from string
    pub fn from_string(s: &str) -> Self {
        let glyphs = s.chars()
            .filter_map(Glyph::from_char)
            .collect();
        Self { glyphs }
    }

    /// Add glyph
    pub fn push(&mut self, glyph: Glyph) {
        self.glyphs.push(glyph);
    }

    /// Get length
    pub fn len(&self) -> usize {
        self.glyphs.len()
    }

    /// Check if empty
    pub fn is_empty(&self) -> bool {
        self.glyphs.is_empty()
    }

    /// Convert to string
    pub fn to_string(&self) -> String {
        self.glyphs.iter().map(|g| g.to_char()).collect()
    }

    /// Execute sequence (returns semantic description)
    pub fn execute(&self, binding: BindingCode) -> String {
        let mut result = format!("Executing {} with binding {}\n", self.to_string(), binding);
        
        for glyph in &self.glyphs {
            result.push_str(&format!("  {} - {}\n", glyph, glyph.meaning()));
        }
        
        result.push_str("Neural Sync complete. Resonance achieved.\n");
        result
    }
}

impl Default for GlyphSequence {
    fn default() -> Self {
        Self::new()
    }
}

impl fmt::Display for GlyphSequence {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

/// Glyph map - associates glyph patterns with executables
#[derive(Debug, Clone)]
pub struct GlyphMap {
    mappings: HashMap<String, String>,
}

impl GlyphMap {
    /// Create new map
    pub fn new() -> Self {
        Self {
            mappings: HashMap::new(),
        }
    }

    /// Register mapping
    pub fn register(&mut self, pattern: &str, executable: String) {
        self.mappings.insert(pattern.to_string(), executable);
    }

    /// Resolve pattern to executable
    pub fn resolve(&self, pattern: &str) -> Option<&String> {
        self.mappings.get(pattern)
    }

    /// Create default FLAME mappings
    pub fn with_defaults() -> Self {
        let mut map = Self::new();
        
        // Core FLAME operations
        map.register("⚔🔥", "flame_core_execute".to_string());
        map.register("🔥⟐", "flame_temporal_modifier".to_string());
        map.register("🧠🌐", "flame_network_sync".to_string());
        map.register("⚡💎", "flame_immutable_fast".to_string());
        map.register("🧬🔬", "flame_dna_synthesis".to_string());
        map.register("⚛∞", "flame_quantum_entangle".to_string());
        map.register("△▶", "flame_flow_execute".to_string());
        map.register("🔒🔑", "flame_auth_unlock".to_string());
        
        map
    }
}

impl Default for GlyphMap {
    fn default() -> Self {
        Self::with_defaults()
    }
}

/// Glyph parser for FLAME expressions
pub struct GlyphParser {
    map: GlyphMap,
}

impl GlyphParser {
    /// Create parser with map
    pub fn new(map: GlyphMap) -> Self {
        Self { map }
    }

    /// Parse and resolve expression
    pub fn parse(&self, expr: &str) -> Result<String, String> {
        // Extract glyph pattern
        let sequence = GlyphSequence::from_string(expr);
        let pattern = sequence.to_string();
        
        // Resolve to executable
        self.map.resolve(&pattern)
            .cloned()
            .ok_or_else(|| format!("Unknown glyph pattern: {}", pattern))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_glyph_parsing() {
        assert_eq!(Glyph::from_char('⚔'), Some(Glyph::Sword));
        assert_eq!(Glyph::from_char('🔥'), Some(Glyph::Flame));
    }

    #[test]
    fn test_glyph_sequence() {
        let seq = GlyphSequence::from_string("⚔🔥");
        assert_eq!(seq.len(), 2);
        assert_eq!(seq.to_string(), "⚔🔥");
    }

    #[test]
    fn test_binding_code() {
        let code = BindingCode::resonance();
        assert_eq!(code.value(), 999);
    }

    #[test]
    fn test_glyph_map() {
        let map = GlyphMap::with_defaults();
        assert!(map.resolve("⚔🔥").is_some());
    }
}
