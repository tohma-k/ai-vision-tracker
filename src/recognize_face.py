import cv2
import face_recognition
import pickle
import serial
import time

DB_FILE = "faces.pkl"
ARDUINO_PORT = "COM9"

arduino = serial.Serial(ARDUINO_PORT, 9600)
time.sleep(2)

with open(DB_FILE, "rb") as f:
    database = pickle.load(f)
    
known_names = [person["name"] for person in database]
known_encodings = [person["encoding"] for person in database]

camera = cv2.VideoCapture(0)

last_message = ""

def send_to_arduino(message):
    global last_message
    if message != last_message:
        arduino.write((message + " \n").encode())
        print("Sent:", message)
        last_message = message
        
while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)
    
    if len(face_encodings) == 0:
        send_to_arduino("NOT_FOUND")
    else:
        face_encoding = face_encodings[0]
        
        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.5
        )
        
        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
            send_to_arduino(f"{name},VERIFIED")
        else:
            send_to_arduino("Unknown, NOT_VERIFIED")
    
    cv2.imshow("Face Recognition", frame)
    
    if cv2.waitkey(1) == ord("q"):
        break

camera.release()
arduino.close()
cv2.destroyAllWindows()