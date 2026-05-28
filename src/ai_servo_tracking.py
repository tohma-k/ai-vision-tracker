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

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

# -----------------------------
# SERVO VARIABLES
# -----------------------------

servo_angle = 90

# smoothing
smoothed_x = None
alpha = 0.15

prev_time = time.time()

last_servo_update = time.time()
servo_update_interval = 0.15

print("Press q to quit.")

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, verbose=False)

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

        smoothed_x = int(
            alpha * best_target["center_x"] +
            (1 - alpha) * smoothed_x
        )

        error_x = smoothed_x - screen_center_x

        # ---------------------------------
        # SERVO CONTROL
        # ---------------------------------

        deadzone = 40

        current_time = time.time()

        if abs(error_x) > deadzone and current_time - last_servo_update > servo_update_interval:

            adjustment = int(error_x * 0.01)

            servo_angle -= adjustment

            servo_angle = max(0, min(180, servo_angle))

            arduino.write(f"{servo_angle}\n".encode())

            print(f"error_x: {error_x}, servo_angle: {servo_angle}")

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
            (smoothed_x, best_target["center_y"]),
            5,
            (0, 0, 255),
            -1
        )

        cv2.line(
            frame,
            (screen_center_x, screen_center_y),
            (smoothed_x, best_target["center_y"]),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"Servo Angle: {servo_angle}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    # -----------------------------
    # FPS
    # -----------------------------

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("AI Servo Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -----------------------------
# CLEANUP
# -----------------------------

arduino.close()

cap.release()

cv2.destroyAllWindows()