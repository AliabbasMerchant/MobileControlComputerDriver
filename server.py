from typing import Optional
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from threading import Thread
from zlib import compress
from mss import mss, tools
import json

import globals
import handler

WIDTH = 1920
HEIGHT = 1080

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
loop = True

@app.route('/connect', methods=['POST'])
def accept_connection():
    body = request.form.to_dict()
    try:
        if body['connectionSecret'] == globals.connection_secret:
            return json.dumps({"ok": True})
        else:
            return json.dumps({"ok": False, "msg": "Invalid Connection Secret"})
    except KeyError:
        return json.dumps({"ok": False, "msg": "Please provide a Connection Secret"})


@app.route('/control', methods=['POST'])
def handle_signals():
    body = request.form.to_dict()
    try:
        if body['connectionSecret'] == globals.connection_secret:
            error = handler.handle(body)
            if error:
                return json.dumps({"ok": False, "msg": error})
            else:
                return json.dumps({"ok": True})
        else:
            return json.dumps({"ok": False, "msg": "Invalid Connection Secret"})
    except KeyError:
        return json.dumps({"ok": False, "msg": "Please provide a Connection Secret"})


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected Successfully'})

@socketio.on('Start Recieving Data')
def send_data(msg):
    global loop
    loop = True
    with mss() as sct:
        # The region to capture
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while loop:
            # Capture the screen
            data = {}
            img = sct.grab(rect)
            
            # Getting raw bytes of the image
            pixels = tools.to_png(img.rgb, img.size)

            # Send pixels
            data["pixels"] = pixels

            emit('data', {'msg': data})

@socketio.on('Close connection')
def close_connection(msg):
    global loop
    loop = False

def serve(port: int):
    socketio.run(app, port=port, host='0.0.0.0')
