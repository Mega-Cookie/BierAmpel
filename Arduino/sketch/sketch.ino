#include <OneWire.h>
#include <DallasTemperature.h>
#include <HX711.h>

const int lightPin = 2;

#define ONE_WIRE_BUS 3
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

const int weightPin =4;

const int DOUT_PIN = 4;
const int SCK_PIN = 5;
HX711 scale;


void setup() {
  Serial.begin(9600);
  pinMode(lightPin, INPUT);
  pinMode(weightPin, INPUT);
  scale.begin(DOUT_PIN, SCK_PIN);
  scale.set_scale();
  scale.tare();
  sensors.begin();
}

void loop() {
  int lightState = !digitalRead(lightPin); 
  sensors.requestTemperatures();
  float tempCelsius = sensors.getTempCByIndex(0);
  if (scale.is_ready()) {
    Serial.print(scale.get_units(), 1);
    Serial.print(",");
  } else {
    Serial.print("HX711 nicht gefunden.");
    Serial.print(",");
  }
  Serial.print(lightState);
  Serial.print(",");
  Serial.println(tempCelsius);
  
  delay(500);
}
