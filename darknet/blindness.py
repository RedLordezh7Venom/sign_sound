import cv2
import numpy as np
import tensorflow as tf
import pyttsx3

# Load YOLO model
net = cv2.dnn.readNet("C:\\Users\\prabh\\darknet\\yolov3.weights", "C:\\Users\\prabh\\darknet\\cfg\\yolov3.cfg")
classes = []

with open("C:\\Users\\prabh\\darknet\\data\\coco.names", "r") as f:
    classes = [line.strip() for line in f]

# Initialize TTS engine
engine = pyttsx3.init()

# Function to get object directions
def get_directions(obj_center, frame_center):
    x, y = obj_center
    fx, fy = frame_center
    threshold = 50

    if x < fx - threshold:
        return "Move right"
    elif x > fx + threshold:
        return "Move left"
    elif y < fy - threshold:
        return "Move down"
    elif y > fy + threshold:
        return "Move up"
    else:
        return "Object centered"

# Function to detect objects and provide instructions
def detect_objects(frame, output_frame):
    height, width, _ = frame.shape
    frame_center = (width // 2, height // 2)

    # YOLO preprocessing
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Get YOLO output layer names
    layer_names = net.getUnconnectedOutLayersNames()

    # Run YOLO forward pass
    detections = net.forward(layer_names)

    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes[class_id] == "person":
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                object_center = (center_x, center_y)

                # Draw bounding box
                cv2.rectangle(output_frame, (center_x-30, center_y-30), (center_x+30, center_y+30), (0, 255, 0), 2)

                # Get and display directions
                directions = get_directions(object_center, frame_center)
                cv2.putText(output_frame, directions, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Speak directions
                engine.say(directions)
                engine.runAndWait()

    return output_frame

# Video capture from webcam (0 for default webcam)
cap = cv2.VideoCapture(0)

# Create a separate window for output
cv2.namedWindow("Obstacle Detection Output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Obstacle Detection Output", 800, 600)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Create a copy of the frame for output
    output_frame = frame.copy()

    # Detect objects and provide instructions
    output_frame = detect_objects(frame, output_frame)

    # Display the output frame
    cv2.imshow("Obstacle Detection Output", output_frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()