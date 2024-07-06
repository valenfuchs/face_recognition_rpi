import os
import subprocess
import csv
from flask import Flask, request, render_template, redirect, url_for
from threading import Thread

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

def run_subprocesses(face_id):
    try:
        # Execute camera capture script as a subprocess
        subprocess.run(['python', 'camera_capture.py', str(face_id)], check=True)
        print("Camera capture script executed successfully.")

        # Execute training script
        subprocess.run(['python', 'training.py'], check=True)
        print("Training script executed successfully.")

        # Execute recognition script
        subprocess.run(['python', 'recognition.py'], check=True)
        print("Recognition script executed successfully.")

        # Redirect to the welcome route
        with app.test_request_context():
            url = url_for('redirect_to_welcome')
            print(f"Redirecting to {url}")
            return redirect(url)
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing subprocess: {e}")
        return "Error occurred during execution."

@app.route('/start_capture', methods=['POST'])
def start_capture():
    csv_file = 'names.csv'

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

    # Run subprocesses in a separate thread
    thread = Thread(target=run_subprocesses, args=(face_id,))
    thread.start()

    return redirect(url_for('capturing'))

@app.route('/capturing')
def capturing():
    return render_template('capturing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/redirect_to_welcome')
def redirect_to_welcome():
    try:
        # Execute telegram script
        subprocess.run(['python', 'telegram.py'], check=True)
        print("Telegram script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing telegram script: {e}")
        return "Error occurred during execution."

    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
