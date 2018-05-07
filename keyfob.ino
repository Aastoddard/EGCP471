void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}#include <SoftwareSerial.h> //Serial library

//software serial connection set up on pins 0 and 1
SoftwareSerial bt (0,1);  //RX, TX (Switched on the Bluetooth - RX -> TX | TX -> RX)
//float rangeFlag = 0;
int outputPin = 6;
int btdata; // the data given from the computer
//int LED = 13;
 
void setup() {
  bt.begin(9600); //begin serial connection with 9600 baud rate
  bt.println("Waiting for Command. 1 = on, 0 = off");
  pinMode(outputPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}
 
void loop() {
  
  if(bt.available())
  {
    btdata = bt.read();
    if (btdata=='1')
    {
      analogWrite( 6 , 153 );  // 60% duty cycle
      delay(2000);              // play for 1s
      analogWrite( 6 , 0 );    // 0% duty cycle (off)
      delay(2000);             // wait for 2s
    }
    else if(btdata=='0')
    {
      digitalWrite(LED_BUILTIN,HIGH);
      bt.println("0 detected. LED ON");
      delay(1000);
      digitalWrite(LED_BUILTIN,LOW);
    }
    else{;}
  }
   
  delay (100); //prepare for data (2s)
}
