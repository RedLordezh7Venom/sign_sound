from flask import Flask, render_template
from threading import Thread
import os
import customtk  # Import your hand sign detection function from customtk

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Create an HTML template with a button to start the process

@app.route('/run_script')
def run_script():
    thread = Thread(target=customtk.detect_hand_sign)  # Run your hand sign detection function in a separate thread
    thread.start()
    return 'Hand sign detection started!'

if __name__ == '__main__':
    app.run(debug=True)
