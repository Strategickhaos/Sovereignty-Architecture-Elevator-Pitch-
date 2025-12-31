// Sperm Whale Coda Module
// Phonetic alphabet with rhythm/tempo/rubato/ornamentation
// Frequency range: 1-30 kHz (clicks), 200-2000 Hz (creaks)
// Combinatorial gates with vowel-like formants

use std::collections::HashMap;

/// Rhythm pattern for sperm whale codas
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Rhythm {
    Regular,    // Evenly spaced clicks
    Irregular,  // Variable inter-click intervals
    Accelerando, // Speeding up (creak)
    Ritardando, // Slowing down
}

/// Tempo for coda sequences
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Tempo {
    Slow,   // < 0.5 clicks/sec
    Medium, // 0.5-2 clicks/sec
    Fast,   // > 2 clicks/sec
}

/// Vowel-like formants in sperm whale dialogues
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VowelFormant {
    A, // Low frequency emphasis
    I, // High frequency emphasis
    Neutral,
}

/// Sperm whale phonetic coda
#[derive(Debug, Clone)]
pub struct SpermCoda {
    pub click_count: usize,        // 3-40 clicks typical
    pub rhythm: Rhythm,
    pub tempo: Tempo,
    pub rubato: bool,              // Expressive timing variation
    pub ornamentation: usize,      // Extra clicks (0-3)
    pub vowel_formant: VowelFormant,
    pub frequency_hz: f64,         // Peak frequency
}

impl SpermCoda {
    /// Create a new sperm coda
    pub fn new(click_count: usize, rhythm: Rhythm, tempo: Tempo) -> Self {
        Self {
            click_count,
            rhythm,
            tempo,
            rubato: false,
            ornamentation: 0,
            vowel_formant: VowelFormant::Neutral,
            frequency_hz: 15000.0, // Default 15 kHz
        }
    }

    /// Validate coda parameters
    pub fn validate(&self) -> Result<(), String> {
        if self.click_count < 3 || self.click_count > 40 {
            return Err(format!("Click count {} outside typical range [3-40]", self.click_count));
        }
        
        if self.frequency_hz < 1.0 || self.frequency_hz > 30000.0 {
            return Err(format!("Frequency {} Hz outside range [1-30000 Hz]", self.frequency_hz));
        }
        
        Ok(())
    }

    /// Calculate combinatorial complexity (phonetic alphabet size)
    pub fn combinatorial_complexity(&self) -> usize {
        let rhythm_variants = 4; // Regular, Irregular, Accelerando, Ritardando
        let tempo_variants = 3;  // Slow, Medium, Fast
        let rubato_variants = 2; // With/without
        let ornament_variants = 4; // 0-3 extra clicks
        let vowel_variants = 3;  // A, I, Neutral
        
        rhythm_variants * tempo_variants * rubato_variants * ornament_variants * vowel_variants
    }

    /// Generate click sequence with timing
    pub fn generate_clicks(&self) -> Vec<f64> {
        let mut clicks = Vec::new();
        let base_interval = match self.tempo {
            Tempo::Slow => 2.0,   // 2 seconds between clicks
            Tempo::Medium => 0.5, // 0.5 seconds
            Tempo::Fast => 0.1,   // 0.1 seconds
        };

        let mut time = 0.0;
        for i in 0..self.click_count {
            let interval = match self.rhythm {
                Rhythm::Regular => base_interval,
                Rhythm::Irregular => base_interval * (1.0 + (i % 3) as f64 * 0.3),
                Rhythm::Accelerando => base_interval * (1.0 - i as f64 / self.click_count as f64 * 0.5),
                Rhythm::Ritardando => base_interval * (1.0 + i as f64 / self.click_count as f64 * 0.5),
            };

            let rubato_adjust = if self.rubato {
                (i as f64 * 0.1).sin() * 0.2 // +/- 20% variation
            } else {
                0.0
            };

            time += interval * (1.0 + rubato_adjust);
            clicks.push(time);
        }

        // Add ornamentation clicks at end
        for j in 0..self.ornamentation {
            time += 0.05; // Very short interval for ornaments
            clicks.push(time);
        }

        clicks
    }

    /// Simulate vowel formant frequencies
    pub fn formant_frequencies(&self) -> (f64, f64) {
        match self.vowel_formant {
            VowelFormant::A => (700.0, 1200.0),   // Low F1, mid F2
            VowelFormant::I => (300.0, 2300.0),   // Very low F1, high F2
            VowelFormant::Neutral => (500.0, 1500.0), // Mid F1, mid F2
        }
    }

