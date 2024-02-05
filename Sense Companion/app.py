from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '<a href="/run_script" class="btn">Go</a>'

@app.route('/run_script')
def run_script():
    os.system('python "C:/Users/prabh/Computervisionprojects/YOLO-NAS Sign Language Detection/customtk.py"')
    return 'Python script executed successfully!'

if __name__ == '__main__':
    app.run(debug=True)
