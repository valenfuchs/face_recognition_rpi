import os
import subprocess
import csv
from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    csv_file = 'names.csv'

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

        return redirect(url_for('capturing'))

    except subprocess.CalledProcessError as e:
        print(f"Error executing subprocess: {e}")
        return "Error occurred during execution."

@app.route('/capturing')
def capturing():
    return render_template('capturing.html')

@app.route('/login')
def login():
    try:
        # Ejecutar solo el script de reconocimiento
        subprocess.run(['python', 'recognition.py'], check=True)
        print("Recognition script executed successfully.")
        return redirect(url_for('welcome'))  # Redirigir a la página de bienvenida después de reconocimiento

    except subprocess.CalledProcessError as e:
        print(f"Error executing recognition subprocess: {e}")
        return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
