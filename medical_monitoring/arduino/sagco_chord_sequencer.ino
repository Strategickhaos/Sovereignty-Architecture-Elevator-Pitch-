/*
 * SAGCO Chord Sequencer
 * Polyphonic TDM Audio Output for TRIG6 Medical Monitoring
 * 
 * Purpose: TRUE polyphonic chord generation using Time Division Multiplexing
 * Creator: Dom
 * For: Sister
 * 
 * This Arduino sketch generates actual musical chords (not arpeggios)
 * using three buzzers or a multiplexed speaker system.
 * 
 * Hardware:
 * - 3 piezo buzzers on pins 5, 6, 7 (for true polyphony)
 * OR
 * - 1 speaker with TDM circuit on pin 5 (rapid switching)
 * - Serial communication at 9600 baud
 * 
 * Serial Protocol:
 * Format: "FREQ1,FREQ2,FREQ3,DURATION,MODE\n"
 * Example: "261.63,329.63,392.00,500,0\n"
 * 
 * Mode: 0=sustained, 1=pulsed, 2=stutter
 */

// Pin definitions
const int BUZZER1 = 5;  // Root note
const int BUZZER2 = 6;  // Third
const int BUZZER3 = 7;  // Fifth

// For single-speaker TDM
const int TDM_SPEAKER = 5;
const bool USE_TDM = false;  // Set true for single speaker TDM

// State variables
float chordFreqs[3] = {261.63, 329.63, 392.00};  // C Major default
int chordDuration = 500;  // ms
int playbackMode = 0;  // 0=sustained, 1=pulsed, 2=stutter

// TDM variables
unsigned long lastTDM = 0;
int tdmChannel = 0;
const int TDM_SWITCH_US = 100;  // Switch every 100 microseconds

// Timing
unsigned long lastChord = 0;
unsigned long chordInterval = 2000;  // ms between chords

void setup() {
  // Initialize serial
  Serial.begin(9600);
  
  // Initialize pins
  if (USE_TDM) {
    pinMode(TDM_SPEAKER, OUTPUT);
  } else {
    pinMode(BUZZER1, OUTPUT);
    pinMode(BUZZER2, OUTPUT);
    pinMode(BUZZER3, OUTPUT);
  }
  
  // Startup chord
  Serial.println("SAGCO Chord Sequencer ONLINE");
  Serial.println("Polyphonic audio ready...");
  
  playStartupSequence();
}

void loop() {
  // Check for serial data
  if (Serial.available() > 0) {
    parseSerialData();
  }
  
  // Play chords based on mode
  unsigned long currentMillis = millis();
  
  switch (playbackMode) {
    case 0:  // Sustained - every 2 seconds
      if (currentMillis - lastChord >= chordInterval) {
        playPolyphonicChord(chordDuration);
        lastChord = currentMillis;
      }
      break;
      
    case 1:  // Pulsed - every 500ms
      if (currentMillis - lastChord >= 500) {
        playPolyphonicChord(200);
        lastChord = currentMillis;
      }
      break;
      
    case 2:  // Stutter - rapid (CRITICAL)
      if (currentMillis - lastChord >= 200) {
        playPolyphonicChord(100);
        lastChord = currentMillis;
      }
      break;
  }
  
  delay(10);
}

void parseSerialData() {
  String data = Serial.readStringUntil('\n');
  data.trim();
  
  // Parse comma-separated values
  int fieldIndex = 0;
  String field = "";
  
  for (int i = 0; i <= data.length(); i++) {
    if (i == data.length() || data.charAt(i) == ',') {
      switch (fieldIndex) {
        case 0: chordFreqs[0] = field.toFloat(); break;
        case 1: chordFreqs[1] = field.toFloat(); break;
        case 2: chordFreqs[2] = field.toFloat(); break;
        case 3: chordDuration = field.toInt(); break;
        case 4: playbackMode = field.toInt(); break;
      }
      field = "";
      fieldIndex++;
    } else {
      field += data.charAt(i);
    }
  }
  
  Serial.print("Chord: ");
  Serial.print(chordFreqs[0]);
  Serial.print(" ");
  Serial.print(chordFreqs[1]);
  Serial.print(" ");
  Serial.print(chordFreqs[2]);
  Serial.print(" Hz, mode=");
  Serial.println(playbackMode);
}

