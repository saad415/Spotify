import spotipy
from spotipy.oauth2 import SpotifyOAuth
from botocore.exceptions import NoCredentialsError
import boto3
import pandas as pd
import io
from datetime import datetime
import os

all_tracks = []
all_track_audio_features = []


def save_token_info(token_info):
    with open('/home/ec2-user/test/spotify_token_info.txt', 'w') as file:
        file.write(str(token_info))

def load_token_info():
    if os.path.exists('/home/ec2-user/test/spotify_token_info.txt'):
        with open('/home/ec2-user/test/spotify_token_info.txt', 'r') as file:
            token_info = eval(file.read())
        return token_info
    else:
        return None

def refresh_token_if_expired(sp_oauth, token_info):
    if sp_oauth.is_token_expired(token_info):
        print("Refreshing expired token")
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        save_token_info(token_info)
    return token_info

# Set your Spotify API credentials
client_id = "484f223094b54d77a0b836e982d81799"
client_secret = "791a80ce2748414bb9b7e455c3d15ccc"
redirect_uri = "https://accounts.spotify.com/authorize"  # This should match the URI set in your Spotify app settings


# AWS credentials (configure these with your own values)
aws_access_key_id = 'AKIAUTEANXGB2VM2JSPP'
aws_secret_access_key = 'QfrguEBd0/8rmXctChoj+oO6WyaZLUZvhU2Jlcht'
s3_bucket_name = 'saad-spotify'
s3_file_key = 'user_data.csv'  # Update to use .csv extension

# Initialize an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# AWS S3 file information
bucket_name = s3_bucket_name
file_key = s3_file_key



# Scope for API access - adjust as needed
scope = "user-read-email user-read-private playlist-read-private playlist-read-collaborative user-top-read user-library-read user-follow-read"

# Initialize the Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

token_info = load_token_info()

if not token_info:
    auth_url = sp_oauth.get_authorize_url()
    print("Please navigate here: ", auth_url)
    response = input("Enter the URL you were redirected to: ")
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    save_token_info(token_info)

token_info = refresh_token_if_expired(sp_oauth, token_info)

# Initialize the Spotify client with the access token
sp = spotipy.Spotify(auth=token_info['access_token'])


def get_user_albums(sp):
    user_albums = sp.current_user_saved_albums()
    albums = []

    while user_albums:
        for item in user_albums['items']:
            album = item['album']
            albums.append({
                'name': album['name'],
                'artists': [artist['name'] for artist in album['artists']],
                'release_date': album['release_date'],
                'total_tracks': album['total_tracks'],
                'Image URL': album['images'][0]['url'],
                'album_id': album['id'],
            })

        # Check if there are more albums to retrieve
        user_albums = sp.next(user_albums) if user_albums['next'] else None

    return albums

def get_all_tracks_in_playlist(playlist_id, sp):
    tracks = []
    offset = 0  # Start with the first page of tracks

    while True:
        playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset)

        if not playlist_tracks['items']:
            break

        for item in playlist_tracks['items']:
            track = item['track']
            
            # Check if the track object is valid
            if track:
                image_url = track['album']['images'][0]['url']
                tracks.append({
                    'playlist_id': playlist_id,
                    'track_name': track['name'],
                    'artist(s)_name': [artist['name'] for artist in track['artists']],
                    'artist_ids': [artist['id'] for artist in track['artists']],
                    'album_name': track['album']['name'],
                    'album_id': track['album']['id'],  # Add album_id field
                    'track_id': track['id'],
                    'Image URL': image_url,
                    'release_date': track['album']['release_date'],
                    'popularity': track['popularity'] 
                })

        offset += len(playlist_tracks['items'])

    return tracks

# Get the current user's playlists
user_playlists = sp.current_user_playlists()


