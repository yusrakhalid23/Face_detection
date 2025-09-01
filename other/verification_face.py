from deepface import DeepFace
import os
import time

target_img = "kashan.jpg"
db_path = "pic/"


results = DeepFace.find(img_path=target_img, db_path=db_path, enforce_detection=True)
if len(results[0]) > 0:
    print("YES")
    a = "YES"
else:
    print("NO")
    a = "NO"