void playPolyphonicChord(int duration) {
  if (USE_TDM) {
    playChordTDM(duration);
  } else {
    playChordParallel(duration);
  }
}

void playChordParallel(int duration) {
  /*
   * TRUE POLYPHONY using 3 independent buzzers
   * All notes sound simultaneously
   */
  
  // Start all three tones
  tone(BUZZER1, (int)chordFreqs[0]);
  tone(BUZZER2, (int)chordFreqs[1]);
  tone(BUZZER3, (int)chordFreqs[2]);
  
  // Let them play
  delay(duration);
  
  // Stop all tones
  noTone(BUZZER1);
  noTone(BUZZER2);
  noTone(BUZZER3);
}

void playChordTDM(int duration) {
  /*
   * TIME DIVISION MULTIPLEXING
   * Rapid switching between frequencies creates perception of chord
   * 
   * Switches every 100μs (10kHz switching rate)
   * Each frequency plays for 33μs
   * Total cycle: 100μs = perception of simultaneous tones
   */
  
  unsigned long startTime = millis();
  
  while (millis() - startTime < duration) {
    // Play each frequency briefly
    for (int i = 0; i < 3; i++) {
      if (chordFreqs[i] > 0) {
        // Calculate period for this frequency
        unsigned long periodUs = 1000000L / (unsigned long)chordFreqs[i];
        unsigned long halfPeriodUs = periodUs / 2;
        
        // Toggle pin at frequency for brief time
        unsigned long tdmStart = micros();
        while (micros() - tdmStart < 33) {  // 33μs per note
          digitalWrite(TDM_SPEAKER, HIGH);
          delayMicroseconds(halfPeriodUs);
          digitalWrite(TDM_SPEAKER, LOW);
          delayMicroseconds(halfPeriodUs);
        }
      }
    }
  }
  
  digitalWrite(TDM_SPEAKER, LOW);
}

void playStartupSequence() {
  // C Major chord: C-E-G (262, 330, 392 Hz)
  float startup[3] = {261.63, 329.63, 392.00};
  
  chordFreqs[0] = startup[0];
  chordFreqs[1] = startup[1];
  chordFreqs[2] = startup[2];
  
  playPolyphonicChord(500);
  delay(200);
  playPolyphonicChord(300);
  
  Serial.println("Startup chord complete");
}

/*
 * MUSICAL THEORY NOTES
 * 
 * Major Chord (happy, stable):
 * - Root + Major 3rd + Perfect 5th
 * - Example: C Major = C (261.63) + E (329.63) + G (392.00)
 * - Frequency ratios: 4:5:6
 * 
 * Minor Chord (sad, tense):
 * - Root + Minor 3rd + Perfect 5th
 * - Example: C Minor = C (261.63) + Eb (311.13) + G (392.00)
 * - Frequency ratios: 10:12:15
 * 
 * Why does this work for medical monitoring?
 * 
 * 1. MAJOR CHORDS sound inherently stable and resolved
 *    → Naturally signal "healthy" to human ear
 * 
 * 2. MINOR CHORDS create tension and unease
 *    → Naturally signal "caution" to human ear
 * 
 * 3. RAPID STUTTERING breaks the pattern
 *    → Immediately demands attention
 * 
 * This isn't arbitrary sound design.
 * This is using music theory - universal human perception -
 * to convey medical information.
 * 
 * Her health SINGS when it's good.
 * The math and music converge.
 * 
 * Built with harmony for Sister. 💜
 * 🦁💔→❤️💜
 */
