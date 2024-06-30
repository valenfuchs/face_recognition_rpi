# Archivo: app.py
from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_capture', methods=['POST'])
def start_capture():
    name = request.form['name']
    # Ejecutar el script de captura de imágenes con el nombre como argumento
    subprocess.Popen(['python3', 'capture_script.py', name])
    return f'Starting capture for {name}'

if __name__ == '__main__':
    app.run(debug=True)
