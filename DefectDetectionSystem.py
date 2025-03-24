# import required libraries
import cv2
import torch
import time
import numpy as np
from datetime import datetime

# Load YOLOv5 model
model_path = 'yolov5/best.pt'  # Path to fine-tuned model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

# Define camera source (0 for USB webcam or adjust for CSI camera)
camera_source = 0  # Use /dev/video0 for USB Camera or 'nvarguscamerasrc' for CSI camera

# Open video capture
cap = cv2.VideoCapture(camera_source)
if not cap.isOpened():
    print("Error: Unable to open camera.")
    exit()

# Set video frame size (optional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define confidence threshold for defect detection
CONFIDENCE_THRESHOLD = 0.5

# Start processing frames
print("Starting defect detection...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    # Perform inference with YOLOv5
    results = model(frame)

    # Extract detections and draw bounding boxes
    for det in results.xyxy[0]:  # detections per frame
        x1, y1, x2, y2, conf, cls = det

        if conf > CONFIDENCE_THRESHOLD:
            # Get label and confidence
            label = f'{model.names[int(cls)]}: {conf:.2f}'
            color = (0, 255, 0) if label.startswith('OK') else (0, 0, 255)  # Green for OK, Red for defect

            # Draw bounding box and label
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Save frame if defect detected
            if not label.startswith('OK'):
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                cv2.imwrite(f'defect_detected_{timestamp}.jpg', frame)
                print(f'Defect detected! Image saved as defect_detected_{timestamp}.jpg')

    # Show the frame
    cv2.imshow('Defect Detection - Packaging Quality', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
