import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import json
from dotenv import load_dotenv

load_dotenv()
# Username: m73pzp0jio9t0tuxh1xxbrzjf
# User ID: 4165514eecb24182


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("usage: python3 file.py [username]")
    sys.exit()

scope = 'user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

res = sp.current_user_top_tracks(limit=20, time_range='long_term')

songs_arr = res['items']

for i, song in enumerate(songs_arr):
    print(song['name'])


# print(json.dumps(top_songs, sort_keys=True, indent=4))
