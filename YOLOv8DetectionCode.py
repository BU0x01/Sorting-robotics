# Import necessary packages
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('yolov8n.pt')  # Pre-trained model

# Define plastic class names
plastic_classes = {0: 'PET', 1: 'HDPE', 2: 'PVC'}

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run object detection
    results = model(frame)

    # Loop through detected objects
    for r in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = map(int, r)
        label = plastic_classes.get(cls, 'Unknown')
        
        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{label} ({conf:.2f})', (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Send classification data to robotic arm
        send_to_arm(label, (x1, y1, x2, y2))

    # Display result
    cv2.imshow('Plastic Detection', frame)
    
    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
