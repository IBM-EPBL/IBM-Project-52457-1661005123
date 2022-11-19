import numpy as np
import cv2
import os
from keras.models import load_model
from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
from keras.preprocessing import image

global graph
global writer
from skimage.transform import resize

writer = None
model = load_model('Balaji.h5')
vals = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
app = Flask(__name__)
print("[info] accessing video stream...")
vs = cv2.VideoCapture(0)


def detect(jpeg):
    img = resize(jpeg, (64, 64, 3))
    copy = img.copy()
    copy = copy[150:150 + 200, 50:50 + 200]
    cv2.imwrite('image.jpg', copy)
    copy_img = image.load_img('image.jpg')
    x = image.img_to_array(copy_img)
    x = np.expand_dims(x, axis=0)
    prediction = np.argmax(model.predict(x), axis=1)
    pred = vals[prediction[0]]
    print("it indicates : ", pred)
    return pred


video_camera = None
global_frame = None


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
            img = resize(frame, (64, 64))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            prediction = np.argmax(model.predict(x), axis=1)
            pred = vals[prediction[0]]
            print("it indicates : ", pred)


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
