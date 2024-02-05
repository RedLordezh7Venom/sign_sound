from customtkinter import *
from PIL import Image

app = CTk()
app.geometry("1000x700")
my_img = CTkImage(dark_image=Image.open('groc.png'),size=(1300,1000))
img_2 = CTkImage(dark_image=Image.open('images.jpeg'),size=(300,50))
img_3 = CTkImage(dark_image=Image.open('images_1.jpeg'),size=(300,50))


frame = CTkLabel(master=app,text="",
                               corner_radius=10,image=my_img)
frame.place(relx=0.5, rely=0.5,anchor="center")

label=CTkLabel(master=app,text="Welcome to SenseCompanion",width=300,height=50,image=img_3,corner_radius=0.4)
label.place(relx=0.5,rely =0.06,anchor="n")


def click_handler():
    '''print("You selected (text to voice conversion ) .")
    from gtts import gTTS
    import os
    def text_to_speech(text, language='en', output_file='output.mp3'):
      """
      Convert text to speech and save it to an audio file.

      Parameters:
      - text: The text to be converted to speech.
      - language: The language of the text (default is English 'en').
      - output_file: The name of the output audio file (default is 'output.mp3').
      """
      tts = gTTS(text=text, lang=language, slow=False)
      tts.save(output_file)
      os.system(output_file)

    # Example Usage:
    text = input("Enter text")
    text_to_speech(text, language='en', output_file='2output.mp3')

    from IPython.display import Audio, display

    # Specify the path to your MP3 file
    mp3_file_path = '/content/2output.mp3'

    # Play the audio in the notebook
    display(Audio(mp3_file_path, autoplay=True))'''
    '''import subprocess
        subprocess.run(["python","./Sign-Language-to-Text-Conversion1/guts.py"])'''
    import subprocess
    subprocess.run(["python", "./voicetextspeech/text to speech.py"])

def click_handler_function1():
    '''import subprocess
    subprocess.run(["python", 
                     "./Sign-Language-to-Text-Conversion1/speefs.py"])'''
    '''import speech_recognition as sr
    from pydub import AudioSegment
    import pyttsx3
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

    # Specify the path to the local MP3 audio file
    speech_to_text()'''
    import subprocess
    subprocess.run(["python","./voicetextspeech/speech to text.py"])

def click_handler_function2():
    '''
    print("You selected hand sign  detection .")
    import cv2
    from super_gradients.training import models
    from super_gradients.common.object_names import Models
    model = models.get('yolo_nas_s', num_classes=26, checkpoint_path = 'model_weights/ckpt_best.pth')

    output = model.predict_webcam()
    models.convert_to_onnx(model=model, input_shape=(3,640,640), out_path='custom.onnx')
    '''
    import subprocess
    subprocess.run(["python", "./Sign-Language-to-Text-Conversion1/predict.py"])

def click_handler_function3():

    '''import cv2  
    import pyttsx3

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
        key = cv2.waitKey(1)
        answer= classNames[classId-1]
        newVoiceRate =40
        text_speech.setProperty('rate',newVoiceRate)
        text_speech.say(answer)
        text_speech.runAndWait()
        if key == 27:
            cv2.destroyAllWindows()'''
    import subprocess

    # Assuming your YOLOv5 directory is at C:/Users/prabh/yolov5
    yolov5_directory = "C:/Users/prabh/yolov5"

    # Replace the paths and options accordingly
    command = f"python {yolov5_directory}/detect.py --source 0"

    # Run the command
    subprocess.run(command, shell=True)

def click_handler_function4():
    import subprocess
    subprocess.run(["python","C:/Users/prabh/darknet/blindness.py"])

btn_text_to_speech = CTkButton(master=app, text="Text to Speech", command=click_handler,height=70,width=700)
btn_text_to_speech.place(relx=0.5, rely=0.25, anchor="center")

btn_function1 = CTkButton(master=app, text="Speech To Text", command=click_handler_function1,height=70,width=700)
btn_function1.place(relx=0.5, rely=0.40, anchor="center")

btn_function2 = CTkButton(master=app, text="Hand Sign Detection", command=click_handler_function2,height=70,width=700)
btn_function2.place(relx=0.5, rely=0.55, anchor="center")

btn_function3 = CTkButton(master=app, text="Object Detection", command=click_handler_function3,height=70,width=700)
btn_function3.place(relx=0.5, rely=0.70, anchor="center")

btn_function4 = CTkButton(master=app, text="Blindness detection", command=click_handler_function4,height=70,width=700)
btn_function4.place(relx=0.5, rely=0.85, anchor="center")


app.mainloop()
