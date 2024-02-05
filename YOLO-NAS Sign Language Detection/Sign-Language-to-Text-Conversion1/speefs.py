import speech_recognition as sr
from pydub import AudioSegment
import pyttsx3
import tkinter as tk
from threading import Thread

def recognize_audio():
    text = speech_to_text()
    if text:
        engine.say("Recognizing...")
        engine.runAndWait()
        print(f"Recognized Text: {text}")
        result_var.set(f"You said: {text}")

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def record_audio():
    engine.say("Recording audio...")
    engine.runAndWait()
    thread = Thread(target=recognize_audio)
    thread.start()

# GUI setup
root = tk.Tk()
root.title("Speech Recognition GUI")

# Create GUI components
record_button = tk.Button(root, text="Record Audio", command=record_audio)
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var)

# Arrange GUI components
record_button.pack(pady=10)
result_label.pack(pady=10)

# Text-to-speech engine
engine = pyttsx3.init()

# Start GUI main loop
root.mainloop()
