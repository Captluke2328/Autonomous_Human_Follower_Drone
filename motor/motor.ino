
#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_DCMotor *Motor1 = AFMS.getMotor(1);
Adafruit_DCMotor *Motor2 = AFMS.getMotor(2);
Adafruit_DCMotor *Motor3 = AFMS.getMotor(3);
Adafruit_DCMotor *Motor4 = AFMS.getMotor(4);

#define numofvaluereceive 2
#define digitpervaluereceive 4 //-255,0255 (4 digits due to negative signs)

int valreceive[numofvaluereceive];
int stringlength = numofvaluereceive * digitpervaluereceive + 1;
int defaultSpeed = 0;

int counter = 0;
bool counterstart = false;
String receivestring;

void setup() {
  Serial.begin(9600);
  AFMS.begin();
  Motor1 -> setSpeed(defaultSpeed);
  Motor2 -> setSpeed(defaultSpeed);
  Motor3 -> setSpeed(defaultSpeed);
  Motor4 -> setSpeed(defaultSpeed);
}

void receivedata() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '$') {
      counterstart = true;
    }
    if (counterstart) {
      if (counter < stringlength) {
        receivestring = String(receivestring + c);
        counter++;
        //$050255
      }
      if (counter >= stringlength) {
        for (int i = 0; i < numofvaluereceive; i++)
        {
          int num = (i * digitpervaluereceive) + 1;
          valreceive[i] = receivestring.substring(num, num + digitpervaluereceive).toInt();
          //valreceive[0] = receivestring.substring(1,4).toInt();
          //valreceive[1] = receivestring.substring(4,7).toInt();
        }
        receivestring = "";
        counter = 0;
        counterstart = false;
      }
    }
  }
}

void moveRobot(int mySpeed, int myTurn, int maxSpeed=255){
  mySpeed = map(mySpeed,-100,100, -maxSpeed, maxSpeed);
  myTurn = map(myTurn,-100,100, -maxSpeed, maxSpeed);

  int leftSpeed = mySpeed - myTurn;
  int rightSpeed = mySpeed + myTurn;

  leftSpeed = constrain(leftSpeed, -maxSpeed, maxSpeed);
  rightSpeed = constrain(rightSpeed, -maxSpeed, maxSpeed);


  if (leftSpeed > 0){
    Motor1 -> run(BACKWARD);
    Motor2 -> run(FORWARD);
    Motor3 -> run(FORWARD);
    Motor4 -> run(BACKWARD); 
  }

  else{
    Motor1 -> run(FORWARD);
    Motor2 -> run(BACKWARD);
    Motor3 -> run(BACKWARD);
    Motor4 -> run(FORWARD); 
  }

  if (rightSpeed > 0){
    Motor1 -> run(BACKWARD);
    Motor2 -> run(FORWARD);
    Motor3 -> run(FORWARD);
    Motor4 -> run(BACKWARD); 
  }
  else{
    Motor1 -> run(FORWARD);
    Motor2 -> run(BACKWARD);
    Motor3 -> run(BACKWARD);
    Motor4 -> run(FORWARD); 
  }

  Motor1 -> setSpeed(abs(leftSpeed));
  Motor2 -> setSpeed(abs(rightSpeed));
  Motor3 -> setSpeed(abs(rightSpeed));
  Motor4 -> setSpeed(abs(leftSpeed));
}

void loop() {
  receivedata();
  moveRobot(valreceive[0], valreceive[1]);
}
