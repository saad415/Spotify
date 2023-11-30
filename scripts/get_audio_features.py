
all_track_audio_features = []
def get_audio_features(sp,all_user_tracks):
   
    for user_tracks in all_user_tracks:
        user_tracks_id = user_tracks['track_id']
        features = get_track_audio_features(user_tracks_id, sp)
        all_track_audio_features.extend(features)

    return all_track_audio_features

def get_track_audio_features(track_id, sp):
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

