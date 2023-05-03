import spotipy
from SpotifyRecommender import SpotifyRecommender
import json
from dotenv import load_dotenv
from flask import Flask, session, request, redirect
from flask_session import Session
import os
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

# db.init_app(app)


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(msg, code):
    return json.dumps({"error": msg}), code


@app.route('/')
def sign_in():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='playlist-modify-public',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return success_response({'sign_in_link': auth_url})

    # Step 3. Signed in, display data
    sp = SpotifyRecommender(auth_manager=auth_manager)
    return success_response(sp.profile_info())


@app.route('/sign_out/')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')


@app.route('/playlists/')
def get_playlists():
    """
    Returns Public Playlists of User
    """
    pass


@app.route('/recommend/')
def get_recs():
    """
    Given a playlist id in the request body, 
    recommends songs based on that playlist.
    """
    pass


@app.route('/add_track/')
def add_track_to_playlist():
    """
    Given a track id and playlist id,
    adds the track to the user's playlist.
    """
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
