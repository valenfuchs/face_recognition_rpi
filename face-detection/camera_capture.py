# camera_capture.py
import cv2
import os
import csv
from picamera2 import Picamera2

def start_capture(face_id):
    COUNT_LIMIT = 30
    BOXCOLOR = (255, 0, 255)
    FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = Picamera2()
    cam.preview_configuration.main.size = (640, 360)
    cam.preview_configuration.main.format = "RGB888"
    cam.preview_configuration.controls.FrameRate = 30
    cam.preview_configuration.align()
    cam.configure("preview")
    cam.start()
    count = 0

    while True:
        # Capture frame from camera
        frame = cam.capture_array()

        # Convert frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = FACE_DETECTOR.detectMultiScale(
            frame_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            # Draw bounding box around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), BOXCOLOR, 3)
            count += 1

            # Ensure dataset folder exists
            if not os.path.exists("dataset"):
                os.makedirs("dataset")

            # Save captured grayscale image
            file_path = os.path.join("dataset", f"User.{face_id}.{count}.jpg")
            if os.path.exists(file_path):
                old_file_path = file_path.replace("dataset", "old_dataset")
                os.rename(file_path, old_file_path)
            cv2.imwrite(file_path, frame_gray[y:y + h, x:x + w])

        # Display frame to user
        cv2.imshow('FaceCapture', frame)

        # Exit conditions
        key = cv2.waitKey(100) & 0xff
        if key == 27 or key == 113 or count >= COUNT_LIMIT:
            break

    # Release camera and close windows
    print("\n [INFO] Done! Thank you")
    cam.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    face_id = int(sys.argv[1])
    start_capture(face_id)
