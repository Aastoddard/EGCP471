#include <SoftwareSerial.h> //Serial library

SoftwareSerial bt (0,1);  //RX, TX (Switched on the Bluetooth - RX -> TX | TX -> RX)
float fsr = 0;
int inputPin = A5;
int btdata; // the data given from the computer
 
void setup() {
  bt.begin(9600);
  pinMode(inputPin, INPUT);
}
 
void loop() {
  fsr = analogRead(inputPin);
  
  bt.print(fsr);
  bt.print("\n");
  
  delay (2000); //prepare for data (2s)
}
