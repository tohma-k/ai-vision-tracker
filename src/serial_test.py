import serial
import time

arduino = serial.Serial("COM9", 9600, timeout=1)
time.sleep(2)

print("Enter pan,tilt values like 90,90. Type q to quit.")

while True:
    command = input("Pan,Tilt: ")

    if command.lower() == "q":
        break

    arduino.write(f"{command}\n".encode())

arduino.close()