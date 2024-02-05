import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageGrab
import easyocr
import cv2
from super_gradients.training import models
from super_gradients.common.object_names import Models
import pyttsx3
import speech_recognition as sr

class TextCaptureApp:
    def __init__(self, master):
        self.master = master
        master.title("Multifunctional Text and Object Detection App")

        # Create a label to display the captured text or object detection result
        self.label = tk.Label(master, text="", font=("Arial", 12))
        self.label.pack(pady=20)

        # Create a stylish menu
        self.menu = ttk.Combobox(master, values=["Text to Speech", "Speech to Text", "Hand Sign Detection", "Object Detection"])
        self.menu.set("Choose an option")
        self.menu.pack(pady=10)

        # Create a button to execute the selected option
        self.execute_button = tk.Button(master, text="Execute", command=self.execute_option)
        self.execute_button.pack(pady=10)

    def capture_text(self):
        # Replace this function with your text capture logic using OCR
        x1, y1, x2, y2 = 100, 100, 500, 300
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        screenshot.save("captured_image.png")
        reader = easyocr.Reader(['en'])
        results = reader.readtext(screenshot)
        text = ' '.join(result[1] for result in results)
        return text

    def text_to_speech(self):
        text = self.capture_text()
        tts = pyttsx3.init()
        tts.say(text)
        tts.runAndWait()

    def speech_to_text(self):
        text = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            text.adjust_for_ambient_noise(source, duration=1)
            audio = text.listen(source, timeout=5)

        try:
            print("Recognizing...")
            text_result = text.recognize_google(audio)
            print("You said:", text_result)
            return text_result
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def object_detection(self):
        text_speech= pyttsx3.init() 


        cap=cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)

        classNames= []
        classFile = "coco.names"
        with open(classFile,'rt') as f: 
            classNames =f.read().rstrip('\n').split('\n')

        configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'frozen_inference_graph.pb'

        net = cv2.dnn_DetectionModel(weightsPath,configPath)

        net.setInputSize (320,320)
        net.setInputScale(1.0/ 127.5) 
        net. setInputMean ((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        while True:
            success,img=cap.read()
            classIds, confs, bbox = net.detect(img, confThreshold=0.5)
            print(classIds, bbox)
            
            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img, classNames[classId-1].upper(), (box [0]+10,box[1]+30),
                            cv2.FONT_HERSHEY_COMPLEX,1,(0,255.0),2) 
            cv2.imshow("output",img)
            cv2.waitKey(1)
            answer= classNames[classId-1]
            newVoiceRate =40
            text_speech.setProperty('rate',newVoiceRate)
            text_speech.say(answer)
            text_speech.runAndWait()
       
    
    def hand_sign(self):
        model = models.get('yolo_nas_s', num_classes=26, checkpoint_path='model_weights/ckpt_best.pth')
        output = model.predict_webcam()
        models.convert_to_onnx(model=model, input_shape=(3, 640, 640), out_path='custom.onnx')
        
    def execute_option(self):
        selected_option = self.menu.get()

        if selected_option == "Text to Speech":
            self.text_to_speech()
        elif selected_option == "Speech to Text":
            self.speech_to_text()
        elif selected_option == "Hand Sign Detection":
            self.hand_sign()
            print("Hand Sign Detection not implemented in this example.")
            # Implement hand sign detection logic here
        elif selected_option == "Object Detection":
            self.object_detection()
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextCaptureApp(root)
    root.mainloop()
