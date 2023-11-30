
def get_user_playlistinfo(sp):
   
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

    return playlist_info

