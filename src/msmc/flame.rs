// flame.rs - Flame IR Integration Module
// Provides integration between FlameLang and MSMC Backend

use crate::backend::{FormSpec, FormKind, SectionSpec, SectionId, VoiceSpec, VoiceId};

/// Represents a theme in the Flame IR
#[derive(Debug, Clone)]
pub struct FlameTheme {
    pub name: String,
    pub node_id: u64,
    pub duration_beats: f32,
}

/// Represents form annotations in Flame IR
#[derive(Debug, Clone)]
pub struct FlameFormAnnotation {
    pub kind: FormKind,
    pub themes: Vec<FlameTheme>,
    pub sequence: Vec<String>,  // e.g., ["A", "B", "A", "C", "A"]
    pub tempo_bpm: f32,
}

impl FlameFormAnnotation {
    /// Convert a FlameFormAnnotation into a FormSpec for MSMC processing
    pub fn to_form_spec(&self) -> FormSpec {
        // Create sections from themes
        let mut sections = Vec::new();
        let mut theme_map = std::collections::HashMap::new();
        
        for (idx, theme) in self.themes.iter().enumerate() {
            let section_id = SectionId(idx as u32);
            theme_map.insert(theme.name.clone(), section_id);
            
            // Create a single voice for each theme
            let voice = VoiceSpec {
                id: VoiceId(0),
                flame_node_id: theme.node_id,
                time_offset_beats: 0.0,
                gain: 1.0,
            };
            
            sections.push(SectionSpec {
                id: section_id,
                name: theme.name.clone(),
                duration_beats: theme.duration_beats,
                voices: vec![voice],
            });
        }
        
        // Map sequence names to section IDs
        let sequence: Vec<SectionId> = self.sequence
            .iter()
            .filter_map(|name| theme_map.get(name).copied())
            .collect();
        
        FormSpec {
            kind: self.kind.clone(),
            sections,
            sequence,
            tempo_bpm: self.tempo_bpm,
        }
    }
}

/// Builder for constructing Rondo forms
pub struct RondoBuilder {
    themes: Vec<FlameTheme>,
    tempo_bpm: f32,
}

impl RondoBuilder {
    pub fn new(tempo_bpm: f32) -> Self {
        Self {
            themes: Vec::new(),
            tempo_bpm,
        }
    }
    
    pub fn add_theme(&mut self, name: &str, node_id: u64, duration_beats: f32) -> &mut Self {
        self.themes.push(FlameTheme {
            name: name.to_string(),
            node_id,
            duration_beats,
        });
        self
    }
    
    /// Build a standard Rondo form: ABACA
    pub fn build_abaca(&self) -> FlameFormAnnotation {
        FlameFormAnnotation {
            kind: FormKind::Rondo,
            themes: self.themes.clone(),
            sequence: vec!["A".to_string(), "B".to_string(), "A".to_string(), "C".to_string(), "A".to_string()],
            tempo_bpm: self.tempo_bpm,
        }
    }
    
    /// Build an extended Rondo form: ABACABA
    pub fn build_abacaba(&self) -> FlameFormAnnotation {
        FlameFormAnnotation {
            kind: FormKind::Rondo,
            themes: self.themes.clone(),
            sequence: vec![
                "A".to_string(), "B".to_string(), "A".to_string(), 
                "C".to_string(), "A".to_string(), "B".to_string(), "A".to_string()
            ],
            tempo_bpm: self.tempo_bpm,
        }
    }
    
    /// Build a custom sequence
    pub fn build_custom(&self, sequence: Vec<String>) -> FlameFormAnnotation {
        FlameFormAnnotation {
            kind: FormKind::Rondo,
            themes: self.themes.clone(),
            sequence,
            tempo_bpm: self.tempo_bpm,
        }
    }
}

/// Builder for constructing Canon forms
pub struct CanonBuilder {
    subject: Option<FlameTheme>,
    num_voices: u32,
    delay_beats: f32,
    tempo_bpm: f32,
}

impl CanonBuilder {
    pub fn new(tempo_bpm: f32) -> Self {
        Self {
            subject: None,
            num_voices: 2,
            delay_beats: 4.0,
            tempo_bpm,
        }
    }
    
    pub fn set_subject(&mut self, name: &str, node_id: u64, duration_beats: f32) -> &mut Self {
        self.subject = Some(FlameTheme {
            name: name.to_string(),
            node_id,
            duration_beats,
        });
        self
    }
    
    pub fn set_voices(&mut self, num_voices: u32) -> &mut Self {
        self.num_voices = num_voices;
        self
    }
    
    pub fn set_delay(&mut self, delay_beats: f32) -> &mut Self {
        self.delay_beats = delay_beats;
        self
    }
    
    pub fn build(&self) -> FlameFormAnnotation {
        let subject = self.subject.as_ref()
            .expect("Canon must have a subject theme");
        
        // For a canon, we create a single section with multiple voices
        // Each voice plays the same theme but offset in time
        let themes = vec![subject.clone()];
        let sequence = vec![subject.name.clone()];
        
        FlameFormAnnotation {
            kind: FormKind::Canon,
            themes,
            sequence,
            tempo_bpm: self.tempo_bpm,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rondo_builder_abaca() {
        let mut builder = RondoBuilder::new(120.0);
        builder
            .add_theme("A", 1, 8.0)
            .add_theme("B", 2, 8.0)
            .add_theme("C", 3, 8.0);
        
        let form = builder.build_abaca();
        assert_eq!(form.kind, FormKind::Rondo);
        assert_eq!(form.sequence.len(), 5);
        assert_eq!(form.sequence, vec!["A", "B", "A", "C", "A"]);
    }
    
    #[test]
    fn test_flame_annotation_to_form_spec() {
        let mut builder = RondoBuilder::new(120.0);
        builder
            .add_theme("A", 1, 8.0)
            .add_theme("B", 2, 8.0);
        
        let annotation = builder.build_custom(vec!["A".to_string(), "B".to_string(), "A".to_string()]);
        let form_spec = annotation.to_form_spec();
        
        assert_eq!(form_spec.kind, FormKind::Rondo);
        assert_eq!(form_spec.sections.len(), 2);
        assert_eq!(form_spec.sequence.len(), 3);
        assert_eq!(form_spec.tempo_bpm, 120.0);
    }
    
    #[test]
    fn test_canon_builder() {
        let mut builder = CanonBuilder::new(120.0);
        builder
            .set_subject("Subject", 1, 16.0)
            .set_voices(3)
            .set_delay(4.0);
        
        let form = builder.build();
        assert_eq!(form.kind, FormKind::Canon);
        assert_eq!(form.themes.len(), 1);
    }
}
