import spotipy
import pandas as pd

from spotipy.oauth2 import SpotifyOAuth
from spotify_api_credentials import client_id, client_secret, redirect_uri



all_tracks = []
user_tracks_id = []
all_track_audio_features = []
all_album_tracks = []




# Initialize the Spotify client with authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='user-read-email user-read-private playlist-read-private playlist-read-collaborative user-top-read user-library-read user-follow-read'))


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

# Define the CSV file path
csv_file = 'user_profile.csv'

# Save the DataFrame to a CSV file
user_data.to_csv(csv_file, index=False)

print(f"User profile information has been written to {csv_file}")

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
csv_file = 'user_playlists.csv'

# Save the DataFrame to a CSV file
df_playlists.to_csv(csv_file, index=False)

print(f'Playlists have been written to {csv_file}')


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

# Example usage:
user_albums = get_user_albums(sp)

# Create a DataFrame from the albums data
df_albums = pd.DataFrame(user_albums)

# Define the CSV file path
csv_file = 'user_albums.csv'

# Save the DataFrame to a CSV file
df_albums.to_csv(csv_file, index=False)

print(f'User albums have been written to {csv_file}')








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

# Define the CSV file path
csv_file = 'user_artists.csv'

# Save the DataFrame to a CSV file
df_all_user_artists.to_csv(csv_file, index=False)

print(f'User artists have been written to {csv_file}')


# Get the current user's playlists
user_playlists = sp.current_user_playlists()

# Print the playlist names and IDs
for playlist in user_playlists['items']:
    print(f"Playlist Name: {playlist['name']}, Playlist ID: {playlist['id']}")

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

# Example usage:
all_user_tracks = get_all_tracks_in_all_playlists(sp)

# Create a DataFrame from the albums data
df_all_user_tracks = pd.DataFrame(all_user_tracks)

# Define the CSV file path
csv_file = 'all_user_tracks.csv'

# Save the DataFrame to a CSV file
df_all_user_tracks.to_csv(csv_file, index=False)

print(f'User albums have been written to {csv_file}')


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


for user_tracks in all_user_tracks:
        user_tracks_id = user_tracks['track_id']
        features = get_tracks_audio_features(user_tracks_id, sp)
        all_track_audio_features.extend(features)


df_audio_features = pd.DataFrame(all_track_audio_features)

csv_file = 'track_audio_features.csv'

df_audio_features.to_csv(csv_file, index=False)

print(f'Track audio features have been written to {csv_file}')


# Get the user's top tracks (limit can be adjusted)
top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')  # Change the limit and time_range as needed

# Create a list to store the top tracks data
top_tracks_data = []

# Extract relevant data from the top tracks
for i, track in enumerate(top_tracks['items'], start=1):
     # Get the album images
    album = track['album']
    images = album['images']
    if images:
        album_image_url = images[0]['url']
    else:
        album_image_url = None
    top_tracks_data.append({
        'Position': i,
        'Track Name': track['name'],
        'Artists': ', '.join([artist['name'] for artist in track['artists']]),
        'Artists_ids':  ', '.join( [artist['id'] for artist in track['artists']]),
        'Album Name': track['album']['name'],
        'Release Date': track['album']['release_date'],
        'Track ID': track['id'],
        'Popularity': track['popularity'],
        'Image URL': album_image_url
    })

# Create a DataFrame from the top tracks data
df_top_tracks = pd.DataFrame(top_tracks_data)

# Define the CSV file path
csv_file = 'top_tracks.csv'

# Save the DataFrame to a CSV file
df_top_tracks.to_csv(csv_file, index=False)


# Get the user's top artists (limit can be adjusted)
top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')  # Change the limit and time_range as needed

# Create a list to store the top artists data
top_artists_data = []

# Extract relevant data from the top artists
for i, artist in enumerate(top_artists['items'], start=1):
    # Get the artist's images
    images = artist['images']
    if images:
        artist_image_url = images[0]['url']
    else:
        artist_image_url = None
    top_artists_data.append({
        'Position': i,
        'Artist id': artist['id'],
        'Artist Name': artist['name'],
        'Genres': ', '.join(artist['genres']),
        'Popularity': artist['popularity'],
        'Image URL': artist_image_url
    })

# Create a DataFrame from the top artists data
df_top_artists = pd.DataFrame(top_artists_data)

# Save the DataFrame to a CSV file
df_top_artists.to_csv('top_artists.csv', index=False)

print("Data has been saved to 'top_artists.csv'")

print('yes')


