/*
 * TRIG6 Potentiometer Interface
 * ==============================
 * 
 * Arduino sketch for reading potentiometer values and sending
 * them to the TRIG6 proof system via serial connection.
 * 
 * Hardware Setup:
 * - Potentiometer connected to A0
 * - Center pin to A0
 * - Outer pins to 5V and GND
 * 
 * Connection:
 * - Upload this sketch to Arduino
 * - Connect via USB (typically COM3 on Windows, /dev/ttyUSB0 on Linux)
 * - Run potentiometer_proof.py with matching serial port
 * 
 * Author: Domenic Gabriel Garza
 * Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
 * Date: 2026-01-25
 */

const int POT_PIN = A0;  // Potentiometer on analog pin A0
const int BAUD_RATE = 9600;
const int READ_DELAY = 100;  // Milliseconds between readings

void setup() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
  
  // Configure analog reference (default is 5V)
  analogReference(DEFAULT);
  
  // Wait for serial connection to stabilize
  delay(1000);
  
  // Send initialization message
  Serial.println("# TRIG6 Potentiometer Interface Ready");
  Serial.println("# Reading from A0, sending to serial");
}

void loop() {
  // Read potentiometer value (0-1023)
  int sensorValue = analogRead(POT_PIN);
  
  // Send raw value to serial
  Serial.println(sensorValue);
  
  // Optional: Add LED feedback
  // Uncomment if you have an LED on pin 13
  // digitalWrite(LED_BUILTIN, sensorValue > 512 ? HIGH : LOW);
  
  // Delay between readings
  delay(READ_DELAY);
}

/*
 * Optional: Enhanced version with smoothing
 * Uncomment below to use exponential moving average filter
 */

/*
// Enhanced version with smoothing filter
const float SMOOTHING_FACTOR = 0.1;  // 0.0-1.0, lower = more smoothing
float smoothedValue = 0;

void loop_smooth() {
  int rawValue = analogRead(POT_PIN);
  
  // Apply exponential moving average
  smoothedValue = (SMOOTHING_FACTOR * rawValue) + 
                  ((1 - SMOOTHING_FACTOR) * smoothedValue);
  
  // Send smoothed value (convert back to int)
  Serial.println((int)smoothedValue);
  
  delay(READ_DELAY);
}
*/

/*
 * Testing Notes:
 * 
 * 1. Verify serial connection:
 *    - Open Arduino IDE Serial Monitor
 *    - Set baud rate to 9600
 *    - Turn potentiometer and observe values changing from 0-1023
 * 
 * 2. Test with Python proof system:
 *    - Close Arduino IDE Serial Monitor (only one app can use serial port)
 *    - Run: python3 potentiometer_proof.py
 *    - Adjust potentiometer while script is running
 *    - Script will map 0-1023 → 0.0-1.0 automatically
 * 
 * 3. Mapping modes:
 *    MODE_NOISE: Pot controls noise/uncertainty parameter
 *    MODE_THETA: Pot controls process phase (0 to 2π)
 *    MODE_DRIFT: Pot controls drift/deviation parameter
 *    MODE_ALPHA: Pot controls damping coefficient
 * 
 * 4. Finding stable basins:
 *    - Turn pot slowly to explore parameter space
 *    - Watch for "PROOF ACHIEVED" messages
 *    - Higher fitness values = more stable materials
 *    - f ≥ 0.5 is threshold for stable basin
 */
