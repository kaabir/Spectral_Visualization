#include "AS726X.h"
AS726X sensor;//Creates the sensor object
const int ledPin = 8;// +ve 8   LED pin number pin of the arduino 
void setup() {
  pinMode(ledPin,OUTPUT);//initialize the digital pin as an output
  Serial.begin(115200);
  sensor.begin();
}

void loop() {
  digitalWrite(ledPin,HIGH);//turn the LED on 
  //sensor.takeMeasurementsWithBulb();
  sensor.takeMeasurements();
  
  Serial.print(sensor.getCalibratedR());
  Serial.print(",");
  Serial.print(sensor.getCalibratedS());
  Serial.print(",");
  Serial.print(sensor.getCalibratedT());
  Serial.print(",");
  Serial.print(sensor.getCalibratedU());
  Serial.print(",");
  Serial.print(sensor.getCalibratedV());
  Serial.print(",");
  Serial.print(sensor.getCalibratedW());

  Serial.println();
}
