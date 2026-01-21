const int shakePin = 2; // Pin where sensor is connected

void setup() {
  Serial.begin(9600);       // Initialize serial communication
  pinMode(shakePin, INPUT); // Set the sensor pin as an input
}

void loop() {
  int shakeState = digitalRead(shakePin); // Read digital signal (0 or 1)
  
  // Plotter expects only numerical values and a newline character
  Serial.println(shakeState); 
  
  delay(10); // Small delay to stabilize the plot
}
