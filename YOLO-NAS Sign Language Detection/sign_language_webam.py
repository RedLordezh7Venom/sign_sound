import cv2
print("*"*235)
from super_gradients.training import models
from super_gradients.common.object_names import Models
model = models.get('yolo_nas_s', num_classes=26, checkpoint_path = 'model_weights/ckpt_best.pth')

output = model.predict_webcam()
models.convert_to_onnx(model=model, input_shape=(3,640,640), out_path='custom.onnx')





'''cam = cv2.VideoCapture(0)
c=1
while True:
    _,img = cam.read()
    cv2.imshow("Frame",img)
    key =cv2.waitKey(20)

    if (key==13):
       cv2.imwrite('Selfie/Selfie_'+str(c)+'.png',img)
       c+=1
    
    if (key==27):
       cam.release()
       break'''

