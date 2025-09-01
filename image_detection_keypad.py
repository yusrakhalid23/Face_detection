import serial
import tkinter as tk
from tkinter import messagebox
import cv2
from deepface import DeepFace
import os
import time
import warnings
import threading
import tensorflow as tf

# Configure TensorFlow and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', module='tensorflow')
tf.compat.v1.losses.sparse_softmax_cross_entropy(labels=[0, 1], logits=[[0.0, 1.0], [1.0, 0.0]])

# Initialize Tkinter root for message boxes
root = tk.Tk()
root.withdraw()  # Hide the main window

# Initialize serial communication
try:
    ser = serial.Serial('COM3', 9600, timeout=0)  # Adjust COM port as necessary
except serial.SerialException as e:
    print(f"Error: Could not open serial port. {e}")
    exit()

db_path = "pic/"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

face_detection_running = False
stop_event = threading.Event()
detection_thread = None

def start_face_detection():
    global face_detection_running
    global stop_event
    global detection_thread

    if face_detection_running:
        print("Face detection is already running.")
        return

    face_detection_running = True
    stop_event.clear()
    print("Face detection started.")

    def face_detection_loop():
        global face_detection_running
        global stop_event

        try:
            while face_detection_running and not stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                    response = messagebox.askyesno("Alert", "Failed to capture frame! Do you want to turn off the light and buzzer?")
                    if response:
                        ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                        print("Turning off the light and buzzer.")
                        time.sleep(2)  # Add delay before checking again
                    continue  # Skip further processing in this loop iteration

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(faces) == 0:
                    ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                    response = messagebox.askyesno("Alert", "No face detected! Do you want to turn off the light and buzzer?")
                    if response:
                        ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                        print("Turning off the light and buzzer.")
                        time.sleep(2)  # Add delay before checking again
                    continue  # Skip further processing in this loop iteration

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.imwrite('detected_face.jpg', frame)
                    print("Image captured because face detected.")
                    time.sleep(1)  # Optional small delay to simulate processing time

                    try:
                        if not os.listdir(db_path):
                            ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                            response = messagebox.askyesno("Alert", "No images in the database! Do you want to turn off the light and buzzer?")
                            if response:
                                ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                                print("Turning off the light and buzzer.")
                                time.sleep(2)  # Add delay before checking again
                        else:
                            results = DeepFace.find(img_path="detected_face.jpg", db_path=db_path, enforce_detection=True)
                            if len(results[0]) > 0:
                                print("Face recognized: YES")
                                ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                            else:
                                print("Face not recognized: NO")
                                ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                                response = messagebox.askyesno("Alert", "Face not recognized! Do you want to turn off the light and buzzer?")
                                if response:
                                    ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                                    print("Turning off the light and buzzer.")
                                    time.sleep(2)  # Add delay before checking again

                    except Exception as e:
                        print(f"Error during face recognition: {e}")
                        ser.write(b'N')  # Send 'N' to Arduino to turn on both the light and buzzer
                        response = messagebox.askyesno("Alert", "Error occurred! Do you want to turn off the light and buzzer?")
                        if response:
                            ser.write(b'Y')  # Send 'Y' to Arduino to turn off both the light and buzzer
                            print("Turning off the light and buzzer.")
                            time.sleep(10)  # Add delay before checking again

                cv2.imshow('Live Face Detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting...")
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

    # Start face detection in a separate thread
    detection_thread = threading.Thread(target=face_detection_loop)
    detection_thread.start()

def stop_face_detection():
    global face_detection_running
    global stop_event
    global detection_thread

    if not face_detection_running:
        print("Face detection is not running.")
        return

    face_detection_running = False
    stop_event.set()  # Signal the detection loop to stop

    if detection_thread and detection_thread.is_alive():
        detection_thread.join()  # Wait for the thread to finish
    print("Face detection stopped.")

def check_serial():
    if ser.in_waiting:
        data = ser.readline().decode().strip()
        print(f"Received data: {data}")  # Debugging print

        if data == "START":
            alert_password_request("START")
        elif data == "STOP":
            alert_password_request("STOP")
        elif data == "Password Correct":
            if pending_command == "START":
                start_face_detection()
            elif pending_command == "STOP":
                stop_face_detection()
        elif data == "Password Incorrect":
            show_password_status("Password Incorrect")

    root.after(100, check_serial)  # Check again after 100ms

def alert_password_request(command):
    global pending_command
    pending_command = command
    alert = tk.Toplevel(root)
    alert.title("Password Alert")
    tk.Label(alert, text="Please enter the password on the keypad.").pack(pady=20)
    alert.after(2000, alert.destroy)  # Close alert after 2 seconds

def show_password_status(status):
    status_alert = tk.Toplevel(root)
    status_alert.title("Password Status")
    tk.Label(status_alert, text=status).pack(pady=20)
    status_alert.after(2000, status_alert.destroy)  # Close status alert after 2 seconds

# Initialize pending command
pending_command = None

# Start checking for serial data
check_serial()

# Run the Tkinter main loop
root.mainloop()
