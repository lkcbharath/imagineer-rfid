/*
Example for TI MSP430 LaunchPads and Energia that reads a card number 
using a RC522 MIFARE module, takes action depending on the card number,
and prints it to the serial monitor.
https://www.addicore.com/RFID-AddiKit-with-RC522-MIFARE-Module-RFID-Cards-p/126.htm

Based on code and ideas from Eelco Rouw (www.43oh.com), Grant Gibson
(www.grantgibson.co.uk), Dr.Leong (www.b2cqshop.com), and
Craig Thompson/Aaron Norris at Addicore.

Minor modifications to above by Frank Milburn 10 June 2015
Released into the public domain

Tested on MSP-EXP430G2 LaunchPad
          MSP-EXP430F5529 LaunchPad
          MSP-EXP430FR5969 LaunchPad
 
Pin Connections
===================================      
RFID Module       MSP430 LaunchPads        
--------------    -----------------
Pin 1  (SDA)      Pin 8  (CS)
Pin 2  (SCK)      Pin 7  (SCK)
Pin 3  (MOSI)     Pin 15 (MOSI)
Pin 4  (MISO)     Pin 14 (MISO)
Pin 5  (IRQ)      Not connected
Pin 6  (GND)      GND
Pin 7  (RST)      Pin 10
Pin 8  (3V3)      3V3

Addicore has a very good introduction to this module, written for Arduino.
Try the site below for additional detail on the module and examples
which include writing to a card, dumping detailed information, changing
the card user ID, etc.  It will run on LaunchPads or Arduinos with the
correct pin connections:  https://github.com/miguelbalboa/rfid
*/

#include "Mfrc522.h"
#include <SPI.h>

int CS = 8;                                 // chip select pin
int NRSTDP = 5;
int BUZZER = 13;
Mfrc522 Mfrc522(CS,NRSTDP);
unsigned char serNum[5];

void beep(int n){                           // Alert for n more times
  int i;
  delay(250);
  digitalWrite(BUZZER,LOW);
  digitalWrite(RED_LED, LOW);
  delay(250);

  for (i=0;i<n;++i){
    digitalWrite(BUZZER,HIGH);
    digitalWrite(RED_LED, HIGH);
    delay(250);
    digitalWrite(BUZZER,LOW);
    digitalWrite(RED_LED, LOW);
    delay(250);
  }
}

void setup() 
{             
  Serial.begin(9600);                        

  SPI.begin();
  digitalWrite(CS, LOW);                    // Initialize the card reader
  pinMode(RED_LED, OUTPUT);                 // Initialize LED for alert
  pinMode(BUZZER,OUTPUT);                   // Initialize Buzzer for alert
  Mfrc522.Init();  
}

void loop()
{
  int i;
  unsigned char status;
  unsigned char str[MAX_LEN];
  	
  status = Mfrc522.Request(PICC_REQIDL, str);
  if (status == MI_OK)                      // Card hovered over sensor
  {
    Serial.println("");
    Serial.print(str[0],BIN);
    Serial.print(str[1],BIN);
    Serial.println("");
  }

  status = Mfrc522.Anticoll(str);
  memcpy(serNum, str, 5);
  if (status == MI_OK)
  {
    digitalWrite(RED_LED, HIGH);              // Actual UID detected!
    digitalWrite(BUZZER,HIGH);
    for(i=0;i<5;++i){
      Serial.print(serNum[i]);
    }
    // Check if card in database or not.
    if ( (serNum[0] == 155 && str[1] == 98 && str[2] == 65 && str[3] == 12 && str[4] == 180)                      
        || (serNum[0] == 171 && str[1] == 238 && str[2] == 239 && str[3] == 102 && str[4] == 204)){
      beep(0);
    }
    else{
      beep(2);
    }
  }
  Mfrc522.Halt();	                        
}