    /// Encode coda as phonetic identifier string
    pub fn phonetic_id(&self) -> String {
        let rhythm_code = match self.rhythm {
            Rhythm::Regular => "R",
            Rhythm::Irregular => "I",
            Rhythm::Accelerando => "A",
            Rhythm::Ritardando => "D",
        };
        
        let tempo_code = match self.tempo {
            Tempo::Slow => "S",
            Tempo::Medium => "M",
            Tempo::Fast => "F",
        };
        
        let rubato_code = if self.rubato { "r" } else { "" };
        let vowel_code = match self.vowel_formant {
            VowelFormant::A => "a",
            VowelFormant::I => "i",
            VowelFormant::Neutral => "n",
        };
        
        format!("{}{}{}{:02}o{}{}", 
            rhythm_code, tempo_code, rubato_code, 
            self.click_count, self.ornamentation, vowel_code)
    }
}

/// Sperm whale phonetic alphabet simulator
pub struct SpermPhoneticAlphabet {
    codas: Vec<SpermCoda>,
    clan: String,
}

impl SpermPhoneticAlphabet {
    /// Create new alphabet for a whale clan
    pub fn new(clan: String) -> Self {
        Self {
            codas: Vec::new(),
            clan,
        }
    }

    /// Add coda to alphabet
    pub fn add_coda(&mut self, coda: SpermCoda) -> Result<(), String> {
        coda.validate()?;
        self.codas.push(coda);
        Ok(())
    }

    /// Generate all possible codas (combinatorial explosion)
    pub fn generate_full_alphabet(&mut self) -> Result<(), String> {
        // Generate subset of 156+ distinct codas
        let click_counts = vec![5, 10, 15, 20];
        let rhythms = vec![Rhythm::Regular, Rhythm::Irregular];
        let tempos = vec![Tempo::Slow, Tempo::Medium, Tempo::Fast];
        let rubatos = vec![false, true];
        let ornaments = vec![0, 1];
        let vowels = vec![VowelFormant::A, VowelFormant::I, VowelFormant::Neutral];

        for &clicks in &click_counts {
            for rhythm in &rhythms {
                for tempo in &tempos {
                    for &rubato in &rubatos {
                        for &ornament in &ornaments {
                            for vowel in &vowels {
                                let mut coda = SpermCoda::new(clicks, rhythm.clone(), tempo.clone());
                                coda.rubato = rubato;
                                coda.ornamentation = ornament;
                                coda.vowel_formant = vowel.clone();
                                
                                self.add_coda(coda)?;
                            }
                        }
                    }
                }
            }
        }

        Ok(())
    }

    /// Get alphabet statistics
    pub fn get_stats(&self) -> HashMap<String, f64> {
        let mut stats = HashMap::new();
        
        let avg_clicks = self.codas.iter()
            .map(|c| c.click_count as f64)
            .sum::<f64>() / self.codas.len() as f64;
        
        let avg_freq = self.codas.iter()
            .map(|c| c.frequency_hz)
            .sum::<f64>() / self.codas.len() as f64;
        
        let with_rubato = self.codas.iter()
            .filter(|c| c.rubato)
            .count() as f64;
        
        stats.insert("coda_count".to_string(), self.codas.len() as f64);
        stats.insert("avg_clicks".to_string(), avg_clicks);
        stats.insert("avg_frequency_hz".to_string(), avg_freq);
        stats.insert("rubato_percent".to_string(), with_rubato / self.codas.len() as f64 * 100.0);
        
        stats
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sperm_coda_creation() {
        let coda = SpermCoda::new(10, Rhythm::Regular, Tempo::Medium);
        assert_eq!(coda.click_count, 10);
        assert!(coda.validate().is_ok());
    }

    #[test]
    fn test_combinatorial_complexity() {
        let coda = SpermCoda::new(10, Rhythm::Regular, Tempo::Medium);
        let complexity = coda.combinatorial_complexity();
        assert_eq!(complexity, 4 * 3 * 2 * 4 * 3); // 288 combinations
    }

    #[test]
    fn test_click_generation() {
        let coda = SpermCoda::new(5, Rhythm::Regular, Tempo::Fast);
        let clicks = coda.generate_clicks();
        assert_eq!(clicks.len(), 5);
        
        // Check timing is increasing
        for i in 1..clicks.len() {
            assert!(clicks[i] > clicks[i-1]);
        }
    }

    #[test]
    fn test_formant_frequencies() {
        let mut coda = SpermCoda::new(10, Rhythm::Regular, Tempo::Medium);
        
        coda.vowel_formant = VowelFormant::A;
        let (f1, f2) = coda.formant_frequencies();
        assert_eq!(f1, 700.0);
        assert_eq!(f2, 1200.0);
    }

    #[test]
    fn test_phonetic_id() {
        let mut coda = SpermCoda::new(10, Rhythm::Regular, Tempo::Medium);
        coda.rubato = true;
        coda.ornamentation = 2;
        coda.vowel_formant = VowelFormant::A;
        
        let id = coda.phonetic_id();
        assert_eq!(id, "RMr10o2a");
    }

    #[test]
    fn test_alphabet_generation() {
        let mut alphabet = SpermPhoneticAlphabet::new("caribbean_clan".to_string());
        assert!(alphabet.generate_full_alphabet().is_ok());
        
        let stats = alphabet.get_stats();
        assert!(stats["coda_count"] >= 156.0); // Should have 288 codas
    }
}
