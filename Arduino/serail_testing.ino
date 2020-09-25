int i = 1;

void setup(){
  Serial.begin(9600);
}

void loop(){
  if (i > 10){
    i = 1;
  }
  Serial.println(String(i));
  i++;   
  delay(1000);
}
