# 🔒 Face Detection IoT System

## 📌 Project Overview
This project integrates **Computer Vision (OpenCV + DeepFace)** with **IoT (Arduino + Sensors/Actuators)** to build a **Smart Face Detection System**.  
It uses a webcam to detect and recognize faces in real-time. If no face or an unknown face is detected, the system turns on a buzzer and light for security alerts. When a known face is recognized, the alert system turns off automatically.

---

## 🚀 Key Features
- ✅ Real-time face detection using **OpenCV Haar Cascade**  
- ✅ Face recognition using **DeepFace** and a local image database  
- ✅ Serial communication with Arduino (`pySerial`)  
- ✅ Automatic control of **buzzer and light** (on unknown face detection)  
- ✅ GUI Alerts via **Tkinter Message Boxes**  
- ✅ Works with webcam for live monitoring  

---

## 🛠️ Tech Stack
- **Python Libraries**:  
  - OpenCV  
  - DeepFace  
  - TensorFlow  
  - Tkinter  
  - PySerial  

- **Hardware**:  
  - Arduino (with buzzer + LED/light)  
  - Webcam  

---

## ⚙️ How It Works
1. The webcam captures frames in real-time.  
2. OpenCV detects faces in the frame.  
3. If a face is detected:
   - DeepFace compares it against the stored face database (`pic/` folder).  
   - If recognized → Arduino receives `Y` → buzzer/light OFF.  
   - If not recognized → Arduino receives `N` → buzzer/light ON.  
4. If no face is detected, buzzer/light also turn ON as a warning.  
5. User can override alerts through Tkinter message box prompts.  

---

## 📂 Project Structure
