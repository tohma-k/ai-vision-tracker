import serial
import time

arduino = serial.Serial('COM9', 9600)

time.sleep(2)

while True:
    status = input("verified? (y/n): ")
    if (status == "y"):
        arduino.write(b"VERIFIED\n")
    elif (status == "n"):
        arduino.write(b"NOT_VERIFIED\n")
    elif (status == "q"):
        break
    else:
        print("Invalid input")