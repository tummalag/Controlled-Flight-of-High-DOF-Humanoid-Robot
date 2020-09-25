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
}


void loop() {
  // put your main code here, to run repeatedly:
  int potentiometerValue =  analogRead(potentiometerPin);
  double degree = enc2deg(potentiometerValue);
  Serial.println(String(degree));
  delay(1);
}
