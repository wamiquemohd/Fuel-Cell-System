//Code for Computing data coming from Fuel Cell


#include <SoftwareSerial.h>

// Best for Teensy LC & 3.2
//SoftwareSerial mySerial(0, 1); // RX,TX
SoftwareSerial mySerial(16, 17);

//byte message[] = {0x00, 0x02, 0x2C, 0x00, 0x0D, 0x00, 0x00, 0x32};
byte rxData[8] ={};


void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }


  Serial.println("GoodMorning Sunshine!");

  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  mySerial.flush();
}

void CalculateValues(){
  float Voltage = 0;
  float Current = 0; 
  float Temperature = 0;  

  if(rxData[0] != 0x00){
//  Serial.println("Incoming Data is incorrect....trying to sync");
  mySerial.flush();
  return;
  }

//Calcutale Voltage

  unsigned int V1 = (rxData[1]<<8)|rxData[2];
  //Serial.print("DEC value V1: " + String(V1));
  Voltage = V1 * 0.077;

//Calculate Current
  unsigned int A1 = (rxData[3]<<8) | rxData[4];
  Serial.print("  DEC value A1: " + String(A1));
  Current = A1 * 0.1 ;

  unsigned int T1 = rxData[7];
  Serial.println("  DEC value T1: " + String(T1));
  Temperature = T1 * 0.5;

  Serial.println("Voltage: " + String(Voltage) + "  Current: "+ String(Current) + "  Temperature: " + String(Temperature));

}



void loop() // run over and over
{
  if(mySerial.available() > 8){
    Serial.println("Received New Data");
    for(int i=0; i<8;i++){
      rxData[i] = mySerial.read();
      Serial.println(rxData[i]);
    }
    CalculateValues();
  }

}


