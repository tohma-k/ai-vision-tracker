import cv2
import face_recognition
import sqlite3

DB_NAME = "faces.db"

def save_face(name, encoding):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    encoding_bytes = encoding.tobytes()

    cursor.execute(
        "INSERT INTO faces (name, encoding) VALUES (?, ?)",
        (name, encoding_bytes)
    )

    connection.commit()
    connection.close()

def main():
    name = input("Enter name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        return

    print("Press SPACE to capture face.")
    print("Press Q to quit.")

    while True:
        ret, frame = camera.read()

        if not ret:
            print("Could not read from camera.")
            break

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1)

        if key == ord(" "):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)

            if len(face_locations) == 0:
                print("No face detected. Try again.")
                continue

            if len(face_locations) > 1:
                print("More than one face detected. Only show one face.")
                continue

            face_encodings = face_recognition.face_encodings(
                rgb_frame,
                face_locations
            )

            encoding = face_encodings[0]

            save_face(name, encoding)

            print(f"Saved face for {name}.")
            break

        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()