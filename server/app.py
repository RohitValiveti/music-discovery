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


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(msg, code):
    return json.dumps({"error": msg}), code


def authenticate():
    """
    Evaluates to False if a user is not signed in. True if signed in. 
    """
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return False, None
    else:
        return True, auth_manager


@app.route('/')
def sign_in():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='playlist-modify-public user-top-read',
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
    return success_response(cache_handler.get_cached_token())


@app.route('/sign-out/')
def sign_out():
    authenticated, _ = authenticate()
    if not authenticated:
        return failure_response('not signed in', 401)
    else:
        session.pop("token_info", None)
        return redirect('/')


@app.route('/playlists/')
def get_playlists():
    """
    Returns Public Playlists of User
    """
    authenticated, auth_manager = authenticate()
    if not authenticated:
        return failure_response('not signed in', 401)
    sp = SpotifyRecommender(auth_manager=auth_manager)
    playlists = sp.playlists()
    return success_response(playlists)


@app.route('/recommend/')
def get_recs():
    """
    Given a playlist id in the request body, 
    recommends songs based on that playlist.
    """
    authenticated, auth_manager = authenticate()
    if not authenticated:
        return failure_response('not signed in', 401)
    sp = SpotifyRecommender(auth_manager=auth_manager)
    playlists = sp.playlists()
    body = json.loads(request.data)
    playlist_id = body.get("playlist_id")

    if playlist_id is None:
        return failure_response("Please Supply Playlist Id", 400)
    if not (playlist_id in playlists):
        return failure_response("Not a valid playlist", 400)

    recs = sp.recommend_tracks(playlist_id)
    return success_response(recs)


@app.route("/song/")
def get_song():
    """
    Returns Song Info given an id.
    """
    authenticated, auth_manager = authenticate()
    if not authenticated:
        return failure_response('not signed in', 401)
    sp = SpotifyRecommender(auth_manager=auth_manager)

    body = json.loads(request.data)
    track_id = body.get("track_id")

    if track_id is None:
        return failure_response("Please Supply Song Id", 400)

    track_info = sp.track_info(track_id)
    if track_info is None:
        return failure_response('Invalid Track id', 400)

    return track_info


@app.route("/user/")
def get_user_info():
    """
    Returns Info of current user.
    """
    authenticated, auth_manager = authenticate()
    if not authenticated:
        return failure_response('not signed in', 401)
    sp = SpotifyRecommender(auth_manager=auth_manager)

    return success_response(sp.profile_info())


@app.route('/add_track/')
def add_track_to_playlist():
    """
    Given a track id and playlist id,
    adds the track to the user's playlist.
    """
    authenticated, auth_manager = authenticate()
    if not authenticated:
        return failure_response('not signed in', 401)
    sp = SpotifyRecommender(auth_manager=auth_manager)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
