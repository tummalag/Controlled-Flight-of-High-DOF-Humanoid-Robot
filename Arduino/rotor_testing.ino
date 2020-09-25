#include <Servo.h>
const int mot[] = {9,10}; // Initializing motor pins
const int mot_L = 0;      // mot[mot_L] is to control left motor.
const int mot_R = 1;      // similarly for right motor

Servo left;               // Creating 2 servos left and right
Servo right;
const double servoMin = 45.0;  // servo PWM min value
const double servoMax = 100.0; // servo PWM max value

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Bot is ready to fly!!");
  pinMode(mot[mot_L],OUTPUT);
  pinMode(mot[mot_R],OUTPUT);
  left.attach(mot[mot_L]);
  right.attach(mot[mot_R]);
  left.write(45);
  right.write(45);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = servoMin; i<servoMax;i++){
    left.write(i);
    Serial.print("Left   ");
    Serial.println(i);
    delay(100);
  }
  for (int i = servoMax; i>servoMin;i--){
    left.write(i);
    Serial.print("Left   ");
    Serial.println(i);
    delay(100);
  }
  for (int i = servoMin; i<servoMax;i++){
    right.write(i);
    Serial.print("Right   ");
    Serial.println(i);
    delay(100);
  }
  for (int i = servoMax; i>servoMin;i--){
    right.write(i);
    Serial.print("Right   ");
    Serial.println(i);
    delay(100);
  }
  delay(1000);
}
