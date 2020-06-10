#include "DHT.h"

//Defining the anolog pins on the arduino board
#define DHTPIN 7 // what digital pin we're connected to
#define DHTTYPE DHT11 // DHT 11
#define ldr_apin A0 // LDR (Light) sensor


//Initializing the values
int led = 9;// LED pin
int val = 0;// Init value 
DHT dht(DHTPIN, DHTTYPE);



void setup() {
  // put your setup code here, to run once:
  Serial.begin (9600);// Setting the baud rate
  dht.begin();
  Serial.println("Starting the Light, Temperature and Humidity sensing");
}

void loop() {
  // put your main code here, to run repeatedly:
  //Setting a delay for 2 seconds before gettign data from the sensors again
  delay(2000);
  

  //Code for the temperature and humitdity sensor to get data
  int h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  int t = dht.readTemperature();
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("\t"); // for splitting
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print("\t"); // for splitting



  
  //Code for the LDR(Light) sensor to get data
  val = analogRead(ldr_apin);// reading data from the sensor
  //Abtaining how much light the LDR is recieving 
  // IF output is 0 the LDR has full light hitting it
  // IF output is 255 the LDR is in complete darkness 
  val = constrain(val,400,500);
  val = map(val,400,500,255,0);

  analogWrite(led, val);//Setting the brightness to the LED from the value from the LDR
 //Displaying the Light
  Serial.print("Light:  ");
  Serial.print(val);
  Serial.print("\n"); // for new line
 // Serial.println();



}
