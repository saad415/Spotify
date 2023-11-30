all_tracks = []


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
    # Get the current user's playlists
    user_playlists = sp.current_user_playlists()

    playlists = user_playlists
    

    for playlist in playlists['items']:
        playlist_id = playlist['id']
        tracks = get_all_tracks_in_playlist(playlist_id, sp)
        all_tracks.extend(tracks)

    return all_tracks
