import boto3
import pandas as pd
import io

def download_csv_files_from_s3(aws_access_key_id, aws_secret_access_key, s3_bucket_name, file_keys):
    # Initialize an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Create a dictionary to store DataFrames
    dataframes = {}

    # Iterate over the list of file keys and download each CSV file
    for file_key in file_keys:
        try:
            response = s3.get_object(Bucket=s3_bucket_name, Key=file_key)
            print("bucket_name: ", s3_bucket_name, "\nfile_key: ", file_key)
            content = response['Body'].read()

            # Read the CSV content into a Pandas DataFrame
            df = pd.read_csv(io.BytesIO(content))

            # Store the DataFrame in the dictionary with the file key as the key
            dataframes[file_key] = df

        except Exception as e:
            print(f"An error occurred for file key '{file_key}': {str(e)}")

    return dataframes

# Example usage:
aws_access_key_id = ''
aws_secret_access_key = ''
s3_bucket_name = ''
file_keys = ['track_audio_features.csv', 'user_playlists.csv', 'all_user_tracks.csv', 'user_profile.csv']  # List of S3 object keys

dataframes = download_csv_files_from_s3(aws_access_key_id, aws_secret_access_key, s3_bucket_name, file_keys)

# Access the downloaded DataFrames by their file keys
if 'track_audio_features.csv' in dataframes:
    track_audio_features = dataframes['track_audio_features.csv']
    # Work with df1

if 'user_playlists.csv' in dataframes:
    user_playlists = dataframes['user_playlists.csv']
    # Work with df2

if 'all_user_tracks.csv' in dataframes:
    all_user_tracks = dataframes['all_user_tracks.csv']

if 'user_profile.csv' in dataframes:
    user_profile = dataframes['user_profile.csv']

if 'user_artists.csv' in dataframes:
    user_artists = dataframes['user_artists.csv']
