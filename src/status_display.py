import serial
import time

arduino = serial.Serial('COM9', 9600)

time.sleep(2)

while True:
    if (input("verified? (y/n): ")):
        arduino.write(b"VERIFIED\n")
    else:
        arduino.write(b"NOT_VERIFIED\n")