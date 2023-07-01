import spotipy
import pandas as pd
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

    def __init__(self, auth_manager):
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def __create_feature_vectors(self, track_dataset_df):
        """
        Creates Feature Vectors for each track in the dataset. 
        Tunable Parameters: Weight of each indicator variable (Genre, key, time_sig, popularity)
        Parameters:
        - all_tracks_df: consists of all tracks in the used dataset, mimicking the "spotify db"
        Returns:
        - dataframe consisting of each track id, and their feature vector normalized.
        """
        # Get Unique Genre Values in df; make col for each genre and its corresponding value 1
        genre_df = pd.get_dummies(track_dataset_df['genre']) * 1

        # Get Unique key Values in df; make col for each key and its corresponding value 1
        key_df = pd.get_dummies(track_dataset_df['key']) * 1

        # Create 5 point buckets for popularity feature (OHE) - Reduces sensitivity to feature
        track_dataset_df['popularity_red'] = track_dataset_df['popularity'].apply(
            lambda x: int(x/5))
        tf_df = pd.get_dummies(track_dataset_df['popularity_red'])
        feature_names = tf_df.columns
        tf_df.columns = ["pop" + "|" + str(i) for i in feature_names]
        tf_df.reset_index(drop=True, inplace=True)
        popularity_cols_df = tf_df * 0.25

        # Scale and Normalize remaining columns
        float_cols = track_dataset_df[['acousticness', 'danceability', 'duration_ms', 'energy',
                                       'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']].reset_index(drop=True)
        scaler = MinMaxScaler()
        floats_scaled = pd.DataFrame(scaler.fit_transform(
            float_cols), columns=float_cols.columns) * 0.2

        # Create OHE Buckets for time_signature feature
        time_sig_df = pd.get_dummies(track_dataset_df['time_signature']) * 0.2

        # Combine all compononets
        tracks_feature_set = pd.concat(
            [genre_df, key_df, time_sig_df, popularity_cols_df, floats_scaled], axis=1)
        tracks_feature_set['id'] = track_dataset_df['track_id'].values

        return tracks_feature_set

    def __filter_user_playlist(self, playlist_id, all_tracks_df):
        """
        Given a user playlist that will be used to make recommendations based off,
        return a 'filtered' playlist of the tracks that are available in the dataset.
        Parameters:
        - playlist_id: id of the user playlist
        - all_tracks_df: tracks dataset
        Returns:
        - refined_playlist_df: filtered playlist of songs in dataset
        """
        user_playlist = self.sp.playlist(playlist_id)
        refined_playlist = pd.DataFrame()
        for ix, i in enumerate(user_playlist['tracks']['items']):
            if i['track'] is not None and i['track']['id'] is not None:
                refined_playlist.loc[ix,
                                     'artist'] = i['track']['artists'][0]['name']
                refined_playlist.loc[ix, 'name'] = i['track']['name']
                refined_playlist.loc[ix, 'id'] = i['track']['id']
                refined_playlist.loc[ix,
                                     'url'] = i['track']['album']['images'][1]['url']
                refined_playlist.loc[ix, 'date_added'] = i['added_at']

        refined_playlist['date_added'] = pd.to_datetime(
            refined_playlist['date_added'])
        refined_playlist = refined_playlist[refined_playlist['id'].isin(
            all_tracks_df['track_id'].values)].sort_values('date_added', ascending=False)

        return refined_playlist

    def __create_playlist_vector(self, tracks_feature_set, refined_playlist, recency_bias=1.2):
        """
        Vectorizes a user playlist by summarizing the playlist dataframe
        into a single dataframe. 
        Tunable paramateres: Recency Bias
        Parameters:
        - tracks_feature_set: Full Feature set of each/all songs in dataset
        - refined_playlist: Refined playlist dataframe (tracks that are in dataset)
        - recency_bias: Weight value for how much to emphasize more recently added songs
        Returns:
        - playlist_vector_weighted_final: Feature Vector summarizing playlist
        - complete_feature_set_nonplaylist: Dataframe where each row is a feature 
        vector for each track not in playlist in dataset
        """
        feature_set_playlist = tracks_feature_set[tracks_feature_set['id'].isin(
            refined_playlist['id'].values)]
        feature_set_playlist = feature_set_playlist.merge(
            refined_playlist[['id', 'date_added']], on='id', how='inner')
        complete_feature_set_nonplaylist = tracks_feature_set[~tracks_feature_set['id'].isin(
            refined_playlist['id'].values)]

        playlist_vector = feature_set_playlist.sort_values(
            'date_added', ascending=False)
        most_recent_date = playlist_vector.iloc[0, -1]

        for ix, row in playlist_vector.iterrows():
            playlist_vector.loc[ix, 'months_back'] = int(
                (most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days / 30)

        playlist_vector['weight'] = playlist_vector['months_back'].apply(
            lambda x: recency_bias ** (-x))

        playlist_vector_weighted = playlist_vector.copy()
        playlist_vector_weighted.update(
            playlist_vector_weighted.iloc[:, :-4].mul(playlist_vector_weighted.weight, 0))
        playlist_vector_weighted_final = playlist_vector_weighted.iloc[:, :-4]

        return playlist_vector_weighted_final.sum(axis=0), complete_feature_set_nonplaylist

    def __generate_recommendations(self, all_tracks_df, playlist_vector, all_tracks_features, recommend_amt=10):
        """
        Generate recommendations based on the playlist vector, using
        the all_tracks_features.
        Parameters:
        - all_tracks_df: All tracks and info in the dataset
        - playlist_vector: Feature Vector summarizing playlist
        - all_tracks_features: All features for each track not in playlist but in dataset
        Returns:
        - rec_10: 10 recommended tracks
        """
        non_playlist_df = all_tracks_df[all_tracks_df['track_id'].isin(
            all_tracks_features['id'].values)]
        non_playlist_df['sim'] = cosine_similarity(all_tracks_features.drop(
            'id', axis=1).values, playlist_vector.values.reshape(1, -1))[:, 0]
        recs = non_playlist_df.sort_values(
            'sim', ascending=False).head(recommend_amt)
        recs['url'] = recs['track_id'].apply(
            lambda x: self.sp.track(x)['album']['images'][1]['url'])

        return recs

    def recommend_tracks(self, playlist_id, recommend_amt=10):
        """
        Recommends tracks based off playlist specified by playlist_id.
        Tracks are pulled from the spotify dataset specified.
        Amount of tracks that are recommended are given by recommend_amt.
        Returns:
        - recs: recommend tracks in dictionary format, {track_name : track_id}
        """
        # Dataset of Spotify tracks Available to recommend from
        spotify_dataset_df = pd.read_csv('SpotifyFeatures.csv')

        refined_playlist = self.__filter_user_playlist(
            playlist_id, spotify_dataset_df)
        dataset_features = self.__create_feature_vectors(spotify_dataset_df)
        playlist_vector, remaining_dataset_features = self.__create_playlist_vector(
            dataset_features, refined_playlist)
        recs = self.__generate_recommendations(
            spotify_dataset_df, playlist_vector, remaining_dataset_features, recommend_amt)
        recs_dict = recs.set_index('track_id')['track_name'].to_dict()
        return recs_dict

    def playlists(self):
        """
        Returns the user's public playlists.
        Formatted in {playlists : [playlist]}
        """
        playlists_res = self.sp.current_user_playlists()['items']
        playlists = []

        for item in playlists_res:
            playlist = {
                'name': item['name'],
                'id': item['id']
            }
            playlists.append(playlist)

        return {"playlists": playlists}

    def add_track_to_playlist(self, track_id, playlist_id):
        """
        Adds track with id track_id to user's playlist with
        id playlist_id.
        """
        track = self.sp.track(track_id)
        uri = [track["uri"]]
        self.sp.playlist_add_items(playlist_id, items=uri)

    def profile_info(self):
        """
        Returns profile statistics about the current user.
        Info returned: display name, followers, number of 
        public playlists, and top 5 tracks of past 4 weeks.
        """
        response = self.sp.current_user()

        profile = {}
        profile['followers'] = response['followers']['total']
        profile['name'] = response['display_name']
        playlists = self.playlists()["playlists"]
        profile['public_playlists'] = len(playlists)

        top_tracks_res = self.sp.current_user_top_tracks(5, 0, "short_term")
        top_tracks = [{"name": track['name'], "id": track['id']}
                      for track in top_tracks_res["items"]]
        profile["top_tracks"] = top_tracks

        return profile

    def track_info(self, track_id):
        """
        Returns Essential information of a track.
        """
        try:
            response = self.sp.track(track_id)
        except spotipy.exceptions.SpotifyException as error:
            return None
        else:
            track = {}
            track['id'] = track_id
            track["name"] = response['name']
            track["album"] = response["album"]["name"]
            artists_objs = response["artists"]
            artists = [artist_obj["name"] for artist_obj in artists_objs]
            track['artists'] = artists
            img_url = response['album']['images'][0]['url']
            track["album_img_url"] = img_url

            return track

    def track_cover(self, track_id):
        """
        Returns URL for Album cover of a track/
        """
        try:
            response = self.sp.track(track_id)
        except spotipy.exceptions.SpotifyException as error:
            return None
        else:
            img_url = response['album']['images'][0]['url']
            return {"album_img_url": img_url}

    def playlist_cover(self, playlist_id):
        """
        Returns url of image of playlist given the playlist id.
        """
        response = self.sp.playlist_cover_image(playlist_id)
        return {"playlist_img_url": response[0]['url']}
