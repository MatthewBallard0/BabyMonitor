
from flask import Flask, Blueprint, render_template, json, request, jsonify, Response
from WebAPI.LoginController import login_controller
from WebAPI.CameraController import camera_controller
import DataAccess.UserDAL

webDirectory = 'web/BabyMonitor/dist/BabyMonitor/'
app = Flask(__name__,
            static_url_path='',
            static_folder=webDirectory,
            template_folder=webDirectory)
app.register_blueprint(login_controller)
app.register_blueprint(camera_controller)
@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)

