import spotipy
import pandas as pd
from spotify_api_credentials import client_id, client_secret, redirect_uri

from scripts.get_user_profile import get_user_profile
from scripts.get_playlist_info import get_user_playlistinfo
from scripts.get_user_followed_artists import get_user_followed_artists
from scripts.get_all_tracks_in_all_playlists import get_all_tracks_in_all_playlists
from scripts.get_audio_features import get_audio_features
from scripts.get_top_tracks import get_top_tracks
from scripts.get_top_artists import get_top_artists

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


    # Get user profile data
    user_data = get_user_profile(sp)
    write_csv(user_data, 'user_profile.csv')

    # Get user Playlists
    playlist_info = get_user_playlistinfo(sp)
    df_playlists = pd.DataFrame(playlist_info)
    write_csv(df_playlists, 'user_playlists.csv')

    #Get user followed artirts
    all_user_artists = get_user_followed_artists(sp)
    df_all_user_artists = pd.DataFrame(all_user_artists)
    write_csv(df_all_user_artists, 'user_artists.csv')  

    #Get All tracks in Playlists
    all_user_tracks = get_all_tracks_in_all_playlists(sp)
    df_all_user_tracks = pd.DataFrame(all_user_tracks)
    write_csv(df_all_user_tracks, 'all_user_tracks.csv') 

    #Get All tracks Audio Features
    all_track_audio_features = get_audio_features(sp,all_user_tracks)
    df_audio_features = pd.DataFrame(all_track_audio_features)
    write_csv(df_audio_features, 'track_audio_features.csv') 

    #Get Top User tracks
    top_tracks_data = get_top_tracks(sp)
    df_top_tracks = pd.DataFrame(top_tracks_data)
    write_csv(df_top_tracks, 'top_tracks.csv') 

    #Get Top User Artists
    top_artists_data = get_top_artists(sp)
    df_top_artists = pd.DataFrame(top_artists_data)
    write_csv(df_top_artists, 'top_artists.csv') 


if __name__ == "__main__":
    main()
