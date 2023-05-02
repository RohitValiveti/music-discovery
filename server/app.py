import json
from flask import Flask, session, request, redirect
from flask_session import Session
import sys
sys.path.insert(0,"..")
from server.SpotifyRecommender import SpotifyRecommender

app = Flask(__name__)

# db.init_app(app)


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(msg, code):
    return json.dumps({"error": msg}), code


def auth():
    pass

# sp = SpotifyRecommender()

# playlists = sp.playlists()

# print(playlists)

auth()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)