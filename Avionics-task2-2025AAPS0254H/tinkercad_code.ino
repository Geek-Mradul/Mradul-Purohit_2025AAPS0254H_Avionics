// Name - Mradul Purohit
// ID - 2025AAPS0254H
// Email ID - f20250254@hyderabad.bits-pilani.ac.in
// Team JANUS Avionics Problem Statement - Task 2 Code
// This code determines the flight state of a device using a force sensor
// and indicates the state with LEDs and a buzzer.

// 1. Defining Constants & Pins
const int FORCE_SENSOR_PIN = A0; // Force sensor on Analog Pin A0
const int GREEN_LED_PIN = 4;     // Green LED for ASCENDING state
const int YELLOW_LED_PIN = 3;    // Yellow LED for APOGEE event
const int RED_LED_PIN = 2;       // Red LED for DESCENDING state
const int BUZZER_PIN = 13;       // Buzzer to sound at apogee

// 2. Stating and Filtering Variables
enum FlightState
{
    ON_PAD,
    ASCENDING,
    DESCENDING
};
FlightState currentState = ON_PAD;

// Variables for the moving average filter to reduce sensor noise.
const int numReadings = 10; // Number of readings to average
int readings[numReadings];  // Array to store the last N readings
int readIndex = 0;          // Index of the current reading
long total = 0;             // Running total of readings
int averageReading = 0;     // The final smoothed/filtered reading

// Variables for state change detection.
int previousAverageReading = 0;  // Store the last loop's average
const int LAUNCH_THRESHOLD = 50; // How much the reading must drop to detect launch
const int NOISE_THRESHOLD = 3;   // Small changes below this are ignored as noise

// 3. Setup Function
void setup()
{
    // Initializing Serial Monitor for debugging.
    Serial.begin(9600);

    // Seting the LED and Buzzer pins as outputs.
    pinMode(GREEN_LED_PIN, OUTPUT);
    pinMode(YELLOW_LED_PIN, OUTPUT);
    pinMode(RED_LED_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);

    // Initializing the filter array by taking a baseline reading.
    delay(100); // Wait for sensor to settle.
    int initialReading = analogRead(FORCE_SENSOR_PIN);
    for (int i = 0; i < numReadings; i++)
    {
        readings[i] = initialReading;
    }
    total = initialReading * numReadings;
    averageReading = initialReading;
    previousAverageReading = initialReading;

    Serial.println("System Initialized. Waiting for Launch.");
}

// 4. Main Loop
void loop()
{
    // A. Read Sensor and Filter Noise
    total = total - readings[readIndex];                // Subtract the oldest reading
    readings[readIndex] = analogRead(FORCE_SENSOR_PIN); // Read from the sensor
    total = total + readings[readIndex];                // Add the new reading
    readIndex = (readIndex + 1) % numReadings;          // Advance the index
    averageReading = total / numReadings;               // Calculate the new average

    // B. Stating Detection Logic
    int readingChange = averageReading - previousAverageReading;

    if (currentState == ON_PAD)
    {
        // A large drop in force/pressure indicates launch.
        if (readingChange < -LAUNCH_THRESHOLD)
        {
            currentState = ASCENDING;
            Serial.println("LAUNCH DETECTED! State -> ASCENDING");
        }
    }
    else if (currentState == ASCENDING)
    {
        // A significant rise in force/pressure indicates the peak has been passed.
        if (readingChange > NOISE_THRESHOLD)
        {
            // This transition from ASCENDING to DESCENDING is APOGEE.
            Serial.println("APOGEE DETECTED! State -> DESCENDING");
            triggerApogeeEvent(); // Ring buzzer and flash LED
            currentState = DESCENDING;
        }
    }

    // C. Update LEDs and Store Reading for Next Loop
    updateLeds();
    previousAverageReading = averageReading;

    delay(100); // Loop every 100ms.
}

// Controling the LEDs based on the current flight state
void updateLeds()
{
    digitalWrite(GREEN_LED_PIN, currentState == ASCENDING);
    digitalWrite(RED_LED_PIN, currentState == DESCENDING);
}

// Called once when apogee is detected to sound the buzzer and flash the LED.
void triggerApogeeEvent()
{
    digitalWrite(YELLOW_LED_PIN, HIGH);
    tone(BUZZER_PIN, 1500, 500); // Sound buzzer at 1500Hz for 500ms.
    delay(500);                  // Keep LED on for the duration of the buzz.
    digitalWrite(YELLOW_LED_PIN, LOW);
}