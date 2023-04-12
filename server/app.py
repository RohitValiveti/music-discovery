import json
from flask import Flask, request

app = Flask(__name__)

# db.init_app(app)


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(msg, code):
    return json.dumps({"error": msg}), code

