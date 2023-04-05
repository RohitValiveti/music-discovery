import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import json
from dotenv import load_dotenv
import pandas as pd
import datetime
import pytz
from dateutil.relativedelta import relativedelta


class SpotifyRecommender:
    """
    Spotify Recommender Class computes song recomendations for for a given user.

    Attributes:
    -  spotify: Spotify object
    """

    def __init__(self):
        load_dotenv()
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope="user-library-read"))

    def get_playlists(self):
        """
        Returns dictionary of user's playlists.
        """
        playlists_res = self.spotify.current_user_playlists()['items']
        playlists = {}
        for item in playlists_res:
            playlists[item['name']] = item['id']
        return playlists

    def _playlist_tracks_metadata(self, playlist_id):
        """
        Given a playlist id, returns a pandas dataframe consisting of key elements of each track.
        """
        playlist = self.spotify.playlist(playlist_id)
        tracks = []
        for item in playlist['tracks']['items']:
            if item['track']['id'] is not None:
                track = item['track']
                track_id = track['id']
                artist_ids = [artist['id'] for artist in track['artists']] if len(
                    track['artists']) > 0 else None
                artist_names = [artist['name'] for artist in track['artists']] if len(
                    track['artists']) > 0 else None
                track_info = {
                    'track_name': track['name'],
                    'track_id': track_id,
                    'artists': artist_names,
                    'artist_ids': artist_ids,
                    'album_name': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'explicit': track['explicit'],
                    'popularity': track['popularity'],
                    'date_added': item['added_at']
                }
                tracks.append(track_info)

        tracks_df = pd.DataFrame(tracks)
        tracks_df['date_added'] = pd.to_datetime(
            tracks_df['date_added'], utc=True)
        now = datetime.datetime.now(pytz.utc)
        tracks_df['months_since_added'] = tracks_df['date_added'].apply(
            lambda x: relativedelta(now, x).months)
        tracks_df = tracks_df.drop(['date_added'], axis=1)

        return tracks_df

    def _extract_track_features(self, track_ids):
        """
        Given a list of track ids, returns a pandas dataframe of key audio features of each track
        """
        audio_features_list = []
        for track_id in track_ids:
            if track_id is not None:
                audio_features = self.spotify.audio_features(track_id)[0]
                audio_features_list.append(audio_features)

        # convert list of dictionaries to Pandas DataFrame
        audio_features_df = pd.DataFrame.from_records(
            audio_features_list, columns=audio_features_list[0].keys())

        # add track ID column to DataFrame
        audio_features_df['track_id'] = track_ids

        # re-order columns to put track_id first
        cols = audio_features_df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        audio_features_df = audio_features_df[cols]
        audio_features_df = audio_features_df.drop(
            ['type', 'id', 'uri', 'track_href', 'analysis_url', 'track_id'], axis=1)
        return audio_features_df

    def create_playlist_df(self, playlist_id):
        """
        Returns a dataframe for the playlsit with the given id. Attributes include thoe returned by
        Spotify Web API's GET Audio Features endpoint and track meta data like name, artist, etc.
        """
        df1 = self._playlist_tracks_metadata(playlist_id)
        df2 = self._extract_track_features(df1['track_id'])
        playlist_df = pd.concat([df1, df2], axis=1)
        return playlist_df
