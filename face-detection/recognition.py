import cv2
import csv
import os 
import numpy as np
from picamera2 import Picamera2
import time
from telegram_bot import enviarMensaje
from led import abrirPuerta

csv_file = 'names.csv'

#Parameters
id = 0
font = cv2.FONT_HERSHEY_COMPLEX
height=1
boxColor=(0,0,255)      #BGR- GREEN
nameColor=(255,255,255) #BGR- WHITE
confColor=(255,255,0)   #BGR- TEAL

face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
# names related to id
names = []
with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        names.append(row[0])

# Create an instance of the PiCamera2 object
cam = Picamera2()
## Initialize and start realtime video capture
# Set the resolution of the camera preview
cam.preview_configuration.main.size = (640, 360)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.controls.FrameRate=30
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

recognized = 0
timer = time.time()
while True:
    frame=cam.capture_array()

    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
            frameGray,      # The grayscale frame to detect
            scaleFactor=1.1,# how much the image size is reduced at each image scale-10% reduction
            minNeighbors=5, # how many neighbors each candidate rectangle should have to retain it
            minSize=(150, 150)# Minimum possible object size. Objects smaller than this size are ignored.
            )
    
    for(x,y,w,h) in faces:
        namepos=(x+5,y-5) 
        confpos=(x+5,y+h-5) 
        cv2.rectangle(frame, (x,y), (x+w,y+h), boxColor, 3) #5 parameters - frame, topleftcoords,bottomrightcooords,boxcolor,thickness

        id, confidence = recognizer.predict(frameGray[y:y+h,x:x+w])
        
        # If confidence is less than 100, it is considered a perfect match
        if confidence < 100:
            id = names[id+1]
            confidence_text = f"{100 - confidence:.0f}%"
            if (100 - confidence) > 64:
                recognized +=1
                abrirPuerta(True)
                enviarMensaje(True, id)
            elif (time.time() - timer > 10):
                abrirPuerta(False)
                enviarMensaje(False, "None")
        else:
            id = "unknown"
            confidence_text = f"{100 - confidence:.0f}%"

        #Display name and confidence of person who's face is recognized
        cv2.putText(frame, str(id), namepos, font, height, nameColor, 2)
        cv2.putText(frame, str(confidence_text), confpos, font, height, confColor, 1)
        
    cv2.imshow('Raspi Face Recognizer',frame)
    if recognized >= 3:
        print("\n [INFO] Face Recognized")
        time.sleep(2)
        break
    key = cv2.waitKey(100) & 0xff
    #Checking keycode
    if key == 27:  # ESCAPE key
        break
    elif key == 113:  # q key
        break

# Release the camera and close all windows
print("\n [INFO] Exiting Program and cleaning up stuff")
cam.stop()
cv2.destroyAllWindows()
