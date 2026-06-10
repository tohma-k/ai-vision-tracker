import cv2
import time
import serial
from ultralytics import YOLO

# -----------------------------
# SERIAL SETUP
# -----------------------------

arduino = serial.Serial("COM9", 9600, timeout=1)

time.sleep(2)

# -----------------------------
# YOLO SETUP
# -----------------------------

print("Loading YOLO model...")
model = YOLO("yolov8n.pt")
print("YOLO loaded.")

print("Opening webcam...")
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

print("Webcam connected.")
print("System ready.")

# -----------------------------
# SERVO VARIABLES
# -----------------------------

pan_angle = 90
tilt_angle = 90

PAN_MIN = 30
PAN_MAX = 150
TILT_MIN = 60
TILT_MAX = 125

deadzone_x = 30
deadzone_y = 30

kp_pan = 0.015
kp_tilt = 0.015

alpha = 0.13

servo_update_interval = 0.10
last_servo_update = time.time()

smoothed_x = None
smoothed_y = None

prev_time = time.time()

print("Press q to quit.")

# -----------------------------
# MAIN LOOP
# -----------------------------

fps_sum = 0.0
fps_count = 0
avg_fps = 0.0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, imgsz=320, verbose=False)

    frame_height, frame_width = frame.shape[:2]

    screen_center_x = frame_width // 2
    screen_center_y = frame_height // 2

    cv2.circle(
        frame,
        (screen_center_x, screen_center_y),
        5,
        (255, 255, 255),
        -1
    )

    best_target = None
    best_distance = float("inf")

    # -----------------------------
    # TARGET SELECTION
    # -----------------------------

    for box in results[0].boxes:

        confidence = float(box.conf[0])

        if confidence < 0.5:
            continue

        class_id = int(box.cls[0])
        label = model.names[class_id]

        if label != "person":
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        target_center_x = (x1 + x2) // 2
        target_center_y = (y1 + y2) // 2

        distance = (
            (target_center_x - screen_center_x) ** 2 +
            (target_center_y - screen_center_y) ** 2
        ) ** 0.5

        if distance < best_distance:
            best_distance = distance
            best_target = {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "center_x": target_center_x,
                "center_y": target_center_y,
                "confidence": confidence
            }

    # -----------------------------
    # TRACKING LOGIC
    # -----------------------------

    if best_target:
        if smoothed_x is None:
            smoothed_x = best_target["center_x"]
            smoothed_y = best_target["center_y"]

        smoothed_x = int(
            alpha * best_target["center_x"] +
            (1 - alpha) * smoothed_x
        )
        smoothed_y = int(
            alpha * best_target["center_y"] +
            (1 - alpha) * smoothed_y
        )

        error_x = smoothed_x - screen_center_x
        error_y = smoothed_y - screen_center_y

        # ---------------------------------
        # SERVO CONTROL
        # ---------------------------------

        current_time = time.time()
        
        if current_time - last_servo_update > servo_update_interval:
            if abs(error_x) > deadzone_x:
                pan_adjustment = error_x * kp_pan

                pan_angle -= pan_adjustment
                
            if abs(error_y) > deadzone_y:
                tilt_adjustment = error_y * kp_tilt
                
                tilt_angle -= tilt_adjustment
                
            pan_angle = max(PAN_MIN, min(PAN_MAX, pan_angle))
            tilt_angle = max(TILT_MIN, min(TILT_MAX, tilt_angle))
            
            arduino.write(f"{int(pan_angle)},{int(tilt_angle)}\n".encode())

            print(
                f"error_x: {error_x}, error_y: {error_y}, "
                f"pan: {pan_angle:.1f}, tilt: {tilt_angle:.1f}"
            )

            last_servo_update = current_time

        # ---------------------------------
        # VISUALIZATION
        # ---------------------------------

        cv2.rectangle(
            frame,
            (best_target["x1"], best_target["y1"]),
            (best_target["x2"], best_target["y2"]),
            (0, 255, 0),
            2
        )

        cv2.circle(
            frame,
            (smoothed_x, smoothed_y),
            5,
            (0, 0, 255),
            -1
        )

        cv2.line(
            frame,
            (screen_center_x, screen_center_y),
            (smoothed_x, smoothed_y),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"Pan: {int(pan_angle)} Tilt: {int(tilt_angle)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        cv2.putText(
            frame,
            f"error_x: {error_x} error_y: {error_y}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2,
        )

    # -----------------------------
    # FPS DISPLAY
    # -----------------------------

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    
    fps_sum += fps
    fps_count += 1
    avg_fps = fps_sum / fps_count

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )
    
    cv2.putText(
        frame,
        f"AVG FPS: {avg_fps:.1f}",
        (20, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("AI Pan-Tilt Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# CLEANUP
# -----------------------------

arduino.close()
cap.release()
cv2.destroyAllWindows()