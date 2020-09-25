#include <Servo.h>
const int mot[] = {5,10}; // Initializing motor pins
const int mot_L = 0;      // mot[mot_L] is to control left motor.
const int mot_R = 1;      // similarly for right motor

Servo left;               // Creating 2 servos left and right
Servo right;
const double servoMin = 60.0;  // servo PWM min value
const double servoMax = 90.0; // servo PWM max value

int potentiometerPin = A1;
const int potRefVal = 550;  // Refereance Value
const int potMinVal = 250;  // Left most value -45 degree
const int potMaxVal = 850;  // Right most value +45 degree

double enc2deg(double enc){
  double deg = (enc - potRefVal)/(potRefVal - potMinVal)*30;
  return deg;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(mot[mot_L],OUTPUT);
  pinMode(mot[mot_R],OUTPUT);
  left.attach(mot[mot_L]);
  right.attach(mot[mot_R]);
  left.write(45);
  //right.write(45);
  delay (1000);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  int potentiometerValue =  analogRead(potentiometerPin);
  double degree = enc2deg(potentiometerValue);
  Serial.println(String(degree));
  left.write(70);
  delay(20);
}
