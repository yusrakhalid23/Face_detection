import cv2
from deepface import DeepFace
import os
import time
import warnings
import tensorflow as tf
import serial as s
from tkinter import Tk, messagebox

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', module='tensorflow')
tf.compat.v1.losses.sparse_softmax_cross_entropy(labels=[0, 1], logits=[[0.0, 1.0], [1.0, 0.0]])

# Initialize serial communication
try:
    ser = s.Serial('COM3', 9600, timeout=0)  # Adjust COM port as necessary
except s.SerialException as e:
    print(f"Error: Could not open serial port. {e}")
    exit()

db_path = "pic/"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize Tkinter root for message box
root = Tk()
root.withdraw()  # Hide the root window

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            # No face detected, turn on buzzer and light
            print("No face detected.")
            ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
            # Display message box to user
            response = messagebox.askyesno("Alert", "No face detected! Do you want to turn off the light and buzzer?")
            if response:
                ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                print("Turning off the light and buzzer.")
                time.sleep(2)  # Add delay before checking again
            else:
                print("Light and buzzer remain on.")

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite('detected_face.jpg', frame)
            print("Image captured because face detected.")
            time.sleep(1)  # Optional small delay to simulate processing time

            try:
                # Check if the database path has images
                if not os.listdir(db_path):
                    print("No images found in the database folder.")
                    ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                    response = messagebox.askyesno("Alert", "No images in the database! Do you want to turn off the light and buzzer?")
                    if response:
                        ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                        print("Turning off the light and buzzer.")
                        time.sleep(2)  # Add delay before checking again
                    else:
                        print("Light and buzzer remain on.")
                else:
                    results = DeepFace.find(img_path="detected_face.jpg", db_path=db_path, enforce_detection=True)

                    if len(results[0]) > 0:
                        print("Face recognized: YES")
                        ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                    else:
                        print("Face not recognized: NO")
                        ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                        # Display message box to user
                        response = messagebox.askyesno("Alert", "Face not recognized! Do you want to turn off the light and buzzer?")
                        if response:
                            ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                            print("Turning off the light and buzzer.")
                            time.sleep(2)  # Add delay before checking again
                        else:
                            print("Light and buzzer remain on.")

            except Exception as e:
                print(f"Error during face recognition: {e}")
                ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                # Display message box to user
                response = messagebox.askyesno("Alert", "Error occurred! Do you want to turn off the light and buzzer?")
                if response:
                    ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                    print("Turning off the light and buzzer.")
                    time.sleep(5)  # Add delay before checking again
                else:
                    print("Light and buzzer remain on.")

        cv2.imshow('Live Face Detection', frame)

        # Check for 'q' press to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    if ser.is_open:
        ser.close()  # Close the serial port when done
    print("Cleaned up resources.")