#code to get tracks audio features
def get_tracks_audio_features(track_id, sp):
    all_track_audio_features = []
    #print(track_id)
    track_audio_features = sp.audio_features(track_id)
    if track_audio_features is not None and track_audio_features[0] is not None:
            audio_feature = track_audio_features[0]
            # Define default values for missing keys
            default_values = {
                'danceability': 0.0,
                'energy': 0.0,
                'key': 0,
                'loudness': 0.0,
                'mode': 0,
                'speechiness': 0.0,
                'acousticness': 0.0,
                'instrumentalness': 0.0,
                'liveness': 0.0,
                'valence': 0.0,
                'tempo': 0.0,
            }
            # Fill missing keys with default values
            audio_feature = {**default_values, **audio_feature}
            all_track_audio_features.append(audio_feature)

       

    return all_track_audio_features




def get_all_tracks_in_playlist(playlist_id, sp):
    tracks = []
    offset = 0  # Start with the first page of tracks

    while True:
        playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset)

        if not playlist_tracks['items']:
            break

        for item in playlist_tracks['items']:
            track = item['track']
            
            # Check if the track object is valid
            if track:
                image_url = track['album']['images'][0]['url']
                tracks.append({
                    'playlist_id': playlist_id,
                    'track_name': track['name'],
                    'artist(s)_name': [artist['name'] for artist in track['artists']],
                    'artist_ids': [artist['id'] for artist in track['artists']],
                    'album_name': track['album']['name'],
                    'album_id': track['album']['id'],  # Add album_id field
                    'track_id': track['id'],
                    'Image URL': image_url,
                    'release_date': track['album']['release_date'],
                    'popularity': track['popularity'] 
                })

        offset += len(playlist_tracks['items'])

    return tracks


def get_all_tracks_in_all_playlists(sp):
    playlists = user_playlists
    

    for playlist in playlists['items']:
        playlist_id = playlist['id']
        tracks = get_all_tracks_in_playlist(playlist_id, sp)
        all_tracks.extend(tracks)

    return all_tracks


