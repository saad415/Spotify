import spotipy
from spotipy.oauth2 import SpotifyOAuth
from botocore.exceptions import NoCredentialsError
import boto3
import pandas as pd
import io
from datetime import datetime
import os

def save_token_info(token_info):
    with open('spotify_token_info.txt', 'w') as file:
        file.write(str(token_info))

def load_token_info():
    if os.path.exists('spotify_token_info.txt'):
        with open('spotify_token_info.txt', 'r') as file:
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


def put_data_in_s3_bucket(sp):
    # Initialize the Spotify client with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

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