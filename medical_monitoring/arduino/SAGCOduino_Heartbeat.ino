/*
 * SAGCOduino Heartbeat
 * Heartbeat Pulse Visualization for TRIG6 Medical Monitoring
 * 
 * Purpose: Visual heartbeat indicator synchronized with patient state
 * Creator: Dom
 * For: Sister
 * 
 * This Arduino sketch creates a pulsing LED heartbeat effect
 * that varies based on the patient's neurological state.
 * 
 * Hardware:
 * - RGB LED (or single LED) on pins 9, 10, 11
 * - Serial communication at 9600 baud
 * 
 * Serial Protocol:
 * Format: "THETA,RISK,BPM\n"
 * Example: "65.5,0.45,72\n"
 * 
 * Heartbeat visualization adapts to:
 * - Risk level (color intensity)
 * - Estimated BPM (pulse rate)
 * - System health (smooth vs irregular)
 */

// Pin definitions
const int LED_R = 9;
const int LED_G = 10;
const int LED_B = 11;

// State variables
float currentTheta = 45.0;
float currentRisk = 0.3;
float targetBPM = 72.0;  // Normal resting heart rate

// Heartbeat parameters
unsigned long lastBeat = 0;
unsigned long beatInterval = 833;  // ms (72 BPM default)
int brightness = 0;
bool increasing = true;

// Color based on risk
int colorR = 0;
int colorG = 255;
int colorB = 0;

void setup() {
  // Initialize serial
  Serial.begin(9600);
  
  // Initialize pins
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  
  // Startup
  Serial.println("SAGCOduino Heartbeat ONLINE");
  Serial.println("Pulse visualization ready...");
  
  // Initial heartbeat
  doHeartbeat();
}

void loop() {
  // Check for serial updates
  if (Serial.available() > 0) {
    parseSerialData();
    updateHeartbeatParams();
  }
  
  // Generate heartbeat pulse
  unsigned long currentMillis = millis();
  if (currentMillis - lastBeat >= beatInterval) {
    doHeartbeat();
    lastBeat = currentMillis;
  }
  
  delay(10);
}

void parseSerialData() {
  String data = Serial.readStringUntil('\n');
  data.trim();
  
  // Parse: THETA,RISK,BPM
  int firstComma = data.indexOf(',');
  int secondComma = data.indexOf(',', firstComma + 1);
  
  if (firstComma > 0 && secondComma > 0) {
    currentTheta = data.substring(0, firstComma).toFloat();
    currentRisk = data.substring(firstComma + 1, secondComma).toFloat();
    targetBPM = data.substring(secondComma + 1).toFloat();
  }
}

void updateHeartbeatParams() {
  // Update beat interval based on BPM
  if (targetBPM > 0) {
    beatInterval = (unsigned long)(60000.0 / targetBPM);
  }
  
  // Update color based on risk
  if (currentRisk < 0.5) {
    // Green - healthy
    colorR = 0;
    colorG = 255;
    colorB = 0;
  } else if (currentRisk < 0.7) {
    // Yellow - watchful
    colorR = 255;
    colorG = 255;
    colorB = 0;
  } else if (currentRisk < 0.9) {
    // Orange - elevated
    colorR = 255;
    colorG = 128;
    colorB = 0;
  } else {
    // Red - critical
    colorR = 255;
    colorG = 0;
    colorB = 0;
  }
}

void doHeartbeat() {
  /*
   * Simulate heartbeat with double-pulse pattern:
   * "lub-dub" - systole and diastole
   */
  
  // First pulse (lub)
  fadeIn(30);
  fadeOut(50);
  
  // Short pause
  delay(80);
  
  // Second pulse (dub)
  fadeIn(20);
  fadeOut(40);
  
  // Rest period
  setLED(0, 0, 0);
}

void fadeIn(int duration) {
  int steps = 20;
  int stepDelay = duration / steps;
  
  for (int i = 0; i <= steps; i++) {
    int brightness = map(i, 0, steps, 0, 255);
    setLED(
      (colorR * brightness) / 255,
      (colorG * brightness) / 255,
      (colorB * brightness) / 255
    );
    delay(stepDelay);
  }
}

void fadeOut(int duration) {
  int steps = 20;
  int stepDelay = duration / steps;
  
  for (int i = steps; i >= 0; i--) {
    int brightness = map(i, 0, steps, 0, 255);
    setLED(
      (colorR * brightness) / 255,
      (colorG * brightness) / 255,
      (colorB * brightness) / 255
    );
    delay(stepDelay);
  }
}

void setLED(int r, int g, int b) {
  analogWrite(LED_R, r);
  analogWrite(LED_G, g);
  analogWrite(LED_B, b);
}

/*
 * BENTOV RESONANCE INTEGRATION
 * 
 * Itzhak Bentov proposed that consciousness operates through
 * standing wave resonances centered around 7 Hz - the heart's
 * natural rhythm creating a standing wave in the aorta.
 * 
 * This heartbeat visualizer can sync with the 7 Hz resonance:
 * - At 72 BPM (1.2 Hz), this creates harmonic coupling
 * - The pulse pattern reflects the "lub-dub" of systole/diastole
 * - Visual feedback connects caregiver to patient's life rhythm
 * 
 * The heartbeat is the drum of consciousness.
 * We visualize the rhythm of life.
 * 
 * Built with resonance for Sister. 💜
 * 🦁💔→❤️💜
 */
