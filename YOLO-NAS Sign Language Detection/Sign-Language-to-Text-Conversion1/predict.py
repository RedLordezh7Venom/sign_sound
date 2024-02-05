#+speaker
import cv2
import numpy as np
from keras.models import load_model
import time
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3

# Load the trained model
model = load_model(
    'C:/Users/prabh/Computervisionprojects/YOLO-NAS Sign Language Detection/Sign-Language-to-Text-Conversion1/model_save'
)

# Mapping index to corresponding letter or "nothing"
letters_mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
                   10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'nothing', 15: 'O', 16: 'P', 17: 'Q', 18: 'R',
                   19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}

# Create a class for the GUI
class SignLanguageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Recognition")

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.letter_box_label = tk.Label(root, text="Current Letter:")
        self.letter_box_label.pack()

        self.letter_var = tk.StringVar()
        self.letter_var.set("")
        self.letter_box = tk.Label(root, textvariable=self.letter_var, font=("Helvetica", 16))
        self.letter_box.pack()

        self.word_label = tk.Label(root, text="Formed Word:")
        self.word_label.pack()

        self.word_var = tk.StringVar()
        self.word_var.set("")
        self.word_display = tk.Label(root, textvariable=self.word_var, font=("Helvetica", 16))
        self.word_display.pack()

        self.sentence_label = tk.Label(root, text="Formed Sentence:")
        self.sentence_label.pack()

        self.sentence_var = tk.StringVar()
        self.sentence_var.set("")
        self.sentence_display = tk.Label(root, textvariable=self.sentence_var, font=("Helvetica", 16))
        self.sentence_display.pack()

        self.last_recognized_time = time.time()
        self.letter = ""
        self.word = ""
        self.sentence = ""

        self.camera = cv2.VideoCapture(0)
        self.show_video()

    def show_video(self):
        _, frame = self.camera.read()
        frame = cv2.flip(frame, 1)

        # Create a separate camera box (ROI) for sign language input
        roi = frame[100:300, 400:600]

        # Draw a rectangle (visible square) around the ROI
        cv2.rectangle(frame, (400, 100), (600, 300), (0, 255, 0), 2)

        # Preprocess the ROI (similar to the preprocessing done during training)
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi_canny = cv2.Canny(roi_gray, 80, 80)
        roi_resized = cv2.resize(roi_canny, (100, 100))
        roi_normalized = roi_resized.reshape(1, 100, 100, 1) / 255.0

        # Make a prediction using the model
        class_probabilities = model.predict(roi_normalized)
        class_index = np.argmax(class_probabilities)

        # Get the predicted letter
        predicted_letter = letters_mapping[class_index]

        # If the predicted letter is 'nothing', add a space to the letter box
        if predicted_letter == "nothing" and time.time() - self.last_recognized_time > 1.5:
            self.letter = ' '
            self.last_recognized_time = time.time()

        # If the predicted letter is not 'nothing' and a certain time has passed since the last recognition
        elif predicted_letter != "nothing" and time.time() - self.last_recognized_time > 1.5:
            if predicted_letter == 'F':  # Use 'F' as a gesture for space
                self.letter = ' '
            else:
                self.letter = predicted_letter
            self.last_recognized_time = time.time()

        # Display the video frame
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        self.video_label.img = img
        self.video_label.config(image=img)

        # Display the current letter on the GUI
        self.letter_var.set("Current Letter: " + self.letter)

        # Repeat the video display
        self.root.after(10, self.show_video)

    def add_letter_to_word(self):
        # Add the current letter to the word
        self.word += self.letter
        self.letter = ""
        self.letter_var.set("Current Letter: " + self.letter)
        self.word_var.set("Formed Word: " + self.word)

    def add_word_to_sentence(self):
        # Add the current word to the sentence
        self.sentence += self.word + ' '
        self.word = ""
        self.word_var.set("Formed Word: " + self.word)
        self.sentence_var.set("Formed Sentence: " + self.sentence)

    def speak_sentence(self):
        # Use pyttsx3 to speak the formed sentence
        engine = pyttsx3.init()
        engine.say(self.sentence)
        engine.runAndWait()

    def close_program(self):
        # Release the camera when the GUI is closed
        self.camera.release()
        cv2.destroyAllWindows()
        self.root.destroy()

# Create the main window and run the GUI
root = tk.Tk()
app = SignLanguageGUI(root)

# Add "Next," "Enter," "Speak," and "Close" buttons
next_button = tk.Button(root, text="Next", command=app.add_letter_to_word)
next_button.pack()

enter_button = tk.Button(root, text="Enter", command=app.add_word_to_sentence)
enter_button.pack()

speak_button = tk.Button(root, text="Speak", command=app.speak_sentence)
speak_button.pack()

close_button = tk.Button(root, text="Close", command=app.close_program)
close_button.pack()

root.mainloop()