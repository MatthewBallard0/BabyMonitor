


from flask import Blueprint, request, jsonify, Response
camera_controller = Blueprint('camera-controller', __name__)
from Services import CameraService

def gen(camera):
    while True:
        yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + camera.get_frame() + b'\r\n\r\n')
@camera_controller.route("/video_feed")
def video_feed():
    return Response(gen(CameraService.camera_service()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')



