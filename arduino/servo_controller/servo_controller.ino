#include <Servo.h>

Servo panServo;

int currentAngle = 90;

void setup() {
    Serial.begin(9600);
    panServo.attach(9);
    panServo.write(currentAngle);
}

void loop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');

        int angle = input.toInt();
        angle = constrain(angle, 0, 180);

        currentAngle = angle;
        panServo.write(currentAngle);
    }
}