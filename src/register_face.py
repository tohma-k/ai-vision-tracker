import cv2
import face_recognition
import pickle
import os

DB_FILE = "faces.pkl"

name = input("Enter name: ")

camera = cv2.VideoCapture(0)
print("Press SPACE to capture face. Press Q to quit.")

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    cv2.imshow("Register Face", frame)
    
    key = cv2.waitKey(1)
    
    if key == ord(" "):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        
        if len(face_locations) == 0:
            print("No face found. Try again.")
            continue
        
        encoding = face_recognition.face_encodings(rgb, face_locations)[0]
        
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "rb") as f:
                database = pickle.load(f)
        
        else:
            database = []
            
        database.append({
            "name": name,
            "encoding": encoding
        })
        
        with open(DB_FILE, "wb") as f:
            pickle.dump(database, f)
        
        print(f"Saved face for {name}")
        break
    
    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()