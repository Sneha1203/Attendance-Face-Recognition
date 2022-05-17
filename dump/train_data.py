from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

import cv2
import os
import numpy as np



def train_images():
    data_dir = ('uploads')
    path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
    
    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')    # conversion to grayscale image
        image_np = np.array(img, 'uint8')
        # id = int(os.path.split(image)[1].split('.')[1])
        id = int(image.split(".")[1])
        faces.append(image_np)
        ids.append(id)
        # cv2.imshow('Training', image_np)
        cv2.waitKey(1) == 13
    ids = np.array(ids)

    classifier = cv2.face.LBPHFaceRecognizer_create()
    classifier.train(faces, ids)
    classifier.write('classifier.xml')
    cv2.destroyAllWindows()
        # messagebox.showinfo('Results', 'Data Sets Trained Successfully!', parent=self.root)

