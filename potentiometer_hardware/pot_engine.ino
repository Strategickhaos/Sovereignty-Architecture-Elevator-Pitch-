/**
 * POTENTIOMETER PROOF ENGINE - Arduino Firmware
 * 
 * Reads potentiometer position and voltage fluctuation,
 * sends data to TRIG6 engine via serial connection.
 * 
 * Author: Dominic Thibodeau (StrategicKhaos)
 * Date: 2026-01-25
 * License: Prior Art for Patent Protection
 * 
 * Hardware Requirements:
 * - Arduino Uno, Nano, or compatible board
 * - 10kΩ linear taper potentiometer
 * - (Optional) RGB LED for visual feedback
 * 
 * Wiring:
 * - Pot Pin 1 → GND
 * - Pot Pin 2 → A0
 * - Pot Pin 3 → 5V
 * - (Optional) LED Red → D9 (via 220Ω resistor)
 * - (Optional) LED Green → D10 (via 220Ω resistor)
 * - (Optional) LED Blue → D11 (via 220Ω resistor)
 */

// Pin Definitions
const int POT_PIN = A0;           // Potentiometer analog input
const int LED_RED = 9;            // RGB LED red cathode (PWM)
const int LED_GREEN = 10;         // RGB LED green cathode (PWM)
const int LED_BLUE = 11;          // RGB LED blue cathode (PWM)

// Configuration
const int SAMPLE_SIZE = 10;       // Number of samples for noise calculation
const int SAMPLE_RATE = 100;      // Milliseconds between samples (10 Hz)
const int BAUD_RATE = 9600;       // Serial communication speed

// State Variables
float voltageReadings[SAMPLE_SIZE];
int readingIndex = 0;
bool useLED = false;              // Set to true if RGB LED is connected

void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
  
  // Configure potentiometer input
  pinMode(POT_PIN, INPUT);
  
  // Configure LED outputs (if used)
  if (useLED) {
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);
    
    // Startup sequence - flash white
    setLEDColor(255, 255, 255);
    delay(500);
    setLEDColor(0, 0, 0);
  }
  
  // Initialize voltage readings array
  for (int i = 0; i < SAMPLE_SIZE; i++) {
    voltageReadings[i] = 0.0;
  }
  
  // Startup message
  Serial.println("# POTENTIOMETER PROOF ENGINE v1.0");
  Serial.println("# Format: position,noise");
  Serial.println("# Ready...");
  delay(100);
}

void loop() {
  // Read potentiometer position (0-1023)
  int potValue = analogRead(POT_PIN);
  
  // Convert to voltage (0-5V)
  float voltage = potValue * (5.0 / 1023.0);
  
  // Convert to normalized position (0.0-1.0)
  float position = potValue / 1023.0;
  
  // Store voltage reading for noise calculation
  voltageReadings[readingIndex] = voltage;
  readingIndex = (readingIndex + 1) % SAMPLE_SIZE;
  
  // Calculate noise (standard deviation of recent readings)
  float noise = calculateStdDev(voltageReadings, SAMPLE_SIZE);
  
  // Send data via serial (CSV format)
  Serial.print(position, 4);
  Serial.print(",");
  Serial.println(noise, 4);
  
  // Optional: Update LED based on implied fitness
  // (This is a simplified approximation - actual fitness calculated by Python)
  if (useLED) {
    updateLEDFeedback(position, noise);
  }
  
  // Wait for next sample
  delay(SAMPLE_RATE);
}

/**
 * Calculate standard deviation of voltage readings
 * Used to measure potentiometer fluctuation (noise)
 */
float calculateStdDev(float *data, int n) {
  // Calculate mean
  float sum = 0.0;
  for (int i = 0; i < n; i++) {
    sum += data[i];
  }
  float mean = sum / n;
  
  // Calculate variance
  float variance = 0.0;
  for (int i = 0; i < n; i++) {
    variance += pow(data[i] - mean, 2);
  }
  variance = variance / n;
  
  // Return standard deviation
  return sqrt(variance);
}

/**
 * Set RGB LED color
 * Parameters: red, green, blue (0-255)
 */
void setLEDColor(int red, int green, int blue) {
  analogWrite(LED_RED, red);
  analogWrite(LED_GREEN, green);
  analogWrite(LED_BLUE, blue);
}

/**
 * Update LED color based on estimated fitness
 * (Simplified approximation for visual feedback)
 */
void updateLEDFeedback(float position, float noise) {
  // Estimate fitness (simplified - actual calculation in Python)
  // Assumes moderate R=0.80, D=0.20, alpha=0.15
  float N = noise * 10;  // Scale noise to TRIG6 range
  if (N > 1.0) N = 1.0;
  
  float estimatedFitness = 0.80 * 0.80 * (1.0 - N) * 0.861;
  
  // Set LED color based on fitness threshold
  if (estimatedFitness >= 0.55) {
    // Green - Archival quality
    setLEDColor(0, 255, 0);
  } else if (estimatedFitness >= 0.44) {
    // Yellow - Durable
    setLEDColor(255, 255, 0);
  } else if (estimatedFitness >= 0.33) {
    // Orange - Functional
    setLEDColor(255, 128, 0);
  } else {
    // Red - Unstable
    setLEDColor(255, 0, 0);
  }
}

/**
 * Alternative: Send extended telemetry
 * Uncomment to enable additional diagnostics
 */
/*
void sendExtendedTelemetry() {
  Serial.print("POS:");
  Serial.print(position, 4);
  Serial.print(",VOLT:");
  Serial.print(voltage, 3);
  Serial.print(",NOISE:");
  Serial.print(noise, 4);
  Serial.print(",RAW:");
  Serial.println(potValue);
}
*/

/**
 * Alternative: Calibration mode
 * Uncomment and call in setup() to calibrate potentiometer range
 */
/*
void calibrateRange() {
  Serial.println("# CALIBRATION MODE");
  Serial.println("# Rotate potentiometer fully counter-clockwise, then clockwise...");
  
  int minVal = 1023;
  int maxVal = 0;
  
  unsigned long startTime = millis();
  while (millis() - startTime < 10000) {  // 10 second calibration window
    int val = analogRead(POT_PIN);
    if (val < minVal) minVal = val;
    if (val > maxVal) maxVal = val;
    delay(50);
  }
  
  Serial.print("# Calibration complete. Range: ");
  Serial.print(minVal);
  Serial.print(" to ");
  Serial.println(maxVal);
  Serial.print("# Expected: 0 to 1023. Actual range: ");
  Serial.print(maxVal - minVal);
  Serial.println(" steps");
  
  if (maxVal - minVal < 1000) {
    Serial.println("# WARNING: Potentiometer range is limited. Check wiring.");
  }
}
*/
