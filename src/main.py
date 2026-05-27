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

    # Process detections
    for box in results[0].boxes:

        confidence = float(box.conf[0])

        # Ignore weak detections
        if confidence < 0.5:
            continue

        class_id = int(box.cls[0])
        label = model.names[class_id]

        # Bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Target center
        target_center_x = (x1 + x2) // 2
        target_center_y = (y1 + y2) // 2

        # Error values
        error_x = target_center_x - screen_center_x
        error_y = target_center_y - screen_center_y

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Draw target center
        cv2.circle(
            frame,
            (target_center_x, target_center_y),
            5,
            (0, 0, 255),
            -1
        )

        # Draw line from screen center to target
        cv2.line(
            frame,
            (screen_center_x, screen_center_y),
            (target_center_x, target_center_y),
            (255, 0, 0),
            2
        )

        # Label text
        label_text = f"{label} {confidence:.2f}"

        cv2.putText(
            frame,
            label_text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        # Error display
        error_text = f"error_x: {error_x}  error_y: {error_y}"

        cv2.putText(
            frame,
            error_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # Only track first detected object for now
        break

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

    # Show frame
    cv2.imshow("AI Vision Tracker", frame)

    # Quit with q key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()