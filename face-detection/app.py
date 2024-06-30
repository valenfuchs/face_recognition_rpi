import cv2
import os
import subprocess
from picamera2 import Picamera2
import csv
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    csv_file = 'names.csv'

    # Constants for face capture
    COUNT_LIMIT = 30
    POS = (30, 60)  # top-left
    FONT = cv2.FONT_HERSHEY_COMPLEX
    HEIGHT = 1.5
    TEXTCOLOR = (0, 0, 255)
    BOXCOLOR = (255, 0, 255)
    WEIGHT = 3
    FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Read last face ID from CSV or initialize
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        last_row = None
        for row in reader:
            last_row = row

    if last_row is not None:
        face_id = int(last_row[1]) + 1
    else:
        face_id = 1

    # Get name from form submission
    name = request.form.get('name')

    # Write new name and ID to CSV
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, face_id])

    # Initialize PiCamera2 object
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

    try:
        # Execute training script
        subprocess.run(['python', 'training.py'], check=True)
        print("Training script executed successfully.")

        # Execute recognition script
        subprocess.run(['python', 'recognition.py'], check=True)
        print("Recognition script executed successfully.")

        # Redirect to capturing.html after successful execution
        return redirect(url_for('/templates/capturing.html'))

    except subprocess.CalledProcessError as e:
        print(f"Error executing subprocess: {e}")
        return "Error occurred during execution."

if __name__ == '__main__':
    app.run(debug=True)
