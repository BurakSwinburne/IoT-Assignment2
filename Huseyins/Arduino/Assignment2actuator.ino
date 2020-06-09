// Must use any of the pins: 3, 5, 6, 9, 10, and 11 when it comes to 
// correctly outputting using analogWrite
int LEDPIN_RED = 9;
int LEDPIN_YELLOW = 10;
int LEDPIN_GREEN = 11;

String dataFromPi = "";

void setup() {
  Serial.begin(115200);
  pinMode(LEDPIN_RED, OUTPUT);
  pinMode(LEDPIN_YELLOW, OUTPUT);
  pinMode(LEDPIN_GREEN, OUTPUT);

  switchoff();
}


void switchoff() {

  // Use analog, just to have the option of having adjustable LED brightness
  analogWrite(LEDPIN_RED, 0);
  analogWrite(LEDPIN_YELLOW, 0);
  analogWrite(LEDPIN_GREEN, 0);  
}


void loop() {

  if(Serial.available() > 0) { // If a Pi has sent serial data to the Arduino
    dataFromPi = Serial.readString();
    dataFromPi.trim(); // Remove the \n newline char from the string

    // Set the heater setting according to the Pi's request
    if (dataFromPi == "Heater: high") {
      switchoff();
      analogWrite(LEDPIN_RED, 255);
    }
    else if (dataFromPi == "Heater: low") {
      switchoff();
      analogWrite(LEDPIN_YELLOW, 255);
    }
    else if (dataFromPi == "Heater: off") {
      switchoff();
      analogWrite(LEDPIN_GREEN, 255);
    }
    dataFromPi = ""; // Once the code has evaulated the string, empty string to avoid repeating the if statement
  }

  delay(500);
}
