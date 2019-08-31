
import cv2
from Services.BaseCameraService import BaseCamera


class camera_service(BaseCamera):
    video_source = 0
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 2160)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        mode = False
        static_back = None
        threshValue = 8
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            _, frame = camera.read()
            if mode is True:
                gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (1, 1), 0)

                if static_back is None:
                    static_back = gray
                    continue
                (allContours, v1) = cv2.findContours(cv2.dilate(cv2.threshold(cv2.absdiff(static_back, gray), threshValue, 255, cv2.THRESH_BINARY)[1] , None, iterations = 1) , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in allContours:
                    if cv2.contourArea(contour) >= 5000:
                        (x, y, w, h) = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,0), 2)
            yield cv2.imencode('.png', frame)[1].tobytes()
