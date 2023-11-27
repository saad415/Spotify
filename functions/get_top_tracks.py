
def get_top_tracks(sp):
   
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


    return top_tracks_data

