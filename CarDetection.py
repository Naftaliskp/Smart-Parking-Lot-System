import cv2
import numpy as np
import serial
import requests
import time
import shutil

j = 0
url='http://192.168.3.88'
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h,):
    label = str(classes[class_id])
    confround = "{:.3f}".format(confidence)
    conf = str(confround)
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.putText(img, conf, (x+3,y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    if (label == "car"):
        print("1")
        ArduinoSerial.write("1".encode('utf-8'))
    else : 
        print("0")
        ArduinoSerial.write("0".encode('utf-8'))

classes = [] # None

ArduinoSerial=serial.Serial('COM6',115200,timeout=0.1)

with open("yolov3.txt", 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 2))

# start = time. time()

while True:
    response=requests.get(f'{url}/capture?_cb={int(round(time.time() * 1000))}', stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    image=cv2.imread('img.png')
    # if ArduinoSerial.read().decode('utf-8') == "1":
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))
    
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    print ("indices")
    print (indices)
    # end = time. time()
    # print ("end-start")
    # print (end-start)
    if indices == ():
        j += 1
        if j > 5:
            print ("kosong ")
            print (j)
            j = 0
            ArduinoSerial.write("0".encode('utf-8'))
    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

    # elif ArduinoSerial.read().decode('utf-8') == "0":
    #     break
    cv2.imshow('object_dectection',image)
    if cv2.waitKey (2) == 27:
        break
cv2.destroyAllWindows()