def put_data_in_s3_bucket(sp):


    # Get the current user's profile
    user_profile = sp.current_user()

    # Extract the required information
    profile_picture = user_profile['images'][0]['url'] if user_profile['images'] else None
    display_name = user_profile['display_name']
    email = user_profile['email']
    country = user_profile['country']

    # Create a DataFrame with the user information
    user_data = pd.DataFrame({
        "Profile Picture": [profile_picture],
        "Display Name": [display_name],
        "Email": [email],
        "Country": [country]
    })

    # Define the CSV file path for user profile data
    user_csv_file = 'user_profile.csv'

    # Save the DataFrame to a CSV file for user profile data
    user_data.to_csv(user_csv_file, index=False)

    # Get the current user's followed artists
    user_followed_artists = sp.current_user_followed_artists()

    # Create a list to store artist information
    all_user_artists = []

    # Define a function to retrieve artist details
    def get_artist_details(artist):
        # Get the artist's tracks
        artist_tracks = sp.artist_top_tracks(artist['id'])

        artist_details = {
            'Artist Name': artist['name'],
            'Artist ID': artist['id'],
            'Followers': artist['followers']['total'],
            'Number of Songs': len(artist_tracks),
            'Image URL': artist['images'][0]['url'] if artist['images'] else None
        }
        return artist_details

    # Iterate through the user's followed artists
    for artist in user_followed_artists['artists']['items']:
        artist_details = get_artist_details(artist)
        all_user_artists.append(artist_details)

    # Create a DataFrame from the collected artist details
    df_all_user_artists = pd.DataFrame(all_user_artists)

    # Define the CSV file path for user artists data
    artists_csv_file = 'user_artists.csv'

    # Save the DataFrame to a CSV file for user artists data
    df_all_user_artists.to_csv(artists_csv_file, index=False)


    # Get the current user's playlists
    user_playlists = sp.current_user_playlists()

    # Create a list to store playlist information
    playlist_info = []

    # Loop through each playlist and get its name, ID, and image URL (if available)
    for playlist in user_playlists['items']:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        
        # Get the playlist's images
        images = playlist['images']
        if images:
            playlist_image_url = images[0]['url']
        else:
            playlist_image_url = None

        playlist_info.append({
            'Playlist Name': playlist_name,
            'Playlist ID': playlist_id,
            'Image URL': playlist_image_url
        })

    # Create a DataFrame from the list of playlists
    df_playlists = pd.DataFrame(playlist_info)

    # Define the CSV file path
    playlist_csv_file = 'user_playlists.csv'

    # Save the DataFrame to a CSV file
    df_playlists.to_csv(playlist_csv_file, index=False)

    # Example usage:
    user_albums = get_user_albums(sp)

    # Create a DataFrame from the albums data
    df_albums = pd.DataFrame(user_albums)

    # Define the CSV file path
    albums_csv_file = 'user_albums.csv'

    # Save the DataFrame to a CSV file
    df_albums.to_csv(albums_csv_file, index=False)

    

    # Example usage:
    all_user_tracks = get_all_tracks_in_all_playlists(sp)

    # Create a DataFrame from the albums data
    df_all_user_tracks = pd.DataFrame(all_user_tracks)

    # Define the CSV file path
    all_users_csv_file = 'all_user_tracks.csv'

    # Save the DataFrame to a CSV file
    df_all_user_tracks.to_csv(all_users_csv_file, index=False)

    for user_tracks in all_user_tracks:
            user_tracks_id = user_tracks['track_id']
            features = get_tracks_audio_features(user_tracks_id, sp)
            all_track_audio_features.extend(features)


    df_audio_features = pd.DataFrame(all_track_audio_features)

    audio_features_csv_file = 'track_audio_features.csv'

    df_audio_features.to_csv(audio_features_csv_file, index=False)


    # Upload both CSV files to AWS S3
    def upload_to_aws(local_file, s3_bucket, s3_key, aws_access_key, aws_secret_access_key):
        try:
            s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_access_key)
            s3.upload_file(local_file, s3_bucket, s3_key)
            print(f"File '{local_file}' uploaded to S3 bucket '{s3_bucket}' with key '{s3_key}'")
        except FileNotFoundError:
            print(f"The file '{local_file}' was not found.")
        except NoCredentialsError:
            print("AWS credentials not available or not configured properly.")

    # Upload user profile CSV file to AWS S3
    upload_to_aws(user_csv_file, s3_bucket_name, 'user_profile.csv', aws_access_key_id, aws_secret_access_key)

    # Upload user artists CSV file to AWS S3
    upload_to_aws(artists_csv_file, s3_bucket_name, 'user_artists.csv', aws_access_key_id, aws_secret_access_key)

    # Upload user playlists CSV file to AWS S3
    upload_to_aws(playlist_csv_file, s3_bucket_name, 'user_playlists.csv', aws_access_key_id, aws_secret_access_key)
    
    # Upload user user_albums CSV file to AWS S3
    upload_to_aws(albums_csv_file, s3_bucket_name, 'user_albums.csv', aws_access_key_id, aws_secret_access_key)
    
    # Upload user user_albums CSV file to AWS S3
    upload_to_aws(all_users_csv_file, s3_bucket_name, 'all_user_tracks.csv', aws_access_key_id, aws_secret_access_key)

    # Upload user user_albums CSV file to AWS S3
    upload_to_aws(audio_features_csv_file, s3_bucket_name, 'track_audio_features.csv', aws_access_key_id, aws_secret_access_key)
    
    print("User profile and artists data have been uploaded to S3.")







# Use the access token
sp = spotipy.Spotify(auth=token_info['access_token'])

put_data_in_s3_bucket(sp)
# Example API call
results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])


def get_user_profile(sp):
   
    user_profile = sp.current_user()
    # Extract the required information
    profile_picture = user_profile['images'][0]['url'] if user_profile['images'] else None
    display_name = user_profile['display_name']
    email = user_profile['email']
    country = user_profile['country']

    # Create a DataFrame with the user information  
    user_data = pd.DataFrame({
    "Profile Picture": [profile_picture],
    "Display Name": [display_name],
    "Email": [email],
    "Country": [country]
    })

    return user_data

#user_data = get_user_profile(sp)
#print(user_data)