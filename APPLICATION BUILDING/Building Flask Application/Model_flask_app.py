from flask import Flask, Response, render_template
import cv2


app = Flask(__name__)
cap = cv2.VideoCapture(0)
@app.route('/')
def index():
    return  render_template('index.html')

def generate_frames():
    while True:
        success, frame = cap.read()
        imgOutput=frame.copy()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + imgOutput + b'\r\n')
@app.route('/predict',methods=['POST','GET'])
def predictions():
    #The prediction model code goes here
    #Once the start Button is pressed the prediction model starts
    pass
@app.route('/stop',methods=['POST','GET'])
def stopping():
    #The text to speech code goes here
    #Once the stop button is pressed the text is converted into speech
    pass

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	app.run(debug=True)