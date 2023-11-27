import spotipy
import pandas as pd
from spotify_api_credentials import client_id, client_secret, redirect_uri

from functions.get_user_profile import get_user_profile
from functions.get_playlist_info import get_user_playlistinfo
from functions.get_user_followed_artists import get_user_followed_artists
from functions.get_all_tracks_in_all_playlists import get_all_tracks_in_all_playlists
from functions.get_audio_features import get_audio_features
from functions.get_top_tracks import get_top_tracks
from functions.get_top_artists import get_top_artists

from helper.write_to_csv import write_csv

from spotipy.oauth2 import SpotifyOAuth

all_tracks = []
user_tracks_id = []
all_track_audio_features = []
all_album_tracks = []


def main():
    # Initialize the Spotify client with authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope='user-read-email user-read-private playlist-read-private playlist-read-collaborative user-top-read user-library-read user-follow-read'))


    
    top_tracks_data = get_top_tracks(sp)
    df_top_tracks = pd.DataFrame(top_tracks_data)
    write_csv(df_top_tracks, 'top_tracks.csv') 

    top_artists_data = get_top_artists(sp)
    df_top_artists = pd.DataFrame(top_artists_data)
    write_csv(df_top_artists, 'top_artists.csv') 


if __name__ == "__main__":
    main()
