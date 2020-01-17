from typing import Optional
from flask import Flask, request
from flask_cors import CORS
import json

import globals
import handler

app = Flask(__name__)
CORS(app)


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


def serve(port: int):
    app.run(port=port, host='0.0.0.0')
