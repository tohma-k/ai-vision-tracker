#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

const int greenLED = 2;
const int redLED = 3;

void setup() {
  Serial.begin(9600);

  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  lcd.begin(16, 2);

  lcd.print("Waiting...");
}

void loop() {
  if (Serial.available()) {
    String status = Serial.readStringUntil('\n');
    status.trim();

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Name");

    lcd.setCursor(0, 1);

    if (status == "VERIFIED") {
      lcd.print("VERIFIED");

      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
    }
    else if (status == "NOT_VERIFIED") {
      lcd.print("NOT VERIFIED");

      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);
    }
  }
}