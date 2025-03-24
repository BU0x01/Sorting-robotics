#include <Servo.h>

Servo base, shoulder, elbow, gripper;

// Pin assignments
const int BASE_PIN = 9;
const int SHOULDER_PIN = 10;
const int ELBOW_PIN = 11;
const int GRIPPER_PIN = 12;

void setup() {
  Serial.begin(9600);
  
  // Attach servos
  base.attach(BASE_PIN);
  shoulder.attach(SHOULDER_PIN);
  elbow.attach(ELBOW_PIN);
  gripper.attach(GRIPPER_PIN);
  
  moveHome();  // Move arm to home position
}

void loop() {
  if (Serial.available() > 0) {
    String plasticType = Serial.readStringUntil('\n');

    if (plasticType == "PET") {
      moveToBin(0);  // Bin 0 for PET
    } else if (plasticType == "HDPE") {
      moveToBin(1);
    } else if (plasticType == "PVC") {
      moveToBin(2);
    }

    delay(500);
    moveHome();  // Return to home position
  }
}

void moveToBin(int bin) {
  switch (bin) {
    case 0:  // PET
      base.write(45);
      shoulder.write(120);
      elbow.write(90);
      gripper.write(45);
      delay(1000);
      gripper.write(90);  // Release object
      break;

    case 1:  // HDPE
      base.write(90);
      shoulder.write(110);
      elbow.write(80);
      gripper.write(45);
      delay(1000);
      gripper.write(90);
      break;

    case 2:  // PVC
      base.write(135);
      shoulder.write(100);
      elbow.write(70);
      gripper.write(45);
      delay(1000);
      gripper.write(90);
      break;
  }
}

void moveHome() {
  base.write(90);
  shoulder.write(90);
  elbow.write(90);
  gripper.write(90);
}
