import requests
import pandas as pd

# Function to get Spotify access token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_data = auth_response.json()
    return auth_data['access_token']

# Function to search for a track and get its ID
def search_track(track_name, artist_name, token):
    query = f"{track_name} artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })
    json_data = response.json()
    try:
        first_result = json_data['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except (KeyError, IndexError):
        return None

# Function to get track details
def get_track_details(track_id, token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })
    json_data = response.json()
    image_url = json_data['album']['images'][0]['url']
    return image_url

# Function to get user playlists
def get_user_playlists(user_id, token):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.get(url, headers={
        'Authorization': f'Bearer {token}'
    })
    json_data = response.json()
    playlists = []
    for item in json_data['items']:
        playlists.append({
            'name': item['name'],
            'id': item['id'],
        })
    return playlists


# Your Spotify API Credentials
client_id = '484f223094b54d77a0b836e982d81799'
client_secret = '791a80ce2748414bb9b7e455c3d15ccc'

# Get Access Token
access_token = get_spotify_token(client_id, client_secret)

# Get user playlists (replace 'your_user_id' with the Spotify user ID)
user_playlists = get_user_playlists('smedjan', access_token)

# Print user playlists
print("User Playlists:")
for playlist in user_playlists:
    print(f"Name: {playlist['name']}, ID: {playlist['id']}")

# Read your DataFrame (replace 'your_file.csv' with the path to your CSV file)
df_spotify = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')

# Loop through each row to get track details and add to DataFrame
for i, row in df_spotify.iterrows():
    track_id = search_track(row['track_name'], row['artist(s)_name'], access_token)
    if track_id:
        image_url = get_track_details(track_id, access_token)
        df_spotify.at[i, 'image_url'] = image_url

# Save the updated DataFrame (replace 'updated_file.csv' with your desired output file name)
df_spotify.to_csv('updated_file.csv', index=False)
