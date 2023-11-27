
def get_top_artists(sp):
   
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


    return top_artists_data

