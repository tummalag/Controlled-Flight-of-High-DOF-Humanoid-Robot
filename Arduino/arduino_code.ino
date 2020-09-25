#include <Servo.h>

const int leftRotor = 9;
const int rightRotor = 8;
Servo left;
Servo right;
const float servoMin = 55;
const float servoMax = 165;
const float binMax = 127;
int potentiometerPin = A1;
int potentiometerValue = 0;
const int potMinVal = 250;
const int potMaxVal = 850;
int prev_err_r = 0; 
int prev_err_l = 0; 
const float kp = 4;
const float kd = 50;
const float ki = 0;
const int dt = 100; // 0.2 sec
float i_err_r = 0;
float i_err_l = 0;
const int potRefVal = 550;
int potStableVal = 550;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Bot is ready to fly!!");
  /*
  Serial.println("Please Enter the Stable angle \n"
                    "'+' indicates Right \n"
                    "'-' indicates Left");
  if (Serial.available){
    float data = Serial.read();
    if (data > 0){
      data = data/(potMaxVal - potRefVal)*
      potStableVal 
    }
  }
  */
  pinMode(leftRotor,OUTPUT);
  pinMode(rightRotor,OUTPUT);
  left.attach(leftRotor);
  right.attach(rightRotor);
  left.write(servoMin);
  right.write(servoMin);
  //int potStableVal = 550;

  
}

void loop() {
  // put your main code here, to run repeatedly:
  potentiometerValue = analogRead(potentiometerPin);
  if (potentiometerValue > 570){
    Serial.print("Right \t");
    int error_R = potentiometerValue - potStableVal;
    Serial.print(error_R);
    Serial.print("\t");
    int thrustR = getThrustValR(error_R);
    left.write(0);
    right.write(thrustR);
    //Serial.print("Right \t");
    //Serial.println(thrustR);
  }
  else if (potentiometerValue < 530){
    Serial.print("Left \t");
    int error_L = potStableVal - potentiometerValue;
    Serial.print(error_L);
    Serial.print("\t");
    int thrustL = getThrustValL(error_L); 
    right.write(0); 
    left.write(thrustL);
    //Serial.print("Left \t");
    //Serial.println(thrustL); 
  }

  else{
   right.write(0); 
   left.write(0);
  }
  Serial.flush();
  delay(dt);
}

int getThrustValR(float error_r){
  /*  This function takes the potentiometer value and 
   *  calculates the thrust value for right thruster with PID controller
   * thrust has the pwm value required to control the rotor for the potentiometer value
   */
  float p_err_r = kp*error_r;
  float d_err_r = kd*(error_r - prev_err_r)/(dt);
  float i_err_r =+ ki*error_r;
  float pid_err_r = p_err_r + d_err_r + i_err_r;
  
  float thrust_r = pid_err_r/(potMaxVal - potStableVal) * (servoMax - servoMin) + servoMin ;
  Serial.println(pid_err_r);
  prev_err_r = error_r;
  return thrust_r;
}

int getThrustValL(float error_l){
  /*  This function takes the potentiometer value and 
   *  calculates the thrust value for left thruster with PID controller
   * thrust has the pwm value required to control the rotor for the potentiometer value
   */
  float p_err_l = kp*error_l;
  float d_err_l = kd*(error_l - prev_err_l)/(dt);
  float i_err_l =+ ki*error_l;
  float pid_err_l = p_err_l + d_err_l + i_err_l;
  
  float thrust_l = pid_err_l/(potMaxVal - potStableVal) * (servoMax - servoMin) + servoMin ;
  Serial.println(pid_err_l);
  prev_err_l = error_l;
  return thrust_l;
}
