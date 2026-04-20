#include <Arduino.h>

int flameSensor = 7;
int buzzer = 8;
int led = 9;

unsigned long flameHoldStart = 0;
const unsigned long holdDuration = 60000; // 60 seconds

bool flameState = false;

void setup() {

  pinMode(flameSensor, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(led, OUTPUT);

  Serial.begin(9600);

}

void loop() {

  int sensorValue = digitalRead(flameSensor);

  // If flame detected
  if (sensorValue == LOW) {

    flameState = true;
    flameHoldStart = millis();
  }

  // Check hold duration
  if (flameState && millis() - flameHoldStart <= holdDuration) {

    Serial.println("FLAME_DETECTED");

    digitalWrite(buzzer, HIGH);
    digitalWrite(led, HIGH);
  }
  else {

    flameState = false;

    Serial.println("NO_FLAME");

    digitalWrite(buzzer, LOW);
    digitalWrite(led, LOW);
  }

  delay(200);
}