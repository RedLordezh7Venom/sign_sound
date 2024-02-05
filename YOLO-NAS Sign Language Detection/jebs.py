import pickle 
import datetime

d=datetime.datetime.now()
a=d.hour
b=d.minute
c=a+b
e=int(c)
print(c)

"PART1"

while True:                #Password manager=Changes the password in every minute. 
  d=int(input("enter password="))
  if d!=e:
    print("wrong password")
  else:
    print("ok")
    break
# Ask the user for input
user_option = input("Enter your option (1, 2, 3, 4 etc.): ")
# Convert the input to an integer
user_option = int(user_option)

# Check the user's option using if-else statements
if user_option == 1:
    print("You selected (text to voice conversion ) .")
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
    display(Audio(mp3_file_path, autoplay=True))


elif user_option == 2:
    import speech_recognition as sr
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
    speech_to_text()
elif user_option == 3:
    print("You selected hand sign  detection .")
    import cv2
    from super_gradients.training import models
    from super_gradients.common.object_names import Models
    model = models.get('yolo_nas_s', num_classes=26, checkpoint_path = 'model_weights/ckpt_best.pth')

    output = model.predict_webcam()
    models.convert_to_onnx(model=model, input_shape=(3,640,640), out_path='custom.onnx')

elif user_option == 4:
    import cv2  
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
        answer= classNames[classId-1]
        newVoiceRate =40
        text_speech.setProperty('rate',newVoiceRate)
        text_speech.say(answer)
        text_speech.runAndWait()




else:
    print("Invalid option. Please choose a valid option.")

# Continue with the rest of your code