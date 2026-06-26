import cv2
import face_recognition
import sqlite3
import numpy as np
import serial
import time

DB_NAME = "faces.db"
ARDUINO_PORT = "COM9"
BAUD_RATE = 9600

def load_faces():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name, encoding FROM faces")
    rows = cursor.fetchall()

    connection.close()

    names = []
    encodings = []

    for name, encoding_bytes in rows:
        encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
        names.append(name)
        encodings.append(encoding)

    return names, encodings

def send_to_arduino(arduino, message, last_message):
    if message != last_message:
        arduino.write((message + "\n").encode())
        print("Sent:", message)
        return message

    return last_message

def main():
    known_names, known_encodings = load_faces()

    if len(known_encodings) == 0:
        print("No faces in database. Run register_face.py first.")
        return

    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE)
    time.sleep(2)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        arduino.close()
        return

    last_message = ""

    print("Recognition started. Press Q to quit.")

    while True:
        ret, frame = camera.read()

        if not ret:
            print("Could not read from camera.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame,
            face_locations
        )

        if len(face_encodings) == 0:
            last_message = send_to_arduino(
                arduino,
                "NOT_FOUND",
                last_message
            )

        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            best_match_index = np.argmin(face_distances)
            best_distance = face_distances[best_match_index]

            if best_distance < 0.5:
                name = known_names[best_match_index]
                status = "VERIFIED"
                label = f"{name} - VERIFIED"
                color = (0, 255, 0)
                message = f"{name},VERIFIED"
            else:
                name = "Unknown"
                status = "NOT VERIFIED"
                label = "Unknown - NOT VERIFIED"
                color = (0, 0, 255)
                message = "Unknown,NOT_VERIFIED"

            last_message = send_to_arduino(
                arduino,
                message,
                last_message
            )

            top, right, bottom, left = face_location

            # Scale box back up because detection was done on 1/4 size frame
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw rectangle around face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw filled rectangle for label background
            cv2.rectangle(
                frame,
                (left, bottom - 25),
                (right, bottom),
                color,
                cv2.FILLED
            )

            # Draw label text
            cv2.putText(
                frame,
                label,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.5,
                (255, 255, 255),
                1
            )

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    camera.release()
    arduino.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()