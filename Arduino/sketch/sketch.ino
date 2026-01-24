#include <OneWire.h>
#include <DallasTemperature.h>
#include <HX711.h>
#include <SoftwareSerial.h>

unsigned long lastTime = 0;
const unsigned long interval = 1000;
const int threshold = 30;
const int lightPin = 2;
const int buzzPin = 6;
int trigger = 0;
int alarm = 0;

#define ONE_WIRE_BUS 3
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

const int DOUT_PIN = 4;
const int SCK_PIN = 5;
HX711 scale;

SoftwareSerial piSerial(10, 11);

void setup() {
  Serial.begin(9600);
  piSerial.begin(9600);
  pinMode(lightPin, INPUT);
//  pinMode(weightPin, INPUT);
  pinMode(buzzPin, OUTPUT);
  digitalWrite(buzzPin, LOW);
  scale.begin(DOUT_PIN, SCK_PIN);
  scale.set_scale();
  scale.tare();
  sensors.begin();
}

void multiPrint(String message) {
  Serial.print(message);   // Print to USB
  piSerial.print(message); // Print to GPIO
}

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastTime >= interval) {
    lastTime = currentTime;
    int lightState = !digitalRead(lightPin);
        if (lightState == 1) {
      trigger++;
    } else {
      trigger=0;
    }
    if (trigger >= threshold) {
      alarm = 1;
      digitalWrite(buzzPin, HIGH);
    } else {
      alarm = 0;
      digitalWrite(buzzPin, LOW);
    }

    sensors.requestTemperatures();
    float tempCelsius = sensors.getTempCByIndex(0);

    if (scale.is_ready()) {
      multiPrint("Gewicht:" + String(scale.get_units(), 1) + ",");
    } else {
      multiPrint("Gewicht: 0,");
    }
    multiPrint("Licht:" + String(lightState) + ",");
    multiPrint("Alarm:" + String(alarm) + ",");
    multiPrint("Temperatur:" + String(tempCelsius) + "\n");
  }  
}