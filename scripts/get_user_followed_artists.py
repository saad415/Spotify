import pandas as pd

def get_user_followed_artists(sp):
   
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

    return all_user_artists

