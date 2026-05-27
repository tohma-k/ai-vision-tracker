import cv2
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

print("Press 'q' to quit.")

prev_time = time.time()

while True:
    # Read frame from webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame.")
        break

    # Run YOLO inference
    results = model(frame, verbose=False)

    # Get frame dimensions
    frame_height, frame_width = frame.shape[:2]

    # Screen center
    screen_center_x = frame_width // 2
    screen_center_y = frame_height // 2

    # Draw screen center
    cv2.circle(
        frame,
        (screen_center_x, screen_center_y),
        5,
        (255, 255, 255),
        -1
    )

    best_target = None
    best_distance = float("inf")

    for box in results[0].boxes:

        confidence = float(box.conf[0])

        if confidence < 0.5:
            continue

        class_id = int(box.cls[0])
        label = model.names[class_id]

        # Track ONLY people
        if label != "person":
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        target_center_x = (x1 + x2) // 2
        target_center_y = (y1 + y2) // 2

        # Distance from screen center
        distance = (
            (target_center_x - screen_center_x) ** 2 +
            (target_center_y - screen_center_y) ** 2
        ) ** 0.5

        # Choose closest target to center
        if distance < best_distance:
            best_distance = distance
            best_target = {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "center_x": target_center_x,
                "center_y": target_center_y,
                "label": label,
                "confidence": confidence
            }

    # Draw chosen target
    if best_target:

        error_x = best_target["center_x"] - screen_center_x
        error_y = best_target["center_y"] - screen_center_y

        # Bounding box
        cv2.rectangle(
            frame,
            (best_target["x1"], best_target["y1"]),
            (best_target["x2"], best_target["y2"]),
            (0, 255, 0),
            2
        )

        # Target center
        cv2.circle(
            frame,
            (best_target["center_x"], best_target["center_y"]),
            5,
            (0, 0, 255),
            -1
        )

        # Tracking line
        cv2.line(
            frame,
            (screen_center_x, screen_center_y),
            (best_target["center_x"], best_target["center_y"]),
            (255, 0, 0),
            2
        )

        # Label
        label_text = (
            f'{best_target["label"]} '
            f'{best_target["confidence"]:.2f}'
        )

        cv2.putText(
            frame,
            label_text,
            (best_target["x1"], best_target["y1"] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        # Error display
        cv2.putText(
            frame,
            f"error_x: {error_x} error_y: {error_y}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
    # FPS calculation
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display FPS
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # Show webcam frame
    cv2.imshow("AI Vision Tracker", frame)

    # Quit with q key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()