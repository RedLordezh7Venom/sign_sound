import os
import tkinter as tk
from tkinter import ttk
from gtts import gTTS
from tkinter import messagebox

def text_to_speech():
    text = text_entry.get()

    if text:
        try:
            language = language_var.get()
            output_file = '2output.mp3'

            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(output_file)
            
            messagebox.showinfo("Success", f"Audio saved as {output_file}")
            import pygame

            def play_mp3(file_path):
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()

            # Example: specify the path to your MP3 file
            mp3_file_path = './2output.mp3'

            # Play the MP3 file
            play_mp3(mp3_file_path)

           

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showwarning("Warning", "Please enter some text.")

# GUI setup
root = tk.Tk()
root.title("Text to Speech Conversion")
root.geometry("400x200")
root.configure(bg="#3498db")  # Set background color to blue

# Create GUI components
label = ttk.Label(root, text="Enter text:")
text_entry = ttk.Entry(root, width=40)
language_label = ttk.Label(root, text="Select language:")
language_var = tk.StringVar()
language_combobox = ttk.Combobox(root, textvariable=language_var, values=["en", "es", "fr", "de"])
convert_button = ttk.Button(root, text="Convert", command=text_to_speech)

# Arrange GUI components
label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
text_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
language_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
language_combobox.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
convert_button.grid(row=2, column=1, pady=10)

# Set default language
language_combobox.set("en")

# Start GUI main loop
root.mainloop()
