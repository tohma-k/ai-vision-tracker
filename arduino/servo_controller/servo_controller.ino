#include <Servo.h>

Servo panServo;
Servo tiltServo;

int panAngle = 90;
int tiltAngle = 90;

void setup() {
    Serial.begin(9600);

    panServo.attach(9);
    tiltServo.attach(10);

    panServo.write(panAngle);
    tiltServo.write(tiltAngle);
}

void loop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');

        int commaIndex = input.indexOf(',');

        if (commaIndex > 0) {
            int pan = input.substring(0, commaIndex).toInt();
            int tilt = input.substring(commaIndex + 1).toInt();

            panAngle = constrain(pan, 30, 150);
            tiltAngle = constrain(tilt, 60, 125);

            panServo.write(panAngle);
            tiltServo.write(tiltAngle);
        }
    }
}