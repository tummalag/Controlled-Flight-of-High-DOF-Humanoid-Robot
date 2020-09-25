#include <Servo.h>

// Desired Values
double theta_D = 15.0;         // angle in degree
int timer = 1000;

const int mot[] = {5,10}; // Initializing motor pins
const int mot_L = 0;      // mot[mot_L] is to control left motor. (yellow wire)
const int mot_R = 1;      // similarly for right motor (white wire)

const double mot_PWM_offset[] = {60,60}; // Motor offset value.

Servo left;               // Creating 2 servos left and right
Servo right;
const double servoMin = 0.0;  // servo PWM min value
const double servoMax = 100.0; // servo PWM max value

int potentiometerPin = A1;
const int potRefVal = 550;  // Refereance Value
const int potMinVal = 250;  // Left most value -45 degree
const int potMaxVal = 850;  // Right most value +45 degree

// Gain constants
const double kp = 0.0919;
const double ki = 0.0;
const double kd = 0.0169;
double p_err = 0.0;
double i_err = 0.0;
double d_err = 0.0;
double prev_error = 0.0;
int const dt = 1000;

double getAngle() {
  int potentiometerValue = analogRead(potentiometerPin);
  double degree = enc2deg(potentiometerValue);
  //Serial.println(potentiometerValue);
  return degree;
}

double enc2deg(double enc){
  double deg = (enc - potRefVal)/(potRefVal - potMinVal)*30;
  return deg;
}

int val2PWM(double val){
  double thrustInPWM = val * (servoMax - servoMin) + servoMin ;
  if( thrustInPWM > servoMax ) thrustInPWM = servoMax;
  if( thrustInPWM < servoMin ) thrustInPWM = servoMin;
  return (int)thrustInPWM;
}
int setMotor(double val){
  double absVal = abs(val);
  val = min(val, 1.0);
  val = max(val,-1.0);
  if (val > 0.0){
    setMotorThrust(mot[mot_L],absVal);
    setMotorThrust(mot[mot_R],servoMin);
    return 0;
  }
   else{
    setMotorThrust(mot[mot_R],absVal);
    setMotorThrust(mot[mot_L],servoMin);
    return 0;
  } 
  return 1;
}

int setMotorThrust(int servo, double err){
  if (servo == mot[mot_L]){
    int thrust = val2PWM(err);
    thrust = min(thrust , servoMax +  mot_PWM_offset[mot_L]);
    thrust = max(thrust + mot_PWM_offset[mot_L] , mot_PWM_offset[mot_L]);
    left.write(thrust);
    //Serial.print("left   ");
    //Serial.println(thrust);
    return 0;
  }
  else{// (servo == mot[mot_R]){
    int thrust = val2PWM(err);
    thrust = min(thrust , servoMax +  mot_PWM_offset[mot_R]);
    thrust = max(thrust + mot_PWM_offset[mot_R] , mot_PWM_offset[mot_R]);
    right.write(thrust);
    //Serial.print("right   ");
    //Serial.println(thrust );
    return 0;
  }
  return 1;
}

int startUp(){
  left.write(45);
  right.write(45);
  delay(2000);
  return 0;
}
//int pid(error){
//}
void setup() {
  Serial.begin(115200);
  //Serial.println("Bot is ready to fly!!");
  pinMode(mot[mot_L],OUTPUT);
  pinMode(mot[mot_R],OUTPUT);
  left.attach(mot[mot_L]);
  right.attach(mot[mot_R]);
  startUp();
  left.write(65);
  right.write(65);
  delay(1000);
  //left.write(mot_PWM_offset[mot_L]);
  //right.write(mot_PWM_offset[mot_R]);
  //delay(2000);
}

void loop() {
  double theta = getAngle();
  double error = theta_D - theta;
  i_err += (dt/1000)*error;
  d_err = (error-prev_error)/(dt/1000);
  double c = kp*error + ki*i_err + kd*d_err;
  prev_error = error;
  //Serial.print(c);
  // Adding threshold 
  c = max(min(c,0.411),0.0);
  setMotor(c);
  Serial.print(c);
  Serial.print("\t");
  Serial.println(theta);
  /*Serial.print(' ');
  //Serial.println(c);
  if ( timer < 0 ){
    timer = 1000;
    theta_D = -theta_D; 
  }
  timer--;
 */
  delay(10);
}
