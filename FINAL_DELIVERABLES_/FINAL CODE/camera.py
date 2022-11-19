import cv2

class VideoCamera():
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)



    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        else:
            return None



