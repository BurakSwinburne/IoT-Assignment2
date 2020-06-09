#include "DHT.h"

#define DHTPIN 8
#define DHTTYPE DHT11

const int ldrPin = A0;
byte dat [5];

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ldrPin, INPUT);
  dht.begin();
}

void loop () {


  while (Serial.available() == 0) {  
    // wait for data... better method available? idk
    //delay(500);
  }

//    while (Serial.available() > 0) {
//      char c = Serial.read();
//      Serial.print(c);  
//    // wait for data... better method available? idk
//    //delay(500);
//  }

  if (serialInHandler()) {
    getVals();
    flushBuffer();
  }
}

void foo() {
    while (Serial.available() > 0) {
    Serial.print("count : ");
    Serial.println(Serial.available());
    Serial.read();    
    }
  }

boolean serialInHandler() {
  Serial.setTimeout(10);
  return Serial.find('t');
}

void flushBuffer() {
  delay(5);
  while (Serial.available() > 0) {
    Serial.read();
     delay(5);
  }
}

void getVals() {
  int l = map(analogRead(ldrPin), 0, 1023, 0, 255);
  float h = dht.readHumidity(); // Read temperature as Celsius (the default)
  float t = dht.readTemperature();// Read temperature as Fahrenheit (isFahrenheit = true)

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print(h);
  Serial.print(',');
  Serial.print(t);
  Serial.print(',');
  Serial.print(l);
}
