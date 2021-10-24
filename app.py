#!/usr/bin/python3
import cv2
import subprocess
from flask import Flask, render_template, Response

from camera import Camera

app = Flask(__name__)

def run_command(command):
    #return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return subprocess.check_output(command).decode('utf-8')

@app.route('/<command>')
def command_server(command):
    return run_command(command)

@app.route("/")
def index():
    #return "Hello World!"
    return render_template("index.html")

@app.route("/stream")
def stream():
    return render_template("stream.html")

def gen(camera):
    while True:
        frame = camera.get_frame()

        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n")
        else:
            print("frame is none")

@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
