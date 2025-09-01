from deepface import DeepFace
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import os

image1 = r"image1.png"
image2 = r"image3.png"

result = DeepFace.verify(img1_path = image1,img2_path = image2,enforce_detection=False)

print(result)
