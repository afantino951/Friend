#include "SevSeg.h"


/*****************
 * SEVSEG
 *****************/
SevSeg sevseg0;
SevSeg sevseg1;
 
byte numDigits = 1;
bool resistorOnSegments = true;
byte hardwareConfig = COMMON_CATHODE;

byte digitPin0[] = {28};
byte segmentPins0[] = {27, 29, 26, 24, 22, 25, 23};

byte digitPin1[] = {36};
byte segmentPins1[] = {35, 37, 34, 32, 30, 33, 31};

/*****************
 * Motor 1
 *****************/
int enA = 2;
int in1 = 38;
int in2 = 39;

/*****************
 * Motor 2
 *****************/
int enB = 3;
int in3 = 40;
int in4 = 41;

/*****************
 * SERIAL
 *****************/
char c;
String serialValues = "";



void setup() {
  sevseg0.begin(hardwareConfig, numDigits, digitPin0, segmentPins0, resistorOnSegments);
  sevseg1.begin(hardwareConfig, numDigits, digitPin1, segmentPins1, resistorOnSegments);

  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  stopAll();
  
}

void loop() {
  if(Serial.available() > 0) {
    c = Serial.read();
    serialValues += c;

    if(serialValues.length() == 12) {
      updateMotors(serialValues);
      serialValues = "";
    }
  }
  
  sevseg0.setNumber(8);
  sevseg1.setNumber(8);

  sevseg0.refreshDisplay();
  sevseg1.refreshDisplay();
  
}

void sendReady() {
  Serial.write("Ready");
}

void stopAll() {
  analogWrite(enA, 0);
  analogWrite(enB, 0);
  
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void updateMotors(String serialValues) {
  int dirA0 = serialValues.substring(6, 7).toInt();
  int dirA1 = serialValues.substring(7, 8).toInt();
  int dirB0 = serialValues.substring(8, 9).toInt();
  int dirB1 = serialValues.substring(9, 10).toInt();

  if (dirA0 == 1) {
    digitalWrite(in1, HIGH);
  } else {
    digitalWrite(in1, LOW);
  }

  if (dirA1 == 1) {
    digitalWrite(in2, HIGH);
  } else {
    digitalWrite(in2, LOW);
  }

  if (dirB0 == 1) {
    digitalWrite(in3, HIGH);
  } else {
    digitalWrite(in3, LOW);
  }

  if (dirB1 == 1) {
    digitalWrite(in4, HIGH);
  } else {
    digitalWrite(in4, LOW);
  }

  analogWrite(enA, serialValues.substring(0,3).toInt());
  analogWrite(enB, serialValues.substring(3, 6).toInt());

  sevseg0.setNumber(serialValues.substring(10,11).toInt());
  sevseg1.setNumber(serialValues.substring(11,12).toInt());
}
