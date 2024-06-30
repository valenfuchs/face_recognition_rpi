from flask import Flask, render_template, Response, request
import cv2
import os
from picamera2 import Picamera2
import csv

app = Flask(__name__, static_folder='static', template_folder='templates')

csv_file = 'names.csv'

# Constants
COUNT_LIMIT = 30
POS = (30, 60)  # top-left
FONT = cv2.FONT_HERSHEY_COMPLEX  # font type for text overlay
HEIGHT = 1.5  # font_scale
TEXTCOLOR = (0, 0, 255)  # BGR- RED
BOXCOLOR = (255, 0, 255)  # BGR- BLUE
WEIGHT = 3  # font-thickness
FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('register.html')

def gen_frames(name):
    # For each person, enter one numeric face id
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header
        last_row = None
        for row in reader:
            last_row = row

    if last_row is not None:
        face_id = int(last_row[1]) + 1
    else:
        face_id = 1

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, face_id])

    print("\n [INFO] Initializing face capture. Look at the camera and wait!")

    # Create an instance of the PiCamera2 object
    cam = Picamera2()
    ## Set the resolution of the camera preview
    cam.preview_configuration.main.size = (640, 480)  # Adjusted resolution for better display
    cam.preview_configuration.main.format = "RGB888"
    cam.preview_configuration.controls.FrameRate = 30
    cam.preview_configuration.align()
    cam.configure("preview")
    cam.start()

    count = 0

    while True:
        frame = cam.capture_array()

        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_DETECTOR.detectMultiScale(
            frameGray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), BOXCOLOR, 3)
            count += 1

            if not os.path.exists("dataset"):
                os.makedirs("dataset")
            file_path = os.path.join("dataset", f"User.{face_id}.{count}.jpg")
            if os.path.exists(file_path):
                old_file_path = file_path.replace("dataset", "old_dataset")
                os.rename(file_path, old_file_path)
            cv2.imwrite(file_path, frameGray[y:y+h, x:x+w])

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if count >= COUNT_LIMIT:
            break

    print("\n [INFO] Done! Thank you")
    cam.stop()

@app.route('/video_feed')
def video_feed():
    name = request.args.get('name', 'Unknown')  # Default name is 'Unknown' if not provided
    return Response(gen_frames(name), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    name = request.form['name']
    return render_template('capturing.html', name=name)  # Pass 'name' to template for display

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
