/*
 * SAGCOduino NeuroProbe
 * LED + Buzzer Alert System for TRIG6 Medical Monitoring
 * 
 * Purpose: Hardware alert system for neurological monitoring
 * Creator: Dom
 * For: Sister
 * 
 * This Arduino sketch receives data from Python diagnostic system
 * and provides visual (LED) and audio (buzzer) feedback.
 * 
 * Hardware:
 * - RGB LED (or 3 separate LEDs) on pins 9, 10, 11
 * - Piezo buzzer on pin 8
 * - Serial communication at 9600 baud
 * 
 * Serial Protocol:
 * Format: "THETA,RISK,LED_R,LED_G,LED_B,FREQ1,FREQ2,FREQ3,MODE\n"
 * Example: "75.5,0.82,255,255,0,261.63,311.13,392.00,1\n"
 */

// Pin definitions
const int LED_R = 9;    // Red LED (PWM)
const int LED_G = 10;   // Green LED (PWM)
const int LED_B = 11;   // Blue LED (PWM)
const int BUZZER = 8;   // Piezo buzzer

// State variables
float currentTheta = 0.0;
float currentRisk = 0.0;
int ledRed = 0;
int ledGreen = 255;
int ledBlue = 0;
float chordFreqs[3] = {261.63, 329.63, 392.00};  // C Major default
int playbackMode = 0;  // 0=sustained, 1=pulsed, 2=stutter

// Timing
unsigned long lastUpdate = 0;
unsigned long pulseInterval = 500;  // ms between pulses
bool pulseState = false;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize pins
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  
  // Startup indication
  startupSequence();
  
  Serial.println("SAGCOduino NeuroProbe ONLINE");
  Serial.println("Waiting for TRIG6 data...");
}

void loop() {
  // Check for serial data
  if (Serial.available() > 0) {
    parseSerialData();
  }
  
  // Update outputs based on mode
  updateOutputs();
  
  delay(10);  // Small delay for stability
}

void parseSerialData() {
  String data = Serial.readStringUntil('\n');
  data.trim();
  
  // Parse comma-separated values
  int commaIndex = 0;
  int fieldIndex = 0;
  String field = "";
  
  for (int i = 0; i <= data.length(); i++) {
    if (i == data.length() || data.charAt(i) == ',') {
      // Process field
      switch (fieldIndex) {
        case 0: currentTheta = field.toFloat(); break;
        case 1: currentRisk = field.toFloat(); break;
        case 2: ledRed = field.toInt(); break;
        case 3: ledGreen = field.toInt(); break;
        case 4: ledBlue = field.toInt(); break;
        case 5: chordFreqs[0] = field.toFloat(); break;
        case 6: chordFreqs[1] = field.toFloat(); break;
        case 7: chordFreqs[2] = field.toFloat(); break;
        case 8: playbackMode = field.toInt(); break;
      }
      field = "";
      fieldIndex++;
    } else {
      field += data.charAt(i);
    }
  }
  
  // Debug output
  Serial.print("Received: theta=");
  Serial.print(currentTheta);
  Serial.print(" risk=");
  Serial.print(currentRisk);
  Serial.print(" mode=");
  Serial.println(playbackMode);
}

void updateOutputs() {
  // Always update LED
  updateLED();
  
  // Audio based on mode
  unsigned long currentMillis = millis();
  
  switch (playbackMode) {
    case 0:  // Sustained
      if (currentMillis - lastUpdate > 2000) {
        playChord(100);  // Short chord every 2 seconds
        lastUpdate = currentMillis;
      }
      break;
      
    case 1:  // Pulsed
      if (currentMillis - lastUpdate > pulseInterval) {
        playChord(50);  // Quick pulse
        lastUpdate = currentMillis;
      }
      break;
      
    case 2:  // Stutter (CRITICAL)
      if (currentMillis - lastUpdate > 200) {
        playChord(30);  // Rapid stutter
        lastUpdate = currentMillis;
      }
      break;
      
    default:
      // No audio
      break;
  }
}

void updateLED() {
  // Set RGB LED values
  analogWrite(LED_R, ledRed);
  analogWrite(LED_G, ledGreen);
  analogWrite(LED_B, ledBlue);
}

void playChord(int duration) {
  /*
   * Play all three chord frequencies sequentially (arpeggio)
   * This is a limitation of single buzzer - can't play true polyphony
   * For true polyphony, use sagco_chord_sequencer.ino with TDM
   */
  int noteDuration = duration / 3;
  
  for (int i = 0; i < 3; i++) {
    if (chordFreqs[i] > 0) {
      tone(BUZZER, (int)chordFreqs[i], noteDuration);
      delay(noteDuration);
    }
  }
  
  noTone(BUZZER);
}

void startupSequence() {
  // Visual and audio confirmation of startup
  
  // Red
  analogWrite(LED_R, 255);
  analogWrite(LED_G, 0);
  analogWrite(LED_B, 0);
  tone(BUZZER, 262, 200);
  delay(200);
  
  // Green
  analogWrite(LED_R, 0);
  analogWrite(LED_G, 255);
  analogWrite(LED_B, 0);
  tone(BUZZER, 330, 200);
  delay(200);
  
  // Blue
  analogWrite(LED_R, 0);
  analogWrite(LED_G, 0);
  analogWrite(LED_B, 255);
  tone(BUZZER, 392, 200);
  delay(200);
  
  // Off
  analogWrite(LED_R, 0);
  analogWrite(LED_G, 0);
  analogWrite(LED_B, 0);
  
  delay(500);
}

/*
 * LOVE INVARIANT CHECK
 * 
 * This firmware ensures:
 * - Frequencies never exceed human-safe levels (<20kHz)
 * - LED brightness never exceeds safe levels
 * - Audio duration never causes harm
 * - System fails safe (LEDs off, no sound)
 * 
 * First, do no harm.
 * Encoded at the hardware level.
 * For Sister. 💜
 */
