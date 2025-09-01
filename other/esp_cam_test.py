import serial
import numpy as np
import cv2

# Replace with the correct serial port for your ESP32-CAM (e.g., 'COM3' for Windows, '/dev/ttyUSB0' for Linux)
serial_port = '/dev/ttyUSB0'
baud_rate = 115200  # This should match the baud rate set in the ESP32-CAM code

# Open the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Frame parameters
frame_width = 640  # Adjust according to the camera frame size
frame_height = 480

# Buffer for storing the incoming frame data
frame_buffer = bytearray()

while True:
    # Read bytes from serial
    bytes_to_read = ser.inWaiting()
    if bytes_to_read > 0:
        data = ser.read(bytes_to_read)
        frame_buffer.extend(data)

        # Look for the JPEG end marker (0xFFD9)
        if len(frame_buffer) > 2 and frame_buffer[-2:] == b'\xff\xd9':
            # Convert the buffer to a numpy array
            jpg_frame = np.frombuffer(frame_buffer, dtype=np.uint8)

            # Decode the JPEG frame
            img = cv2.imdecode(jpg_frame, cv2.IMREAD_COLOR)

            # Display the frame
            if img is not None:
                cv2.imshow('ESP32-CAM Video Stream', img)

            # Clear the buffer for the next frame
            frame_buffer = bytearray()

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Close the serial port and the OpenCV window
ser.close()
cv2.destroyAllWindows()
