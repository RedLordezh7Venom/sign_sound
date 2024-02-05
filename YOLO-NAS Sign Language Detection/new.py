import tkinter as tk
from tkinter import ttk
import pyautogui
import pyttsx3
import speech_recognition as sr
import cv2
import threading
import time

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI with PyAutoGUI")
        
        # Create buttons
        self.mouse_button = ttk.Button(root, text="Mouse Click", command=self.perform_mouse_click)
        self.tts_button = ttk.Button(root, text="Text-to-Speech", command=self.perform_text_to_speech)
        self.stt_button = ttk.Button(root, text="Speech-to-Text", command=self.perform_speech_to_text)
        self.webcam_button = ttk.Button(root, text="Webcam Capture", command=self.perform_webcam_capture)

        # Place buttons on the grid
        self.mouse_button.grid(row=0, column=0, padx=10, pady=10)
        self.tts_button.grid(row=0, column=1, padx=10, pady=10)
        self.stt_button.grid(row=1, column=0, padx=10, pady=10)
        self.webcam_button.grid(row=1, column=1, padx=10, pady=10)

    def perform_mouse_click(self):
        pyautogui.click(100, 100)

    def perform_text_to_speech(self):
        text_to_speech("Welcome to the PyAutoGUI GUI!")

    def perform_speech_to_text(self):
        spoken_text = speech_to_text()
        if spoken_text:
            print("Spoken Text:", spoken_text)

    def perform_webcam_capture(self):
        threading.Thread(target=capture_webcam_image).start()

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def capture_webcam_image():
    print("You selected live web cam detection .")
    import cv2
    from super_gradients.training import models
    from super_gradients.common.object_names import Models
    model = models.get('yolo_nas_s', num_classes=26, checkpoint_path = 'model_weights/ckpt_best.pth')

    output = model.predict_webcam()
    models.convert_to_onnx(model=model, input_shape=(3,640,640), out_path='custom.onnx')

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
