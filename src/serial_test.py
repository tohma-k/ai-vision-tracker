import serial
import time

arduino = serial.Serial("COM9", 9600, timeout=1)
time.sleep(2)

print("Connected to Arduino.")
print("Enter angle from 0 to 180. Type q to quit.")

while True:
    angle = input("Angle: ")

    if angle.lower() == "q":
        break

    if not angle.isdigit():
        print("Enter a number.")
        continue

    value = int(angle)

    if value < 0 or value > 180:
        print("Angle must be 0-180.")
        continue

    arduino.write(f"{value}\n".encode())
    print(f"Sent: {value}")

arduino.close()