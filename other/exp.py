import cv2
from deepface import DeepFace
import os
import time
import warnings
import tensorflow as tf
import serial as s

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', module='tensorflow')
tf.compat.v1.losses.sparse_softmax_cross_entropy(labels=[0, 1], logits=[[0.0, 1.0], [1.0, 0.0]])

ser = s.Serial('COM3', 9600, timeout = 0)


db_path = "pic/"
# Load the pre-trained Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the video capture object (0 for default webcam)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the faces and capture image if faces detected
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
       # Capture the image when a face is detected
        cv2.imwrite('detected_face.jpg', frame)
        print("Image captured because face detected.")
        # Add a delay of 2 seconds
        time.sleep(2)
        # Use DeepFace to find matches in the database
        results = DeepFace.find(img_path="detected_face.jpg", db_path=db_path, enforce_detection=True)
        if len(results[0]) > 0:
            print("YES")
            a = "YES"
        else:
            print("NO")
            a = "NO"
                  
        
        
        break

    # Display the resulting frame
    cv2.imshow('Live Face Detection', frame)

    # # Add a delay of 2 seconds
    # time.sleep(60)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()