import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


class SpotifyRecommender:
    """
    Spotify Recommender Class computes song recomendations for for a given user.
    Provides Wrapper Functionality for Spotify Web API to retreive user and track
    information, and perform other profile functionality

    Attributes:
    -  sp: Spotify object
    """

    def __init__(self):
        load_dotenv()
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope="user-library-read"))

    def __create_feature_vectores(self, all_tracks_df):
        """
        Creates feature vector for each song in all_tracks_df.

        Parameters:
        - all_tracks_df: consists of all tracks in the used dataset, mimicking the "spotify db"
        Returns:
        - dataframe consisting of each track id, and their feature vector normalized.
        """

        # seperate feature columns and id column
        features_only_df = all_tracks_df.drop(
            ['name', 'album', 'artists', 'artist_ids', 'id'], axis=1).reset_index(drop=True)
        id_df = all_tracks_df[['id']]

        scaler = MinMaxScaler()
        features_scaled = pd.DataFrame(scaler.fit_transform(
            features_only_df), columns=features_only_df.columns) * 0.2

        final_df = pd.concat([id_df, features_scaled], axis=1)
        return final_df

    def __tracks_from_playlist(self, id):
        """
        Given a playlist id, returns a pandas dataframe consisting of key elements of each song
        """
        playlist = self.sp.playlist(id)
        tracks = []
        for item in playlist['tracks']['items']:
            if item['track']['id'] is not None:
                track = item['track']
                track_id = track['id']
                track_info = {
                    'id': track_id,
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

    def __extract_tracks_features(self, ids):
        """
        Given a list of track ids, returns a pandas dataframe of key audio features of each track
        """
        audio_features_list = []
        for track_id in ids:
            if track_id is not None:
                audio_features = self.sp.audio_features(track_id)[0]
                audio_features_list.append(audio_features)

        # convert list of dictionaries to Pandas DataFrame
        audio_features_df = pd.DataFrame.from_records(
            audio_features_list, columns=audio_features_list[0].keys())

        # add track ID column to DataFrame
        audio_features_df['id'] = ids

        # re-order columns to put track_id first
        cols = audio_features_df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        audio_features_df = audio_features_df[cols]
        audio_features_df = audio_features_df.drop(
            ['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
        return audio_features_df

    def __create_playlist_df(self, id):
        """
        Returns a dataframe for the playlsit with the given id. Attributes include those returned by
        Spotify Web API's GET Audio Features endpoint and track meta data like name, artist, etc.
        """
        df1 = self.__tracks_from_playlist(id)
        df2 = self.__extract_tracks_features(df1['id'])
        playlist_df = pd.concat([df1, df2], axis=1)
        return playlist_df

    def __create_playlist_vector(self, full_feature_set_df, playlist_df, weight_factor=1.2):
        """
        Generates a single vector desribing a playlist dataframe.
        Removes those songs in the playlist from the full_feature_set_df

        Parameters:
        - full_feature_set_df: All tracks of the dataset
        - playlist_df: Dataframe consisting of the songs in the playlist and their features
        - weight_factor: value representing bias of more recently added songs
        Returns:
        - sum_vect: 1D vector summarizing the features of the playlist
        - refined: All tracks in dataset as defined by full_feature_set_df, except those in the playlist_df
        """
        # Compute full_feature_set_df
        # refined_complete_df =
        merged_df = pd.merge(
            full_feature_set_df, playlist_df['id'], on='id', how='left', indicator=True)
        pruned_df = merged_df[merged_df['_merge']
                              == 'left_only'].drop(columns='_merge')

        playlist_df = playlist_df.drop(['id'], axis=1)
        # Note: Popularity feature is not given in kaggle dataset;may need to drop that column as well.
        playlist_df = playlist_df.drop(['popularity'], axis=1)

        # Compute Weight for each song of playlist; given from their months_since_added
        # More recent the song was added, the more weight is is given
        playlist_df['weight'] = playlist_df['months_since_added'].apply(
            lambda x: weight_factor ** (-x))
        playlist_df.update(playlist_df.mul(playlist_df.weight, 0))
        playlist_df = playlist_df.drop(
            ['weight', 'months_since_added'], axis=1)

        # Normalize Data (15 features)
        df = playlist_df.apply(lambda iterator: (
            (iterator - iterator.mean())/iterator.std()).round(2))
        df_normalized = df.apply(lambda iterator: (
            (iterator.max() - iterator)/(iterator.max() - iterator.min())).round(2))
        sum_vect = df_normalized.sum(axis=0)

        return sum_vect, pruned_df

    def __generate_recommendations(self, spotify_df, playlist_vect, refined_feature_set):
        """
        Return Recommenmdations based on playlist.

        Parameters:
        - spotify_df : Dataframe of all songs in spotify (or in the used dataset)
        - playlist_vect: vector representing the playlist
        - refined_feature_set: feature set of songs that are not in playlist

        Returns:
        - recommended_10_songs: Top 10 recommended songs based on playlists
        """

        non_playlist_df = spotify_df[spotify_df['id'].isin(
            refined_feature_set['id'].values)]
        non_playlist_df['sim'] = cosine_similarity(refined_feature_set.drop(
            'id', axis=1).values, playlist_vect.values.reshape(1, -1))[:, 0]
        recommended_10_songs = non_playlist_df.sort_values(
            'sim', ascending=False).head(10)
        recommended_10_songs['url'] = recommended_10_songs['id'].apply(
            lambda x: self.sp.track(x)['album']['images'][1]['url'])

        return recommended_10_songs

    def recommend_tracks(self, playlist_id):
        """
        Recommend 10 tracks based off the playlist given by playlist_id.

        Parameters:
        - playlist_id: id of the playlist to recommend tracks off of.

        Returns:
        - recommended_10: 10 tracks recommended. (currentltly a data frame)
        """
        spotify_df = pd.read_csv('tracks_features.csv')
        spotify_df = spotify_df.drop(
            ['album_id', 'track_number', 'disc_number', 'year', 'release_date'], axis=1)

        full_feature_set_df = self.__create_feature_vectores(spotify_df)
        playlist_df = self.__create_playlist_df(playlist_id)
        playlist_vect, refined_feature_set = self.__create_playlist_vector(
            full_feature_set_df, playlist_df)
        recommended_10 = self.__generate_recommendations(
            spotify_df, playlist_vect, refined_feature_set)

        # Format recommended tracks as {name: id}

        return recommended_10.set_index('id')['name'].to_dict()

    def playlists(self):
        """
        Returns the user's public playlists.
        Formatted in {name : id}
        """
        playlists_res = self.sp.current_user_playlists()['items']
        playlists = {}

        for item in playlists_res:
            playlists[item['name']] = item['id']

        return playlists
    
    def add_track_to_playlist(self, track_id, playlist_id):
        """
        Adds track with id track_id to user's playlist with
        id playlist_id.
        """
        pass
