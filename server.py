from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from mss import mss, tools
import json

import globals
import handler
import logger

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
            logger.log(f"Client {request.remote_addr} Connected!")
            return json.dumps({"ok": True})
        else:
            logger.debug(f"Client {request.remote_addr} sent invalid connection secret. Connection declined")
            return json.dumps({"ok": False, "msg": "Invalid Connection Secret"})
    except KeyError:
        logger.debug(f"Client {request.remote_addr} did not send a connection secret. Connection declined")
        return json.dumps({"ok": False, "msg": "Please provide a Connection Secret"})


@app.route('/control', methods=['POST'])
def handle_signals():
    body = request.form.to_dict()
    try:
        if body['connectionSecret'] == globals.connection_secret:
            logger.log(f"Received command {body} from client {request.remote_addr}")
            error = handler.handle(body)
            if error:
                logger.log(f"Error {error} while accepting control from client {request.remote_addr}")
                return json.dumps({"ok": False, "msg": error})
            else:
                logger.log(f"Successfully exectued control {body} from client {request.remote_addr}")
                return json.dumps({"ok": True})
        else:
            logger.debug(f"Client {request.remote_addr} sent invalid connection secret. Control declined")
            return json.dumps({"ok": False, "msg": "Invalid Connection Secret"})
    except KeyError:
        logger.debug(f"Client {request.remote_addr} did not send a connection secret. Control declined")
        return json.dumps({"ok": False, "msg": "Please provide a Connection Secret"})


@socketio.on('connect')
def test_connect():
    logger.log(f"Client socket connection established")
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
            logger.debug(f"Screen frame shared with client")

@socketio.on('Close connection')
def close_connection(msg):
    logger.log(f"Client socket connection closed")
    global loop
    loop = False

def serve(port: int):
    socketio.run(app, port=port, host='0.0.0.0')
