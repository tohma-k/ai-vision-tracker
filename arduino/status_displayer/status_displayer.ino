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
    String message = Serial.readStringUntil('\n');
    message.trim();

    lcd.clear();

    if (message == "NOT_FOUND") {
      lcd.setCursor(0, 0);
      lcd.print("NOT FOUND");

      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, LOW);
      return;
    }

    int commaIndex = message.indexOf(',');
    String name = message.substring(0, commaIndex);
    String status = message.substring(commaIndex + 1);

    lcd.setCursor(0, 0);
    lcd.print(name);

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