import cv2
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize a variable to store the captured face image
captured_face_img = None
webcam_active = True  # Flag to keep track of webcam state

# Function to continuously update the image label with the webcam feed
def update_frame():
    global cap, img_label, captured_face_img, webcam_active

    if webcam_active:
        # Capture a frame from the webcam
        ret, frame = cap.read()
        if ret:
            # Resize the frame to make the webcam feed smaller
            frame = cv2.resize(frame, (200, 150))  # Width=200, Height=150

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) > 0:
                # Draw a rectangle around the detected face
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Convert the frame to RGB for Tkinter and PIL
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img)

            # Display the webcam feed in the Tkinter window
            img_label.config(image=img_tk)
            img_label.image = img_tk

        # Continue updating the frame every 20 ms
        root.after(20, update_frame)

# Function to capture an image with face detection
def capture_image():
    global cap, img_label, captured_face_img, webcam_active

    # Capture a frame from the webcam
    ret, frame = cap.read()
    if ret:
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            # Assume we are interested in the first detected face
            (x, y, w, h) = faces[0]

            # Draw a rectangle around the detected face (optional)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Crop the face from the frame
            face_img = frame[y:y+h, x:x+w]

            # Resize the captured face image to a smaller size (e.g., 150x150)
            face_img_resized = cv2.resize(face_img, (150, 150))  # Width=150, Height=150

            # Convert the face to RGB for Tkinter and PIL
            img = cv2.cvtColor(face_img_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            captured_face_img = img  # Store the captured face image

            # Display the captured face image with a broad border
            img_tk = ImageTk.PhotoImage(image=img)
            img_label.config(image=img_tk, bd=10, relief="solid")
            img_label.image = img_tk

            # Stop the webcam feed
            webcam_active = False

            messagebox.showinfo("Image Capture", "Face captured successfully! You can now save it.")
        else:
            messagebox.showwarning("Face Detection", "No face detected. Please try again.")
    else:
        messagebox.showerror("Image Capture", "Failed to capture image")

# Function to save the captured image with the specified name
def save_image():
    global captured_face_img

    if captured_face_img is None:
        messagebox.showwarning("Save Image", "No image to save. Please capture an image first.")
        return

    image_name = image_name_entry.get().strip()
    if not image_name:
        messagebox.showwarning("Save Image", "Please enter a name for the image.")
        return
    db_path = "pic/"
    # Save the face image to a file with the given name
    image_filename = os.path.join(db_path, f"{image_name}.jpg")
    captured_face_img.save(image_filename)
    messagebox.showinfo("Save Image", f"Image saved successfully as {image_filename}!")

# Set up the main Tkinter window
root = Tk()
root.title("Capture Face Image")

# Disable maximize button
root.resizable(False, False)

# Set the window size to 600x400 pixels
root.geometry("600x400")

# Create and pack the left_frame
left_frame = Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ns')

# Create and position the right_frame at the top-right corner
right_frame = Frame(root)
right_frame.grid(row=0, column=2, padx=90, pady=10, sticky='ne')

# Add label and entry for the image name on the left side
image_name_label = Label(left_frame, text="Enter Image Name:")
image_name_label.grid(row=0, column=0, pady=(10, 0))

image_name_entry = Entry(left_frame)
image_name_entry.grid(row=0, column=2, padx=(8, 0), pady=(20, 10))

# Create buttons for capturing and saving the image on the left side
capture_button = Button(left_frame, text="Capture Face", command=capture_image)
capture_button.grid(row=1, column=0, columnspan=2, pady=10)

save_button = Button(left_frame, text="Save Image", command=save_image)
save_button.grid(row=1, column=2, columnspan=2, pady=10)

# Create a label to display the captured image on the right side
img_label = Label(right_frame, bd=5, relief="solid")  # Adding a broad border
img_label.pack()

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Start updating the frame
update_frame()

# Run the Tkinter main loop
root.mainloop()

# Release the webcam when the application is closed
cap.release()
